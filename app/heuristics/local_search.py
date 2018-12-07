import numpy as np
import pandas as pd
from collections import OrderedDict
import time
from heuristics import utils
from models.schedule import Schedule
from multiprocessing import Process, Manager


def early_multiprocessing_func(job, value, previous_schedule, neighbourhood):
    schedule = previous_schedule.move_job(job)

    # if utils.is_valid(n_jobs, schedule):
    tardy_seq = OrderedDict(
        sorted(schedule.tardy_seq.items(), key=lambda x: x[1]['pb']))
    schedule.tardy_seq = tardy_seq
    cost = utils.get_cost(schedule)
    neighbourhood.append([schedule, cost])


def tardy_multiprocessing_func(job, value, previous_schedule, neighbourhood):
    schedule = previous_schedule.move_job(job)

    if value['p'] <= previous_schedule.start:

        schedule = previous_schedule.move_job(job)

        early_seq = OrderedDict(
            sorted(schedule.early_seq.items(), key=lambda x: x[1]['pa']))
        schedule.early_seq = early_seq
        cost = utils.get_cost(schedule)
        neighbourhood.append([schedule, cost])


def get_neighbourhood_multiprocessing(n_jobs, previous_schedule, previous_cost):
    manager = Manager()
    neighbourhood = manager.list()
    neighbour = previous_schedule
    # cost = [utils.get_cost(previous_schedule)]
    cost = previous_cost

    processes = []

    for job, value in previous_schedule.early_seq.items():

        p = Process(
            target=early_multiprocessing_func, args=(job, value, previous_schedule, neighbourhood))
        processes.append(p)
        p.start()

    for job, value in previous_schedule.tardy_seq.items():
        p = Process(
            target=tardy_multiprocessing_func, args=(job, value, previous_schedule, neighbourhood))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    # cost.sort(reverse=False)
    # neighbour = sorted(neighbourhood, key=lambda x: x[1])[0]
    neighbour = neighbourhood[0]

    return neighbour[1], neighbour[0]


def get_neighbourhood(n_jobs, previous_schedule, previous_cost):

    neighbourhood = []
    cost = previous_cost

    for job, value in previous_schedule.early_seq.items():

        schedule = previous_schedule.move_job(job)

        tardy_seq = OrderedDict(
            sorted(schedule.tardy_seq.items(), key=lambda x: x[1]['pb']))
        schedule.tardy_seq = tardy_seq
        cost = utils.get_cost(schedule)
        neighbourhood.append([schedule, cost])

    for job, value in previous_schedule.tardy_seq.items():
        if value['p'] <= previous_schedule.start:

            schedule = previous_schedule.move_job(job)

            early_seq = OrderedDict(
                sorted(schedule.early_seq.items(), key=lambda x: x[1]['pa']))
            schedule.early_seq = early_seq
            cost = utils.get_cost(schedule)
            neighbourhood.append([schedule, cost])

    best_neighbour = sorted(neighbourhood, key=lambda x: x[1])[0]

    best_schedule = best_neighbour[0]
    best_cost = best_neighbour[1]

    return best_cost, best_schedule


def create_schedule(n_jobs, schedule, cost):
    k = 200

    for i in range(k):
        new_cost, new_schedule = get_neighbourhood(n_jobs, schedule, cost)
        if new_cost < cost:
            cost = new_cost
            schedule = new_schedule
        else:
            break

        if i == k - 1:
            print('\n\n reached max_k \n\n')

    return cost, schedule
