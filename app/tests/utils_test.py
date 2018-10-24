def sequence_test(df=None, schedule=None):
    start = schedule.start
    early_seq = schedule.early_seq
    tardy_seq = schedule.tardy_seq

    # check if the solution satisfies the problem restrictions
    dict_intersect = (set(early_seq.keys()) & set(tardy_seq.keys()))

    if start < 0 or len(early_seq) + len(tardy_seq) != len(df.index) or len(dict_intersect) > 0:
        print('start < 0: {} < 0'.format(start))
        print('len(early_seq) + len(tardy_seq) == len(df.index): {} == {}'.format(
            len(early_seq) + len(tardy_seq), len(df.index)))
        print('len(dict_intersect) > 0: {}'.format(dict_intersect))
        raise ValueError('Solution is wrong')
