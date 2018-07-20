from __future__ import print_function
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import copy
import os
import operator

class Tests:
    def __init__(self):
        g = 7

    def main(self):
        # print('main')
        # print("age" + "{:8d}".format(2302), end=' ')
        # print("i  " + "{:8d}".format(2))
        # print("in " + "{:8d}".format(22), end=' ')
        # print("   " + "{:>8s}".format(str(round(2.392320,1)))) # output

        # stats = {'a': 1000, 'b': 3000, 'c': 100, 'd': 3000}
        # h = max(stats.iteritems(), key=operator.itemgetter(1))[0]
        # print(h)
        # del stats['d'], stats['b']
        # h = max(stats.iteritems(), key=operator.itemgetter(1))[0]
        # print(stats)
        s = [1,2,3]
        g = [11,22,33]
        fitnesses = {}
        j = 0
        i = 0

        while i < 2 * len(s):
            print("i", i)
            fitnesses[i] = s[j]
            i += 1
            print("i", i)
            fitnesses[i] = g[j]
            i += 1
            j += 1
        print(fitnesses)

    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory. ' + directory)

    def tups(self, y):
        tuples = []
        for i in range(0, len(y)):
            tuples.append((i, y[i]))
        print(tuples)
        return tuples

    # high not inclusive
    def ord_list(self, low, high):
        list = []
        for i in range(low, high):
            print(i, end='  ')
            list.append(i)
        print()
        return list


u = Tests()
u.main()
u.createFolder('./yoyoyo/')
