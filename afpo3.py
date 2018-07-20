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


class GENETIC_ALGORITHM:
    def __init__(self, fit_ids):
        fff = 1
        self.fit_ids = fit_ids

        # Alphanumeric string
        # self.id_strings = []
        # ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

        # ############### random values test pareto ###############
        # default x, y, popsize values for af_pareto()
        self.ymax = 15
        self.popsize = 25
        self.ys = np.random.randint(4, self.ymax, self.popsize)
        self.xs = np.random.randint(0, self.popsize, self.popsize)
        self.af_pareto_math(self.xs, self.ys)
        print('\n############# test graph done #############\n')

    def main(self):
        t_end = time.time() + 60 * c.minutes
        envs = ENVIRONMENTS()
        print('envs to run:', c.envsToRun, '   initial popsize:', c.num_rand_phc)
        parents = POPULATION(c.num_rand_phc + len(self.fit_ids))
        parents.InitializeRandomPop()
        parents.Evaluate(envs, pp=False, pb=True)
        parents.Print()

        if c.alg == 'afpo':
            self.afpo()
        elif c.alg == 'garef':
            parents = self.garef(c.numGensDivPop, envs, parents, t_end)

        self.ShowEvaluatePop(parents, envs, pp=True, pb=False)

    def ShowEvaluatePop(self, parents, envs, pp=True, pb=False):
        for j in range(0, len(parents.p)):
            raw_input('press enter to continue...')
            for e in c.envsToRun:
                # for j in range(0, 1):
                parents.p[j].Start_Evaluation(envs.envs[e], pp, pb)

    ###################################### main ######################################
    def afpo(self):
        envs = ENVIRONMENTS()
        print('envs to run:', c.envsToRun, '   pop init:', c.num_rand_phc + len(self.fit_ids))
        parents = POPULATION(c.num_rand_phc + len(self.fit_ids))
        parents.InitializeRandomPop()

        parents = self.phc_ga(parents, envs, c.afpo2_phc_gens)
        print('\n############# phc done #############\n')

        for i in range(0, len(parents.p)):
            parents.p[i].age += i
        for i in range(0, len(parents.p)):
            print('p[' + str(i) + '].age =', parents.p[i].age)
        # 3rd arg gens=2 by default
        parents = self.af_pareto_ga(parents, envs, c.afpo2_afpo_gens)
        parents.Pickling618()
    ###################################### main ######################################

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

    def af_pareto_ga(self, parents, envs, gens=2):

        def inner(parents, envs):
            parents_temp = self.af_pareto_spop(parents, envs)
            # print("parents type:", type(parents))
            # print("parents.p type:", type(parents.p))
            # print("parents.p[0] type:", type(parents.p[0]))
            parents_temp.IncrementAges()
            parents_temp.Print()
            return parents_temp

        t_end = time.time() + 60 * c.minutes
        if c.gen_mode == 'time':
            i = 0
            while time.time() < t_end:
                print("\n##########********* af_pareto_spop gen", i, "*********##########")
                parents = inner(parents, envs)
                i += 1
        elif c.gen_mode == 'gens':
            for i in range(0, gens):
                print("\n##########********* af_pareto_spop gen", i, "*********##########")
                parents = inner(parents, envs)
        else:
            print("c.gen_mode must be 'time' or 'gens'. exiting.")
            exit(0)
        return parents


    # def af_pareto_spop(self, parents, envs):
    #     children = copy.deepcopy(parents)
    #     children.Mutate()
    #
    #     single = POPULATION(1)
    #     single.InitializeRandomPop()
    #     single.Evaluate(envs, pp=False, pb=True)
    #     parents.Evaluate(envs, pp=False, pb=True)
    #     children.Evaluate(envs, pp=False, pb=True)
    #
    #     # combine single, parents, children into one pop
    #     pcc = POPULATION(1 + 2 * len(parents.p))
    #     pcc.p[0] = single.p[0]
    #     for i in range(1, len(parents.p) + 1):
    #         pcc.p[i] = parents.p[i - 1]
    #     for i in range(len(parents.p) + 1, len(parents.p) + len(children.p) + 1):
    #         pcc.p[i] = children.p[i - len(children.p) - 1]
    #
    #
    #     # these methods in pop class all return lists
    #     s_fits = single.GetFits()
    #     s_ages = single.GetAges()
    #     p_fits = parents.GetFits()
    #     p_ages = parents.GetAges()
    #     c_fits = children.GetFits()
    #     c_ages = children.GetAges()
    #
    #     pc_fits = np.concatenate((p_fits, c_fits))
    #     pc_fits = np.concatenate((s_fits, pc_fits))
    #     pc_ages = np.concatenate((p_ages, c_ages))
    #     pc_ages = np.concatenate((s_ages, pc_ages))
    #
    #     min_fitness_pc = self.return_second_highest_in_list_or_dict(pc_fits)
    #     for i in range(0, len(pc_fits)):
    #         if pc_fits[i] == 0:
    #             pc_fits[i] = min_fitness_pc / 10.0
    #             pcc.p[i].fitness = min_fitness_pc / 10.0
    #
    #     pc_fits_inv = []
    #     print('pc_fits', pc_fits)
    #     for i in range(0, len(pc_fits)):
    #         pc_fits_inv.append(pc_fits[i]**-1)
    #
    #     # returns a list right now
    #     dominant_inds = np.array(self.af_pareto_math(pc_ages, pc_fits_inv))
    #     print('********** exit af_pareto_math **********\n')
    #     print('dominant inds', dominant_inds)
    #
    #     # new_pop = POPULATION(len(dominant_inds))
    #     # count = 0
    #
    #     print('******* len of pcc.p', len(pcc.p), '*******')
    #
    #     # for i in dominant_inds:
    #     #     print('i in dominant inds is', i)
    #     #     new_pop.p[count] = pcc_trim.p[i]
    #     #     count += 1
    #     if len(dominant_inds) < c.target_afpop:
    #         new_popsize = c.target_afpop
    #     else:
    #         new_popsize = len(dominant_inds)
    #     print("new pop size ", new_popsize)
    #     new_pop = POPULATION(new_popsize)
    #     for i in range(0, new_popsize):
    #         # print("type of pcc.p[dominant_inds[" + str(i % len(dominant_inds)) + "]]", type(pcc.p[dominant_inds[i % len(dominant_inds)]]))
    #         new_pop.p[i] = copy.deepcopy( pcc.p[dominant_inds[i % len(dominant_inds)]] )
    #         # print(new_pop.p[i].age)
    #
    #     print('new pop len', len(new_pop.p))
    #
    #     return new_pop

    def af_pareto_spop(self, front, envs):
        target_popsize = 20
        pcc = POPULATION(target_popsize)

        single = POPULATION(1)
        single.InitializeRandomPop()
        single.Evaluate(envs, False, True)

        num_remain = target_popsize - (len(front.p) + 1)
        if num_remain > 0:
            pccr = POPULATION(num_remain)
            for i in range(0, num_remain):
                pccr.p[i] = copy.deepcopy(pcc.p[i % len(front.p)])
            pccr.Mutate()
            pccr.Evaluate()

        for i in range(0, target_popsize):
            if i == 0:
                pcc.p[i] = single.p[0]
            elif i < len(front.p) + 1:
                pcc.p[i] = front.p[i - 1]
            else:
                pcc.p[i] = pccr[i - (len(front) + 1)]

        ages = pcc.GetAges()
        fits = pcc.GetFits()
        print('fits', fits, '  ages', ages)

        fits_inv = []
        for i in range(0, len(fits)):
            if fits[i] != 0:
                fits_inv.append(fits[i]**-1)
            else:
                fits_inv.append(10**6)

        dominant_inds = np.array(self.af_pareto_math(ages, fits_inv))
        new_pop = POPULATION(len(dominant_inds))
        for i in range(0, target_popsize):
            dominant_inds_index = i % len(dominant_inds)
            new_pop.p[i] = copy.deepcopy(pcc.p[dominant_inds_index])
            if i >= len(dominant_inds):
                new_pop.p[i].Mutate()

        del pcc
        new_pop.Print()
        return new_pop


    # takes a list or dictionary and returns the lowest nonzero value, assuming all
    # values are 0 or positive
    def return_second_highest_in_list_or_dict(self, ld):
        ldtype = str(type(ld))
        dicttype = str(type({0:0}))
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

    # graphs input and returns indices of places in the two arrays that are on pareto front, dominant points
    # takes dictionaries xs and ys
    def af_pareto_math(self, xs, ys):
        print('\n***** enter af_pareto_math *****')
        # find max val in ys
        maxval = 0
        for i in range(0, len(ys)):
            if ys[i] > maxval:
                maxval = i
        ymax = maxval

        popsize = len(ys)
        print('popsize', popsize)
        # ord_list = self.ord_list(0, popsize)
        # checked_list = [False] * popsize
        # dominated_dict = {}
        dominated_list = []

        for i in range(0, len(xs)):
            dominated_list.append(0)

        # for k in xs.keys():
        #     dominated_dict[k] = 0

        print('xs', xs)
        print('len xs', len(xs))
        print('ys', ys)
        print('len ys', len(ys))
        print('ymax', ymax)
        # print('\ncl', checked_list, '\ndl', dominated_list)
        # print('\nol', ord_list)
        for i in range(0, len(xs)):
            # if c.print_par_val == 1:
            #     print('i', i)
            #     print('xs[' + str(i) + ']', xs[i])
            #     print('ys[' + str(i) + ']', ys[i])
            for j in range(0, len(xs)):
                # if c.print_par_val == 1:
                #     print('    j', j)
                #     print('    ys[' + str(j) + ']', ys[j])
                #     print('    xs[' + str(j) + ']', xs[j])
                if j == i: continue
                if ys[i] < ys[j] and xs[i] < xs[j]:
                    dominated_list[j] = 1
                elif ys[j] < ys[i] and xs[j] < xs[i]:
                    dominated_list[i] = 1
                    break
                else:
                    pass
        print('list of dominated indices 0 or 1', dominated_list)

        pareto_front_x = []
        pareto_front_y = []

        xx_copy = []
        yy_copy = []
        domnt_inds = []

        for i in range(0, len(dominated_list)):
            if dominated_list[i] == 0:
                pareto_front_x.append(xs[i])
                pareto_front_y.append(ys[i])
                domnt_inds.append(i)
            else:
                xx_copy.append(xs[i])
                yy_copy.append(ys[i])

        if c.show_graph == True:
            self.graph_both(pareto_front_x, pareto_front_y, xx_copy, yy_copy, popsize, ymax)

        return domnt_inds

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

        plt.savefig('P-front' + title_tag + '.pdf')
        plt.show()

    def conv_list_dict(self, list):
        dict = {}
        for i in range(0, len(list)):
            dict[i] = list[i]
        return dict

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
