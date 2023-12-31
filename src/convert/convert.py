from loguru import logger
from pathlib import Path
import ffmpeg
import asyncio
from src.shared import decode

error_logger = logger.opt(exception=True)

SAMPLE_RATE = 48000


class ConvertFailed(Exception):
    def __init__(self, msg='', *args, return_code: int = 0, stdout: str = None, stderr: str = None):
        super().__init__((msg, *args))
        self.msg = msg
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return (
            f'ConvertFailed: {self.msg}\n\t'
            f'return code: {self.return_code}\n\tstdout: {self.stdout}\n\tstderr: {self.stderr}'
        )


class FFmpeg:
    @classmethod
    async def get_info(cls, path: Path) -> dict:
        return ffmpeg.probe(str(path.absolute()))


async def _is_wav(info: dict) -> bool:
    return info['format']['format_name'] == 'wav' and any(stream['codec_type'] == 'audio' for stream in info['streams'])


async def _has_audio(info: dict) -> bool:
    return any(stream['codec_type'] == 'audio' for stream in info['streams'])


async def convert(input_path: Path, output_path: Path = None):
    input_path = input_path.absolute()

    new_input = None
    try:
        info = await FFmpeg.get_info(input_path)
        # logger.debug('got media info: {}', info)
    except Exception:
        error_logger.error('got media info failed')
        raise TypeError('Unsupported file type')

    if not await _is_wav(info):
        if not (await _has_audio(info)):
            logger.error('file is not a media file, raise error')
            raise TypeError('Unsupported file type')

    output_path = output_path.absolute() if output_path is not None else (new_input or input_path).with_suffix('.dfpwm')

    logger.debug('try to convert to dfpwm {} -> {}', (new_input or input_path), output_path)
    process = await asyncio.subprocess.create_subprocess_shell(  # 转 dfpwm 需要 ffmpeg 5.x 版本  # 不需要了 (x
        f'ffmpeg -i "{(new_input or input_path)}" "{output_path.with_suffix(".wav")}" -y',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        close_fds=True,
        start_new_session=True,
        shell=True
    )

    data, stderr = await process.communicate()
    stderr = decode(stderr)

    if process.returncode != 0:
        input_path.unlink(True)
        raise ConvertFailed(f'To wav failed', return_code=process.returncode, stdout=None, stderr=stderr)

    process = await asyncio.subprocess.create_subprocess_shell(
        f'java -jar "{Path("res/LionRay.jar").absolute()}" "{output_path.with_suffix(".wav")}" "{output_path}"',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        close_fds=True,
        start_new_session=True,
        shell=True
    )

    stdout, stderr = await process.communicate(data)
    stdout = decode(stdout)
    stderr = decode(stderr)

    if process.returncode != 0:
        input_path.unlink(True)
        raise ConvertFailed('To dfpwm failed', return_code=process.returncode, stdout=stdout, stderr=stderr)


async def convert_by_python(input_data: bytes | Path) -> bytes:
    """
    使用 dfpwm 库转换
    :param input_data: 文件二进制内容 或 路径
    :return:
    :copied from: https://github.com/CyanChanges/python-dfpwm
    """
    import soundfile as sf
    from io import BytesIO
    import dfpwm

    data, sample_rate = sf.read(BytesIO(input_data) if isinstance(input_data, bytes) else input_data)
    if sample_rate != SAMPLE_RATE:
        data = dfpwm.resample(data, SAMPLE_RATE)

    if len(data.shape) > 0 and data.shape[1] > 1:  # 多个声道获取第一个
        data = data[:, 0]

    return dfpwm.compressor(data.astype('float32'))  # 转换, 使用 float32 而非 double 以适配 dfpwm.compressor
