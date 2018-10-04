from heuristics import constructive as h_cons
import sys
import os.path
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_problems(filename, heur):
    data_file_path = BASE_DIR + '/data/{}'.format(filename)

    h_list = [0.2, 0.4, 0.6, 0.8]
    # h_list = [0.8]

    with open(data_file_path, 'r') as sch_file:
        n_problems = int(sch_file.readline().strip())

        for i in range(n_problems):
            jobs = []
            n_jobs = int(sch_file.readline().strip())

            # print labels
            if i == 0:
                print('n={}'.format(n_jobs), end = '\t')
                print(''.join('h = {:<8}'.format(h) for h in h_list))

            for _ in range(n_jobs):
                jobs.append([int(e) for e in sch_file.readline().strip().split()])

            problem = pd.DataFrame(jobs, columns=['p', 'a', 'b'])

            print('\nk = {} \t'.format(i + 1), end='')
            for h in h_list:
                if heur == 'constructive':
                    cost = h_cons.run(problem, round(h*problem['p'].sum()))
                    print('{:<12d}'.format(cost), end = '')

def main(**kwargs):
    heur = 'constructive'
    filename = 'sch10.txt'

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