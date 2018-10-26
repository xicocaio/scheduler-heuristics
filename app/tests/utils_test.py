from heuristics import utils


def sequence_test(df=None, schedule=None):
    if utils.is_valid(len(df.index), schedule):
        pass
    else:
        raise ValueError('Solution is wrong')
