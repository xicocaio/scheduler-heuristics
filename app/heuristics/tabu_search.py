import numpy as np
import pandas as pd
from collections import OrderedDict
import time
import sys
from heuristics import utils
from models.schedule import Schedule

# tabu for each number of jobs
TABU_DURATION = {10: 4, 20: 6, 50: 20, 100: 35, 200: 70, 500: 150, 1000: 350}
MAX_ITER = {10: 100, 20: 200, 50: 900,
            100: 2000, 200: 2000, 500: 3000, 1000: 1500}
MAX_COST = sys.maxsize


def get_neighbourhood(previous_schedule):

    neighbourhood = []

    for inserted_job, job_data in previous_schedule.early_seq.items():

        schedule = previous_schedule.move_job(inserted_job)

        tardy_seq = OrderedDict(
            sorted(schedule.tardy_seq.items(), key=lambda x: x[1]['pb']))
        schedule.tardy_seq = tardy_seq
        cost = utils.get_cost(schedule)
        neighbourhood.append([inserted_job, schedule, cost])

    for inserted_job, job_data in previous_schedule.tardy_seq.items():
        if job_data['p'] <= previous_schedule.start:

            schedule = previous_schedule.move_job(inserted_job)

            early_seq = OrderedDict(
                sorted(schedule.early_seq.items(), key=lambda x: x[1]['pa']))
            schedule.early_seq = early_seq
            cost = utils.get_cost(schedule)
            neighbourhood.append([inserted_job, schedule, cost])

    # return sorted neighbourhood by cost ascending
    return sorted(neighbourhood, key=lambda x: x[2])


def create_schedule(n_jobs, opt_schedule, opt_cost):
    cur_cost = opt_cost
    cur_schedule = opt_schedule

    tabu_dict = dict()

    k = MAX_ITER[n_jobs]
    tabu_duration = TABU_DURATION[n_jobs]

    for iteration in range(0, k):
        neighbourhood = get_neighbourhood(cur_schedule)

        for inserted_job, schedule, cost in neighbourhood:
            if cost < opt_cost:
                tabu_dict[inserted_job] = iteration + tabu_duration
                opt_cost, opt_schedule = cost, schedule
                cur_cost, cur_schedule = cost, schedule
                break
            elif inserted_job not in tabu_dict or tabu_dict[inserted_job] < iteration:
                tabu_dict[inserted_job] = iteration + tabu_duration
                cur_cost, cur_schedule = cost, schedule
                break

    return opt_cost, opt_schedule
