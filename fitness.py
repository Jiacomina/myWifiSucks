from math import log, sqrt, log10, pi
import numpy as np
"""
Calculates the fitness for positions in a room given a WiFi node placement
"""


def getStrength(x_node, y_node, x1, y1):
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

    sig_stren_router = 23      #sig_stren_router = signal strength at the router (dB)
    L0 = 40.04                  #L0 = path loss at 1m from router
    #r = 100                     #r = max. radius of router
    n = 2
    #dist = straight-line distance from router
    dist = sqrt((x_node - x1)**2 + (y_node - y1)**2)

    #sig_stren is the signal strength at pixel
    if dist == 0:
        sig_stren = sig_stren_router
    else:
        #sig_stren = sig_stren_router - (L0 + 20 * L_exp * log10(dist))
        sig_stren = sig_stren_router - (10 * n * log10(dist)) + 20 * log10(0.12) - 20 * log10(4*pi)
    if sig_stren > 0: 
        sig_stren = 0
    return sig_stren

class FitnessLandscape():
    def __init__(self, width, height, num_nodes):
        
        # create np array that is size of room to store fitness values
        self.x = np.linspace(0, width, width+1, dtype = np.int16)
        self.y = np.linspace(0, width, width+1, dtype = np.int16)                            
        self.z = np.zeros((width+1, width+1))  # fitness value stored here
        self.num_nodes = num_nodes
        self.width = width
        self.height = height
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
        self.z = np.zeros((self.width+1, self.height+1))  # fitness value stored here // reset
        for index in range(0, self.num_nodes):
            node_x = x_values[index*2]
            node_y = x_values[index*2+1]
            #print("node_num: ",index, "node_x:", node_x, "node:y", node_y)

            for x_point in self.x:
                for y_point in self.y:
                    # strength in dbm
                    strength = getStrength(node_x, node_y, x_point, y_point)
                    previous_strength = self.z[int(x_point)][int(y_point)]
                    if(strength > previous_strength or previous_strength == 0):
                        self.z[int(x_point)][int(y_point)] = strength
        fitness = -1 * self.getAreaSum()
        #print("Fitness: ", fitness, "x_values: ", x_values)
        return fitness
    
    def getZ(self):
        return self.z
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

