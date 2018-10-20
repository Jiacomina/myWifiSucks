"""
Creates a fitness landscape or map.
Can calculate the room fitness according to given node positions
"""
from math import sqrt, log10, pi
import numpy as np
from intersections import intersection

class FitnessLandscape():
    """
    Fitness Landscape object containing wall and map data
    Scale: Image scaling factor. 
        Each pixel by default is 1m wide, for scale = 2. each pixel will be 2m wide
    Walls: Array containg start and end points for each wall in the room map
    Map_array: array of values dictating room specifications where:
        0: wall
        255: free space
        128: no go zone
    """
    def __init__(self, width, height, num_nodes, map_array, walls, scale):
        # create np array that is size of room to store fitness values
        self.x = np.linspace(0, width-1, width, dtype=np.int16)
        self.y = np.linspace(0, height-1, height, dtype=np.int16)
        self.z = np.zeros((width, height))  # fitness value stored here
        self.num_nodes = num_nodes
        self.width = width
        self.height = height
        self.map_array = map_array
        print(map_array)
        self.walls = walls
        self.scale = scale
        self.minStrength = -50
        print("Num Nodes: ", self.num_nodes)
        print("Scale: ", self.scale)

    def getAreaSum(self):
        """ Calculates and returns the sum of fitness for all cells in the map"""
        area_sum = 0
        rows = self.z.shape[0]
        cols = self.z.shape[1]
        for x in range(0, rows - 1):
            for y in range(0, cols -1):
                priority_multi = self.priority_multiplier(x, y)
                area_sum += self.z[x][y]*priority_multi
        return area_sum

    def getFitness(self, x_values):
        """ For given number of nodes and node positions,
            iterates through each node and each cell in the map.
            Calculates fitness at each cell.
            cells store the highest fitness generated by any of the nodes """
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

        return fitness

    def priority_multiplier(self, x_coord, y_coord):
        ''' Returns the mupltiplying factor for priorities. 
        Because pyswarm MINIMISES the fitness, higher priority should produce lower fitness.
        Therefore first priority (green pixels) returns a multiplying factor of 1/3 and
        second priority (red pixels) returns a multiplying factor of 2/3. 
        The default multiplier (white pixels) is 1'''
        pixel_value = self.map_array[x_coord][y_coord]
        if pixel_value == 255 or pixel_value == 0:
            return 1
        if pixel_value == 79:  # SECOND PRIORITY = RED
            return 2/3
        if pixel_value == 149:  # FIRST PRIORITY = GREEN
            return 1/3
        else:
            print("Image pixel has unknown value: ", pixel_value)
            exit()

    def check_pos(self, x_values):
        """ checks if array x_values contains valid room positions.
        Returns 1 if position is on a wall, or if it is a 'no-go' zone. """
        num_values = len(x_values)
        x_values = (np.rint(x_values))
        x_values = x_values.astype(int)
        for index in range(0, num_values, 2):
            x_coord = x_values[index]
            y_coord = x_values[index + 1]
            maxWidth = self.width - 1
            maxHeight = self.height - 1
            if x_coord == 0 or y_coord == 0:
                # print(x_coord, y_coord, " On edge 0")
                return np.full(num_values, -1)
            elif (x_coord == maxWidth or y_coord == maxWidth) or (x_coord == maxHeight or y_coord == maxHeight):
                # print(x_coord, y_coord, " On edge max")
                return np.full(num_values, -1)
            elif self.map_array[x_coord][y_coord] == 0:  # is a wall
                # print(x_coord, y_coord, " is a wall")
                return np.full(num_values, -1)
            elif self.map_array[x_coord][y_coord] == 128:  # is no go zone
                # print(x_coord, y_coord, " is in no go zone")
                return np.full(num_values, -2)
        return np.full(num_values, 1)

    def getStrength(self, x_node, y_node, X1, Y1):
        """Signal strength loss equation with distance drop-off and walls (Kelly's paper)
        Assume zero signal at walls
        (x_node,y_node) = router location
        (X1,Y1) = pixel location
        freq = 2.4ghz"""

        #grocery store path loss exp
        # L_exp = 1.8     #L_exp = path loss exponent (n)

        # #Wall losses
        # k_1 = 2         #k_i = no. of walls of type i
        # k_2 = 3
        # L_1 = 3.4       #L_i = Loss of wall type i
        L_2 = 6.9
        # L0 = 40.04                  #L0 = path loss at 1m from router
        # #r = 100                     #r = max. radius of router

        sig_stren_router = 23      #sig_stren_router = signal strength at the router (dB)
        n = 2
        num_walls = 0

        for wall in self.walls:
            if intersection(wall[0], wall[1], [x_node, y_node], [X1, Y1]):
                num_walls = num_walls + 1

        #dist = straight-line distance from router.
        # Multiply by room mesurement scale factor
        # (so that image file can be small whilst still getting large maps)
        x_delta = (x_node - X1)*self.scale
        y_delta = (y_node - Y1)*self.scale
        dist = sqrt((x_delta)**2 + (y_delta)**2)
        #sig_stren is the signal strength at pixel
        if dist == 0:
            sig_stren = sig_stren_router
        else:
            #sig_stren = sig_stren_router - (L0 + 20 * L_exp * log10(dist))  num_walls*L_2)
            path_loss = -(10 * n * log10(dist)) + (20 * log10(0.12)) - (20 * log10(4*pi)) - num_walls*L_2
            sig_stren = sig_stren_router + path_loss
        # if sig_stren > 0:
        #     sig_stren = 0
        # check for walls
        if sig_stren < self.minStrength:
            self.minStrength = sig_stren
        return sig_stren
