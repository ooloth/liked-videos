import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        style="{",
        format="{asctime} {levelname:<8} {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
