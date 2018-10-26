from heuristics import constructive as heur_cons, local_search as heur_local, utils
import sys
import os
import pandas as pd
import time
import numpy as np
from collections import OrderedDict
from models.result import Result, Schedule
from tests import utils_test
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_NUMBER_OF_PROBLEMS = 10


def print_results(n_jobs, h_list, heur, results, elapsed_total_time, filename_prefix):
    cost_results_file_path, time_results_file_path = get_out_filepaths(heur)

    results_file_path = BASE_DIR + \
        '/output/{}-{}-results.txt'.format(filename_prefix, heur)

    print('n={}'.format(n_jobs), end='\t')
    print(''.join('h = {:<8}'.format(h) for h in h_list))

    with open(cost_results_file_path, 'a') as cost_file, open(time_results_file_path, 'a') as time_file, open(results_file_path, 'w') as results_file:
        results_file.write('{}\n'.format(DEFAULT_NUMBER_OF_PROBLEMS))
        results_file.write(';'.join('{}'.format(h) for h in h_list) + '\n')
        results_file.write('{}'.format(n_jobs))
        for i in range(len(results)):
            job = i + 1
            print('\nk = {} \t'.format(job), end='')
            results_file.write('\n{}'.format(job))
            result = results[i]
            for r in result:
                h = r.h
                d = r.schedule.d
                start = r.schedule.start
                early_seq = r.schedule.early_seq
                tardy_seq = r.schedule.tardy_seq
                cost = r.cost
                time = r.time

                print('{:<12d}'.format(cost), end='')
                cost_file.write('{};'.format(cost))
                time_file.write('{0:.2f};'.format(1000 * time))
                results_file.write('\n{}|{}|{}|{}|{}|{}'.format(
                    h, d, start, json.dumps(list(early_seq.items())), json.dumps(list(tardy_seq.items())), cost))

            cost_file.write('\n')
            time_file.write('\n')
            # results_file.write('\n')

        cost_file.write('\n')
        time_file.write('\n')
        results_file.write('\n')

    print('\n\nproblem time: {:<.2f} ms\n\n\n'.format(
        1000 * elapsed_total_time), end='')


def read_problems(data_file_path):
    with open(data_file_path, 'r') as sch_file:
        n_problems = int(sch_file.readline().strip())

        for i in range(n_problems):
            jobs = []
            n_jobs = int(sch_file.readline().strip())

            for _ in range(n_jobs):
                jobs.append(
                    [int(e) for e in sch_file.readline().strip().split()] + [0, 0])

            df = pd.DataFrame(jobs, columns=['p', 'a', 'b', 'pa', 'pb'])
            df['pa'] = df['p'] / df['a']
            df['pb'] = df['p'] / df['b']

            yield {'i': i, 'n_jobs': n_jobs, 'df': df}


def read_cons_results(data_file_path):
    with open(data_file_path, 'r') as sch_file:
        n_problems = int(sch_file.readline().strip())
        h_list = [float(e) for e in sch_file.readline().strip().split(';')]
        n_jobs = int(sch_file.readline().strip())

        for _ in range(n_problems):
            job = int(sch_file.readline().strip())
            for _ in h_list:
                h, d, start, early_seq, tardy_dict, cost = sch_file.readline().strip().split('|')
                schedule = Schedule(int(d), int(start), OrderedDict(json.loads(
                    early_seq)), OrderedDict(json.loads(tardy_dict)))
                result = Result(n_jobs, float(h), schedule, int(cost))

                yield result


def run_problems(input_filename, h_list, heur):
    results = []

    if heur == 'cons':
        data_file_path = BASE_DIR + '/data/{}.txt'.format(input_filename)

        for problem in read_problems(data_file_path):
            n_jobs = problem['n_jobs']
            df = problem['df']
            total_p = df['p'].sum()
            result = []
            for h in h_list:
                d = int(h * total_p)

                t = time.process_time()

                schedule = heur_cons.create_schedule(df, d, h)

                elapsed_t = time.process_time() - t

                # veryfing if sequence is valid
                utils_test.sequence_test(df, schedule)

                cost = utils.get_cost(schedule)

                result_h = Result(n_jobs, h, schedule, cost, elapsed_t)
                result.append(result_h)

            results.append(result)

    if heur == 'local':
        data_file_path = BASE_DIR + \
            '/output/{}-cons-results.txt'.format(input_filename)
        h_list_len = len(h_list)
        result = []

        for cons_result in read_cons_results(data_file_path):
            t = time.process_time()

            schedule = heur_local.create_schedule(
                cons_result.h, cons_result.schedule, cons_result.cost)

            elapsed_t = time.process_time() - t

            cost = utils.get_cost(schedule)

            result_h = Result(cons_result.n_jobs, cons_result.h,
                              schedule, cost, elapsed_t)

            result.append(result_h)

            if len(result) >= h_list_len:
                results.append(result)
                result = []

    return results


def get_out_filepaths(heur):
    costs_file_path = BASE_DIR + '/output/{}-costs.txt'.format(heur)
    times_file_path = BASE_DIR + '/output/{}-times.txt'.format(heur)

    return costs_file_path, times_file_path


def clear_out_files(heur):
    costs_file_path, times_file_path = get_out_filepaths(heur)
    open(costs_file_path, 'w').close()
    open(times_file_path, 'w').close()


def main(**kwargs):
    heur = 'cons'
    filenames = ['sch10', 'sch20', 'sch50',
                 'sch100', 'sch200', 'sch500', 'sch1000']
    h_list = [0.2, 0.4, 0.6, 0.8]
    # h_list = [0.2]

    for k, v in kwargs.items():
        if k == 'heur':
            heur = v
        if k == 'filename':
            filenames = [v]
        if k == 'h':
            h = int(v)

    clear_out_files(heur)

    for filename in filenames:
        n_jobs = int(filename.replace('sch', ''))
        start_time = time.process_time()

        results = run_problems(filename, h_list, heur)

        elapsed_total_time = time.process_time() - start_time

        print_results(n_jobs, h_list, heur, results,
                      elapsed_total_time, filename)


if __name__ == '__main__':
    main(**dict(arg.replace('-', '').split('=')
                for arg in sys.argv[1:]))  # kwargs
