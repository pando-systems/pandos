import os
import logging


PANDOS_DISABLE_FEATURE_MATURITY_LOGS = int(os.environ.get(
    "PANDOS_DISABLE_FEATURE_MATURITY_LOGS",
    default="0"
))


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        encoding="utc-8",
        level=logging.INFO,  # TODO: Parametrize log-level
    )
    return logging.getLogger(name)
