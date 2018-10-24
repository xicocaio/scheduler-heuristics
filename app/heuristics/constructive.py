import numpy as np
import pandas as pd
from collections import OrderedDict
import time
from heuristics import utils


def heur(df=None, d=None, h=None):
    # jobs after d
    early_dict = OrderedDict()

    ba_diff_asc = False

    # best for ba_diff_df descending, for h=0.2, results were better with
    # ba_diff_df ascending
    if h > 0.5:
        ba_diff = 1  # best overall = 1
    elif 0.25 < h <= 0.5:
        ba_diff = 3  # best overall = 3
    else:
        ba_diff = 5  # best overall = 5

    # # best for ba_diff_df ascending
    # if h > 0.75:
    #     ba_diff = 1  # best overall = 1
    # elif 0.5 < h <= 0.75:
    #     ba_diff = 2  # best overall = 2
    # else:
    #     ba_diff = 3  # best overall = 3 for h=0.2 k < 50, else best = 5

    # the idea here is to place the jobs with lower ba_diff in tardy group
    tardy_dict = df[df['b'] - df['a'] <= ba_diff].to_dict('index')

    # we then pick the reamining jobs, order them by highest p/a first and, if
    # they fit, try to place them on early group
    ba_diff_df = df[df['b'] - df['a'] >
                    ba_diff].sort_values(['pa'], ascending=ba_diff_asc)

    early_time_window = d
    for idx, row in ba_diff_df.iterrows():
        if idx not in early_dict and idx not in tardy_dict:
            p = row['p']
            if early_time_window - p >= 0:
                early_dict[idx] = row.to_dict()
                early_time_window -= p
            else:
                tardy_dict[idx] = row.to_dict()

    tardy_dict = OrderedDict(
        sorted(tardy_dict.items(), key=lambda x: x[1]['pb']))
    early_dict = OrderedDict(
        sorted(early_dict.items(), key=lambda x: x[1]['pa']))

    return utils.get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict


# return (get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict)
def run(df=None, d=None, h=None):
    cost = heur(df, d, h)

    return cost
