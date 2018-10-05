import pandas as pd
from collections import OrderedDict
import time


#  calculates final cost
def get_cost(d=None, df=None, early_dict=None, tardy_dict=None):
    early_cost = tardy_cost = 0
    early_time_window = 0
    start = end = d
    
    # process early jobs
    for job, p in reversed(list(early_dict.items())):
        a = df.iloc[job]['a']
        early_cost += a * (d - start)
        start -= p
        early_time_window += p

    # check if the solution satisfies the problem restrictions
    if early_time_window > d or len(early_dict) + len(tardy_dict) != len(df.index):
    	print('early_time_window > d: {} > {}'.format(early_time_window, d))
    	print('len(early_dict) + len(tardy_dict) == len(df.index): {} == {}'.format(len(early_dict) + len(tardy_dict), len(df.index)))
    	raise ValueError('Solution is wrong')

    # process tardy jobs
    for job, p in reversed(list(tardy_dict.items())):
        b = df.iloc[job]['b']
        end += p
        tardy_cost += b * (end - d)

    return int(early_cost + tardy_cost)


# slow code | order by p/b and p/a and b and a
def h3(df=None, d=None):
    # jobs before d
    early_list = []
    # jobs after d
    tardy_list = []
    start_time = d
    end_time = d
    cost = 0

    # 1 - append generate p/a and p/b
    df['p/a'] = df['p'] / df['a']
    df['p/b'] = df['p'] / df['b']

    # 2 - create lists sorted by desc p/a asc a and p/b desc b asc
    df_sorted_pa = df.sort_values(by=['p/a', 'a'], ascending=[False, True])
    df_sorted_pb = df.sort_values(by=['p/b', 'b'], ascending=[False, True])

    # 3 - select the job with highest value in both lists and
    # add to early_list if p/a is higher than p/b
    # add to tardy_list otherwise
    while len(df_sorted_pa.index) > 0 or len(df_sorted_pb.index) > 0:
        if len(df_sorted_pa.index) > 0 and df_sorted_pa.iloc[0]['p/a'] >= df_sorted_pb.iloc[0]['p/b']:
            new_start_time = start_time - df_sorted_pa.iloc[0]['p']
            idx = df_sorted_pa.index[0]
            if new_start_time >= 0:
                early_list.append(idx)
                start_time = new_start_time
                df_sorted_pb.drop([idx], inplace=True)
            df_sorted_pa.drop([idx], inplace=True)

        else:
            idx = df_sorted_pb.index[0]
            tardy_list.append(idx)
            end_time = end_time + df_sorted_pb.iloc[0]['p']
            try:
                df_sorted_pa.drop([idx], inplace=True)
            except Exception as e:
                df_sorted_pb.drop([idx], inplace=True)
                continue
            df_sorted_pb.drop([idx], inplace=True)

    cost_early_list = 0
    start = d
    for job in reversed(early_list):
        p = df.iloc[job]['p']
        a = df.iloc[job]['a']
        cost_early_list += a * (d - start)
        start -= p

    cost_tardy_list = 0
    end = d
    for job in reversed(tardy_list):
        p = df.iloc[job]['p']
        b = df.iloc[job]['b']
        end += p
        cost_tardy_list += b * (end - d)

    cost = cost_early_list + cost_tardy_list

    return int(cost)


# order by p/a,a and p/b,b merged
def h2(df=None, d=None):
    # jobs before d
    early_dict = OrderedDict()
    # jobs after d
    tardy_dict = OrderedDict()

    ratios = pd.concat((df['p'], df['p']), keys=['a', 'b']).to_frame()
    ratios['m'] = pd.concat((df['a'], df['b']), keys=['a', 'b'], axis=0)
    ratios['r'] = ratios['p'] / ratios['m']
    ratios.sort_values(by=['r', 'm'], ascending=[False, True], inplace=True)

    # great output for explaining my heuristic
    # print(df)
    # print(ratios)

    early_window = d
    for index, row in ratios.iterrows():
        if index[1] not in early_dict and index[1] not in tardy_dict:
            p = df.iloc[index[1]]['p']
            if index[0] == 'a':
                if early_window - p > 0:
                    early_dict[index[1]] = int(p)
                    early_window -= p
            else:
                tardy_dict[index[1]] = int(p)

        # if len(early_dict) + len(tardy_dict) == len(df.index):
        # 	break

    return get_cost(d, df, early_dict, tardy_dict)


# best one: order by p/a and p/b merged
def h1(df=None, d=None):
    # jobs before d
    early_dict = OrderedDict()
    # jobs after d
    tardy_dict = OrderedDict()

    # order all jobs by ratio p/a joined with p/b in desc order
    ratios = pd.concat([df['p'] / df['a'], df['p'] / df['b']], keys=['a', 'b'], names=['r'])
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
    early_window = d
    for index, row in ratios.iteritems():
        if index[1] not in early_dict and index[1] not in tardy_dict:
            p = df.iloc[index[1]]['p']
            if index[0] == 'a':
                if early_window - p > 0:
                    early_dict[index[1]] = int(p)
                    early_window -= p
            else:
                tardy_dict[index[1]] = int(p)

    return get_cost(d, df, early_dict, tardy_dict)


def run(df=None, d=None):
    # t = time.process_time()

    cost = h1(df, d)
    # cost = h2(df, d)
    # cost = h3(df, d)

    # elapsed_t = time.process_time() - t
    # print('{} ms'.format(1000 * elapsed_t))

    return cost
