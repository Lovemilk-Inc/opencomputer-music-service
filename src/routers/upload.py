from datetime import datetime, timedelta
from fastapi import APIRouter, UploadFile, File, Request
from src.config import config
from src.convert.convert import convert, convert_by_python
from src.shared import get_ipaddress, ApiResponse
from pathlib import Path
from loguru import logger

error_logger = logger.opt(exception=True)

router = APIRouter(prefix='/api/upload', tags=['upload'], default_response_class=ApiResponse)
last_calls: dict[str, datetime] = {}


def file_compare(file_a: Path, file_b: Path, chunk: int = 512):
    with file_a.open('rb') as fA:
        with file_b.open('rb') as fB:
            if fA.read(chunk) != fB.read(chunk):
                return False

    return True


@router.post('/file')
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        # ip = ip_address(request.client.host)  # 这个是 Cloudflare Proxy 的 IP
        ip = get_ipaddress(request)
    except Exception:
        error_logger.error('failed to parse ip address')
        return {
            'code': 500,
            'msg': 'failed to parse ip address'
        }

    if ip.is_global:
        last_call = last_calls.get(str(ip))
        if last_call is not None:
            dt = datetime.now() - last_call
            if dt.total_seconds() < config.call_cd:
                return {
                    'code': 429,
                    'msg': 'Too many requests',
                    'data': {
                        'least': (datetime.now() + (timedelta(seconds=config.call_cd) - dt)).timestamp()
                    }
                }

        last_calls[request.client.host] = datetime.now()

    uploaded_path = config.temp_path / file.filename
    size = file.size

    logger.debug('received filename: {}, size: {}', file.filename, size)

    if size is None:
        return {
            'code': 400,
            'msg': 'failed to get file size'
        }
    elif size > config.max_size:
        return {
            'code': 400,
            'msg': f'file too large (must be less than {config.max_size / 1024 ** 2} MiB)'
        }

    with uploaded_path.open('wb') as fp:
        for i in range((size // config.read_chuck) + 1):
            part = await file.read(config.read_chuck)
            fp.write(part)

    output = config.data_path / uploaded_path.with_suffix('.dfpwm').name

    error = None
    try:
        output.write_bytes(await convert_by_python(uploaded_path.read_bytes()))
        logger.debug('use convert_by_python success')
    except Exception as e:
        error_logger.error('failed to convert use dfpwm module')
        error = e

    if error:
        try:
            await convert(
                uploaded_path,
                output
            )
            error = None
            logger.debug('use convert (by FFmpeg) success')
        except Exception as e:
            error_logger.error('failed to convert use FFmpeg')
            error = e

    if error:
        return {
            'code': 500,
            'msg': str(error)
        }

    try:
        target = config.upload_path / uploaded_path.name
        uploaded_path.replace(target)
        if uploaded_path.is_file():
            uploaded_path.unlink()

        logger.debug('move {} -> {}', uploaded_path, target)
        return {
            'code': 200,
            'msg': 'in progress',
            'data': {
                'id': output.name,
                'link': f'{request.url.scheme}://{request.url.netloc}/api/download/?filename={output.name}'
            }
        }
    except Exception as e:
        error_logger.error('failed to write file')
        return {
            'code': 400 if isinstance(e, TypeError) else 500,
            'msg': str(e),
        }
    finally:
        if uploaded_path.is_file():
            uploaded_path.unlink()
