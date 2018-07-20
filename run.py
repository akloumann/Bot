from __future__ import print_function
from envs import ENVIRONMENTS
from pop import POPULATION
from afpo5t2 import GENETIC_ALGORITHM
import const as c
import time
import pyrosim
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import pickle
import os

alg = GENETIC_ALGORITHM()

mode = 't'
mode = 'r'
if mode == 't':
    envs = ENVIRONMENTS()
    pop = POPULATION(10)
    pop.InitializeRandomPop()
    pop.Evaluate(envs, False, True)
    for i in range(0, len(pop.p)):
        pop.p[i].age += i

    pop.Print()

    frontpop = alg.gen_par_front_pop(pop, envs)
    frontpop.Print()
else:
    # alg.main()
    alg.combo_simple_phc_ga()