"""
Program to calculate optimal wifi node positioning using PSO
Floor plan can be can be read in as a greyscale image file e.g. png.
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from pyswarm import pso
from floorMap import FloorMap
from fitness import FitnessLandscape

MAP_FILEPATH = 'wall3.png'
NUM_NODES = 1
SCALE = 1/3
SWARM_SIZE = 2
MAX_ITER = 1

# read image file, print WIDTH, HEIGHT and dimensions (RGBA == 4 dimensions)
FLOOR_MAP = FloorMap(MAP_FILEPATH)
(WIDTH, HEIGHT) = (FLOOR_MAP.width, FLOOR_MAP.height)
MAP_ARRAY = FLOOR_MAP.array
print("Read Image: ", MAP_FILEPATH, "  WIDTH: ", WIDTH, "  HEIGHT: ", HEIGHT)

MAP_IMG = FLOOR_MAP.get_transparent_img()
WALLS = FLOOR_MAP.get_walls()
print(WALLS)

LB = np.full((NUM_NODES*2), 0)          # lower bounds of fitness lanscape
UB = np.empty((NUM_NODES*2))
UB[::2] = WIDTH - 1
UB[1::2] = HEIGHT - 1  # upper bounds of fitness lanscape

# Create new fitnessLandscape object
FIT_LANDSCAPE = FitnessLandscape(WIDTH, HEIGHT, NUM_NODES, MAP_ARRAY, WALLS, SCALE)

# run pso on fitnessLandscape object
# optimal positions stored as array in x_optimals eg. [x1, y1, x2, y2]
OPTIMAL_POSITIONS, FITNESS = pso(
    FIT_LANDSCAPE.getFitness,
    LB,
    UB,
    swarmsize=SWARM_SIZE,
    maxiter=MAX_ITER,
    debug=True,
    phip=0.4,
    phig=0.4,
    omega=0.6)

print("Position optimals: ", OPTIMAL_POSITIONS)
print("Optimal Fitness: ", FITNESS)

#create get z values(fitness values) using the optimal x y positions
FIT_LANDSCAPE.getFitness(OPTIMAL_POSITIONS)

Z = FIT_LANDSCAPE.z # 2D array of fitness values
X = FIT_LANDSCAPE.x # 1D array of x axis values
Y = FIT_LANDSCAPE.y # 1D array of y axis values

levels = MaxNLocator(nbins=100).tick_values(Z.min(), 0)
# create contour plot from x, y and z arrays
fig2, axis2 = plt.subplots()
cp = axis2.contourf(Y, X, Z, cmap='jet', levels = levels)
cb = fig2.colorbar(cp)  # contour plot legend bar

# overlay with map image
axis2.imshow(MAP_IMG, zorder=10)

#plot nodes
#plt.scatter(optimal_positions[1::2], optimal_positions[0::2], c='m')
plt.show()
