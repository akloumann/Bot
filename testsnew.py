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
import utils

# mode = 't'
# mode = 'r'
# if mode == 't':
#     envs = ENVIRONMENTS()
#     pop = POPULATION(10)
#     pop.InitializeRandomPop()
#     pop.Evaluate(envs, False, True)
#     for i in range(0, len(pop.p)):
#         pop.p[i].age += i
#
#     pop.Print()
#
#     alg = GENETIC_ALGORITHM()
#
#     frontpop = alg.gen_par_front_pop(pop, envs)
#     frontpop.Print()
# else:
#     alg = GENETIC_ALGORITHM()
#     # alg.main()
#     alg.combo_simple_phc_ga()

h = []
i = 0
val = 0
while i < 31:
    h.append(val)
    if i < 15:
        val += 1
    else:
        val -= 1
    i += 1

print('huh')
print(h)

utils.graph_sub([h], True, 'yo', 2, 2)
#
# fig, axes = plt.subplots(2, 2, sharex=True, sharey=True) # subplot_kw=dict(polar=True))
# axes[0, 0].plot(h)
# axes[0, 1].plot(h)
# axes[1, 1].scatter(range(len(h)), h)
# plt.show()