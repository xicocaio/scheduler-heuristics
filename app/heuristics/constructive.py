import numpy as np
import pandas as pd
from collections import OrderedDict
import time
from  heuristics import utils


def heur(df=None, d=None, h=None):
    # jobs after d
    early_dict = OrderedDict()

    ratios_pa_ascending = False

    # best for ratios pa descending, for h=0.2, results were better with pa
    # ascending
    if h > 0.5:
        ba_diff = 1  # best overall = 1
    elif 0.25 < h <= 0.5:
        ba_diff = 3  # best overall = 3
    else:
        ba_diff = 5  # best overall = 5

    # # best for ratios pa ascending
    # if h > 0.75:
    #     ba_diff = 1  # best overall = 1
    # elif 0.5 < h <= 0.75:
    #     ba_diff = 2  # best overall = 2
    # else:
    #     ba_diff = 3  # best overall = 3 for h=0.2 k < 50, else best = 5

    tardy_dict = df[df['b'] - df['a'] <= ba_diff].to_dict('index')
    ratios = df[df['b'] - df['a'] >
                ba_diff].sort_values(['pa'], ascending=ratios_pa_ascending)

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
                early_dict[idx] = {'a': row['a'], 'b': row['b'], 'p': p, 'pa': row['pa'], 'pb': row['pb']}
                early_time_window -= p
            else:
                tardy_dict[idx] = {'a': row['a'], 'b': row['b'], 'p': p, 'pa': row['pa'], 'pb': row['pb']}

    tardy_dict = OrderedDict(
        sorted(tardy_dict.items(), key=lambda x: x[1]['pb']))
    early_dict = OrderedDict(
        sorted(early_dict.items(), key=lambda x: x[1]['pa']))

    return utils.get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict


# return (get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict)
def run(df=None, d=None, h=None):
    cost = heur(df, d, h)

    return cost
