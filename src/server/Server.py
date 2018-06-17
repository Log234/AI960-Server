from threading import Thread

import eventlet
import socketio
from eventlet import wsgi

from src.statistics.Statistics import GlobalStatistics, GameStatistics


class ChessNamespace(socketio.Namespace):
    def __init__(self, position_function, get_global_stats, get_game_stats, room):
        super(ChessNamespace, self).__init__(None)
        self.get_position = position_function
        self.get_global_stats = get_global_stats
        self.get_game_stats = get_game_stats
        self.public_room = room

    def on_connect(self, sid, environment):
        print('Connected: ', sid)
        position = self.get_position()
        global_stats: GlobalStatistics = self.get_global_stats()
        game_stats: GameStatistics = self.get_game_stats()

        data = {
            "position": position,
            "gamesPlayed": global_stats.games_played,
            "whiteWins": global_stats.white_wins,
            "draws": global_stats.draws,
            "blackWins": global_stats.draws,
            "turn": game_stats.turn
        }
        self.emit('sendGame', data=data, room=sid)
        print('Sent game: ', data)
        self.enter_room(sid, self.public_room)
        print("Entered room: ", sid, " - ", self.public_room)


class Server:
    public_room = "atrium"
    sio: socketio.server = socketio.Server(async_mode='gevent')
    app = socketio.Middleware(sio)

    def __init__(self, position_function, get_global_stats, get_game_stats):
        self.sio.register_namespace(
            ChessNamespace(position_function, get_global_stats, get_game_stats, self.public_room))

    def init_server(self):
        wsgi.server(eventlet.listen(("localhost", 8000)), self.app)

    def start(self):
        thread = Thread(target=self.init_server)
        thread.start()
        print("Server started")

    def send_position(self, data):
        self.sio.emit('sendPosition', data=data, room=self.public_room)
        print('Broadcast position: ', data)

    def send_game(self, data):
        self.sio.emit('sendGame', data=data, room=self.public_room)
