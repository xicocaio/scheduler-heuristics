import pandas as pd


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
