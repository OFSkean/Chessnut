import evaluation.corex as ce
from config import *
import pickle
import numpy as np
import glob
import chess.pgn
import search.node
import wrappers.board
import os

def load():
    return pickle.load(open(COREX_LOCATION, 'rb'))

def load_dataset():
    try:
        loadedDataset = np.load(COREX_DATASET_LOCATION)
        print("Using loaded dataset")
        return loadedDataset
    except FileNotFoundError:
        pass

    files = glob.glob(DATASET_LOCATION + DATASET_PREFIX)

    # load the games
    games = []
    for f in files:
        print("Loading ", f)
        loadedFile = open(f, 'r')
        for i in range(GAMES_PER_FILE):
            newGame = chess.pgn.read_game(loadedFile)
            plyCount = plyCount = sum(1 for _ in newGame.mainline())

            if plyCount > MINIMUM_PLY_COUNT:
                games.append((newGame, plyCount))
        loadedFile.close()

    # extract positions from the games
    print("Gathering positions")
    bitStrings = np.zeros(shape=(GAMES_PER_FILE*PLY_PER_GAME*len(files), NUM_BITS))
    seenBitStrings = 0
    for g, p in games:
        chosenPly = np.random.randint(MIDDLEGAME_START, p, PLY_PER_GAME)
        board = g.board()

        currentPly = 0
        seenMoves = 0
        for move in g.mainline_moves():
            currentPly += 1
            board.push(move)

            if currentPly in chosenPly:
                bitStrings[seenBitStrings, :] = (search.node.Node(None, None, wrappers.board.Board(board.fen())).get_bitboard_representation())
                seenMoves += 1
                seenBitStrings += 1

            if seenMoves >= PLY_PER_GAME:
                break

    # gather unique positions
    uniqueBitStrings = np.unique(bitStrings, axis=0)
    np.save(COREX_DATASET_LOCATION, uniqueBitStrings)

    print("Finished loading dataset")
    return uniqueBitStrings

def train(reuse=False):
    dataset = load_dataset()
    cor = ce.Corex(n_hidden=NUM_FEATURES)
    if reuse:
        cor = load()

    print("Fitting dataset to Corex")
    cor.fit(dataset)

    print("Saving Corex")
    cor.save(COREX_LOCATION)
    return cor