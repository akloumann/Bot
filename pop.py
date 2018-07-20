from __future__ import print_function
from indv import INDIVIDUAL
import copy
import random
import const as c
import operator
import pickle
import matplotlib.pyplot as plt
import numpy as np
import math

prnt = False


class POPULATION:

    def __init__(self, popSize):
        self.popSize = popSize
        self.p = {}
        self.angle = random.uniform(0, math.pi / 3)

    def FillWithRandIndv(self, index):
        first = np.random.random_sample((c.numInputs, c.numHidden)) * 2 - 1
        second = np.random.random_sample((c.numHidden, c.numOutputs)) * 2 - 1

        genome = [first, second]
        self.p[index] = INDIVIDUAL(index, genome, 0)  # age=0

    def InitializeRandomPop(self):
        for i in range(0, self.popSize):
            first = np.random.random_sample((c.numInputs, c.numHidden)) * 2 - 1
            second = np.random.random_sample((c.numHidden, c.numOutputs)) * 2 - 1
            genome = [first, second]
            self.p[i] = INDIVIDUAL(i, genome, 0)  # age=0

    def InitializeUniformPop(self, genome):
        for i in range(0, len(self.p)):
            self.p[i] = INDIVIDUAL(i, genome, 0)

    def IncrementAges(self):
        # print("    length self.p   ", len(self.p))
        for i in range(0, len(self.p)):
            # print("in IncrementAges() ind", i, "age", self.p[i].age)
            self.p[i].age = self.p[i].age + 1

    # def Print(self, gen=0):
    #     for i in self.p:
    #         self.p[i].Print()
    #     print()

    def Print(self, gen=0):
        align_val = "{:^" + str(9) + "s}"
        print("Inds:  |", end=" ")
        for i in self.p:
            print(align_val.format(str(i)), end=" | ")
        print()

        print("IDs :  |", end=" ")
        for i in self.p:
            print(align_val.format(str(self.p[i].ID)), end=" | ")
        print()

        # print("Ages:  |", end=" ")
        # for i in self.p:
        #     print(align_val.format(str(self.p[i].age)), end=" | ")
        # print()

        print("CosTh: |", end=" ")
        for i in self.p:
            print(align_val.format(str(round(self.p[i].avgCosThetaBotLight, 3))), end=" | ")
        print()

        # print("JAM:   |", end=" ")
        # for i in self.p:
        #     print(align_val.format(str(round(self.p[i].jointAngMult, 3))), end=" | ")
        #
        # print()

        print("Dists: |", end=" ")
        for i in self.p:
            print(align_val.format(str(round(self.p[i].avgDist, 3))), end=" | ")
        print()

        print("Fits:  |", end=" ")
        for i in self.p:
            print(align_val.format(str(round(self.p[i].fitness, 3))), end=" | ")
        print()

    def PrintDists(self, gen=0):
        # print('PrintDists popsize:', len(self.p))
        print(gen, end=' ')
        for i in self.p:
            self.p[i].PrintDist()
        print()

    # # Called after Evaluate()
    # def AgeFitPO(self):
    #     fit_inv_vals = []
    #     for i in range(0, len(self.p)):
    #         fit_inv_vals.append(self.p[i].fitness)
    #
    #
    #     # #######################################################
    #     # high = 15
    #     # size = 15
    #     # yy = np.random.randint(4, 15, size)
    #     # xx = np.random.randint(0, size, size)
    #     # ord_list = self.ord_list(0, size)
    #     # checked_list = [False] * size
    #     # dominated_list = [0] * size
    #     #
    #     # print('xx', xx, '\nyy', yy, '\nol', ord_list, '\ncl', checked_list, '\ndl', dominated_list)
    #     # print()
    #     #
    #     # for i in range(0, size):
    #     #     for j in range(0, size):
    #     #         if j == i:
    #     #             continue
    #     #         if yy[i] < yy[j] and xx[i] < xx[j]:
    #     #             dominated_list[j] = 1
    #     #         elif yy[j] < yy[i] and xx[j] < xx[i]:
    #     #             dominated_list[i] = 1
    #     #             break
    #     # print('dl', dominated_list)
    #     #
    #     # pareto_front_x = []
    #     # pareto_front_y = []
    #     # xx_copy = []
    #     # yy_copy = []
    #     #
    #     # for i in range(0, size):
    #     #     if dominated_list[i] == 0:
    #     #         pareto_front_x.append(xx[i])
    #     #         pareto_front_y.append(yy[i])
    #     #     else:
    #     #         xx_copy.append(xx[i])
    #     #         yy_copy.append(yy[i])
    #     # #######################################################
    #

    def Evaluate(self, envs, pp, pb):
        for i in self.p:
            self.p[i].fitness = 0
            self.p[i].avgDist = 0
            self.p[i].envsProg = []

        for e in c.envsToRun:
            # print('e', e)
            send = True
            for i in self.p:
                self.p[i].Start_Evaluation(envs.envs[e], pp, pb)
                send = False
            for i in self.p:
                self.p[i].Compute_Fitness(envs.envs[e])

        for i in self.p:
            self.p[i].fitness /= c.numEnvs
            self.p[i].fitness *= 1 / (1 + np.std(self.p[i].envsProg))
            self.p[i].fitness = round(self.p[i].fitness, 4)
            self.p[i].avgDist /= c.numEnvs

    def Mutate(self):
        for i in self.p:
            self.p[i].Mutate()

    def ReplaceWith(self, other):
        for i in self.p:
            if self.p[i].fitness < other.p[i].fitness:
                self.p[i] = other.p[i]

    # called in geneticAlgorithm.py
    def FillFrom(self, other):
        # this fills the first slots with the best individuals in parent pop
        self.CopyBestFrom(other)
        # this fills remaining slots
        self.CollectChildrenFrom(other)

    # called in FillFrom()
    # need to fill several instead of just first
    def CopyBestFrom(self, other):
        fitnesses = {}
        bestinds = {}
        j = 0
        i = 0
        while i < 2 * len(self.p):
            fitnesses[i] = other.p[j].fitness
            i += 1
            fitnesses[i] = self.p[j].fitness
            j += 1
            i += 1

        for i in range(0, c.cutoff):
            maxfitkey = max(fitnesses.iteritems(), key=operator.itemgetter(1))[0]
            if maxfitkey % 2 == 0:
                self.p[i] = copy.deepcopy(other.p[maxfitkey / 2])
                del fitnesses[maxfitkey], fitnesses[maxfitkey + 1]
            else:
                self.p[i] = copy.deepcopy(self.p[maxfitkey / 2])
                del fitnesses[maxfitkey], fitnesses[maxfitkey - 1]

    # called in FillFrom()
    # fills up the remaining slots of the children population and mutates them.
    def CollectChildrenFrom(self, other):
        for i in range(c.cutoff, self.popSize):
            winner = self.WinnerOfTournamentSelection(other, i)
            self.p[i] = copy.deepcopy(winner)
            self.p[i].Mutate()

    # called in CollectChildrenFrom()
    # this function accepts the children object and the parent object (other), generates
    # 2 distinct random numbers between 0 and popSize that are used as indices to pick two random
    # individuals from the parent population, compare their fitness, and return the index of the better one.
    def WinnerOfTournamentSelection(self, other, i):
        p1 = random.randint(0, self.popSize - 1)

        # first 2 parents, second 2 children
        four_fitnesses = []
        four_fitnesses.append(other.p[i].fitness)
        four_fitnesses.append(other.p[p1].fitness)
        four_fitnesses.append(self.p[i].fitness)
        four_fitnesses.append(self.p[p1].fitness)

        hi_ind = four_fitnesses.index(max(four_fitnesses))

        if hi_ind == 0:
            return other.p[i]
        elif hi_ind == 1:
            return other.p[p1]
        elif hi_ind == 2:
            return self.p[i]
        elif hi_ind == 3:
            return self.p[p1]

    ############# Original #####################
    # # called in geneticAlgorithm.py
    # def FillFrom(self, other):
    #     # this fills the first slots with the best individuals in parent pop
    #     self.CopyBestFrom(other)
    #     # this fills remaining slots
    #     self.CollectChildrenFrom(other)
    #
    # # called in FillFrom()
    # # need to fill several instead of just first
    # def CopyBestFrom(self, other):
    #     # stores fitness vals in dictionary fitnesses.
    #     fitnesses = {}
    #     bestInds = {}
    #     for i in range(0, self.popSize):
    #         fitnesses[i] = other.p[i].fitness
    #
    #     # searches fitnesses for highest val and returns key (index)
    #     for i in range(0, c.cutoff):
    #         bestInds[i] = max(fitnesses.iteritems(), key=operator.itemgetter(1))[0]
    #         # print('max fitness', i, ':', fitnesses[bestInds[i]])
    #         del fitnesses[bestInds[i]]
    #
    #     for i in range(0, c.cutoff):
    #         # print('bestInds[' + str(i) +']', bestInds[i])
    #         self.p[i] = copy.deepcopy(other.p[bestInds[i]])
    #
    # # called in FillFrom()
    # # fills up the remaining slots of the children population and mutates them.
    # def CollectChildrenFrom(self, other):
    #     for i in range(c.cutoff, self.popSize):
    #         winner = self.WinnerOfTournamentSelection(other, i)
    #         self.p[i] = copy.deepcopy(winner)
    #         self.p[i].Mutate()
    #
    # # # called in CollectChildrenFrom()
    # # # this function accepts the children object and the parent object (other), generates
    # # # 2 distinct random numbers between 0 and popSize that are used as indices to pick two random
    # # # individuals from the parent population, compare their fitness, and return the index of the better one.
    # # def WinnerOfTournamentSelection(self, other, i):
    # #     p1 = random.randint(0, self.popSize - 1)
    # #
    # #     if (other.p[p1].fitness > other.p[i].fitness):
    # #         betterInd = p1; #label = 'p1'
    # #     else:
    # #         betterInd = i; #label = 'p' + str(i)
    # #
    # #     return other.p[betterInd]
    #
    # def WinnerOfTournamentSelection(self, other, i):
    #     p1 = random.randint(0, self.popSize - 1)
    #
    #     if (other.p[p1].fitness > other.p[i].fitness):
    #         betterInd = p1; #label = 'p1'
    #     else:
    #         betterInd = i; #label = 'p' + str(i)
    #
    #     return other.p[betterInd]

    ####################### Original ###########
    def Pickling(self, other):
        # print(other.p[0].genome)

        for i in range(0, len(other.p)):
            print('fitnesss to pickle:', other.p[i].fitness)
            # fitnessScaled = round(other.p[i].fitness, 3)
            fitnessScaled = int(other.p[i].fitness)
            filename = 'genome' + str(fitnessScaled)
            pathSave = c.pathSave
            filename = pathSave + filename
            e = open(filename, 'w')
            pickle.dump(self.p[i].genome, e)
            e.close()

    def GetFits(self):
        fits = []
        for i in range(0, len(self.p)):
            fits.append(self.p[i].fitness)
        return fits

    def GetFitsInv(self):
        fits_inv = []
        for i in range(0, len(self.p)):
            if self.p[i].fitness > 0:
                fits_inv.append(self.p[i].fitness ** -1)
            elif self.p[i].fitness == 0:
                fits_inv.append(10 ** 6)
            else:
                raise ValueError("Fitness " + fits[i] + " less than 0. -AK")
        return fits_inv

    def GetAges(self):
        ages = []
        for i in range(0, len(self.p)):
            ages.append(self.p[i].age)
        return ages

    def Pickling618(self):
        # print(other.p[0].genome)

        for i in range(0, len(self.p)):
            # print('fitness pickle:', self.p[i].fitness)
            fitnessScaled = int(self.p[i].fitness * 100)
            filename = 'genome' + str(fitnessScaled) + str(i)
            pathSave = c.pathSave
            filename = pathSave + filename
            e = open(filename, 'w')
            pickle.dump(self.p[i].genome, e)
            e.close()

        # filenameBot = 'bot' + str(fitnessScaled)
        # fullPath = '/home/iskander/PycharmProjects/EvoBotProject/genomes/'
        # filenameBot = fullPath + filenameBot
        # e = open(filenameBot, 'w')
        # pickle.dump(self.p[0], e)
        # e.close()

        # # probably don't need to open pickled genome here
        # g = open(filename, 'r')
        # newGenome = pickle.load(g)
        # print('Again\n', newGenome)
