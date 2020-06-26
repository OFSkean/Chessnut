import chess
import chess.pgn
from collections import deque

class Board:
    def __init__(self, fen=None):
        self.board = chess.Board(fen)
        if not fen:
            self.board.reset()

    def is_over(self):
        return self.board.is_game_over()

    def get_fen(self):
        return self.board.fen()

    def get_legal_moves(self):
        return self.board.generate_legal_moves()

    def get_mirror(self):
        return Board(self.board.mirror().fen())

    def apply_move(self, move):
        return self.board.push(move)

    def get_pieces(self):
        return self.board.piece_map()

    def can_white_short_castle(self):
        return self.board.has_kingside_castling_rights(chess.WHITE)

    def can_white_long_castle(self):
        return self.board.has_queenside_castling_rights(chess.WHITE)

    def can_black_short_castle(self):
        return self.board.has_kingside_castling_rights(chess.BLACK)

    def can_black_long_castle(self):
        return self.board.has_queenside_castling_rights(chess.BLACK)

    def get_history(self):
        return [m.uci() for m in self.board.move_stack]

    def convert_to_game(self):
        game = chess.pgn.Game()

        # Undo all moves.
        switchyard = deque()
        while self.board.move_stack:
            switchyard.append(self.board.pop())

        game.setup(self.board)
        node = game

        # Replay all moves.
        while switchyard:
            move = switchyard.pop()
            node = node.add_variation(move)
            self.board.push(move)

        game.headers["Result"] = self.board.result()
        return game

    def is_checkmate(self):
        return self.board.is_checkmate()

    def white_to_move(self):
        return self.board.turn == chess.WHITE