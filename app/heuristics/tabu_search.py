import numpy as np
import pandas as pd
from collections import OrderedDict
import time
import sys
from heuristics import utils
from models.schedule import Schedule

# tabu for each number of jobs
TABU_DURATION = {10: 8, 20: 10, 50: 10, 100: 10, 200: 20, 500: 25, 1000: 50}
MAX_ITER = {10: 20, 20: 40, 50: 20, 100: 25, 200: 40, 500: 50, 1000: 100}
MAX_COST = sys.maxsize


def get_neighbour_evaluation(opt_cost, best_neighbour_cost, best_neighbour, neighbour, job, tabu_dict, current_turn):
    neighbour_cost = utils.get_cost(neighbour)

    # aspiration criteria
    if neighbour_cost < opt_cost:
        opt_cost = neighbour_cost
        return opt_cost, neighbour_cost, neighbour, job
    else:
        if neighbour_cost < best_neighbour_cost and (job not in tabu_dict or tabu_dict[job] < current_turn):
            best_neighbour_cost = neighbour_cost
            return opt_cost, best_neighbour_cost, neighbour, job

    return opt_cost, best_neighbour_cost, best_neighbour, job


def get_neighbourhood(n_jobs, current_turn, opt_cost, cur_cost, cur_schedule, tabu_dict):
    neighbour = cur_schedule
    best_neighbour = cur_schedule
    best_neighbour_cost = MAX_COST
    cost = MAX_COST
    selected_job = -1

    for job, value in cur_schedule.early_seq.items():

        neighbour = cur_schedule.move_job(job)

        tardy_seq = OrderedDict(
            sorted(neighbour.tardy_seq.items(), key=lambda x: x[1]['pb']))
        neighbour.tardy_seq = tardy_seq

        opt_cost, best_neighbour_cost, best_neighbour, selected_job = get_neighbour_evaluation(
            opt_cost, best_neighbour_cost, best_neighbour, neighbour, job, tabu_dict, current_turn)

    for job, value in cur_schedule.tardy_seq.items():
        if value['p'] <= cur_schedule.start:

            neighbour = cur_schedule.move_job(job)

            early_seq = OrderedDict(
                sorted(neighbour.early_seq.items(), key=lambda x: x[1]['pa']))
            neighbour.early_seq = early_seq

            opt_cost, best_neighbour_cost, best_neighbour, selected_job = get_neighbour_evaluation(
                opt_cost, best_neighbour_cost, best_neighbour, neighbour, job, tabu_dict, current_turn)

    tabu_dict[selected_job] = current_turn + TABU_DURATION[n_jobs]

    return best_neighbour_cost, best_neighbour, tabu_dict


def create_schedule(n_jobs, schedule, cost):
    iteration = 0

    opt_cost = cost
    opt_schedule = schedule

    tabu_dict = dict()

    k = MAX_ITER[n_jobs]

    for i in range(k):
        cost, schedule, tabu_dict = get_neighbourhood(n_jobs, i, opt_cost, cost, schedule, tabu_dict)
        if cost < opt_cost:
            opt_cost = cost
            opt_schedule = schedule

        # if i == k - 1:
        #     print('\n\n reached max_k \n\n')

    return opt_cost, opt_schedule
