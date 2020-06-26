# Training Config
SAVE_PGN = True
GAMES_LOCATION="C:/Users/ofsk222/PycharmProjects/Chessnut/artifacts/games/"

# Representation Config
NUM_BITS = 773

# Search Config
SEARCH_DEPTH = 2

# Genetic Configuration
GENERATIONS_LOCATION="C:/Users/ofsk222/PycharmProjects/Chessnut/artifacts/generations/"

NUM_FEATURES = 20
TOURNAMENT_GAMES = 4
TOURNAMENT_SIZE = 6
GENE_VALUE_MAGNITUDE = 10
MAX_GENE_EVALUATION = NUM_FEATURES * GENE_VALUE_MAGNITUDE
POPULATION_SIZE = 20
MUTATE_CHANCE = 0.5
NEXT_GEN_INITIAL_SIZE = 15
NUM_TOURNAMENTS = 3
NUM_GENERATIONS = 3

# CorEx Configuration
COREX_LOCATION="C:/Users/ofsk222/PycharmProjects/Chessnut/artifacts/corex"
COREX_DATASET_LOCATION="C:/Users/ofsk222/PycharmProjects/Chessnut/artifacts/corex_data.npy"
DATASET_LOCATION="H:/chess/datasets/"
DATASET_PREFIX="ficsgamesdb*"
NUM_BATCHES = 1
BATCH_SIZE = 10000
MINIMUM_PLY_COUNT = 30
MIDDLEGAME_START = 10
PLY_PER_GAME = 3
GAMES_PER_FILE = 10000