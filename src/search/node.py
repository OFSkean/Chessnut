from wrappers.board import Board
import numpy as np
import random
from config import *

representationMap = {
    'r': 0, 'n': 1, 'b': 2, 'q': 3, 'k': 4, 'p': 5,
    'R': 6, 'N': 7, 'B': 8, 'Q': 9, 'K': 10, 'P': 11
}

class Node:
    def __init__(self, parentFen=None, move=None, board: Board = None):
        if not parentFen:
            assert board
            self.our_board = board
            self.their_board = board.get_mirror()
            self.parent = None
        else:
            assert parentFen and move
            self.move = move
            self.their_board = Board(parentFen)
            self.their_board.apply_move(move)
            self.our_board = self.their_board.get_mirror()

        self.evaluation = None
        self.children = []
        self.bitboard = None
        self.pruned = False

    def not_evaluated(self):
        return self.evaluation is None

    def get_evaluation(self):
        return self.evaluation

    def set_evaluation(self, e):
        self.evaluation = e

    def get_bitboard_representation(self):
        if self.bitboard is None:
            rep = np.zeros(NUM_BITS, dtype=int)

            # set piece bits
            for i, p in self.our_board.get_pieces().items():
                rep[i*12+representationMap[p.symbol()]] = 1

            # set castling bits
            rep[-5] = self.our_board.can_white_short_castle()
            rep[-4] = self.our_board.can_white_long_castle()
            rep[-3] = self.our_board.can_black_short_castle()
            rep[-2] = self.our_board.can_black_long_castle()
            rep[-1] = self.our_board.white_to_move()
            self.bitboard = rep.reshape((1, NUM_BITS))
            self.bitboard_str = ''.join([str(x) for x in self.bitboard[0].tolist()])

        return self.bitboard

    def get_children(self):
        if not self.children:
            self.children = [Node(self.our_board.get_fen(), m) for m in self.our_board.get_legal_moves()]
            return self.children
        else:
            return [c for c in self.children if not c.is_pruned()]

    def is_pruned(self):
        return self.pruned

    def prune(self):
        self.pruned = True

    def num_children(self):
        return len(self.get_children())

    def __hash__(self):
        hash(self.bitboard)

    def get_ancestor_move(self):
        currentAncestor = self.parent
        while currentAncestor.parent:
            currentAncestor = currentAncestor.parent

        return currentAncestor.move

    def get_random_move(self):
        return random.choice(self.children)

    def is_terminal(self):
        return self.our_board.is_over()


