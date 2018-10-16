import numpy as np
import pandas as pd
from collections import OrderedDict
import time


# # calculates final cost
def get_cost_h2(d=None, df=None, early_dict=None, tardy_dict=None):
    early_cost = tardy_cost = 0
    early_time_window = 0
    end_of_job = d

    # process early jobs
    for job, p in early_dict.items():
        a = df.iloc[job]['a']
        early_cost += a * (d - end_of_job)
        end_of_job -= p
        early_time_window += p

    # check if the solution satisfies the problem restrictions
    if early_time_window > d or len(early_dict) + len(tardy_dict) != len(df.index):
        print('early_time_window > d: {} > {}'.format(early_time_window, d))
        print('len(early_dict) + len(tardy_dict) == len(df.index): {} == {}'.format(
            len(early_dict) + len(tardy_dict), len(df.index)))
        raise ValueError('Solution is wrong')

    # process tardy jobs
    end_of_job = d
    for job, p in tardy_dict.items():
        b = df.iloc[job]['b']
        end_of_job += p
        tardy_cost += b * (end_of_job - d)

    return int(early_cost + tardy_cost)


#  calculates final cost
# def get_cost(d=None, df=None, early_dict=None, tardy_dict=None):
#     early_cost = tardy_cost = 0
#     early_time_window = 0
#     start = end = d

#     # process early jobs
#     for job, p in early_dict.items():
#         a = df.iloc[job]['a']
#         early_cost += a * (d - start)
#         start -= p[1]
#         early_time_window += p[1]

#     # check if the solution satisfies the problem restrictions
#     if early_time_window > d or len(early_dict) + len(tardy_dict) != len(df.index):
#         print('early_time_window > d: {} > {}'.format(early_time_window, d))
#         print('len(early_dict) + len(tardy_dict) == len(df.index): {} + {} == {}'.format(len(early_dict), len(tardy_dict),
#                                                                                          len(df.index)))
#         raise ValueError('Solution is wrong')

#     # process tardy jobs
#     for job, p in tardy_dict.items():
#         b = df.iloc[job]['b']
#         end += p[1]
#         tardy_cost += b * (end - d)

#     return int(early_cost + tardy_cost)

# calculates final cost
def get_cost_h3(d=None, df=None, early_dict=None, tardy_dict=None):
    early_cost = tardy_cost = 0
    early_time_window = 0
    end_of_job = d

    # process early jobs
    for job, values in early_dict.items():
        a = df.iloc[job]['a']
        early_cost += a * (d - end_of_job)
        end_of_job -= values['p']
        early_time_window += values['p']

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
        b = df.iloc[job]['b']
        end_of_job += values['p']
        tardy_cost += b * (end_of_job - d)

    return int(early_cost + tardy_cost)


# best one: order by p/a and p/b merged
def h4(df=None, d=None):
    # jobs before d
    early_dict = dict()
    # jobs after d
    tardy_dict = dict()

    df['p/a'] = df['p'] / df['a']
    df['p/b'] = df['p'] / df['b']

    df['b/a'] = df['b'] / df['a']

    df_sorted_ba = df.sort_values(by=['b/a'], ascending=[False])

    # order all jobs by ratio p/a joined with p/b in desc order
    # ratios = pd.concat([df['p'] / df['a'], df['p'] / df['b']], keys=['a', 'b'], names=['r'])
    # ratios.sort_values(ascending=[False], inplace=True)
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
    early_time_window = d
    i = 0
    j = len(df.index) - 1
    while i <= j:
        idx = df_sorted_ba.index[i]
        if idx not in early_dict and idx not in tardy_dict:
            p = df_sorted_ba.iloc[i]['p']
            pa = df_sorted_ba.iloc[i]['p/a']
            ba = df_sorted_ba.iloc[i]['b/a']
            if early_time_window - p > 0 and ba >= 1:
                early_dict[idx] = [int(pa), int(p)]
                early_time_window -= p
            else:
                tardy_dict[idx] = [int(df_sorted_ba.iloc[i]['p/b']), int(p)]

        idx = df_sorted_ba.index[j]
        ba = df_sorted_ba.iloc[j]['b/a']
        if idx not in early_dict and idx not in tardy_dict and ba <= 1:
            p = df_sorted_ba.iloc[j]['p']
            tardy_dict[idx] = [int(df_sorted_ba.iloc[j]['p/b']), int(p)]
            j -= 1

        i += 1

    early_dict = OrderedDict(sorted(early_dict.items(), key=lambda x: x[1][0]))
    tardy_dict = OrderedDict(sorted(tardy_dict.items(), key=lambda x: x[1][0]))
    # print(early_dict)
    # early_jobs = pd.DataFrame.from_dict(early_dict, orient='index', columns=['p/a', 'p'])

    return (get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict)

# order by p/a,a and p/b,b merged


