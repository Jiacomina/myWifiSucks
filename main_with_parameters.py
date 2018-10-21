"""
Program to calculate optimal wifi node positioning using PSO
Floor plan can be can be read in as a greyscale image file e.g. png.
"""
from config import (MAP_FILEPATH, NUM_NODES, SCALE, SWARM_SIZE, phip, phig, omega, SWARM_SIZE_FIXED,
MAX_ITER_FIXED, MIN_STEP_FIXED, phip_fixed, phig_fixed, omega_fixed)

import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from pyswarm import pso
from floorMap import FloorMap
from fitness import FitnessLandscape


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

LB = np.full((NUM_NODES*2), 1)          # lower bounds of fitness lanscape
UB = np.empty((NUM_NODES*2))
UB[::2] = WIDTH - 2
UB[1::2] = HEIGHT - 2  # upper bounds of fitness lanscape

# Create new fitnessLandscape object
FIT_LANDSCAPE = FitnessLandscape(WIDTH, HEIGHT, NUM_NODES, MAP_ARRAY, WALLS, SCALE)

# run pso on fitnessLandscape object
# optimal positions stored as array in x_optimals eg. [x1, y1, x2, y2]

# run pso with the varying results
#OPTIONS: stop pso after either minstep=MIN_STEP and/or  maxiter=MAX_ITER,

# Will need to now save figures in file with correct labels. Hopefully can have this code sit and run to generate all
# the data. Should have an output file that also saves metrics like computation time

#################################  Vary swarm size parameter  #################################

for size in SWARM_SIZE:
    OPTIMAL_POSITIONS, FITNESS = pso(
        FIT_LANDSCAPE.getFitness,
        LB,
        UB,
        swarmsize=size,
        minstep=MIN_STEP_FIXED,
        maxiter=MAX_ITER_FIXED,
        debug=True,
        phip=phip_fixed,
        phig=phig_fixed,
        omega=omega_fixed,
        f_ieqcons=FIT_LANDSCAPE.check_pos,
        map_img = MAP_IMG)

print("Position optimals: ", OPTIMAL_POSITIONS)
print("Optimal Fitness: ", FITNESS)

#create get z values(fitness values) using the optimal x y positions
FIT_LANDSCAPE.getFitness(OPTIMAL_POSITIONS)

Z = FIT_LANDSCAPE.z # 2D array of fitness values
X = FIT_LANDSCAPE.x # 1D array of x axis values
Y = FIT_LANDSCAPE.y # 1D array of y axis values

levels = MaxNLocator(nbins=100).tick_values(int(Z.min())-1, int(Z.max())+1)
# create contour plot from x, y and z arrays
fig2, axis2 = plt.subplots()
cp = axis2.contourf(Y, X, Z, cmap='gist_rainbow', levels = levels)
cb = fig2.colorbar(cp)  # contour plot legend bar

# overlay with map image
axis2.imshow(WALL_IMG, zorder=10)

#plot nodes
#plt.scatter(optimal_positions[1::2], optimal_positions[0::2], c='m')
fig2.savefig("./plotframes/contourPlot.png", dpi=250)
plt.show()

#################################  Vary pbest coefficient  #################################

for pbest in phip:
    OPTIMAL_POSITIONS, FITNESS = pso(
        FIT_LANDSCAPE.getFitness,
        LB,
        UB,
        swarmsize=SWARM_SIZE_FIXED,
        minstep=MIN_STEP_FIXED,
        maxiter=MAX_ITER_FIXED,
        debug=True,
        phip=pbest,
        phig=phig_fixed,
        omega=omega_fixed,
        f_ieqcons=FIT_LANDSCAPE.check_pos,
        map_img = MAP_IMG)

print("Position optimals: ", OPTIMAL_POSITIONS)
print("Optimal Fitness: ", FITNESS)

#create get z values(fitness values) using the optimal x y positions
FIT_LANDSCAPE.getFitness(OPTIMAL_POSITIONS)

Z = FIT_LANDSCAPE.z # 2D array of fitness values
X = FIT_LANDSCAPE.x # 1D array of x axis values
Y = FIT_LANDSCAPE.y # 1D array of y axis values

