from __future__ import print_function
import const as c
import time
import pyrosim
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import pickle
import os

def conv_list_dict(list):
    dict = {}
    for i in range(0, len(list)):
        dict[i] = list[i]
    return dict


# takes a list or dictionary and returns the lowest nonzero value, assuming all
# values are 0 or positive
def return_second_highest_in_list_or_dict(ld):
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
def ord_list(low, high):
    list = []
    for i in range(low, high):
        print(i, end='  ')
        list.append(i)
    print()
    return list


# yvals should be lists
def graph(yvals, show_graph, title_tag):

    ymax = max(yvals)
    popsize = len(yvals)

    plt.figure(1)
    plt.plot(yvals, 'bo')
    # plt.plot(non_par_front_x, non_par_front_y, 'ro')
    plt.title(title_tag)
    # plt.xlim(-5, popsize)
    # plt.ylim(-1, ymax)

    my_path = os.path.dirname(__file__)
    # plt.savefig('pfront' + str(time.time()) + '.pdf')
    plt.savefig(my_path + '/newf/graph' + str(time.time()) + title_tag + '.png')

    # show_graph = True
    if show_graph:
        plt.show()


# yvals should be list of lists
def graph_sub(yvals, show_graph, title_tag, a=1, b=1):

    ymax = max(yvals)
    popsize = len(yvals)

    fig, axes = plt.subplots(a, b, sharex=True, sharey=True)  # subplot_kw=dict(polar=True))
    axes[0, 0].plot(yvals[0])
    axes[0, 1].plot(yvals[0])
    axes[1, 1].scatter(range(len(yvals[0])), yvals[0])
    plt.title(title_tag)

    my_path = os.path.dirname(__file__)
    # plt.savefig('pfront' + str(time.time()) + '.pdf')
    plt.savefig(my_path + '/newf/graph' + str(time.time()) + title_tag + '.png')

    show_graph = True
    if show_graph:
        plt.show()


# all arguments should be lists
def graph_both3(xvals, yvals, dominant_inds):
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
