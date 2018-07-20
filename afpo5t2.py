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
    def __init__(self, fit_ids=[]):
        fff = 1
        self.fit_ids = fit_ids

        # Alphanumeric string
        # self.id_strings = []
        # ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

        # ############### random values test pareto ###############
        # default x, y, popsize values for af_pareto()
        self.ys = np.random.randint(4, 15, 25)
        self.xs = np.random.randint(0, 25, 25)
        self.calc_pareto_front(self.xs, self.ys)
        print('\n############# test graph done #############\n')

    def main(self):
        envs = ENVIRONMENTS()
        parents = POPULATION(c.num_rand_phc + len(self.fit_ids))
        print('envs:', c.envsToRun, '   pop init:', c.num_rand_phc + len(self.fit_ids))

        parents.InitializeRandomPop()
        parents.Evaluate(envs, False, True)
        for i in range(0, len(parents.p)):
            parents.p[i].age += i

        self.afpo(parents, envs)

    def afpo(self, parents, envs):
        def inner(parents, envs, i):
            print("\n##########********* generation", i, "*********##########")
            front = self.gen_par_front_pop(parents, envs)
            if len(front.p) < c.target_afpop:
                target_popsize = c.target_afpop
            else:
                target_popsize = len(front.p) * 2
            print("target_popsize:", target_popsize)
            new_pop = POPULATION(target_popsize)
            for i in range(0, target_popsize):
                new_pop.p[i] = copy.deepcopy(front.p[i % len(front.p)])
                if i >= len(front.p):
                    new_pop.p[i].Mutate()
            return new_pop

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

        final_pop_front = self.gen_par_front_pop(parents, envs)
        final_pop_front.Pickling618()
        self.ShowEvaluatePop(final_pop_front, envs, pp=True, pb=False)

    def gen_par_front_pop(self, parents, envs):
        ages = parents.GetAges()
        fits = parents.GetFits()
        fits_inv = parents.GetFitsInv()

        dom_inds = self.calc_pareto_front(ages, fits_inv)

        self.graph_both3(ages, fits_inv, dom_inds)

        par_front_pop = POPULATION(len(dom_inds))
        for i in range(0, len(dom_inds)):
            par_front_pop.p[i] = copy.deepcopy(parents.p[dom_inds[i]])

        return par_front_pop

    # graphs input and returns indices of places in the two arrays that are on pareto front, dominant points
    # takes dictionaries xs and ys
    def calc_pareto_front(self, xs, ys):
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

    def phc_ga(self, parents, envs):
        print("***** Entering phc_ga() *****")
        def inner(parents, envs, i):
            children = copy.deepcopy(parents)
            children.Mutate()
            # parents.Evaluate(envs, pp=False, pb=True)
            children.Evaluate(envs, pp=False, pb=True)
            print('\n\n******* phc gen', i, '*******')
            print("*** Parents  ***")
            parents.Print()
            print("*** Children ***")
            children.Print(i)
            parents.ReplaceWith(children)
            parents.IncrementAges()
            print('Spaghetti pop dists')
            parents.PrintDists(i)
            return parents

        if c.gen_mode == 'time':
            t_end = time.time() + 60 * c.minutes
            i = 0
            while(time.time() < t_end):
                parents = inner(parents, envs, i)
                i += 1
        elif c.gen_mode == 'gens':
            for i in range(0, c.gens):
                parents = inner(parents, envs, i)

        return parents

    def combo_simple_phc_ga(self):
        envs = ENVIRONMENTS()
        # parents = POPULATION(c.num_rand_phc)
        # print('envs:', c.envsToRun, '   pop init:', c.num_rand_phc)
        # parents.InitializeRandomPop()
        # parents.Evaluate(envs, False, True)

        pop_phc = POPULATION(c.combo_ga_num_slots)

        for k in range(0, c.combo_ga_num_slots):
            print("***** Slot number", k, "*****")
            pop_phc.p[k] = self.simple_ga(envs)
            pop_phc.p[k].ID = k

        pop_phc = self.phc_ga(pop_phc, envs)
        pop_phc.Pickling618()
        self.ShowEvaluatePop(pop_phc, envs, True, False)


    def simple_ga(self, envs):
        def inner(parents, envs, i):
            # children = POPULATION(len(parents.p))
            children = copy.deepcopy(parents)
            children.FillFrom(parents)
            children.Evaluate(envs, False, True)
            print("\n*** Generation", i, "***")
            print("\n***  Parents   ***")
            parents.Print()
            print("***  Children  ***")
            children.Print()
            print()
            parents = children
            return parents

        envs = ENVIRONMENTS()
        parents = POPULATION(c.popsize_simple_ga)
        print('envs:', c.envsToRun, '   pop init:', c.popsize_simple_ga)
        parents.InitializeRandomPop()
        parents.Evaluate(envs, False, True)

        # if c.gen_mode == 'time':
        #     t_end = time.time() + 60 * c.minutes
        #     i = 0
        #     while(time.time() < t_end):
        #         parents = inner(parents, envs, i)
        #         i += 1
        # elif c.gen_mode == 'gens':
        #     for i in range(0, c.gens):
        #         parents = inner(parents, envs, i)

        for i in range(0, c.numGensDivPop):
            parents = inner(parents, envs, i)

        return parents.p[0]

    def ShowEvaluatePop(self, parents, envs, pp=True, pb=False):
        for j in range(0, len(parents.p)):
            raw_input('press enter to continue...')
            for e in c.envsToRun:
                # for j in range(0, 1):
                parents.p[j].Start_Evaluation(envs.envs[e], pp, pb)


# start_ga = GENETIC_ALGORITHM()
# start_ga.main()
