from __future__ import print_function
from envs import ENVIRONMENTS
from pop import POPULATION
import const as c
import time
import pyrosim
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import pickle
import os


class GENETIC_ALGORITHM:
    def __init__(self, fit_ids):
        fff = 1
        self.fit_ids = fit_ids

        # Alphanumeric string
        # self.id_strings = []
        # ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

        # ############### random values test pareto ###############
        # default x, y, popsize values for af_pareto()
        self.ys = np.random.randint(4, 15, 25)
        self.xs = np.random.randint(0, 25, 25)
        self.af_pareto_math(self.xs, self.ys)
        print('\n############# test graph done #############\n')

    def main(self):
        # t_end = time.time() + 60 * c.minutes
        # ############### useful if using another alg ##############
        # envs = ENVIRONMENTS()
        # print('envs to run:', c.envsToRun, '   initial popsize:', c.num_rand_phc)
        # parents = POPULATION(c.num_rand_phc + len(self.fit_ids))
        # parents.InitializeRandomPop()
        # parents.Evaluate(envs, pp=False, pb=True)
        # parents.Print()
        # ############### useful if using another alg ##############

        self.afpo()

    def ShowEvaluatePop(self, parents, envs, pp=True, pb=False):
        for j in range(0, len(parents.p)):
            raw_input('press enter to continue...')
            for e in c.envsToRun:
                # for j in range(0, 1):
                parents.p[j].Start_Evaluation(envs.envs[e], pp, pb)

    def afpo(self):
        envs = ENVIRONMENTS()
        print('envs to run:', c.envsToRun, '   pop init:', c.num_rand_phc + len(self.fit_ids))
        parents = POPULATION(c.num_rand_phc + len(self.fit_ids))
        parents.InitializeRandomPop()

        # parents = self.phc_ga(parents, envs, c.afpo2_phc_gens)
        # print('\n############# phc done #############\n')

        parents.Evaluate(envs, False, True)

        for i in range(0, len(parents.p)):
            parents.p[i].age += i
        # for i in range(0, len(parents.p)):
        #     print('p[' + str(i) + '].age =', parents.p[i].age)
        print("Initial population age adjusted")
        parents.Print()

        finalpop = self.af_pareto_ga(parents, envs)

        frontinds = self.af_pareto_math(finalpop.GetAges(), finalpop.GetFits())
        finalpopfront = POPULATION(len(frontinds))
        for i in range(0, len(frontinds)):
            finalpopfront.p[i] = finalpop.p[frontinds[i]]
        finalpopfront.Pickling618()
        self.ShowEvaluatePop(finalpopfront, envs, pp=True, pb=False)

    def af_pareto_ga(self, parents, envs):

        def inner(parents, envs, i):
            print("\n##########********* af_pareto_spop gen", i, "*********##########")
            parents_temp = self.af_pareto_spop(parents, envs)
            # print("parents type:", type(parents))
            # print("parents.p type:", type(parents.p))
            # print("parents.p[0] type:", type(parents.p[0]))
            print("parents popsize:", len(parents.p))
            parents_temp.IncrementAges()
            return parents_temp

        t_end = time.time() + 60 * c.minutes
        if c.gen_mode == 'time':
            i = 0
            while time.time() < t_end:
                parents = inner(parents, envs, i)
                parents.Print()
                i += 1
        elif c.gen_mode == 'gens':
            for i in range(0, c.gens):
                parents = inner(parents, envs, i)
        return parents

    def af_pareto_spop(self, parents, envs):
        target_popsize = c.target_afpop
        # pcc new population with target popsize
        pcc = POPULATION(target_popsize)
        # pcc.InitializeRandomPop() # not necessary..?

        # add new random individual
        single = POPULATION(1)
        single.InitializeRandomPop()

        # print("parents print?")
        # parents.Print()

        pcc.p[0] = single.p[0]
        for i in range(1, target_popsize):
            # print("i?", i, "    size of pop?", len(parents.p))
            pcc.p[i] = copy.deepcopy(parents.p[i % len(parents.p)])
            if i % 2 == 0:
                pcc.p[i].Mutate()

        pcc.Evaluate(envs, False, True)

        ages = pcc.GetAges()
        fits = pcc.GetFits()
        print('fits', fits)
        print('ages', ages)

        # if fitness is 0 inverse fitness set to 10000
        fits_inv = []
        for i in range(0, len(fits)):
            if fits[i] != 0:
                fits_inv.append(fits[i] ** -1)
            else:
                fits_inv.append(10 ** 4)

        dominant_inds = np.array(self.af_pareto_math(ages, fits_inv))
        print("dominant inds", dominant_inds)
        self.graph_both3(ages, fits_inv, dominant_inds)

        # self.graph_both2(ages, fits_inv, dominant_inds) # dominant inds not right, should be list 1s and 0s
        # self.graph_both(pareto_front_x, pareto_front_y, xx_copy, yy_copy, popsize, ymax)

        new_pop = POPULATION(len(dominant_inds))
        for i in range(0, target_popsize):
            dominant_inds_index = i % len(dominant_inds)
            new_pop.p[i] = copy.deepcopy(pcc.p[dominant_inds_index])
            if i >= len(dominant_inds):
                new_pop.p[i].Mutate()

        del pcc
        # new_pop.Print()
        return new_pop

    # graphs input and returns indices of places in the two arrays that are on pareto front, dominant points
    # takes dictionaries xs and ys
    def af_pareto_math(self, xs, ys):
        print('\n******** enter af_pareto_math ********')

        print('len xs', len(xs), 'len ys', len(ys))
        print('xs', xs)
        print('ys', np.array(ys).round(3))

        temp_list_inds = []
        dominated_inds = []
        for i in range(0, len(xs)):
            temp_list_inds.append(i)
            for j in range(0, len(xs)):
                if ys[i] < ys[j] and xs[i] <= xs[j]:
                    dominated_inds.append(j)
                elif ys[j] < ys[i] and xs[j] <= xs[i]:
                    dominated_inds.append(i)

        dominant_inds = list(set(temp_list_inds).difference(set(dominated_inds)))
        dominant_inds.sort()

        print('\n******** exit af_pareto_math  ********')
        return dominant_inds

    def af_pareto_mathOLD(self, xs, ys):
        print('\n******** enter af_pareto_math ********')

        dominated_list = []
        for i in range(0, len(xs)):
            dominated_list.append(0)

        print('len xs', len(xs), 'len ys', len(ys))
        print('xs', xs)
        print('ys', np.array(ys).round(3))

        for i in range(0, len(xs)):
            for j in range(0, len(xs)):
                if ys[i] < ys[j] and xs[i] <= xs[j]:
                    dominated_list[j] = 1
                elif ys[j] < ys[i] and xs[j] <= xs[i]:
                    dominated_list[i] = 1
                #     break
                # else:
                #     pass
        print('list of dominated indices 0 or 1', dominated_list)

        domnt_inds = []
        for i in range(0, len(dominated_list)):
            if dominated_list[i] == 0:
                domnt_inds.append(i)

        # self.graph_both(pareto_front_x, pareto_front_y, xx_copy, yy_copy, popsize, ymax)
        # self.graph_both2(xs, ys, dominated_list)

        print('\n******** exit af_pareto_math  ********')
        return domnt_inds

    # all arguments should be lists
    def graph_both3(self, xvals, yvals, dominant_inds):
        if len(xvals) != len(yvals):
            print("Error!  len xvals", len(xvals), " len yvals", len(yvals))
            print("xvals", xvals)
            print("yvals", yvals)
            print("dominds", dominant_inds)
            exit(0)

        ymax = max(yvals)
        popsize = len(yvals)

        par_front_x = []
        par_front_y = []
        non_par_front_x = []
        non_par_front_y = []
        for i in range(0, len(xvals)):
            if i in dominant_inds:
                par_front_x.append(xvals[i])
                par_front_y.append(yvals[i])
            else:
                non_par_front_x.append(xvals[i])
                non_par_front_y.append(yvals[i])

        plt.figure(1)
        plt.plot(par_front_x, par_front_y, 'bo')
        plt.plot(non_par_front_x, non_par_front_y, 'ro')
        plt.title("afpo")
        plt.xlim(-1, popsize)
        plt.ylim(-1, ymax)

        my_path = os.path.dirname(__file__)
        # plt.savefig('pfront' + str(time.time()) + '.pdf')
        plt.savefig(my_path + '/newf/pfront' + str(time.time()) + '.png')

        if c.show_graph is True:
            plt.show()

    # all arguments should be lists
    def graph_both2(self, xvals, yvals, dominant_inds):
        if len(xvals) != len(yvals) or len(xvals) != len(dominant_inds):
            print("Error!  len xvals", len(xvals), " len yvals", len(yvals), " len dominds", len(dominant_inds))
            print("xvals", xvals)
            print("yvals", yvals)
            print("dominds", dominant_inds)
            exit(0)

        ymax = max(yvals)
        popsize = len(yvals)

        par_front_x = []
        par_front_y = []
        non_par_front_x = []
        non_par_front_y = []
        for i in range(0, len(xvals)):
            if dominant_inds[i] == 0:
                par_front_x.append(xvals[i])
                par_front_y.append(yvals[i])
            elif dominant_inds[i] == 1:
                non_par_front_x.append(xvals[i])
                non_par_front_y.append(yvals[i])

        plt.figure(1)
        plt.plot(par_front_x, par_front_y, 'bo')
        plt.plot(non_par_front_x, non_par_front_y, 'ro')
        plt.title("afpo")
        plt.xlim(-1, popsize)
        plt.ylim(-1, ymax)

        my_path = os.path.dirname(__file__)
        # plt.savefig('pfront' + str(time.time()) + '.pdf')
        plt.savefig(my_path + '/newf/pfront' + str(time.time()) + '.png')

        if c.show_graph is True:
            plt.show()

    def graph_both(self, par_front_x, par_front_y, dominated_x, dominated_y, popsize, ymax, title_tag="default_title"):
        plt.figure(1)
        print('ymax', ymax)
        # plt.subplot(211)
        # plt.plot(xs, ys, 'ro')
        # plt.xlim(-1, popsize)
        # plt.ylim(-1, ymax)
        # plt.subplot(212)
        plt.plot(par_front_x, par_front_y, 'bo')
        plt.plot(dominated_x, dominated_y, 'ro')
        plt.title(title_tag)
        plt.xlim(-1, popsize)
        plt.ylim(-1, ymax)

        my_path = os.path.dirname(__file__)
        # plt.savefig('pfront' + str(time.time()) + '.pdf')
        plt.savefig(my_path + '/newf/pfront' + str(time.time()) + '.png')

        if c.show_graph == True:
            plt.show()

    def phc_ga(self, parents, envs, gens):
        for i in range(0, gens):
            children = copy.deepcopy(parents)
            children.Mutate()
            parents.Evaluate(envs, pp=False, pb=True)
            children.Evaluate(envs, pp=False, pb=True)
            print('******* phc gen', i, '*******')
            parents.Print()
            children.Print(i)
            parents.ReplaceWith(children)
            parents.IncrementAges()
            print('Spaghetti pop dists')
            parents.PrintDists(i)
        return parents

    def conv_list_dict(self, list):
        dict = {}
        for i in range(0, len(list)):
            dict[i] = list[i]
        return dict

    # takes a list or dictionary and returns the lowest nonzero value, assuming all
    # values are 0 or positive
    def return_second_highest_in_list_or_dict(self, ld):
        ldtype = str(type(ld))
        dicttype = str(type({0: 0}))
        tempdict = {}
        if ldtype == dicttype:
            tempdict = ld
        else:
            for i in range(0, len(ld)):
                tempdict[i] = ld[i]

        minm = float('inf')
        for i in tempdict:
            if tempdict[i] == 0:
                pass
            else:
                if tempdict[i] < minm:
                    minm = tempdict[i]
        return minm

    # returns a list of ints starting at low, ending at high - 1.
    def ord_list(self, low, high):
        list = []
        for i in range(low, high):
            print(i, end='  ')
            list.append(i)
        print()
        return list


fit_ids_load = []
start_ga = GENETIC_ALGORITHM(fit_ids_load)
start_ga.main()
