import numpy as np
import pandas as pd
from collections import OrderedDict
import time

# calculates final cost


def get_cost(d=None, df=None, early_dict=None, tardy_dict=None):
    early_cost = tardy_cost = 0
    early_time_window = 0
    end_of_job = d

    # process early jobs
    for job, values in early_dict.items():
        a = values['a']
        p = values['p']
        early_cost += a * (d - end_of_job)
        end_of_job -= p
        early_time_window += p

    # check if the solution satisfies the problem restrictions
    dict_intersect = set(early_dict.keys()) & set(tardy_dict.keys())
    if early_time_window > d or len(early_dict) + len(tardy_dict) != len(df.index) or len(dict_intersect) > 0:
        print('early_time_window > d: {} > {}'.format(early_time_window, d))
        print('len(early_dict) + len(tardy_dict) == len(df.index): {} == {}'.format(
            len(early_dict) + len(tardy_dict), len(df.index)))
        print('len(dict_intersect) > 0: {}'.format(dict_intersect))
        raise ValueError('Solution is wrong')

    # process tardy jobs
    end_of_job = d
    for job, values in tardy_dict.items():
        b = values['b']
        end_of_job += values['p']
        tardy_cost += b * (end_of_job - d)

    return int(early_cost + tardy_cost)


def heur(df=None, d=None, h=None):
    # jobs after d
    early_dict = OrderedDict()

    if h > 0.5:
        ba_diff = 1
    elif 0.25 < h <= 0.5:
        ba_diff = 3
    else:
        ba_diff = 6

    tardy_dict = df[df['b'] - df['a'] <= ba_diff].to_dict('index')
    ratios = df[df['b'] - df['a'] >
                ba_diff].sort_values(['pa'], ascending=False)

    # the idea here is to place the jobs with higher ratio
    # farthest from the center d and in the group that
    # corresponds to that calculated penalty
    # eg. a job that has the highest ratio r = 10
    # with p = 10 and a = 1, will be placed in the early group
    # farthest to the left of d as possible, the next one in order
    # will go after the last one, and so on
    # unless there is no space on early group
    # in this case this job is ignored, and we follow to the next one
    # eg. a job that has the highest ratio r = 10 p = 10 and b= 1
    # will be placed in the late group farthest to the right of d as possible
    # the next one in order will go after the last one, and so on
    # t = time.process_time()
    early_time_window = d
    for idx, row in ratios.iterrows():
        if idx not in early_dict and idx not in tardy_dict:
            p = row['p']
            if early_time_window - p >= 0:
                early_dict[idx] = {'a': row['a'], 'p': p, 'pa': row['pa']}
                early_time_window -= p
            else:
                tardy_dict[idx] = {'b': row['b'], 'p': p, 'pb': row['pb']}

    tardy_dict = OrderedDict(
        sorted(tardy_dict.items(), key=lambda x: x[1]['pb']))
    early_dict = OrderedDict(
        sorted(early_dict.items(), key=lambda x: x[1]['pa']))

    return get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict


# return (get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict)
def run(df=None, d=None, h=None):
    cost = heur(df, d, h)

    return cost
