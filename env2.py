from __future__ import print_function
import random
import copy
import const as c
import math
import pyrosim


class ENVIRONMENT:

    def __init__(self, ID):
        self.ID = ID
        self.obstacles = {}
        self.l = 2 * c.L
        self.w = 2 * c.L
        self.h = 3 * c.L
        self.PrintVals()
        self.wall_height = c.obstH
        self.long_wall_len = c.lightDist / 2.0

    def PlaceObstacle(self, pos, sim):
        self.obst_locs.append(pos)
        return sim.send_box(x=pos[0], y=pos[1], z=0.5 * c.obstH, length=c.obstL, width=c.obstW, height=c.obstH,
                            r=1, g=0, b=0, collision_group='obstacles')

    def PlaceAnotherCourse(self, sim):
        self.PlaceObstacle()

    def PlaceLightSourceAngle(self, sim):
        xpos = c.lightDist * math.cos(self.angle)
        ypos = c.lightDist * math.sin(self.angle)
        self.lightSourcePos = (xpos, ypos)
        # print('xy', xpos, ypos)
        # print('angle', self.angle)

        self.lightsource = sim.send_box(x=xpos, y=ypos, z=0.5 * c.lightSrcH, length=c.obstL, width=c.obstW,
                                        height=c.lightSrcH, r=0.9, g=1, b=0)

        light_top = sim.send_box(x=xpos, y=ypos, z=c.obstW + c.lightSrcH, length=2 * c.obstL, width=2 * c.obstW,
                                 height=2 * c.obstW, r=0.9, g=1, b=0)

        light_base = sim.send_box(x=xpos, y=ypos, z=c.obstW, length=2 * c.obstL, width=2 * c.obstW,
                                  height=2 * c.obstW, r=0.9, g=1, b=0)

        sim.send_fixed_joint(first_body_id=self.lightsource, second_body_id=light_top)
        sim.send_fixed_joint(first_body_id=self.lightsource, second_body_id=light_base)

        sim.send_light_source(body_id=self.lightsource)

        self.obst_pos_sensors = {}
        for i in range(0, len(self.obstacles)):
            self.obst_pos_sensors[i] = sim.send_position_sensor(body_id=self.obstacles[i])

    def SendObstPosSensors(self, sim):
        self.obst_pos_sensors = {}
        for i in range(0, len(self.obstacles)):
            self.obst_pos_sensors[i] = sim.send_position_sensor(body_id=self.obstacles[i])

    def PlaceObstacleCourse6(self, sim, switch):
        z = c.wallH / 2
        self.walls = {}

        self.walls[0] = sim.send_box(x=c.wallDist, y=0, z=z, length=c.wallDist * 2, width=c.wallW, height=c.wallH,
                           r=1, g=0, b=0, collision_group='obstacles')
        self.walls[1] = sim.send_box(x=0, y=-(c.wallDist - c.wallW/2), z=z, length=c.wallW, width=c.wallDist * 2 - c.wallW, height=c.wallH,
                           r=1, g=0, b=0, collision_group='obstacles')
        self.walls[2] = sim.send_box(x=-c.wallDist, y=0, z=z, length=c.wallDist * 2, width=c.wallW, height=c.wallH,
                           r=1, g=0, b=0, collision_group='obstacles')
        if switch == 0:
            self.walls[3] = sim.send_box(x=c.wallCut / 2, y=c.wallDist - c.wallW/2, z=z, length=c.wallW,
                                     width=c.wallDist * 2 - c.wallW - c.wallCut, height=c.wallH,
                                     r=1, g=0, b=0, collision_group='obstacles')
        elif switch == 1:
            self.walls[3] = sim.send_box(x=-c.wallCut / 2, y=c.wallDist - c.wallW / 2, z=z, length=c.wallW,
                                         width=c.wallDist * 2 - c.wallW - c.wallCut, height=c.wallH,
                                         r=1, g=0, b=0, collision_group='obstacles')

        for w in self.walls:
            sim.send_fixed_joint(first_body_id=self.walls[w], second_body_id=pyrosim.Simulator.WORLD)

    # should be called something else. creates box environment
    def PlaceLightSourceToFront(self, sim, version):
        self.angle = math.pi / 2
        self.PlaceLightSourceAngle(sim)
        # self.PlaceRandomObstacles(sim)
        self.PlaceObstacleCourse6(sim, version)


    def PrintVals(self):
        print()
        # print('\nID:', self.ID, '  l:', self.l, '  w:', self.w, '  h:', self.h, '  x:', self.x, '  y:', self.y, '  z:', self.z)

    def SendTo(self, sim):
        if (self.ID == 1):
            self.angle = math.pi / 4
            self.PlaceLightSourceAngle(sim)
        elif (self.ID == 2):
            self.angle = math.pi / 2
            self.PlaceLightSourceAngle(sim)
        elif (self.ID == 3):
            self.angle = math.pi * 3 / 4
            self.PlaceLightSourceAngle(sim)
        elif (self.ID == 6):
            self.PlaceLightSourceToFront(sim, 0)
        elif (self.ID == 7):
            self.PlaceLightSourceToFront(sim, 1)


    def SendID(self, sim, id):
        marker_radius = c.R / 2
        marker_length = c.L / 4
        if id <= 5:
            for i in range(0, id):
                sim.send_cylinder(x=-.1 + i * 2 * marker_radius, y=-4 * c.L, z=marker_radius / 2, length=marker_length,
                                  radius=marker_radius, r1=0, r2=1, r3=0)
        if id > 5:
            for i in range(0, 5):
                sim.send_cylinder(x=-.1 + i * 2 * marker_radius, y=-4 * c.L, z=marker_radius / 2, length=marker_length,
                                  radius=marker_radius, r1=0, r2=1, r3=0)
            for i in range(5, id):
                sim.send_cylinder(x=-.1 + (i - 5) * 2 * marker_radius, y=-4 * c.L - 1.6 * marker_length,
                                  z=marker_radius / 2, length=marker_length,
                                  radius=marker_radius, r1=0, r2=1, r3=0)

    # def SendTo(self, sim):
    #
    #     if c.obstacles == True:
    #         self.obstacles = {}
    #
    #         tupleDict = {}
    #         for i in range(0, c.numObstacles):
    #             x = random.randint(-15, 15)
    #             y = random.randint(5, 20)
    #             tupleDict[i] = (x, y)
    #         # print(tupleDict)
    #
    #         for i in range(0, c.numObstacles):
    #             self.obstacles[i] = sim.send_box(x=tupleDict[i][0]/10.0, y=tupleDict[i][1]/10.0, z=self.z, length=self.l, width=self.w, height=self.h, r=1, g=0, b=0)
    #
    #     self.lightsource = sim.send_box(x=self.x, y=self.y, z=self.z, length=self.l, width=self.w, height=self.h)
    #     sim.send_light_source(body_id=self.lightsource)
