from pathlib import Path
from fastapi import APIRouter
from src.config import config
from src.shared import ApiResponse

router = APIRouter(prefix='/api/file', tags=['file'], default_response_class=ApiResponse)


@router.get('/outputs')
async def list_outputs():
    def _callback(item: Path):
        stat = item.stat()

        return {'name': item.name, 'size': stat.st_size, 'created': stat.st_ctime}

    try:
        return {
            'code': 200,
            'msg': 'success',
            'data': {
                'files': tuple(map(_callback, config.data_path.iterdir()))
            }
        }
    except Exception as e:
        return {
            'code': 500,
            'msg': str(e),
        }


@router.get('/file/{file_id}')
async def file_info(file_id: str):
    try:
        file = {v.name: v for v in config.data_path.iterdir()}[file_id]
    except KeyError:
        return {
            'code': 400,
            'msg': f'Not found file: {file_id}',
        }
    except Exception as e:
        return {
            'code': 500,
            'msg': str(e),
        }

    stat = file.stat()

    return {
        'code': 200,
        'msg': 'success',
        'data': {
            'name': file_id,
            'size': stat.st_size,
            'created': stat.st_ctime
        }
    }
