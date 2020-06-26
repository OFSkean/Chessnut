import wrappers.board
from evaluation.genetics import *
import engine.engine as ee
numberOfGames = 1000

if __name__ == "__main__":
    ee.train()
"""
results = {'checkmate': 0, 'draw': 0}
checkmates = {'white': 0, 'black': 0}

while numberOfGames > 0:
    board = wrappers.board.Board()
    while not board.is_over():
        move = startSearch(board)
        board.apply_move(move.uci())

    if board.is_checkmate():
        results['checkmate'] += 1
        blackVictor = board.white_to_move()
        if blackVictor:
            checkmates['black'] += 1
        else:
            checkmates['white'] += 1

    else:
        results['draw'] += 1

    numberOfGames -= 1

print(results)
print(checkmates)
"""

