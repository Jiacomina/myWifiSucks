"""
Program to calculate optimal wifi node positioning using BRUTE FORCE
Floor plan can be can be read in as a greyscale image file e.g. png.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# import packages for program timer
import atexit
from time import time, strftime, localtime
from datetime import timedelta

# local  modules
from floorMap import FloorMap
from fitness import FitnessLandscape


# CUSTOM VARIABLES THAT CAN BE CHANGED
# default file path, can also change this by adding filename as command line argument
MAP_FILEPATH = './Images/wall3priorities.png' 
NUM_NODES = 1
SCALE = 1

# get filepath from command line arguments
if len(sys.argv) > 1:
    MAP_FILEPATH = './Images/' + sys.argv[1]

# read image file, print WIDTH, HEIGHT and dimensions (RGBA == 4 dimensions)
FLOOR_MAP = FloorMap(MAP_FILEPATH)
(WIDTH, HEIGHT) = (FLOOR_MAP.width, FLOOR_MAP.height)
MAP_ARRAY = FLOOR_MAP.array
print(MAP_ARRAY)
print("Read Image: ", MAP_FILEPATH, "  WIDTH: ", WIDTH, "  HEIGHT: ", HEIGHT)

MAP_IMG = FLOOR_MAP.image
WALL_IMG = FLOOR_MAP.get_transparent_img()
WALLS = FLOOR_MAP.get_walls()
print(WALLS)

# Create new fitnessLandscape object
FIT_LANDSCAPE = FitnessLandscape(WIDTH, HEIGHT, NUM_NODES, MAP_ARRAY, WALLS, SCALE)
best_fitness = 0
best_x = 0
best_y = 0
fitness_array = np.zeros([WIDTH, HEIGHT])
for x in range(0, WIDTH):
    print("X:", x,"/",WIDTH)
    for y in range(0, HEIGHT):
        fitness = FIT_LANDSCAPE.getFitness([x, y])
        fitness_array[x][y] = fitness
        if best_fitness < fitness:
            best_fitness = fitness
            best_x = x
            best_y = y
percent_fitness_array = fitness_array/best_fitness

# create contour plot from x, y and z arrays
fig2, axis2 = plt.subplots()
levels = MaxNLocator(nbins=100).tick_values(0, 1)
cp = axis2.contourf(range(0,HEIGHT), range(0,WIDTH), percent_fitness_array, cmap='gist_rainbow', levels = levels)
cb = fig2.colorbar(cp)  # contour plot legend bar

# overlay with map image
axis2.imshow(WALL_IMG, zorder=10)

#plot nodes
#plt.scatter(optimal_positions[1::2], optimal_positions[0::2], c='m')
fig2.savefig("./plotframes/BruteForcePlot.png", dpi=250)
plt.show()
        