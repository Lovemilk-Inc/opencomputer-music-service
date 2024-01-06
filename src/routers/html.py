from pathlib import Path
# import urllib.parse
# from time import time as get_time
# from random import choice
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse, Response
# from fastapi.exceptions import HTTPException
from loguru import logger

error_logger = logger.opt(exception=True)

router = APIRouter(tags=['page'])

# SPACES = ['', ' ', '　']
# FUCK_STRING = 'fuckTo=CyanChanges'


@router.get("/favicon.ico")
async def favicon():
    # from src.shared import session
    # fuck_to = ''
    # for char in FUCK_STRING:
    #     fuck_to += char + choice(SPACES)
    # arg, val = fuck_to.split('=', 2)
    #
    # args = {
    #     get_time(): get_time(),
    #     arg: val
    # }
    #
    # url = f'https://content.cyans.me/static/lovemilk-hosted/oms/favicon.ico?' + urllib.parse.urlencode(args)
    # logger.debug('request favicon URL: {}', url)
    # try:
    #     response = await session.get(url, headers={
    #         'Origin': 'https://content.cyans.me',
    #         'Referer': 'https://content.cyans.me',
    #         'User-Agent': 'Chromium:Fuck Cyan!'
    #     })
    #     if not response.headers.get('Content-Type', '').startswith('image'):
    #         raise HTTPException(status_code=400, detail='一定是 CyanChanges 干的!')
    #
    #     return Response(content=await response.read(), media_type='image')
    # except HTTPException:
    #     raise
    # except Exception as e:
    #     error_logger.error('failed to get favicon')
    #     raise HTTPException(status_code=404, detail=repr(e))
    return FileResponse(Path('static/favicon.ico'))


@router.get('/', response_class=HTMLResponse)
async def index():
    return Path('static/html/index.html').read_text('u8')
