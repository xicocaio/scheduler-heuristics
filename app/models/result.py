from .schedule import Schedule


class Result:

    def __init__(self, n_jobs, h, schedule, cost, time=None):
        self.n_jobs = n_jobs
        self.h = h
        self.schedule = schedule
        self.cost = cost
        self.time = time
