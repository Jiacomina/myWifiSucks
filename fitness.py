from math import log, sqrt, log10, pi, floor
import numpy as np
import sys
from intersections import intersection
"""
Calculates the fitness for positions in a room given a WiFi node placement
"""

class FitnessLandscape():
    def __init__(self, width, height, num_nodes, MAP_ARRAY, walls):
        # create np array that is size of room to store fitness values
        self.x = np.linspace(0, width-1, width, dtype = np.int16)
        self.y = np.linspace(0, width-1, width, dtype = np.int16)                            
        self.z = np.zeros((width, width))  # fitness value stored here
        self.num_nodes = num_nodes
        self.width = width
        self.height = height
        self.MAP_ARRAY = MAP_ARRAY
        self.walls = walls
        self.fitness = 0
        print("Num Nodes: ", self.num_nodes)

    def getAreaSum(self):
        area_sum = 0
        rows = self.z.shape[0]
        cols = self.z.shape[1]
        for x in range(0, cols - 1):
            for y in range(0, rows -1):
                area_sum += self.z[y][x]
        return area_sum

    def getFitness(self, x_values):
        self.z = np.zeros((self.width, self.height))  # fitness value stored here // reset
        for index in range(0, self.num_nodes):
            node_x = x_values[index*2]
            node_y = x_values[index*2+1]

            for x_point in self.x:
                for y_point in self.y:
                    # strength in dbm
                    strength = self.getStrength(node_x, node_y, x_point, y_point)
                    previous_strength = self.z[int(x_point)][int(y_point)]
                    if(strength > previous_strength or previous_strength == 0):
                        self.z[int(x_point)][int(y_point)] = strength
        fitness = -1 * self.getAreaSum()
        self.fitness = fitness
        return fitness
    
    def getZ(self):
        return self.z
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def check_pos(self, x_values):
        num_values = len(x_values)
        for index in range(0, num_values, 2):
            x_coord = x_values[index]
            y_coord = x_values[index + 1]
            if(self.MAP_ARRAY[int(x_coord)][int(y_coord)] == 0):
                return 0
        return 1

    def getStrength(self, x_node, y_node, x1, y1):
        #Signal strength loss equation with distance drop-off and walls (Kelly's paper)
        #Assume zero signal at walls
        #(x_node,y_node) = router location
        #(x1,y1) = pixel location
        ###freq = 2.4ghz

        #grocery store path loss exp
        L_exp = 1.8     #L_exp = path loss exponent (n)

        #Wall losses (NEED TO FIND GENERAL MODEL FOR FINDING WALL LOSS AT WIFI FREQS AND A WAY TO COUNT NO> OF EACH WALL TYPE)
        k_1 = 2         #k_i = no. of walls of type i
        k_2 = 3
        L_1 = 3.4       #L_i = Loss of wall type i
        L_2 = 6.9
        L0 = 40.04                  #L0 = path loss at 1m from router
        #r = 100                     #r = max. radius of router

        sig_stren_router = 23      #sig_stren_router = signal strength at the router (dB)
        n = 2
        num_walls = 0
        
        for wall in self.walls:
            if(intersection(wall[0], wall[1], [x_node,y_node], [x1, y1])):
                num_walls = num_walls + 1

        #dist = straight-line distance from router
        x_delta = x_node - x1
        y_delta = y_node - y1
        dist = sqrt((x_delta)**2 + (y_delta)**2)

        #sig_stren is the signal strength at pixel
        if dist == 0:
            sig_stren = sig_stren_router
        else:
            #sig_stren = sig_stren_router - (L0 + 20 * L_exp * log10(dist))
            sig_stren = sig_stren_router - (10 * n * log10(dist)) + 20 * log10(0.12) - 20 * log10(4*pi + num_walls*L_2)
        if sig_stren > 0: 
            sig_stren = 0

        # check for walls
        return sig_stren

