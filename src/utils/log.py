# -*- coding: utf-8 -*-
import logging
import logging.handlers
import pathlib

from typing import Final

TARANIS_LOGGER_ID: Final[str] = 'taranis'
logger = logging.getLogger(TARANIS_LOGGER_ID)

TARANIS_LOG_FILE: Final[pathlib.Path] = pathlib.Path(f'logs/{TARANIS_LOGGER_ID}.log')

def taranis_logger_config(level: int = logging.INFO) -> logging.Logger:
    """Configure the taranis logger
    Provides a logger that outputs to both the console and to a log
    file. The log file is configured to rotate every night at midnight.
    
    Parameters
    ----------
    level
        The debugging level, should probably use constants from the
        `logging` module.
    
    """
    logger: logging.Logger = logging.getLogger(TARANIS_LOGGER_ID)
    logger.setLevel(level)
    log_format = logging.Formatter(
                    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
    )
    log_dir = TARANIS_LOG_FILE.parents[0]
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.TimedRotatingFileHandler(
                        filename=str(TARANIS_LOG_FILE),
                        encoding='utf-8',
                        when='midnight',
                        backupCount=10
    )
    file_handler.setFormatter(log_format)
    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def get_taranis_logger() -> logging.Logger:
    """Grab a DBot Logger
    """
    return logging.getLogger(TARANIS_LOGGER_ID)