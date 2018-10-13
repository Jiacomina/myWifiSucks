"""
Program to calculate optimal wifi node positioning using PSO
Floor plan can be can be read in as a greyscale image file e.g. png.
"""
import matplotlib.pyplot as plt
import numpy as np
from pyswarm import pso
from floorMap import FloorMap
from fitness import FitnessLandscape
from intersections import intersection

MAP_FILEPATH = 'wall3small.png'
NUM_NODES = 2


# read image file, print width, height and dimensions (RGBA == 4 dimensions)
floor_map = FloorMap(MAP_FILEPATH)
(width, height) = (floor_map.width, floor_map.height)
MAP_ARRAY = floor_map.get_array()
print("Read Image: ", MAP_FILEPATH, "  Width: ", width, "  Height: ", height)

MAP_IMG = floor_map.get_transparent_img()
walls = floor_map.get_walls()

# overlay with map image
plt.imshow(MAP_IMG, zorder=10)

lb = np.full((NUM_NODES*2), 0)          # lower bounds of fitness lanscape
ub = np.full((NUM_NODES*2), width-1)      # upper bounds of fitness lanscape
# get fitness values, store in z
fit_landscape = FitnessLandscape(width, height, NUM_NODES, MAP_ARRAY, walls)

x_optimals, fitness = pso(fit_landscape.getFitness, lb, ub, ieqcons = [fit_landscape.check_pos], swarmsize = 50, maxiter = 10, debug = True)
print("x_optimals: ", x_optimals)
fit_landscape.getFitness(x_optimals)  #get z of best fitness
z = fit_landscape.getZ()
x = fit_landscape.getX()
y = fit_landscape.getY()

# create contour plot from z, x and y
cplot = plt.contourf(x, y, z, cmap = 'gist_rainbow', levels = 100)
plt.colorbar()
plt.scatter(x_optimals[1::2], x_optimals[0::2], c='m')
plt.show()