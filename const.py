import math

print_func = 1
print_par_val = 0
quick = False
quick = True
if quick:
    target_afpop = 5
    popsize_simple_ga = 8
    combo_ga_num_slots = 8
    num_rand_phc = 11
    show_graph = True
    # show_graph = False
    save_graph = True
    # save_graph = False
    evalTime = 225
    envsToRun = [1]
    gens = 3
    gen_mode = 'gens'
    gen_mode = 'time'
    minutes = 0.05
    numGensDivPop = 25
    alg = 'afpo'
else:
    target_afpop = 31
    popsize_simple_ga = 25
    combo_ga_num_slots = 12
    num_rand_phc = 34
    # show_graph = True
    show_graph = False
    save_graph = True
    # save_graph = False
    evalTime = 550
    envsToRun = [1, 2, 3]
    gens = 40
    # gen_mode = 'gens'
    gen_mode = 'time'
    minutes = 100
    numGensDivPop = 15
    alg = 'afpo'
#################################
cutoff = 2

numEnvs = len(envsToRun)

# fit_labels = [6375, 10652, 3386, 11824, 31118]
fit_labels = []

popSize = 12

pathLoad = '/home/iskander/PycharmProjects/EvoBotProject2/genomes/run05040227/good/'
pathSave = '/home/iskander/PycharmProjects/Bots/genomes/'
# envsToRun = [6, 7]

# envsToRun = [1]


fitness_scale = 10 ** 7

numInputs = 17
numHidden = 12
numOutputs = 9

L = 0.13
R = L / 5
# Pi = 3.14159


angle_range_deg = 140
angle_range = math.pi * angle_range_deg / 180

fitPenMult = 0.7

upJointHalfRange = math.pi / 3
lowJointHalfRange = math.pi / 2

maxAvgAngUpJ = upJointHalfRange / 2
maxAvgAngLoJ = lowJointHalfRange / 2

lightDistMult = 20
lightDist = lightDistMult * L
lightSrcL = L
lightSrcW = L
lightSrcH = 4.7 * L

numObstacles = 7
obstacles = True

wallDist = lightDist / 2.8

obstL = 0.5 * L
obstW = 0.5 * L
obstH = 3 * L

####### Wall #######
wallL = wallDist * 2
wallW = L
wallH = 2.5 * L
wallCutFrac = 0.7
wallCut = wallDist * wallCutFrac

bodyAngDeg = 45
bodyAng = math.pi * bodyAngDeg / 180

mutateRandFreq = 15
numBigMutate = 2
mutateFreq = 20

spinSpeed = 4

pickleFreq = 1

sigfigs = 2


def round_matrix(h):
    for i in range(0, len(h)):
        for j in range(0, len(h[i])):
            h[i][j] = round(h[i][j], sigfigs)
    return h
