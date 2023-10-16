import os
import logging


def get_logger(name: str):
    logging.basicConfig(
        encoding="utc-8",
        level=logging.INFO,  # TODO: Parametrize log-level
    )
    return logging.getLogger(name)
