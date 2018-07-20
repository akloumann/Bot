from __future__ import print_function
from robot2 import ROBOT
import random
import pyrosim
import matplotlib.pyplot as plt
import math
import numpy as np
import const as c
import pickle


# need to change init(), Mutate(), send_synapses() in robot.py and init() in robot.py.

class INDIVIDUAL:

    def __init__(self, i, genome, age):
        self.genome = genome
        self.fitness = 0
        self.ID = i
        self.age = age

    def Start_Evaluation(self, env, pp, pb):
        self.sim = pyrosim.Simulator(play_paused=pp, play_blind=pb, eval_time=c.evalTime)
        # self.sim.make_movie(movie_name= '/home/iskander/PycharmProjects/EvoBotProject/genomes/a.mpg')

        self.robot = ROBOT(self.sim, self.genome)

        env.SendTo(self.sim)
        env.SendID(self.sim, self.ID)

        # print('num bodies', self.sim.get_num_bodies())

        self.sim.assign_collision('obstacles', 'robot')
        self.sim.assign_collision('obstacles', 'supports')
        self.sim.start()

    # called in Evaluate in POPULATION
    def Compute_Fitness(self, env):
        self.sim.wait_to_finish()

        # this is set to false at the beginning of each individual eval so that if any
        # obst knocked during sim this individual loses points
        # env.knocked_check = False

        x = self.sim.get_sensor_data(sensor_id=self.robot.P4, svi=0)
        y = self.sim.get_sensor_data(sensor_id=self.robot.P4, svi=1)
        z = self.sim.get_sensor_data(sensor_id=self.robot.P4, svi=2)

        self.lightSensorData = self.sim.get_sensor_data(sensor_id=self.robot.L4)
        self.vestibularSensorDataBox = self.sim.get_sensor_data(sensor_id=self.robot.vestibularSensorBox)

        # ################################### joint angles ###################################
        self.propData0 = self.sim.get_sensor_data(sensor_id=self.robot.propSensUp0)
        self.propData2 = self.sim.get_sensor_data(sensor_id=self.robot.propSensUp2)
        self.propData4 = self.sim.get_sensor_data(sensor_id=self.robot.propSensUp4)
        self.propData6 = self.sim.get_sensor_data(sensor_id=self.robot.propSensUp6)
        self.propData1 = self.sim.get_sensor_data(sensor_id=self.robot.propSensLow1)
        self.propData3 = self.sim.get_sensor_data(sensor_id=self.robot.propSensLow3)
        self.propData5 = self.sim.get_sensor_data(sensor_id=self.robot.propSensLow5)
        self.propData7 = self.sim.get_sensor_data(sensor_id=self.robot.propSensLow7)

        self.avgAngJ0 = abs(np.average(self.propData0))
        self.avgAngJ2 = abs(np.average(self.propData2))
        self.avgAngJ4 = abs(np.average(self.propData4))
        self.avgAngJ6 = abs(np.average(self.propData6))
        self.avgAngJ1 = abs(np.average(self.propData1))
        self.avgAngJ3 = abs(np.average(self.propData3))
        self.avgAngJ5 = abs(np.average(self.propData5))
        self.avgAngJ7 = abs(np.average(self.propData7))

        # adding this avg vestibular sensor data to fitness penalty
        # print('avg v sens:', np.average(self.vestibularSensorDataBox))
        jointAngMult = 1 / (1 + self.avgAngJ0 + self.avgAngJ1 + self.avgAngJ2 + self.avgAngJ3 + \
                            self.avgAngJ4 + self.avgAngJ5 + self.avgAngJ6 + self.avgAngJ7)
        # ################################### joint angles ###################################

        ################################### point to src ###################################
        xb = self.sim.get_sensor_data(sensor_id=self.robot.P4b, svi=0)
        yb = self.sim.get_sensor_data(sensor_id=self.robot.P4b, svi=1)

        botVector = []
        botLightSrcVector = []
        cosThetaBotLight = []
        for i in range(0, c.evalTime):
            botVector.append((x[i] - xb[i], y[i] - yb[i]))
            botLightSrcVector.append((env.lightSourcePos[0] - xb[i], env.lightSourcePos[1] - yb[i]))

        for i in range(0, c.evalTime):
            botLightSrcAbs = math.sqrt(botLightSrcVector[i][0] ** 2 + botLightSrcVector[i][1] ** 2)
            botVectorAbs = math.sqrt(botVector[i][0] ** 2 + botVector[i][1] ** 2)
            # print('light vector length', lightVectorAbs)
            # print('bot vector length', botVectorAbs)
            dotProd = botVector[i][0] * botLightSrcVector[i][0] + botVector[i][1] * \
                      botLightSrcVector[i][1]
            cosThetaBotLight.append(dotProd / (botLightSrcAbs * botVectorAbs))

        avgCosThetaBotLight = abs(np.average(cosThetaBotLight))

        ################################### point to src ###################################


        # ################################### point to src ###################################
        # xb = self.sim.get_sensor_data(sensor_id=self.robot.P4b, svi=0)
        # yb = self.sim.get_sensor_data(sensor_id=self.robot.P4b, svi=1)
        #
        # self.botVector = []
        # self.botLightSrcVector = []
        # self.cosBotLightVect = []
        # for i in range(0, c.evalTime):
        #     self.botVector.append((x[i] - xb[i], y[i] - yb[i]))
        #     self.botLightSrcVector.append((env.lightSourcePos[0] - xb[i], env.lightSourcePos[1] - yb[i]))
        #
        # for i in range(0, c.evalTime):
        #     lightVectorAbs = math.sqrt(self.botLightSrcVector[i][0] ** 2 + self.botLightSrcVector[i][1] ** 2)
        #     botVectorAbs = math.sqrt(self.botVector[i][0] ** 2 + self.botVector[i][1] ** 2)
        #     # print('light vector length', lightVectorAbs)
        #     # print('bot vector length', botVectorAbs)
        #     dotProd = self.botVector[i][0] * self.botLightSrcVector[i][0] + self.botVector[i][1] * \
        #               self.botLightSrcVector[i][1]
        #     self.cosBotLightVect.append(dotProd / (lightVectorAbs * botVectorAbs))
        # # print('cos bot light vect', self.cosBotLightVect)
        # # print('avg cos light vect', np.average(self.cosBotLightVect))
        # # print('cosBotLight angle 0 ', math.acos(self.cosBotLightVect[0])*180/math.pi)
        # ################################### point to src ###################################


        # ########################## all related to speed ##########################
        # # creates array with speed moving from origin at each time step
        # self.distOrg = (x ** 2 + y ** 2) ** 0.5
        # self.speed = np.zeros(c.evalTime)
        # for i in range(1, c.evalTime):
        #     self.speed[i] = self.distOrg[i] - self.distOrg[i - 1]
        #

        # creates array with speed moving toward target at each time step
        # speedTarget = np.zeros(c.evalTime)
        # for i in range(1, c.evalTime):
        #     speedTarget[i] = self.distTarget[i - 1] - self.distTarget[i]
        # avgSpeedTarget = np.average(speedTarget)
        # stdSpeedTarget = np.std(speedTarget)
        # speedFitnessFactor = 5 * avgSpeedTarget / (1 + stdSpeedTarget)

        # # single values from data
        # self.avgSpeed = np.average(self.speed)
        # self.avgSpeedTarget = np.average(self.speedTarget)
        #
        # s = slice(c.evalTime * 3 / 4, c.evalTime, 1)
        # self.speedLastQ = self.speed[s]
        #
        # self.avgSpeedLastQ = np.average(self.speedLastQ)
        # ########################## all related to speed ##########################

        # ############################## obstacle data ###############################
        # self.obstacles_data_z = {}
        # for i in range(0, len(env.obstacles)):
        #     self.obstacles_data_z[i] = self.sim.get_sensor_data(sensor_id=env.obst_pos_sensors[i], svi=2)
        # # print(min(self.obstacles_data_z[0]))
        #
        # self.knocked = 0
        # for i in range(0, len(self.obstacles_data_z)):
        #     if min(self.obstacles_data_z[i]) != max(self.obstacles_data_z[i]):
        #         self.knocked += 1
        #         env.knocked_check = True
        # # print('knocked', self.knocked)
        #
        # fitnessToAdd = ((1/(1 + self.distTarget[-1]))**2.5) * self.avgSpeedTarget * \
        #                jointAngMult * np.average(self.cosBotLightVect)/(1 + self.knocked) * (10 ** 8)
        #
        # fitnessToAdd = ((1/(1 + self.distTarget[-1]))**2.5) * self.avgSpeedTarget * \
        #                jointAngMult * np.average(self.cosBotLightVect) * (10 ** 7)
        #
        # fitnessToAdd = ((1/(1 + self.distTarget[-1]))**2.5) * self.avgSpeedTarget * \
        #                jointAngMult * np.average(self.cosBotLightVect) * (10 ** 7)
        # ############################## obstacle data ###############################

        ############################ distance to target ####################################
        self.distTarget = self.lightSensorData ** (-0.5)
        ############################ distance to target ####################################

        fitnessToAdd = 1000 * jointAngMult * (self.distTarget[-1] ** -2) * avgCosThetaBotLight # * speedFitnessFactor
        # print("avg costheta", avgCosThetaBotLight, "  jointangmult", jointAngMult, "  disttarg", self.distTarget[-1]**-2)
        if np.average(self.vestibularSensorDataBox) > 0.3 or self.vestibularSensorDataBox.max() > 0.4:
            fitnessToAdd *= 0.01
            # fitnessToAdd /= 7

        self.fitness += fitnessToAdd
        self.avgDist += self.distTarget[-1]
        self.envsProg.append(self.fitness)

        del self.sim

    def Mutate(self):
        # rand = random.randint(0, c.mutateRandFreq - 1)
        rand = random.randint(0, 4)

        if rand != 0:
            num_mutations = 1
        else:
            num_mutations = 2

        for i in range(0, num_mutations):
            layer = random.randint(0, 1)
            if layer == 0:
                row = random.randint(0, c.numInputs - 1)
                col = random.randint(0, c.numHidden - 1)
            else:
                row = random.randint(0, c.numHidden - 1)
                col = random.randint(0, c.numOutputs - 1)

            geneToMutate = self.genome[layer][row][col]
            self.genome[layer][row, col] = random.gauss(geneToMutate, math.fabs(geneToMutate))
            if self.genome[layer][row, col] > 1:
                self.genome[layer][row, col] = 1
            elif self.genome[layer][row, col] < -1:
                self.genome[layer][row, col] = -1

    def Print(self):
        # print('[ind:', self.ID, '| age:', self.age, '| fit:', round(self.fitness, 3), '] ', end=' ')
        print('  [ind:', self.ID, '| age:', self.age, '| fit:', round(self.fitness, 3), end='')
        if c.alg == 'afpo2':
            print('| inv fit:', round(self.fitness ** -1, 3), ']')
        else:
            print(']')

    def PrintDist(self):
        print('[dist', self.ID, '', round(self.avgDist, 3), '] ', end=' ')

    def SetID(self, id):
        self.ID = id
