from fastapi import APIRouter, Request

from src.config import config
from src.shared import get_ipaddress, ApiResponse

from loguru import logger

error_logger = logger.opt(exception=True)

router = APIRouter(prefix='/api/common', tags=['common'], default_response_class=ApiResponse)


@router.get('/limit')
async def get_limit():
    return {
        'maxsize': config.max_size,
        'cd': config.call_cd
    }


@router.get('/ipapi')
async def ipapi(request: Request):
    from src.shared import session

    try:
        res = await session.get(f'http://ip-api.com/json/{get_ipaddress(request)}', params={'fields': '66846719'})
        data = await res.json()

        logger.debug('ip-api response: {}', data)
        if data.get('message', '').lower() not in {'reserved range', 'private range'}:
            return {
                'code': res.status if res.status != 200 else (200 if data.get('status', '') == 'success' else 400),
                **data
            }
        return {
            'code': 233,
            'message': 'CyanChanges',
            'country': 'United States',
            'countryCode': 'US'
        }
    except Exception as e:
        error_logger.error('failed to get ip api')
        return {
            'code': 400,
            'country': 'China',
            'countryCode': 'CN',
        }
