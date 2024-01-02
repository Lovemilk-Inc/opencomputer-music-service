import sys
from loguru import logger

from src.shared import check_ffmpeg, app
from src.log import replace_uvicorn_logger
from src.routers.upload import router as upload_router
from src.routers.download import router as download_router
from src.routers.file import router as list_router
from src.routers.html import router as html_router
from src.routers.common import router as common_router

logger.remove()
logger.add(sys.stderr, backtrace=False)
logger.add(
    'logs/{time:YYYY-MM-DD}.error.log',
    rotation='00:00',
    diagnose=True,  # 显示错误原因 (将错误 stack 的每个 obj 的内容显示出来)
    retention='7 days',
    level='ERROR',
    encoding='u8',
)
logger.error(f'{"=" * 40} error loguru started! {"=" * 40}')
logger.add(
    'logs/{time:YYYY-MM-DD}.log',
    rotation='00:00',
    retention='7 days',
    backtrace=False,
    encoding='u8',
)
logger.success(f'{"=" * 40} loguru started! {"=" * 40}')
replace_uvicorn_logger(logger)
check_ffmpeg()


app.include_router(upload_router)
app.include_router(download_router)
app.include_router(list_router)
app.include_router(html_router)
app.include_router(common_router)
