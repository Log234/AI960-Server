import random

import chess.svg


def test():
    game = ChessGame()
    print(game.board)


class ChessGame:
    board = chess.Board.from_chess960_pos(random.randint(0, 959))
