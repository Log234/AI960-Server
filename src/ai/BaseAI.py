import string
from abc import abstractmethod


class BaseAI:
    @abstractmethod
    def get_move(self, fen: string, time_limit: int) -> string:
        pass