levels = MaxNLocator(nbins=100).tick_values(int(Z.min())-1, int(Z.max())+1)
# create contour plot from x, y and z arrays
fig2, axis2 = plt.subplots()
cp = axis2.contourf(Y, X, Z, cmap='gist_rainbow', levels = levels)
cb = fig2.colorbar(cp)  # contour plot legend bar

# overlay with map image
axis2.imshow(WALL_IMG, zorder=10)

#plot nodes
#plt.scatter(optimal_positions[1::2], optimal_positions[0::2], c='m')
fig2.savefig("./plotframes/contourPlot.png", dpi=250)
plt.show()

#################################  Vary gbest coefficient  #################################

for gbest in phig:
    OPTIMAL_POSITIONS, FITNESS = pso(
        FIT_LANDSCAPE.getFitness,
        LB,
        UB,
        swarmsize=SWARM_SIZE_FIXED,
        minstep=MIN_STEP_FIXED,
        maxiter=MAX_ITER_FIXED,
        debug=True,
        phip=phig_fixed,
        phig=gbest,
        omega=omega_fixed,
        f_ieqcons=FIT_LANDSCAPE.check_pos,
        map_img = MAP_IMG)

print("Position optimals: ", OPTIMAL_POSITIONS)
print("Optimal Fitness: ", FITNESS)

#create get z values(fitness values) using the optimal x y positions
FIT_LANDSCAPE.getFitness(OPTIMAL_POSITIONS)

Z = FIT_LANDSCAPE.z # 2D array of fitness values
X = FIT_LANDSCAPE.x # 1D array of x axis values
Y = FIT_LANDSCAPE.y # 1D array of y axis values

levels = MaxNLocator(nbins=100).tick_values(int(Z.min())-1, int(Z.max())+1)
# create contour plot from x, y and z arrays
fig2, axis2 = plt.subplots()
cp = axis2.contourf(Y, X, Z, cmap='gist_rainbow', levels = levels)
cb = fig2.colorbar(cp)  # contour plot legend bar

# overlay with map image
axis2.imshow(WALL_IMG, zorder=10)

#plot nodes
#plt.scatter(optimal_positions[1::2], optimal_positions[0::2], c='m')
fig2.savefig("./plotframes/contourPlot.png", dpi=250)
plt.show()

#################################  Vary inertia weight coefficient ##################################

for acc in omega:
    OPTIMAL_POSITIONS, FITNESS = pso(
        FIT_LANDSCAPE.getFitness,
        LB,
        UB,
        swarmsize=SWARM_SIZE_FIXED,
        minstep=MIN_STEP_FIXED,
        maxiter=MAX_ITER_FIXED,
        debug=True,
        phip=phig_fixed,
        phig=phig_fixed,
        omega=acc,
        f_ieqcons=FIT_LANDSCAPE.check_pos,
        map_img = MAP_IMG)

print("Position optimals: ", OPTIMAL_POSITIONS)
print("Optimal Fitness: ", FITNESS)

#create get z values(fitness values) using the optimal x y positions
FIT_LANDSCAPE.getFitness(OPTIMAL_POSITIONS)

Z = FIT_LANDSCAPE.z # 2D array of fitness values
X = FIT_LANDSCAPE.x # 1D array of x axis values
Y = FIT_LANDSCAPE.y # 1D array of y axis values

levels = MaxNLocator(nbins=100).tick_values(int(Z.min())-1, int(Z.max())+1)
# create contour plot from x, y and z arrays
fig2, axis2 = plt.subplots()
cp = axis2.contourf(Y, X, Z, cmap='gist_rainbow', levels = levels)
cb = fig2.colorbar(cp)  # contour plot legend bar

# overlay with map image
axis2.imshow(WALL_IMG, zorder=10)

#plot nodes
#plt.scatter(optimal_positions[1::2], optimal_positions[0::2], c='m')
fig2.savefig("./plotframes/contourPlot.png", dpi=250)
plt.show()

