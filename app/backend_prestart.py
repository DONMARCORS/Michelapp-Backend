import logging
import sys
import os

from sqlalchemy import text
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed


# add parent directory to Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5 # 5 minutes
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise e
    
def main() -> None:
    logger.info("Initializing database...")
    init()
    logger.info("Database initialized.")


if __name__ == "__main__":
    main()