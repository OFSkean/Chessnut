import time

class Monitor:
    def __init__(self, statNames, active=False, totalRuns=0):
        self.active = active
        self.stats = {}
        self.runs = totalRuns
        for name in statNames:
            self.stats[name] = 0

    def display(self):
        for key, val in self.stats.items():
            print(key, val)

    def get_stat_names(self):
        return None

    def get_stat(self, name):
        return self.stats[name]

    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def increment_stat(self, name, value=1):
        self.stats[name] += value

    def reset(self):
        for key in self.stats:
            self.stats[key] = 0

class SearchMonitor(Monitor):
    def __init__(self, active=False):
        super().__init__(self.get_stat_names(), active)
        self.timeStart = time.time()

    def get_stat_names(self):
        return ['alphaBetaCalls', 'alphaBreaks', 'betaBreaks', 'nodesVisited', 'nodesEvaluated', 'BNSLoops', 'time', 'cacheHits']

    def time_start(self):
        self.timeStart = time.time()

    def time_end(self):
        self.increment_stat('time', time.time() - self.timeStart)