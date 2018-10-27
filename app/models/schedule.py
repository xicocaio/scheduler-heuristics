from collections import OrderedDict


class Schedule:

    def __init__(self, d, start, early_seq, tardy_seq):
        self.d = d
        self.start = start  # maybe do this p_sum_early = sum(item['p'] for item in early_seq.values())
        self.early_seq = early_seq
        self.tardy_seq = tardy_seq
