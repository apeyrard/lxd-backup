import logging
from systemd.journal import JournalHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = JournalHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
