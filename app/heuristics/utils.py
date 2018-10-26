import pandas as pd
from models.schedule import Schedule


def is_valid(n_jobs, schedule=None):
    start = schedule.start
    early_seq = schedule.early_seq
    tardy_seq = schedule.tardy_seq

    # check if the solution satisfies the problem restrictions
    dict_intersect = (set(early_seq.keys()) & set(tardy_seq.keys()))

    if start < 0 or len(early_seq) + len(tardy_seq) != n_jobs or len(dict_intersect) > 0:
        print('start < 0: {} < 0'.format(start))
        print('len(early_seq) + len(tardy_seq) != n_jobs: {} != {}'.format(
            len(early_seq) + len(tardy_seq), n_jobs))
        print('len(dict_intersect) > 0: {}'.format(dict_intersect))

        return False

    return True


def get_cost(schedule):
    early_cost = tardy_cost = 0
    d = end_of_job = schedule.d

    # process early jobs
    for job, values in schedule.early_seq.items():
        a = values['a']
        p = values['p']
        early_cost += a * (d - end_of_job)
        end_of_job -= p

    # process tardy jobs
    end_of_job = d
    for job, values in schedule.tardy_seq.items():
        b = values['b']
        end_of_job += values['p']
        tardy_cost += b * (end_of_job - d)

    return int(early_cost + tardy_cost)
