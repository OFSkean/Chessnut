from config import *
import random

class Individual:
    def __init__(self, id):
        self.genes = [random.uniform(-GENE_VALUE_MAGNITUDE, GENE_VALUE_MAGNITUDE) for i in range(NUM_FEATURES)]
        self.id = id

    def __str__(self):
        return str(self.id)

    def get_position_evaluation(self, labels):
        s = 0
        for i in range(NUM_FEATURES):
            if labels[0][i]:
                s += self.genes[i]
        return s

    def crossover(self, mate):
        crossoverPoint = random.randint(3, NUM_FEATURES-3)
        selfGoesFirst = random.randint(0, 1)
        offspring = Individual(self.id)

        offspring.genes[0:crossoverPoint] = self.genes[0:crossoverPoint] if selfGoesFirst else mate.genes[0:crossoverPoint]
        offspring.genes[crossoverPoint+1:] = self.genes[crossoverPoint+1:] if not selfGoesFirst else mate.genes[crossoverPoint+1:]

        return offspring

    def mutate(self):
        if random.random() > MUTATE_CHANCE:
            mutateIndex = random.randint(0, NUM_FEATURES-1)
            self.genes[mutateIndex] = random.uniform(-GENE_VALUE_MAGNITUDE, GENE_VALUE_MAGNITUDE)

        return self

class Generation:
    def __init__(self, initialPopulation=None):
        self.numPopulation = POPULATION_SIZE
        if initialPopulation:
            self.population = initialPopulation
        else:
            self.population = []

        self.initialize_population()

    def initialize_population(self):
        # reset id of initial population
        for i in range(len(self.population)):
            self.population[i].id = i

        while len(self.population) < self.numPopulation:
            newId = len(self.population)
            self.population.append(Individual(newId))

    def random_sample(self, sampleSize):
        return random.sample(self.population, sampleSize)

    def get_individual_with_id(self, theId):
        for i in self.population:
            if i.id == theId:
                return i

    def save(self, theId):
        with open(GENERATIONS_LOCATION + str(theId), 'w') as outFile:
            for i in self.population:
                outFile.write(''.join([str(j) for j in i.genes]) + '\n')

class Tournament:
    def __init__(self, competitors):
        self.competitors = competitors
        self.scores = {}
        self.processes = []

    def setup_tournament(self):
        matchings = []
        for a in range(len(self.competitors)):
            for b in range(a+1, len(self.competitors)):
                for match in range(TOURNAMENT_GAMES):
                    matchings.append((self.competitors[a], self.competitors[b]))

        for i in self.competitors:
            self.scores[i.id] = 0

        return matchings

    def import_scores(self, s):
        for i in s:
            if len(i) == 2:
                self.scores[i[0]] += 1
            else:
                self.scores[i[0]] += 0.5
                self.scores[i[1]] += 0.5

    def organize_scores(self):
        pretty_scores = {}
        for i in range(TOURNAMENT_SIZE):
            pretty_scores[self.competitors[i].id] = self.scores[i]

        return pretty_scores

    def get_top_two(self):
        ez = [(k, v) for k, v in self.scores.items()]
        ez = list(sorted(ez, key=lambda x: x[1], reverse=True))

        return (ez[0][0], ez[1][0])
