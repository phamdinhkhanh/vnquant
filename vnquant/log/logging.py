import logging

logging.basicConfig(
     format="%(asctime)s - %(name)s - %(levelname)s \
     - %(funcName)s - line %(lineno)d - %(message)s",
     datefmt="[%Y-%m-%d %H:%M:%S]",
     force=True
)

logger = logging.getLogger("Assitant")
logger.setLevel(logging.INFO)
