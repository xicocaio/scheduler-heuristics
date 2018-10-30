import numpy as np
import pandas as pd
from collections import OrderedDict
import time
from heuristics import utils
from models.schedule import Schedule


def get_neighbourhood(n_jobs, previous_schedule, previous_cost):

    neighbourhood = []
    neighbour = previous_schedule
    # cost = [utils.get_cost(previous_schedule)]
    cost = previous_cost

    for job, value in previous_schedule.early_seq.items():

        schedule = previous_schedule.move_job(job)

        # if utils.is_valid(n_jobs, schedule):
        tardy_seq = OrderedDict(
            sorted(schedule.tardy_seq.items(), key=lambda x: x[1]['pb']))
        schedule.tardy_seq = tardy_seq
        new_cost = utils.get_cost(schedule)
        if new_cost <= cost:
            cost = new_cost
            neighbour = schedule

    for job, value in previous_schedule.tardy_seq.items():
        if value['p'] <= previous_schedule.start:

            schedule = previous_schedule.move_job(job)

        # if utils.is_valid(n_jobs, schedule):
            early_seq = OrderedDict(
                sorted(schedule.early_seq.items(), key=lambda x: x[1]['pa']))
            schedule.early_seq = early_seq
            new_cost = utils.get_cost(schedule)
            if new_cost <= cost:
                cost = new_cost
                neighbour = schedule

    # cost.sort(reverse=False)

    return cost, neighbour


def create_schedule(n_jobs, schedule, cost):
    k = 5 if n_jobs > 200 else 200

    for i in range(k):
        new_cost, new_schedule = get_neighbourhood(n_jobs, schedule, cost)
        if new_cost < cost:
            cost = new_cost
            schedule = new_schedule
        else:
            break

        # if i == k - 1:
        #     print('\n\n reached max_k \n\n')

    return cost, schedule

def get_neighbourhood_two_moves(n_jobs, previous_schedule, previous_cost):

    neighbourhood = []
    neighbour = previous_schedule
    # cost = [utils.get_cost(previous_schedule)]
    cost = previous_cost

    for job, value in previous_schedule.early_seq.items():

        schedule = previous_schedule.move_job(job)

        # if utils.is_valid(n_jobs, schedule):
        tardy_seq = OrderedDict(
            sorted(schedule.tardy_seq.items(), key=lambda x: x[1]['pb']))
        schedule.tardy_seq = tardy_seq
        new_cost = utils.get_cost(schedule)
        if new_cost <= cost:
            cost = new_cost
            neighbour = schedule

    for job, value in previous_schedule.tardy_seq.items():
        if value['p'] <= previous_schedule.start:

            schedule = previous_schedule.move_job(job)

        # if utils.is_valid(n_jobs, schedule):
            early_seq = OrderedDict(
                sorted(schedule.early_seq.items(), key=lambda x: x[1]['pa']))
            schedule.early_seq = early_seq
            new_cost = utils.get_cost(schedule)
            if new_cost <= cost:
                cost = new_cost
                neighbour = schedule

    # cost.sort(reverse=False)

    return cost, neighbour


def create_schedule(n_jobs, schedule, cost):
    k = 5 if n_jobs > 200 else 200

    for i in range(k):
        new_cost, new_schedule = get_neighbourhood(n_jobs, schedule, cost)
        if new_cost < cost:
            cost = new_cost
            schedule = new_schedule
        else:
            break

        # if i == k - 1:
        #     print('\n\n reached max_k \n\n')

    return cost, schedule


