import asyncio
from abc import ABC, abstractmethod
from traceback import print_exc


class Task(ABC):
    @staticmethod
    @abstractmethod
    def execute():
        ...

    @classmethod
    def start_loop(cls):
        while True:
            try:
                asyncio.get_event_loop().run_until_complete(
                    cls.execute()
                )
            except Exception:
                print_exc()
