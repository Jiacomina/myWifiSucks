"""
Program to calculate optimal wifi node positioning using PSO
Floor plan can be can be read in as a greyscale image file e.g. png.
"""
import matplotlib.pyplot as plt
import numpy as np
from pyswarm import pso
from read_image import load_floor_plan
from fitness import FitnessLandscape

MAP_FILEPATH = 'wall1small.png'
NUM_NODES = 4


# read image file, print width, height and dimensions (RGBA == 4 dimensions)
MAP_ARRAY = load_floor_plan(MAP_FILEPATH)
(width, height, dim) = MAP_ARRAY.shape
print("Read Image: ", MAP_FILEPATH, "  Width: ", width, "  Height: ", height)

# overlay with map image
plt.imshow(MAP_ARRAY, zorder=10)

lower_bounds = np.full((NUM_NODES*2), 0)
upper_bounds = np.full((NUM_NODES*2), width)
# get fitness values, store in z
fit_landscape = FitnessLandscape(width, height, NUM_NODES)

x_optimals, fitness = pso(fit_landscape.getFitness, lower_bounds, upper_bounds, swarmsize = 100, maxiter = 10, minstep = 0.8, debug = True, phip = 1, phig = 1)
print("x_optimals: ", x_optimals)
fit_landscape.getFitness(x_optimals)  #get z of best fitness
z = fit_landscape.getZ()
x = fit_landscape.getX()
y = fit_landscape.getY()

# create contour plot from z, x and y
cplot = plt.contourf(x, y, z, cmap = 'gist_rainbow', levels = 100)
plt.colorbar()
#plt.scatter(x_optimals[1::2], x_optimals[0::2], c='m')
plt.show()