from __future__ import print_function
import pyrosim
import const as c
import random
import numpy as np
import math

class ROBOT:
    # def __init__(self, sim, wts):
    #     self.send_objects(sim)
    #     self.send_joints(sim)
    #     self.send_sensors(sim)
    #     self.send_neurons(sim)
    #     self.send_hidden_neurons(sim)
    #     self.send_synapses(sim, wts)
    #
    #     del self.O
    #     del self.J
    #     del self.S
    #     del self.SN
    #     del self.MN
    #     del self.HL

    def __init__(self, sim, wts):

        wts[0] = c.round_matrix(wts[0])
        wts[1] = c.round_matrix(wts[1])

        # print('wts[0][0] in robot init', wts[0][0])

        self.jointHeight = (c.L) * math.cos(math.pi / 4)
        self.boxZ = 2 * self.jointHeight + c.R
        self.boxHeight = 2 * c.R
        self.boxLength = 3.5 * c.L
        self.boxWidth = 1.6 * c.L

        self.boxPos = c.R

        self.bZ = 1.3 * self.boxZ
        self.bbY = self.boxPos - 0.275*self.boxLength
        self.bfY = self.boxPos + 0.275*self.boxLength

        self.rodLength = c.R
        self.rayRodZ = self.boxZ + self.boxHeight / 2 + self.rodLength * 3 / 4
        self.rodY = self.boxLength/4

        self.send_objects(sim)
        self.send_joints(sim)
        self.send_sensors(sim)
        self.send_neurons(sim)
        self.send_hidden_neurons(sim)
        self.send_synapses(sim, wts)

        del self.O
        del self.J
        del self.S
        del self.SN
        del self.MN
        del self.H

    def send_objects(self, sim):

        self.bf = sim.send_box(x=0, y=self.boxPos + 0.275*self.boxLength, z=self.boxZ, length=0.45*self.boxLength, width=self.boxWidth,
                               height=self.boxHeight, r=0.5, g=0.5, b=0.5, collision_group='robot')

        self.bb = sim.send_box(x=0, y=self.boxPos - 0.275*self.boxLength, z=self.boxZ, length=0.45*self.boxLength, width=self.boxWidth,
                               height=self.boxHeight, r=0.5, g=0.5, b=0.5, collision_group='robot')

        self.spinRod = sim.send_cylinder(x=0, y=self.rodY, z=self.boxZ + self.boxHeight / 2 + self.rodLength / 2, length=self.rodLength,
                                    radius=self.rodLength/4, capped=False)

        self.rayRod = sim.send_cylinder(x=0, y=self.rodY + self.rodLength / 2, z=self.boxZ + self.boxHeight / 2 + self.rodLength * 3 / 4,
                                   length=1.5*self.rodLength, radius=self.rodLength / 4, capped=False, r1=0, r2=1, r3=0)

        # self.O0 = sim.send_box(x=0, y=self.boxPos, z=self.boxZ, length=self.boxLength, width=self.boxWidth,
        #                        height=self.boxHeight, r=0.5, g=0.5, b=0.5)

        self.O1 = sim.send_cylinder(x=c.L, y=1.5 * c.L, z=1.5 * self.jointHeight + c.R, length=c.L, radius=c.R,
                                    r1=0, r2=1, r3=1, r=1, g=0, b=0.2)

        self.O2 = sim.send_cylinder(x=-c.L, y=1.5 * c.L, z=1.5 * self.jointHeight + c.R, length=c.L, radius=c.R,
                                    r1=0, r2=1, r3=1, r=0, g=1, b=0.2)

        self.O3 = sim.send_cylinder(x=c.L, y=-1.5 * c.L, z=1.5 * self.jointHeight + c.R, length=c.L, radius=c.R,
                                    r1=0, r2=1, r3=1, r=0, g=0, b=1)

        self.O4 = sim.send_cylinder(x=-c.L, y=-1.5 * c.L, z=1.5 * self.jointHeight + c.R, length=c.L, radius=c.R,
                                    r1=0, r2=1, r3=1, r=1, g=0, b=1)

        self.O5 = sim.send_cylinder(x=c.L, y=1.5 * c.L, z=0.5 * self.jointHeight + c.R, length=c.L, radius=c.R,
                                    r1=0, r2=-1, r3=1, r=1, g=0, b=0, collision_group='robot')

        self.O6 = sim.send_cylinder(x=-c.L, y=1.5 * c.L, z=0.5 * self.jointHeight + c.R, length=c.L, radius=c.R,
                                    r1=0, r2=-1, r3=1, r=0, g=1, b=0, collision_group='robot')

        self.O7 = sim.send_cylinder(x=c.L, y=-1.5 * c.L, z=0.5 * self.jointHeight + c.R, length=c.L, radius=c.R,
                                    r1=0, r2=-1, r3=1, r=0, g=0, b=1, collision_group='robot')

        self.O8 = sim.send_cylinder(x=-c.L, y=-1.5 * c.L, z=0.5 * self.jointHeight + c.R, length=c.L, radius=c.R,
                                    r1=0, r2=-1, r3=1, r=1, g=0, b=1, collision_group='robot')



        self.O = {}
        self.O[0] = self.bf
        self.O[1] = self.O1
        self.O[2] = self.O2
        self.O[3] = self.O3
        self.O[4] = self.O4
        self.O[5] = self.O5
        self.O[6] = self.O6
        self.O[7] = self.O7
        self.O[7] = self.O7
        self.O[8] = self.O8

    def send_joints(self, sim):
        xJ = c.L
        yUpJ = 1.5 * c.L
        zUpJ = 2 * self.jointHeight + c.R
        yLoJ = 1.5 * c.L - 0.5 * self.jointHeight
        zLoJ = self.jointHeight + c.R
        yLoJB = -1.5 * c.L - 0.5 * self.jointHeight

        # box to red upper leg
        self.J0 = sim.send_hinge_joint(x=xJ, y=yUpJ, z=zUpJ, n1=-1, n2=0, n3=0,
                                       first_body_id=self.bf, second_body_id=self.O1, lo=-c.upJointHalfRange,
                                       hi=c.upJointHalfRange)

        self.J1 = sim.send_hinge_joint(x=xJ, y=yLoJ, z=zLoJ, n1=-1, n2=0, n3=0,
                                       first_body_id=self.O1, second_body_id=self.O5, lo=-c.lowJointHalfRange,
                                       hi=c.lowJointHalfRange)

        self.J2 = sim.send_hinge_joint(x=-xJ, y=yUpJ, z=zUpJ, n1=-1, n2=0, n3=0,
                                       first_body_id=self.bf, second_body_id=self.O2, lo=-c.upJointHalfRange,
                                       hi=c.upJointHalfRange)

        self.J3 = sim.send_hinge_joint(x=-xJ, y=yLoJ, z=zLoJ, n1=-1, n2=0, n3=0,
                                       first_body_id=self.O2, second_body_id=self.O6, lo=-c.lowJointHalfRange,
                                       hi=c.lowJointHalfRange)

        self.J4 = sim.send_hinge_joint(x=xJ, y=-yUpJ, z=zUpJ, n1=-1, n2=0, n3=0,
                                       first_body_id=self.bb, second_body_id=self.O3, lo=-c.upJointHalfRange,
                                       hi=c.upJointHalfRange)

        self.J5 = sim.send_hinge_joint(x=xJ, y=yLoJB, z=zLoJ, n1=-1, n2=0, n3=0,
                                       first_body_id=self.O3, second_body_id=self.O7, lo=-c.lowJointHalfRange,
                                       hi=c.lowJointHalfRange)

        self.J6 = sim.send_hinge_joint(x=-xJ, y=-yUpJ, z=zUpJ, n1=-1, n2=0, n3=0,
                                       first_body_id=self.bb, second_body_id=self.O4, lo=-c.upJointHalfRange,
                                       hi=c.upJointHalfRange)

        self.J7 = sim.send_hinge_joint(x=-xJ, y=yLoJB, z=zLoJ, n1=-1, n2=0, n3=0,
                                       first_body_id=self.O4, second_body_id=self.O8, lo=-c.lowJointHalfRange,
                                       hi=c.lowJointHalfRange)

        self.spinRodJoint = sim.send_hinge_joint(x=0, y=self.rodY, z=self.boxZ, lo=0, hi=2.0, n1=0, n2=0, n3=1, first_body_id=self.O[0],
                                       second_body_id=self.spinRod, position_control=False, speed=c.spinSpeed)

        self.bodyJoint = sim.send_hinge_joint(x=0, y=self.boxPos, lo=-c.bodyAng, hi=c.bodyAng, n1=0, n2=0, n3=1,
                                              first_body_id=self.bb, second_body_id=self.bf)

        # these two neurons are here because they don't need to be added the neural network.
        # the motor neuron outputs a constant value
        mn1 = sim.send_motor_neuron(joint_id=self.spinRodJoint, start_value=0)
        inpn = sim.send_user_input_neuron(1.0)
        sim.send_synapse(source_neuron_id=inpn, target_neuron_id=mn1, weight=1.0)

        # not in NN
        self.JfixRod = sim.send_hinge_joint(x=0, y=0, z=self.boxZ, lo=0, hi=0, n1=0, n2=0, n3=1,
                                            first_body_id=self.spinRod, second_body_id=self.rayRod)

        self.J = {}
        self.J[0] = self.J0
        self.J[1] = self.J1
        self.J[2] = self.J2
        self.J[3] = self.J3
        self.J[4] = self.J4
        self.J[5] = self.J5
        self.J[6] = self.J6
        self.J[7] = self.J7
        # self.J[8] = self.J8
        self.J[8] = self.bodyJoint

    def send_sensors(self, sim):
        self.T0 = sim.send_touch_sensor(body_id=self.O5)
        self.T1 = sim.send_touch_sensor(body_id=self.O6)
        self.T2 = sim.send_touch_sensor(body_id=self.O7)
        self.T3 = sim.send_touch_sensor(body_id=self.O8)
        self.P4 = sim.send_position_sensor(body_id=self.bf)
        self.P4b = sim.send_position_sensor(body_id=self.bb)
        self.L4 = sim.send_light_sensor(body_id=self.bf)
        self.R5 = sim.send_ray_sensor(body_id=self.rayRod, x=0, y=self.rodY + 1.01*self.rodLength, z=self.rayRodZ,
                                      max_distance=c.lightDist/2.0, r1=0, r2=1, r3=0)

        self.touchSensorBoxData = sim.send_touch_sensor(body_id=self.bf)
        self.propSensUp0 = sim.send_proprioceptive_sensor(joint_id=self.J[0])
        self.propSensUp2 = sim.send_proprioceptive_sensor(joint_id=self.J[2])
        self.propSensUp4 = sim.send_proprioceptive_sensor(joint_id=self.J[4])
        self.propSensUp6 = sim.send_proprioceptive_sensor(joint_id=self.J[6])

        self.propSensLow1 = sim.send_proprioceptive_sensor(joint_id=self.J[1])
        self.propSensLow3 = sim.send_proprioceptive_sensor(joint_id=self.J[3])
        self.propSensLow5 = sim.send_proprioceptive_sensor(joint_id=self.J[5])
        self.propSensLow7 = sim.send_proprioceptive_sensor(joint_id=self.J[7])

        self.vestibularSensorBox = sim.send_vestibular_sensor(body_id=self.bf)

        self.propSensRod = sim.send_proprioceptive_sensor(joint_id=self.spinRodJoint)
        self.propSensBody = sim.send_proprioceptive_sensor(joint_id=self.J[8])

        self.S = {}
        self.S[0] = self.T0
        self.S[1] = self.T1
        self.S[2] = self.T2
        self.S[3] = self.T3
        self.S[4] = self.L4
        self.S[5] = self.propSensUp0
        self.S[6] = self.propSensUp2
        self.S[7] = self.propSensUp4
        self.S[8] = self.propSensUp6
        self.S[9] = self.propSensLow1
        self.S[10] = self.propSensLow3
        self.S[11] = self.propSensLow5
        self.S[12] = self.propSensLow7
        self.S[13] = self.vestibularSensorBox
        self.S[14] = self.propSensRod
        self.S[15] = self.propSensBody
        self.S[16] = self.P4
        # self.S[17] = self.R5
        # self.S[17] = self.P4b

    def send_neurons(self, sim):
        self.SN = {}
        for s in self.S:
            # print('s', s)
            self.SN[s] = sim.send_sensor_neuron(sensor_id=self.S[s])
        # self.SN[len(self.SN)] = sim.send_function_neuron()
        # print('len SN', len(self.SN))

        self.MN = {}
        for j in self.J:
            self.MN[j] = sim.send_motor_neuron(joint_id=self.J[j], tau=0.3)

    def send_hidden_neurons(self, sim):
        self.H = {}
        for h in range(0, c.numHidden):
            self.H[h] = sim.send_hidden_neuron(tau=1.0, alpha=1.0)

    def send_synapses(self, sim, wts):
        for j in self.SN:
            for i in self.H:
                sim.send_synapse(source_neuron_id=self.SN[j], target_neuron_id=self.H[i], weight=wts[0][j, i])
        for j in self.H:
            for i in self.MN:
                sim.send_synapse(source_neuron_id=self.H[j], target_neuron_id=self.MN[i], weight=wts[1][j, i])