def h3(df=None, d=None, h=None):
    # jobs after d
    early_dict = OrderedDict()

    if h > 0.5:
        ba_coef = 1.25
    elif h == 0.4:
        ba_coef = 1.5  # the best one for k=100 was 1.5, but was not very good for k=10
    elif h == 0.2:
        ba_coef = 2.5  # the best one for k=100 was 2.5, tried a little above and a little below, and this was the best, but was not very good for k=10 or 20

    # if len(df.index) >= 50:
    #     if h > 0.5:
    #         ba_coef = 1.25
    #     elif h == 0.4:
    #         ba_coef = 1.5  # the best one for k=100 was 1.5, but was not very good for k=10
    #     elif h == 0.2:
    #         ba_coef = 2.5  # the best one for k=100 was 2.5, tried a little above and a little below, and this was the best, but was not very good for k=10 or 20
    # else:
    #     if h > 0.75:
    #         ba_coef = 1.3
    #     elif h >= 0.5:
    #         ba_coef = 1.5
    #     elif h > 0.25:
    #         ba_coef = 1.4
    #     else:
    #         ba_coef = 1.5  # the best one for k=100 was 1.5, but was not very good for k=10

    # order all jobs by ratio p/a joined with p/b in desc order

    # pa = pd.concat((df['p'] / df['a'], df['b'] / df['a']), axis=1)
    # pb = pd.concat((df['p'] / df['b'], df['b'] / df['a']), axis=1)

    # ratios = pd.concat((pa, pb), keys=['a', 'b'])
    # ratios.columns = ['r', 'ba']

    ratios = df[['p', 'b']][df['b'] / df['a'] <= ba_coef]
    ratios['pb'] = df['p'] / df['b']
    tardy_dict = ratios.to_dict('index')
    # print(ratios)

    #
    #
    # OUTSTANDING RESULTS FOR HIGHER VALUES OF K WHEN COMPLETING FROM CLOSE TO d TO START OF SEQUENCE, just change ascending to TRUE below
    #
    #
    #

    ratios = df[['p', 'b', 'a']][df['b'] / df['a'] > ba_coef]
    ratios['pb'] = df['p'] / df['b']
    ratios['pa'] = df['p'] / df['a']
    ratios.sort_values(['pa'], ascending=True, inplace=True)
    # print(ratios)

    # test = test.assign(f = test['p'] / test['a']).sort_values('f', ascending=[True])
    # print(test)
    # print(test.to_dict('index'))

    # ratios.sort_values(['r'],ascending=[False], inplace=True)

    # print(ratios)

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
    early_time_window = d
    for idx, row in ratios.iterrows():
        if idx not in early_dict and idx not in tardy_dict:
            p = row['p']
            if early_time_window - p >= 0:
                early_dict[idx] = {'a': row['a'], 'p': p, 'pa': row['pa']}
                early_time_window -= p
            else:
                tardy_dict[idx] = {'b': row['a'], 'p': p, 'pb': row['pb']}

    tardy_dict = OrderedDict(
        sorted(tardy_dict.items(), key=lambda x: x[1]['pb']))
    early_dict = OrderedDict(
        sorted(early_dict.items(), key=lambda x: x[1]['pa']))
    # print(tardy_dict)

    # early_df = pd.DataFrame.from_dict(early_dict, orient='index', columns=['a', 'pa', 'p'])
    # print(early_df)
    # early_df.sort_values(['pa'], ascending=False, inplace=True)
    # print(early_df)

    return (get_cost_h3(d, df, early_dict, tardy_dict), early_dict, tardy_dict)

#


def h2(df=None, d=None, h=None):
    # jobs before d
    early_dict = OrderedDict()
    # jobs after d
    tardy_dict = OrderedDict()

    if h > 0.5:
        ba_coef = 1.25
    elif h == 0.4:
        ba_coef = 1.5  # the best one for k=100 was 1.5, but was not very good for k=10
    elif h == 0.2:
        ba_coef = 2.5  # the best one for k=100 was 2.5, tried a little above and a little below, and this was the best, but was not very good for k=10 or 20

    # order all jobs by ratio p/a joined with p/b in desc order

    pa = pd.concat((df['p'] / df['a'], df['b'] / df['a']), axis=1)
    pb = pd.concat((df['p'] / df['b'], df['b'] / df['a']), axis=1)

    ratios = pd.concat((pa, pb), keys=['a', 'b'])
    ratios.columns = ['r', 'b/a']

    ratios.sort_values(['r'], ascending=[False], inplace=True)

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

    early_time_window = d
    for index, row in ratios.iterrows():
        if index[1] not in early_dict and index[1] not in tardy_dict:
            p = df.iloc[index[1]]['p']
            if index[0] == 'a' and row['b/a'] >= ba_coef:
                if early_time_window - p > 0:
                    early_dict[index[1]] = int(p)
                    early_time_window -= p
            else:
                tardy_dict[index[1]] = int(p)

    # correct the order of thd dicts so they are sequential
    early_dict = OrderedDict(reversed(list(early_dict.items())))
    tardy_dict = OrderedDict(reversed(list(tardy_dict.items())))

    return (get_cost_h2(d, df, early_dict, tardy_dict), early_dict, tardy_dict)


# first version
def h1(df=None, d=None):
    # jobs before d
    early_dict = OrderedDict()
    # jobs after d
    tardy_dict = OrderedDict()

    # order all jobs by ratio p/a joined with p/b in desc order
    ratios = pd.concat([df['p'] / df['a'], df['p'] / df['b']],
                       keys=['a', 'b'], names=['r'])
    ratios.sort_values(ascending=[False], inplace=True)

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
    early_time_window = d
    for index, row in ratios.iteritems():
        if index[1] not in early_dict and index[1] not in tardy_dict:
            p = df.iloc[index[1]]['p']
            if index[0] == 'a':
                if early_time_window - p > 0:
                    early_dict[index[1]] = int(p)
                    early_time_window -= p
            else:
                tardy_dict[index[1]] = int(p)

        # correct the order of thd dicts so they are sequential
    early_dict = OrderedDict(reversed(list(early_dict.items())))
    tardy_dict = OrderedDict(reversed(list(tardy_dict.items())))

    return (get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict)


# return (get_cost(d, df, early_dict, tardy_dict), early_dict, tardy_dict)
def run(df=None, d=None, h=None):
    # t = time.process_time()

    # cost = h1(df, d)
    # cost = h2(df, d, h)
    cost = h3(df, d, h)
    # cost = h4(df, d)

    # elapsed_t = time.process_time() - t
    # print('{} ms'.format(1000 * elapsed_t))

    return cost
