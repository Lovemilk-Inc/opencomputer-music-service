from fastapi import APIRouter
from fastapi.responses import FileResponse
from loguru import logger

from src.config import config
from src.shared import ApiResponse

router = APIRouter(prefix='/api/download', tags=['download'], default_response_class=ApiResponse)


@router.get("/")
async def download_file(filename: str):
    full_filename = config.data_path / filename
    logger.debug('download {}, full filename: {}', filename, full_filename.absolute())

    if not full_filename.is_file():
        return {
            'code': 404,
            'msg': 'file not found'
        }

    if full_filename.parent != config.data_path:
        logger.debug('file is not in data dir, 403!')
        return {
            'code': 403,
            'msg': 'invalid filename'
        }

    return FileResponse(filename=full_filename.name, path=full_filename, content_disposition_type='attachment')
