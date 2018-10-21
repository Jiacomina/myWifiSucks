"""
Program to calculate optimal wifi node positioning using BRUTE FORCE
Floor plan can be can be read in as a greyscale image file e.g. png.

Brute for diagram if NUM_NODES = 1 is created, saved in plotframes/bruteForcePlot.png
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from timer import time, endlog
import atexit
from multiprocessing import Pool 
from numpy import unravel_index
import itertools

# local  modules
from floorMap import FloorMap
from fitness import FitnessLandscape
from timer import log

# CUSTOM VARIABLES THAT CAN BE CHANGED
# default file path, can also change this by adding filename as command line argument
MAP_FILEPATH = './Images/wall3priorities.png' 
NUM_NODES = 2
SCALE = 1

# get filepath from command line arguments
if len(sys.argv) > 1:
    MAP_FILEPATH = './Images/' + sys.argv[1]

# read image file, print WIDTH, HEIGHT and dimensions (RGBA == 4 dimensions)
FLOOR_MAP = FloorMap(MAP_FILEPATH)
(WIDTH, HEIGHT) = (FLOOR_MAP.width, FLOOR_MAP.height)
MAP_ARRAY = FLOOR_MAP.array
print("Read Image: ", MAP_FILEPATH, "  WIDTH: ", WIDTH, "  HEIGHT: ", HEIGHT)

MAP_IMG = FLOOR_MAP.image
WALL_IMG = FLOOR_MAP.get_transparent_img()
WALLS = FLOOR_MAP.get_walls()

# START TIMER
start = time()
log("Start Program")

# Create new fitnessLandscape object
FIT_LANDSCAPE = FitnessLandscape(WIDTH, HEIGHT, NUM_NODES, MAP_ARRAY, WALLS, SCALE)

# attempt brute force computation
print("Attempting brute force")
# create list containing all pixel coordinates 
array_of_permutations = []
for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        array_of_permutations.append([x, y])

print("Creating array of point permutations...")
if NUM_NODES > 1:
    # make larger list for n nodes
    array_of_permutations = itertools.permutations(array_of_permutations, NUM_NODES)

# change format of points from ( [[0,1], [0, 2]],  [[0,1],[0, 2]] ) -> ([0, 1, 0, 2],[0, 1, 0, 2])
# because that is how pyswarm pso() reads it
print("Reformatting permutated points")
points = []
for pos in array_of_permutations:
    pos = list(itertools.chain.from_iterable(pos))
    print(pos)
    points.append(pos)

# function that gets fitness value for given point coordinates
def get_fitness(point):
    fitness = FIT_LANDSCAPE.getFitness(point)
    print("X:", point, " FITNESS:", fitness)
    return [point, fitness]

print("Start multithreaded fitness calculations for each point")
# Set up mulltiprocessing
pool = Pool()

# calculate get_fitness() for each item in the points list, result is returned as a 1D array
results = pool.map(get_fitness, points)

# end mulltiprocessing
pool.close() 
pool.join()

# extract fitnesses and positions from results array
fitness_array = [item[1] for item in results]
positions = [item[0] for item in results]

# find best and mac fitness
max_fitness = max(fitness_array)
best_fitness = min(fitness_array)

# get x and y coordinates of best solution
best_coord = positions[fitness_array.index(best_fitness)]

# convert fitness values to a value from 0 - 1
percent_fitness_array = 1-(fitness_array-best_fitness)/(max_fitness - best_fitness)
print("Worst fitness", max_fitness)
print("Best fitness", best_fitness)
print("Optimal Position: ", best_coord)

# End Timer
atexit.register(endlog, start)

# Create visual plot if num_nodes is 1
if(NUM_NODES == 1):

    # create array to store fitness values
    z = np.zeros([WIDTH, HEIGHT], dtype=float)
    # convert 1D fitnesses array into 2D array
    for index, fit in enumerate(percent_fitness_array):
        x = positions[index][0]
        y = positions[index][1]
        z[x][y] = fit

    # create contour plot from x, y and z arrays
    fig2, axis2 = plt.subplots()
    levels = MaxNLocator(nbins=100).tick_values(0, 1)
    cp = axis2.contourf(range(0,HEIGHT), range(0,WIDTH), z, cmap='gnuplot', levels = levels)
    cb = fig2.colorbar(cp)  # contour plot legend bar

    # overlay with map image
    axis2.imshow(WALL_IMG, zorder=10)

    #plot nodes
    fig2.savefig("./plotframes/BruteForcePlot.png", dpi=250)
 
        