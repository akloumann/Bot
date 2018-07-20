from __future__ import print_function
from envs import ENVIRONMENTS
from pop import POPULATION
import const as c
import time
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import pickle


### new
# parents0 = POPULATION(100)
# parents0.Initialize()
# parents0.Evaluate(envs, pp=False, pb=True)
# parents0.Print()
# print('********************* done')
### new end

fit_labels = c.fit_labels
filename = 'genome' + str(fit_labels[-1])

pathLoad = c.pathLoad
filename = pathLoad + filename
g = open(filename, 'r')
genome = pickle.load(g)
g.close()

# first = np.random.random_sample((c.numInputs, c.numHidden)) * 2 - 1
# second = np.random.random_sample((c.numHidden, c.numOutputs)) * 2 - 1
# genome = [first, second]

envs = ENVIRONMENTS()
parents = POPULATION(1, -1)

parents.InitializeUniformPop(genome)
parents.Evaluate(envs, pp=False, pb=True)
parents.Print()

# # i = 0
# # t_end = time.time() + 60 * c.minutes
# for i in range(0, 1):
# # while time.time() < t_end:
#     # the POPULATION constructor creates an empty dictionary and stores the variable popSize
#     children = POPULATION(c.popSizeGA1, i)
#     children.Print()
#     children.FillFrom(parents)
#
#     # print('seconds remaining', t_end - time.time())
#
#     print('\n0', end=' ')
#     parents.Print()
#     children.Evaluate(envs, pp=False, pb=True)
#     print(i, end=' ')
#     children.Print(i)
#     children.PrintDists(i)
#     parents = children
#     #
#     # if i % c.pickleFreq == 0:
#     #     parents.PicklingGA1(parents)
#     # i += 1
#
# # parents.PicklingGA1(parents)

for e in c.envsToRun:
        print('id', parents.p[0].ID, '   env', e)
        print()
        parents.p[0].Start_Evaluation(envs.envs[e], pp=True, pb=False)

# parents.p[0].Start_Evaluation(envs.envs[3], pp=True, pb=False)
# parents.p[0].Start_Evaluation(envs.envs[0], pp=True, pb=False)
# parents.p[0].Start_Evaluation(envs.envs[1], pp=True, pb=False)
# parents.p[0].Start_Evaluation(envs.envs[2], pp=True, pb=False)
# parents.p[1].Start_Evaluation(envs.envs[0], pp=True, pb=False)
# parents.p[1].Start_Evaluation(envs.envs[1], pp=True, pb=False)
# parents.p[1].Start_Evaluation(envs.envs[2], pp=True, pb=False)
# parents.p[1].Start_Evaluation(envs.envs[3], pp=True, pb=False)
#
# parents.p[3].Start_Evaluation(envs.envs[0], pp=True, pb=False)
# parents.p[4].Start_Evaluation(envs.envs[0], pp=True, pb=False)
# parents.p[5].Start_Evaluation(envs.envs[0], pp=True, pb=False)

# print('joint 0 red avg angle    ', parents.p[0].avgAngleJ0)
# print('joint 2 green avg angle  ', parents.p[2].avgAngleJ2)
# print('joint 4 blue angle       ', parents.p[4].avgAngleJ4)
# print('joint 6 purple angle     ', parents.p[6].avgAngleJ6)

###########################################
# UNCOMMENT!
# plt.figure(1)
# plt.subplot(411)
# plt.plot(parents.p[0].distOrg)
# plt.ylabel('distance')
# plt.subplot(412)
# plt.plot(parents.p[0].speed)
# plt.ylabel('speed')
# plt.subplot(413)
# plt.plot(parents.p[0].distTarget)
# plt.ylabel('dist target')
# plt.subplot(414)
# plt.plot(parents.p[0].vestibularSensorDataBox)
# plt.ylabel('vest sens body')
#
# plt.figure(2)
# plt.subplot(411)
# plt.plot(parents.p[0].propData0)
# plt.ylabel('joint 0 red')
# plt.subplot(412)
# plt.plot(parents.p[0].propData2)
# plt.ylabel('joint 2 green')
# plt.subplot(413)
# plt.plot(parents.p[0].propData4)
# plt.ylabel('joint 4 blue')
# plt.subplot(414)
# plt.plot(parents.p[0].propData6)
# plt.ylabel('joint 6 purple')
#
# plt.show()
###########################################

#########################################
# print(parents.p[0].genome)
# genome = parents.p[0].genome
# print('fitness to pickle:', parents.p[0].fitness)
#
# filename = 'bot' + str(parents.p[0].fitness)
# fullPath = '/home/iskander/PycharmProjects/EvoBotProject/genomes/'
# filename = fullPath + filename
# e = open(filename, 'w')
# pickle.dump(genome, e)
# e.close()
#
# g = open(filename, 'r')
# newGenome = pickle.load(g)
# print('Again\n', newGenome)

# DILL.pickleGenome(parents)
#
# class DILL:
#     @staticmethod
#     def pickleGenome(parents):
#         genome = parents.p[0].genome
#         print('fitness to pickle:', parents.p[0].fitness)
#         e = open('bot.p', 'w')
#         pickle.dump(genome, e)
#         e.close()
#
#         g = open('bot.p', 'r')
#         newGenome = pickle.load(g)
#     print('Again\n', newGenome)
########################################

# f = open('robot.p', 'w')
# pickle.dump(parents, f)
# f.close

# f = plt.figure()
# panel = f.add_subplot(131)
# # panel.set_ylim(-2, 0.5)
# plt.plot(y)
# panel = f.add_subplot(132)
# plt.plot(z)
# plt.show()
