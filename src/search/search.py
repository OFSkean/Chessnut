import random
from engine.monitor import SearchMonitor
import evaluation.corex_manager as cm

#monitor = SearchMonitor(True)
currentIndividual = None
corex = cm.load()

evaluationCache = {}

def update_current_individual(individual):
    global currentIndividual
    currentIndividual = individual

def evaluate_node(node):
    rep = node.get_bitboard_representation()
    if (currentIndividual, node.bitboard_str) in evaluationCache:
        #monitor.increment_stat('cacheHits')
        return evaluationCache[(currentIndividual, node.bitboard_str)]
    else:
        labels = corex.predict(rep)
        evaluation = currentIndividual.get_position_evaluation(labels)
        evaluationCache[(currentIndividual, node.bitboard_str)] = evaluation
        return evaluation

"""
An implementation of the Alpha Beta Pruning algorithm
Inputs:
    node: root node of the game tree envelope
    depth: the depth of the search. is the bound to the number of recursive calls
    alpha: initial alpha bound, used to prune min-player nodes
    beta: initial beta bound, used to prune max-player nodes
    maximizingPlayer: keeps track of if the node is a min-player or max-player node
"""
def alphabeta(node, depth, alpha, beta, maximizingPlayer):
    #monitor.increment_stat('alphaBetaCalls')

    if depth is 0 or node.is_terminal():
        #monitor.increment_stat('nodesEvaluated')
        return evaluate_node(node)

    if maximizingPlayer:
        value = -1000
        for child in node.get_children():
            #monitor.increment_stat('nodesVisited')
            if alpha > beta:
                #monitor.increment_stat('betaBreaks')
                break  # β cut-off

            value = max(value, alphabeta(child, depth-1, alpha, beta, False))
            alpha = max(alpha, value)
        return value

    else:
        value = 1000
        for child in node.get_children():
            #monitor.increment_stat('nodesVisited')
            if beta < alpha:
                #monitor.increment_stat('alphaBreaks')
                break   # α cut-off

            value = min(value, alphabeta(child, depth-1, alpha, beta, True))
            beta = min(beta, value)
        return value

"""
An implementation of the Best Node Search (BNS) Algorithm
Inputs:
    node: root node of the game tree envelope
    alpha: initial alpha bound, set to minimum leaf node value
    beta: initial beta bound, set to maximum leaf node value
    searchDepth: the depth for the alpha-beta function call
"""
def best_node_search(node, alpha, beta, searchDepth):
    def next_guess(a, b, c):
        return random.randint(a, b)

    numSubtrees = node.num_children()
    numBetter = 0
    bestMove = random.choice(node.children)

    #monitor.time_start()
    firstPass = True
    while firstPass or not ((abs(beta - alpha) <= 1) or numBetter == 1):
        #monitor.increment_stat('BNSLoops')
        if firstPass:
            firstPass = False

        testValue = next_guess(alpha, beta, numSubtrees)
        numBetter = 0
        childrenToPrune = []

        # find which children exceed the test value
        for child in node.get_children():
            bestChildValue = alphabeta(child, searchDepth, testValue, testValue + 1, False)

            if bestChildValue >= testValue:
                numBetter += 1
                bestMove = child
            else:
                childrenToPrune.append(child)

        # update alpha and beta values with new bounds
        if numBetter == 0:
            beta = testValue
        else:
            alpha = testValue
            numSubtrees = numBetter
            for child in childrenToPrune:
                child.prune()

    #monitor.time_end()
    #monitor.display()
    #monitor.reset()
    return bestMove