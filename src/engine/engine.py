import wrappers.board
import search.node
from search.search import *
from config import *
from datetime import datetime
from evaluation.genetics import *
import multiprocessing as mp
import os

def self_play(individualA, individualB):
    whiteIndividual = random.choice([individualA, individualB])
    blackIndividual = individualB if (whiteIndividual == individualA) else individualA

    update_current_individual(whiteIndividual)

    theBoard = wrappers.board.Board()
    moveCount = 0
    while not theBoard.is_over():
        root = search.node.Node(None, None, theBoard)
        m = best_node_search(root, -MAX_GENE_EVALUATION, MAX_GENE_EVALUATION, SEARCH_DEPTH)
        theBoard.apply_move(m.move)
        print("%5d: %d vs %d: %s" % (moveCount, whiteIndividual.id, blackIndividual.id, m.move.uci()))

        if theBoard.white_to_move():
            update_current_individual(whiteIndividual)
        else:
            update_current_individual(blackIndividual)
        moveCount += 1
    if SAVE_PGN:
        filename = str(whiteIndividual.id) + '_' + str(blackIndividual.id) + '_' +  str(datetime.now())[0:22]
        filename = filename.replace(' ', '-')
        filename = filename.replace(':', '.')

        with open(GAMES_LOCATION+filename, 'w') as outfile:
            outfile.write(str(theBoard.convert_to_game()))

    #print("finished")
    if theBoard.is_checkmate():
        if theBoard.white_to_move():
            print("%d has beat %d" % (blackIndividual.id, whiteIndividual.id))
        else:
            print("%d has beat %d" % (whiteIndividual.id, blackIndividual.id))
        return blackIndividual if theBoard.white_to_move() else whiteIndividual

    else:
        print("%d has drawn %d" % (blackIndividual.id, whiteIndividual.id))
        return None

def play_tournament_game(matching):
    a, b = matching
    victor = self_play(a, b)

    if victor:
        return (victor.id, 1)
    else:
        return (a.id, b.id, 0.5)

def run_tournaments(g):
    fitIndividualIndices = []

    for i in range(NUM_TOURNAMENTS):
        t = Tournament(g.random_sample(TOURNAMENT_SIZE))

        matchings = t.setup_tournament()

        print("Starting Tournament ", i)
        p = mp.Pool(6)
        scores = p.map(play_tournament_game, matchings)

        t.import_scores(scores)
        print(t.scores)

        winner, runnerup = t.get_top_two()
        fitIndividualIndices.append(winner)
        fitIndividualIndices.append(runnerup)

        print('---')

    fitIndividuals = [g.get_individual_with_id(i) for i in fitIndividualIndices]
    return fitIndividuals

def train():
    currentGeneration = Generation()
    currentGeneration.save(0)
    for i in range(1, NUM_GENERATIONS+1):
        print("Training Generation ", i)
        fitIndividuals = run_tournaments(currentGeneration)

        offspring = []
        for a in range(len(fitIndividuals)):
            for b in range(a + 1, len(fitIndividuals)):
                offspring.append(fitIndividuals[a].crossover(fitIndividuals[b]).mutate())

        currentGeneration = Generation(offspring)
        currentGeneration.save(i)

        print('----')