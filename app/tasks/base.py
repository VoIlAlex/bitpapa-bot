import asyncio
import logging
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from time import sleep
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)


class Task(ABC):
    @staticmethod
    @abstractmethod
    def execute():
        ...

    @classmethod
    def start_loop(cls):
        last_processed_time: Optional[datetime] = None
        while True:
            try:
                if last_processed_time is not None and datetime.now() - last_processed_time < timedelta(milliseconds=400):
                    sleep(0.5)
                    continue
                logger.info("Processing iteration started.")
                asyncio.get_event_loop().run_until_complete(
                    cls.execute()
                )
                last_processed_time = datetime.now()
                logger.info("Processing iteration complete.")
            except Exception:
                logger.error(f"Error while processing.\n{traceback.format_exc()}")
