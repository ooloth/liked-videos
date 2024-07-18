import logging


# TODO: add color? by log level? by log message section?
def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        style="{",
        format="{asctime} {levelname:<8} {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
