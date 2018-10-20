"""
Program to calculate optimal wifi node positioning using PSO
Floor plan can be can be read in as a greyscale image file e.g. png.
"""
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from pyswarm import pso
from floorMap import FloorMap
from fitness import FitnessLandscape
import itertools

MAP_FILEPATH = './Images/wall1nogo.png'
NUM_NODES = 1
SCALE = 1/3
SWARM_SIZE = 50
MAX_ITER = 6

if len(sys.argv) > 1:
    MAP_FILEPATH = './Images/' + sys.argv[1]

# read image file, print WIDTH, HEIGHT and dimensions (RGBA == 4 dimensions)
FLOOR_MAP = FloorMap(MAP_FILEPATH)
(WIDTH, HEIGHT) = (FLOOR_MAP.width, FLOOR_MAP.height)
MAP_ARRAY = FLOOR_MAP.array
print("Read Image: ", MAP_FILEPATH, "  WIDTH: ", WIDTH, "  HEIGHT: ", HEIGHT)

MAP_IMG = FLOOR_MAP.get_transparent_img()
WALLS = FLOOR_MAP.get_walls()
print(WALLS)  # How is this printing an array? Does python automatically do this?

LB = np.full((NUM_NODES*2), 1)          # lower bounds of fitness landscape, start at 1, *2 for x y [x1 = 1 y1 =1]
UB = np.empty((NUM_NODES*2))
UB[::2] = WIDTH - 2  # every 2nd element, y for each node, equals width - 2
UB[1::2] = HEIGHT - 2  # the upper bound for each x coordinate of every node = height - 2


# Create new fitnessLandscape object
FIT_LANDSCAPE = FitnessLandscape(WIDTH, HEIGHT, NUM_NODES, MAP_ARRAY, WALLS, SCALE)

# attempt brute force computation

print("Attempting brute force")

# start by creating an array "array_of_permutations" that has all the possible and allowed x and y values
# for node positions. Have x and y values for all node positions, even if they are repeated

# btw allowing repetitions makes code inefficient, but for now not a big deal. Can optimise later if time - again
# shouldn't matter too much

y_length = WIDTH - 2
x_length = HEIGHT - 2
a = 1
b = 1
index = 0
array_of_permutations = []

while index < x_length:
    array_of_permutations.append(a)
    a = a + 1
    index = index + 1

while index < (x_length + y_length):
    array_of_permutations.append(b)
    b = b + 1
    index = index + 1

# technically we created an array with x y values for one node, extend this array for all nodes

node = 2
while node <= NUM_NODES:
    array_of_permutations.extend(array_of_permutations)
    node = node + 1

print("array of permutations: ", array_of_permutations)

# create all the possible x y values for our map for all the nodes

all_x_y_pos = itertools.permutations(array_of_permutations, NUM_NODES * 2)
# for pos in all_x_y_pos:
    # print(pos)

# compute fitness for all x y points for all nodes and find best position

final_fitness = 0  # variable to store our best fitness value
previous_fitness = -1
best_pos_for_nodes = []
for pos in all_x_y_pos:
    fitness = FIT_LANDSCAPE.getFitness(pos)
    if fitness > previous_fitness:
        final_fitness = fitness
        previous_fitness = fitness
        best_pos_for_nodes = pos

print("best position for nodes: ", pos, "\tfitness: ", final_fitness)

# maybe some visualization here, sorry still too dumb at python to do quickly :(