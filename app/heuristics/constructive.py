import pandas as pd
from collections import OrderedDict
import time


# def get_obj_f(early_list=None, tardy_list=None):
# 	return sum(early_list['p']*early_list['b']) + sum(tardy_list['p']*early_list['a'])


def run(df=None, d=None):
    # jobs before d
    early_dict = OrderedDict()
    # early_list = []
    # tardy_list = []
    # jobs after d
    tardy_dict = OrderedDict()
    start_time = d
    end_time = d
    cost = 0

    # 1 - append generate p/a and p/b
    # df['p/a'] = df['p'] / df['a']
    # df['p/b'] = df['p'] / df['b']

    # TODO: append a and b for sort as second criteria
    ratios = pd.concat([df['p'] / df['a'], df['p'] / df['b']], keys=['a', 'b'], names=['r'])
    ratios.sort_values(ascending=[False], inplace=True)

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

    early_cost = 0
    start = d
    for job, p in reversed(list(early_dict.items())):
        a = df.iloc[job]['a']
        early_cost += a * (d - start)
        start -= p
    # print('d: {}, job: {}, start: {}, end: {}, cost early_list: {}'.format(d, job, start, start + p, early_cost))

    tardy_cost = 0
    end = d
    for job, p in reversed(list(tardy_dict.items())):
        b = df.iloc[job]['b']
        end += p
        tardy_cost += b * (end - d)
    # print('d: {}, job: {}, start: {}, end: {}, cost tardy_list: {}'.format(d, job, end - p, end, tardy_cost))

    cost = early_cost + tardy_cost

    # great output for explaining my heuristic
    # print(df)
    # print(ratios.sort_values(ascending=[False]))

    # t = time.process_time()
    # elapsed_t = time.process_time() - t
    # print('{} ms'.format(1000 * elapsed_t))

    # 2 - create lists sorted by desc p/a asc a and p/b desc b asc
    # df_sorted_pa = df.sort_values(by=['p/a', 'a'], ascending=[False, True])
    # df_sorted_pb = df.sort_values(by=['p/b', 'b'], ascending=[False, True])

    # 3 - select the job with highest value in both lists and
    # add to early_list if p/a is higher than p/b
    # add to tardy_list otherwise

    # t = time.process_time()
    # while len(df_sorted_pa.index) > 0 or len(df_sorted_pb.index) > 0:
    # 	if len(df_sorted_pa.index) > 0 and df_sorted_pa.iloc[0]['p/a'] >= df_sorted_pb.iloc[0]['p/b']:
    # 		new_start_time = start_time - df_sorted_pa.iloc[0]['p']
    # 		idx = df_sorted_pa.index[0]
    # 		if new_start_time >= 0:
    # 			early_list.append(idx)
    # 			start_time = new_start_time
    # 			df_sorted_pb.drop([idx], inplace = True)
    # 		df_sorted_pa.drop([idx], inplace = True)

    # 	else:
    # 		idx = df_sorted_pb.index[0]
    # 		tardy_list.append(idx)
    # 		end_time = end_time + df_sorted_pb.iloc[0]['p']
    # 		try:
    # 			df_sorted_pa.drop([idx], inplace = True)
    # 		except Exception as e:
    # 			df_sorted_pb.drop([idx], inplace = True)
    # 			continue
    # 		df_sorted_pb.drop([idx], inplace = True)

    # # t = time.process_time()
    # cost_early_list = 0
    # start = d
    # for job in reversed(early_list):
    # 	p = df.iloc[job]['p']
    # 	a = df.iloc[job]['a']
    # 	cost_early_list += a * (d - start)
    # 	start -= p
    # 	# print('d: {}, job: {}, start: {}, end: {}, cost early_list: {}'.format(d, job, start, start + p, cost_early_list))

    # cost_tardy_list = 0
    # end = d
    # for job in reversed(tardy_list):
    # 	p = df.iloc[job]['p']
    # 	b = df.iloc[job]['b']
    # 	end += p
    # 	cost_tardy_list += b * (end - d)
    # 	# print('d: {}, job: {}, start: {}, end: {}, cost tardy_list: {}'.format(d, job, end - p, end, cost_tardy_list))

    # cost = cost_early_list + cost_tardy_list

    # elapsed_t = time.process_time() - t
    # print('{} ms'.format(1000 * elapsed_t))

    return int(cost)
