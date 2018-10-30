from collections import OrderedDict


class Schedule:

    def __init__(self, d, start, early_seq, tardy_seq):
        self.d = d

        # maybe do this p_sum_early = sum(item['p'] for item in
        # early_seq.values())
        self.start = start

        self.early_seq = early_seq
        self.tardy_seq = tardy_seq

    def move_job(self, job):
        start = self.start
        early_seq = self.early_seq.copy()
        tardy_seq = self.tardy_seq.copy()

        if job in early_seq:
            values = early_seq[job]
            start = start + values['p']
            del(early_seq[job])
            tardy_seq[job] = values
        else:
            values = tardy_seq[job]
            start = start - values['p']
            del(tardy_seq[job])
            early_seq[job] = values

        return Schedule(self.d, start, early_seq, tardy_seq)
