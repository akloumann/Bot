from __future__ import print_function
import random
import copy
import const as c
from env2 import ENVIRONMENT

class ENVIRONMENTS:
    def __init__(self):
        self.envs = {}
        # for i in range(0, c.numEnvs):
        for i in c.envsToRun:
            self.envs[i] = ENVIRONMENT(i)