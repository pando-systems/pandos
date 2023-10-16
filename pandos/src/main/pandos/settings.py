import os
import logging


def get_logger(name: str):
    logging.basicConfig(
        encoding="utc-8",
        level=logging.INFO,
    )
    return logging.getLogger(name)
