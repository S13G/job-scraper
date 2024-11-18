import logging  # noqa


def configure_logging(log_level="INFO"):
    logging.basicConfig(  # noqa
        filename="scraper/logs/scraper.log",
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",  # noqa
    )
    # Return the logger instance
    return logging.getLogger(__name__)  # noqa
