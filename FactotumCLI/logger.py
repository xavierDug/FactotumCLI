import logging

logging.basicConfig(
    filename="factotum.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)

def log_task(message):
    logging.info(message)
