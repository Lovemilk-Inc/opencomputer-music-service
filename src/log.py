"""
将 FastApi 日志输出为 Loguru 日志
"""

import logging
from loguru import logger

__all__ = (
    'LoguruHandler',
    'replace_uvicorn_logger'
)


class LoguruHandler(logging.Handler):
    def __init__(self, target_logger, level: int | str = 0):
        """
        Handler, 只要 logging.logger.addHandler(<self>) 即可
        :param target_logger: loguru Logger (loguru 没有类型 无法 typing)
        :param level: 日志等级
        """
        super().__init__(level)
        self._target_logger = target_logger

    def emit(self, record):
        try:
            level = self._target_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        self._target_logger.opt(depth=depth, exception=record.exc_info) \
            .log(level, record.getMessage())


def replace_uvicorn_logger(target_logger):
    """
    替换 uvicorn 的 logger 为 loguru 的 logger, 在 startup 调用即可
    :param target_logger: loguru Logger, 之后会使用该 logger 输出
    :return: None
    """
    base_uvicorn_logger: logging.Logger = logging.getLogger('uvicorn')
    for handler in base_uvicorn_logger.handlers:  # 关闭旧的 handler 以不输出到控制台
        # 由于 uvicorn 与 uvicorn.access 基本相同, 所以 uvicorn 不添加 loguru 的 handler
        handler: logging.Handler
        handler.close()
    base_uvicorn_logger.handlers = []
    base_uvicorn_logger.disabled = True
    logging.root.manager.loggerDict.pop('uvicorn')

    # 找到 uvicorn 所有 logger
    loggers: set[logging.Logger] = {
        target_logger for target_logger in logging.root.manager.loggerDict.values()
        if isinstance(target_logger, logging.Logger)
    }

    loguru_handler: logging.Handler = LoguruHandler(target_logger)
    for logging_logger in loggers:
        if getattr(logging_logger, '__loguru_handled', False):
            logger.debug(f'Uvicorn_logger ({logging_logger.name}) was handled, skip to handle')
            continue

        for handler in logging_logger.handlers:  # 关闭旧的 handler 以不输出到控制台
            handler.close()
        logging_logger.handlers = []  # 清空 handlers
        logging_logger.addHandler(loguru_handler)  # 添加 loguru 的 handler
        setattr(logging_logger, '__loguru_handled', True)
