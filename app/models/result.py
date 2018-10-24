from .schedule import Schedule


class Result:

    def __init__(self, h, schedule, cost, time=None):
        self.h = h
        self.schedule = schedule
        self.cost = cost
        self.time = time
