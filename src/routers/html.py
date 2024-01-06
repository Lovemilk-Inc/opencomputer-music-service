from pathlib import Path
from time import time as get_time
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response
from fastapi.exceptions import HTTPException
from loguru import logger
error_logger = logger.opt(exception=True)

router = APIRouter(tags=['page'])


@router.get("/favicon.ico")
async def favicon():
    from src.shared import session
    url = (f'https://content.cyans.me/static/lovemilk-hosted/oms/favicon.ico?'
           f'{get_time()}={get_time()}&fuckTo=CyanChanges')
    logger.debug('request favicon URL: {}', url)
    try:
        response = await session.get(url, headers={
            'Origin': 'https://content.cyans.me',
            'Referer': 'https://content.cyans.me',
        })
        return Response(content=await response.read(), media_type='image')
    except Exception:
        error_logger.error('failed to get favicon')
        raise HTTPException(status_code=404)

@router.get('/', response_class=HTMLResponse)
async def index():
    return Path('static/html/index.html').read_text('u8')
