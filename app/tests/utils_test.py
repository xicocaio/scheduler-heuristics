from heuristics import utils


def sequence_test(n_jobs, schedule):
    if utils.is_valid(n_jobs, schedule):
        pass
    else:
        raise ValueError('Solution is wrong')
