import pandas as pd
from models.schedule import Schedule


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
