import random

import chess
from chess import Board


class ChessGame:
    board: Board

    def __init__(self):
        self.board = chess.Board.from_chess960_pos(random.randint(0, 959))

    def new_game(self):
        self.board = chess.Board.from_chess960_pos(random.randint(0, 959))

    def get_current_player(self):
        return self.board.turn

    def make_move(self, move):
        self.board.push(move)

    def get_position(self):
        return self.board.shredder_fen()

    def get_result(self):
        return self.board.result()

    def is_game_over(self, claim_draw):
        return self.board.is_game_over(claim_draw)
