from heuristics import constructive as h_cons
import sys
import os.path
import pandas as pd
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_problems(filename, heur):
    data_file_path = BASE_DIR + '/data/{}.txt'.format(filename)
    cost_results_file_path = BASE_DIR + '/results/{}-costs.txt'.format(filename)
    time_results_file_path = BASE_DIR + '/results/{}-time.txt'.format(filename)

    h_list = [0.2, 0.4, 0.6, 0.8]
    # h_list = [0.8]



    with open(data_file_path, 'r') as sch_file, open(cost_results_file_path, 'w') as cost_file, open(time_results_file_path, 'w') as time_file:
        n_problems = int(sch_file.readline().strip())

        for i in range(n_problems):
            jobs = []
            n_jobs = int(sch_file.readline().strip())

            # print labels
            if i == 0:
                print('n={}'.format(n_jobs), end='\t')
                print(''.join('h = {:<8}'.format(h) for h in h_list))

            for _ in range(n_jobs):
                jobs.append([int(e) for e in sch_file.readline().strip().split()])

            problem = pd.DataFrame(jobs, columns=['p', 'a', 'b'])

            print('\nk = {} \t'.format(i + 1), end='')
            for h in h_list:
                if heur == 'constructive':
                    t = time.process_time()
                    cost, early_dict, tardy_dict = h_cons.run(problem, int(h * problem['p'].sum()))
                    elapsed_t = time.process_time() - t
                    print('{:<12d}'.format(cost), end='')
                    cost_file.write('{};'.format(cost))
                    time_file.write('{0:.2f};'.format(1000 * elapsed_t))

            cost_file.write('\n')
            time_file.write('\n')


def main(**kwargs):
    heur = 'constructive'
    filename = 'sch10'

    for k, v in kwargs.items():
        if k == 'heur':
            heur = v
        if k == 'filename':
            filename = v
        if k == 'h':
            h = int(v)

    run_problems(filename, heur)


if __name__ == '__main__':
    main(**dict(arg.replace('-', '').split('=') for arg in sys.argv[1:]))  # kwargs
