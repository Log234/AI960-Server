import random
import string
from time import sleep

from chess import Board

from src.ai.BaseAI import BaseAI


class BasicAI(BaseAI):
    def get_move(self, fen: string, time_limit: int) -> string:
        sleep(time_limit)
        board = Board(fen, True)
        moves = list(board.legal_moves.__iter__())
        return moves[random.randint(0, len(moves) - 1)]
