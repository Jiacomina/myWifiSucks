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
import os
from timer import time, endlog, log
import atexit
from pyswarm import pso
from floorMap import FloorMap
from fitness import FitnessLandscape

if len(sys.argv) > 1:
    MAP_FILEPATH = './Images/' + sys.argv[1]

# Make data directory
directory = 'parameter_testing_data/'+sys.argv[1] + '/'

if not os.path.exists(directory):
    os.makedirs(directory)

filename = directory + 'results.txt'
if os.path.exists(filename):
    append_write = 'w' # append if already exists
else:
    append_write = 'w' # make a new file if not

data_file = open(filename,append_write)
data_file.write(sys.argv[1] + '\n\n')

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

	# START TIMER
	start = time()
	log("Start Program")

	print("Processing Size: ", directory, size)
	data_file.write("Size: "+ str(size) + '\n')
	OPTIMAL_POSITIONS, FITNESS, ITER= pso(
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
        map_img=MAP_IMG,
		processes=4,
		draw_figures=False,
		directory=directory)

	print("Position optimals: ", OPTIMAL_POSITIONS)
	print("Optimal Fitness: ", FITNESS)
    
	data_file.write("Optimal Position: "+ str(OPTIMAL_POSITIONS) + '\n')
	data_file.write("Fitness: "+ str(FITNESS) + '\n')
	data_file.write("Iterations: "+ str(ITER) + '\n')
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
	fig2.savefig(directory +"size_" + str(size) + ".png", dpi=200)

	elapsed = endlog(start)
	data_file.write("Time elapsed: " + str(elapsed) + '\n\n')

#################################  Vary pbest coefficient  #################################
for pbest in phip:
	# START TIMER
	start = time()
	log("Start Program")
	data_file.write("Pbest: "+ str(pbest) + '\n')
	print("Processing Pbest: ", directory, pbest)
	OPTIMAL_POSITIONS, FITNESS, ITER= pso(
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
		map_img = MAP_IMG,
		processes = 4,
		draw_figures = False)
	
	print("Position optimals: ", OPTIMAL_POSITIONS)
	print("Optimal Fitness: ", FITNESS)

	data_file.write("Optimal Position: "+ str(OPTIMAL_POSITIONS) + '\n')
	data_file.write("Fitness: "+ str(FITNESS) + '\n')
	data_file.write("Iterations: "+ str(ITER) + '\n')

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

	fig2.savefig(directory +"pbest_" + str(pbest) + ".png", dpi=200)
	elapsed = endlog(start)
	data_file.write("Time elapsed: " + str(elapsed) + '\n\n')

#################################  Vary gbest coefficient  #################################

for gbest in phig:
	# START TIMER
	start = time()
	log("Start Program")
	data_file.write("Gbest: "+ str(gbest) + '\n')
	print("Processing Gbest: ", directory, gbest)
	OPTIMAL_POSITIONS, FITNESS, ITER= pso(
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
        map_img = MAP_IMG,
		processes = 4,
        draw_figures = False)

	print("Position optimals: ", OPTIMAL_POSITIONS)
	print("Optimal Fitness: ", FITNESS)

	data_file.write("Optimal Position: "+ str(OPTIMAL_POSITIONS) + '\n')
	data_file.write("Fitness: "+ str(FITNESS) + '\n')
	data_file.write("Iterations: "+ str(ITER) + '\n')

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

	fig2.savefig(directory +"gbest_" + str(gbest) + ".png", dpi=200)
	elapsed = endlog(start)
	data_file.write("Time elapsed: " + str(elapsed) + '\n\n')

#################################  Vary inertia weight coefficient ##################################

for acc in omega:
	# START TIMER
	start = time()
	log("Start Program")
	data_file.write("Acc: "+ str(acc) + '\n')
	print("Processing Acc: ", directory, acc)
	OPTIMAL_POSITIONS, FITNESS, ITER= pso(
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
        map_img = MAP_IMG,
        draw_figures = False,
		processes = 4)

	print("Position optimals: ", OPTIMAL_POSITIONS)
	print("Optimal Fitness: ", FITNESS)

	data_file.write("Optimal Position: "+ str(OPTIMAL_POSITIONS) + '\n')
	data_file.write("Fitness: "+ str(FITNESS) + '\n')
	data_file.write("Iterations: "+ str(ITER) + '\n')

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

	fig2.savefig(directory +"acc_" + str(acc) + ".png", dpi=200)
	elapsed = endlog(start)
	data_file.write("Time elapsed: " + str(elapsed) + '\n\n')

data_file.close()
