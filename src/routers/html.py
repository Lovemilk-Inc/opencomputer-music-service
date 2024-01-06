from pathlib import Path
from time import time as get_time
from random import choice
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

TIMESTAMP_ARGV_NAME = [
    '_t', '_ts', '_d', '_date', '_c', '_cyan'
]

router = APIRouter(tags=['page'])


@router.get("/favicon.ico")
async def favicon():
    return RedirectResponse(
        f'https://content.cyans.me/static/lovemilk-hosted/oms/favicon.ico?'
        f'{choice(TIMESTAMP_ARGV_NAME)}={get_time()}&fuckTo=CyanChanges',
        status_code=301
    )


@router.get('/', response_class=HTMLResponse)
async def index():
    return Path('static/html/index.html').read_text('u8')
