from time import sleep

from src import game
from src.ai import BasicAI
from src.server import Server
from src.statistics.Statistics import GlobalStatistics, GameStatistics

global_statistics = GlobalStatistics()
game_statistics = GameStatistics()


def get_global_statistics() -> GlobalStatistics:
    return global_statistics


def get_game_statistics() -> GameStatistics:
    return game_statistics


game = game.ChessGame()
server = Server(game.get_position, get_global_statistics, get_game_statistics)
server.start()

time_limit = 3

whiteAI = BasicAI()
blackAI = BasicAI()

claim_draw = False

while True:
    while not game.is_game_over(claim_draw):
        if game.get_current_player() == 0:
            game_statistics.turn += 1
            move = whiteAI.get_move(game.get_position(), time_limit)
        else:
            move = blackAI.get_move(game.get_position(), time_limit)
        print("Move: ", move)
        game.make_move(move)
        data = {
            "position": game.get_position(),
            "turn": game_statistics.turn
        }
        server.send_position(data)

    sleep(3)
    global_statistics.games_played += 1
    result = game.get_result()
    if result == "1-0":
        global_statistics.white_wins += 1
    elif result == "0-1":
        global_statistics.black_wins += 1
    else:
        global_statistics.draws += 1
    game_statistics = GameStatistics()
    game.new_game()
    data = {
        "position": game.get_position(),
        "gamesPlayed": global_statistics.games_played,
        "whiteWins": global_statistics.white_wins,
        "draws": global_statistics.draws,
        "blackWins": global_statistics.black_wins,
        "turn": game_statistics.turn
    }
    server.send_game(data)
