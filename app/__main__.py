from heuristics import constructive as h_cons, local_search as h_local
import sys
import os
import pandas as pd
import time
import numpy as np
from collections import OrderedDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COST_RESULTS_FILE_PATH = BASE_DIR + '/results/sch-costs.txt'
TIME_RESULTS_FILE_PATH = BASE_DIR + '/results/sch-time.txt'
SEQUENCE_RESULTS_FILE_PATH = BASE_DIR + '/results/sch-sequence.txt'


def run_problems(filename, heur):
    data_file_path = BASE_DIR + '/data/{}.txt'.format(filename)

    h_list = [0.2, 0.4, 0.6, 0.8]
    # h_list = [0.2]

    total_time = time.process_time()

    with open(data_file_path, 'r') as sch_file, open(COST_RESULTS_FILE_PATH, 'a') as cost_file, open(TIME_RESULTS_FILE_PATH, 'a') as time_file, open(SEQUENCE_RESULTS_FILE_PATH, 'a') as sequence_file:
        n_problems = int(sch_file.readline().strip())

        for i in range(n_problems):
            jobs = []
            n_jobs = int(sch_file.readline().strip())

            # print labels
            if i == 0:
                print('n={}'.format(n_jobs), end='\t')
                print(''.join('h = {:<8}'.format(h) for h in h_list))

            for _ in range(n_jobs):
                jobs.append(
                    [int(e) for e in sch_file.readline().strip().split()] + [0, 0])

            problem = pd.DataFrame(jobs, columns=['p', 'a', 'b', 'pa', 'pb'])
            problem['pa'] = problem['p'] / problem['a']
            problem['pb'] = problem['p'] / problem['b']
            total_p = problem['p'].sum()

            print('\nk = {} \t'.format(i + 1), end='')
            for h in h_list:
                cost = 0
                early_dict = OrderedDict()
                tardy_dict = OrderedDict()
                d = int(h * total_p)

                t = time.process_time()
                if heur == 'constructive':
                    cost, early_dict, tardy_dict = h_cons.run(
                        problem, d, h)
                elif heur == 'local':
                    cost, early_dict, tardy_dict = h_local.run(
                        problem, d, h)

                elapsed_t = time.process_time() - t

                print('{:<12d}'.format(cost), end='')
                cost_file.write('{};'.format(cost))
                time_file.write('{0:.2f};'.format(1000 * elapsed_t))
                sequence_file.write('{};{};{}\n'.format(
                    d, early_dict, tardy_dict))

            cost_file.write('\n')
            time_file.write('\n')
            sequence_file.write('\n')

        cost_file.write('\n')
        time_file.write('\n')
        sequence_file.write('\n')

    elapsed_total_time = time.process_time() - total_time
    print('\n\nproblem time: {:<.2f} ms\n\n'.format(
        1000 * elapsed_total_time), end='')


def main(**kwargs):
    heur = 'constructive'
    filenames = ['sch10', 'sch20', 'sch50',
                 'sch100', 'sch200', 'sch500', 'sch1000']

    for k, v in kwargs.items():
        if k == 'heur':
            heur = v
        if k == 'filename':
            filenames = [v]
        if k == 'h':
            h = int(v)

    # clear output file before writting
    open(COST_RESULTS_FILE_PATH, 'w').close()
    open(TIME_RESULTS_FILE_PATH, 'w').close()
    open(SEQUENCE_RESULTS_FILE_PATH, 'w').close()
    for f in filenames:
        run_problems(f, heur)


if __name__ == '__main__':
    main(**dict(arg.replace('-', '').split('=')
                for arg in sys.argv[1:]))  # kwargs
