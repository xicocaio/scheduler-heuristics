import pandas as pd
import time

# def get_obj_f(early_list=None, tardy_list=None):
# 	return sum(early_list['p']*early_list['b']) + sum(tardy_list['p']*early_list['a'])


def run(df=None, d=None):
	# jobs before d
	early_list = []
	# jobs after d
	tardy_list = []
	start_time = d
	end_time = d

	# 1 - append generate p/a and p/b
	df['p/a'] = df['p'] / df['a']
	df['p/b'] = df['p'] / df['b']

	# t = time.process_time()
	# elapsed_t = time.process_time() - t
	# print(elapsed_t)

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
				df_sorted_pb = df_sorted_pb.drop([idx])

			df_sorted_pa = df_sorted_pa.drop([idx])

		else:
			idx = df_sorted_pb.index[0]
			tardy_list.append(idx)
			end_time = end_time + df_sorted_pb.iloc[0]['p']
			try:
				df_sorted_pa = df_sorted_pa.drop([idx])
			except Exception as e:
				df_sorted_pb = df_sorted_pb.drop([idx])
				continue
			df_sorted_pb = df_sorted_pb.drop([idx])


	# print('early_list: {}, tardy_list: {}'.format(early_list,tardy_list))
	# print(df)

	cost_early_list = 0
	start = d
	for job in reversed(early_list):
		p = df.iloc[job]['p']
		a = df.iloc[job]['a']
		cost_early_list += a * (d - start)
		start -= p
		# print('d: {}, job: {}, start: {}, end: {}, cost early_list: {}'.format(d, job, start, start + p, cost_early_list))

	cost_tardy_list = 0
	end = d
	for job in reversed(tardy_list):
		p = df.iloc[job]['p']
		b = df.iloc[job]['b']
		end += p
		cost_tardy_list += b * (end - d)
		# print('d: {}, job: {}, start: {}, end: {}, cost tardy_list: {}'.format(d, job, end - p, end, cost_tardy_list))

	cost = cost_early_list + cost_tardy_list
	return int(cost)


