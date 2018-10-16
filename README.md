# scheduler-heuristics
Solving the scheduler early tardy (E/T) just in time (JIT) common due date (CDD) scheduling problem with constructive, local search and tabu search heuristics

## Stack

The stack bellow was used mostly due to it's ease of installation, configuration and also efficiency and portability.
* Language: Python (3.5.2)

## Pre-installation

This system was developed in Ubuntu 16.04, but will work properly on any other Operational System(OS X, Windows, etc.).

However, this guide will only include instructions for plugins and packages that are not already installed on this OS. For this reason, we assume that technologies like a python interpreter and SQLite are ready for use, and should not be on the scope of this document.

* Now install pipenv dependency manager:

```bash

$ pip install --user pipenv

```

## Project configuration

Now we'll start setting up the project.

* Clone the repo from github and change to project root directory.
After that install project dependencies and go topython virtual env, by running:

```bash
$ pipenv install
$ pipenv shell
```

## Running the project

Now we will run the simulations of the project, for a given file.

* The project will do the following actions
    1. Run simulations on the specified file for all values of h(0.2, 0.4. 0.6, 0.8)

```bash
$ python app --filename=sch10
```
