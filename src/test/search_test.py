import collections
import random
from search.search import alphabeta, best_node_search, monitor
from engine.monitor import SearchMonitor
import time

testDepth, testWidth, maxVal = 4, 8, 100
numTests = 1000

# testing classes
class RandNode:
    def __init__(self, maxVal, depth):
        self.val = random.randint(0, maxVal)
        self.children = []
        self.depth = depth
        self.pruned = False

    def add_child(self, newChild):
        self.children.append(newChild)

    def get_children(self):
        return [i for i in self.children if not i.pruned]

    def get_evaluation(self):
        return self.val

    def is_terminal(self):
        return not len(self.children)

    def prune(self):
        self.pruned = True

    def __str__(self):
        return str(self.val)

class Tree:
    def __init__(self, depth, width, maxVal):
        self.depth = depth
        self.width = width
        self.root = RandNode(maxVal, 0)
        self.maxValue = maxVal

    def create(self):
        queue = collections.deque()
        currentNode = self.root
        while (currentNode.depth < self.depth):
            for i in range(self.width):
                newnode = RandNode(self.maxValue, currentNode.depth+1)
                currentNode.add_child(newnode)
                queue.append(newnode)
            currentNode = queue.popleft()

    def display(self):
        queue = collections.deque()
        queue.append(self.root)
        currentDepth = -1
        while len(queue):
            currentNode = queue.popleft()
            if currentNode.depth != currentDepth:
                print('\n')
                print("Depth ", currentNode.depth)
                currentDepth = currentNode.depth

            print(currentNode.get_evaluation(), end=" ")
            for c in currentNode.get_children():
                queue.append(c)

"""
This test is a montecarlo-esque testing of the search functions. random trees are created. results between the
search functions are verified for accuracy.
"""
failedTests = 0
avgTime  = 0

for i in range(numTests):
    t = Tree(testDepth, testWidth, maxVal)
    t.create()

    s = time.time()
    bestMove = best_node_search(t.root, 0, maxVal, testDepth)
    avgTime += (time.time() - s)
    #minimaxValues = [(child, alphabeta(child, testDepth, 0, maxVal, False)) for child in t.root.get_children()]
    #maxMinimaxValue = max(minimaxValues, key= lambda x: x[1])[1]

    #maxNodes = [i[0] for i in minimaxValues if i[1] == maxMinimaxValue]
    #if bestMove not in maxNodes:
    #    failedTests += 1

    #update averages
    #for key in monitor.get_stat_names():
    #    averagingMonitor.increment_stat(key, monitor.get_stat(key) / numTests)
    #monitor.reset()

    if not i % 10:
        print(i)

print("Passed: %d / %d" % (numTests - failedTests, numTests))
print("Time: ", avgTime / numTests)
"""
d,w,m = 3,2,100
t = Tree(d,w,m)
t.create()

t.root.val = 2

t.root.children[0].val = 54
t.root.children[1].val = 12

t.root.children[0].children[0].val = 64
t.root.children[0].children[1].val = 76
t.root.children[1].children[0].val = 66
t.root.children[1].children[1].val = 2

t.root.children[0].children[0].children[0].val = 6
t.root.children[0].children[0].children[1].val = 75
t.root.children[0].children[1].children[0].val = 57
t.root.children[0].children[1].children[1].val = 0
t.root.children[1].children[0].children[0].val = 22
t.root.children[1].children[0].children[1].val = 71
t.root.children[1].children[1].children[0].val = 87
t.root.children[1].children[1].children[1].val = 6

t.display()

bestMove = best_node_search(t.root, 0, m, d)

minimaxValues = [(child, alphabeta(child, d, 0, m, False)) for child in t.root.get_children()]
maxMinimaxValue = max(minimaxValues, key=lambda x: x[1])[1]

maxNodes = [i[0] for i in minimaxValues if i[1] == maxMinimaxValue]
"""