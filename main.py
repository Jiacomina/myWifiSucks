"""
Program to calculate optimal wifi node positioning using PSO
Floor plan can be can be read in as a greyscale image file e.g. png.
"""
import matplotlib.pyplot as plt
#from pyswarm import pso
import read_image

MAP_FILEPATH = 'wall2.png'

def printNodes(x_coords, y_coords):
    plt.scatter(x_coords, y_coords)

MAP_ARRAY = read_image.load_floor_plan(MAP_FILEPATH)
plt.imshow(MAP_ARRAY)
printNodes(x_coords = [100, 23, 223], y_coords = [42, 180, 101])
plt.show()


