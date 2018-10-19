"""
Reads in image from file name and returns as an array
"""
from sys import exit
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class FloorMap():
    """ room image map object """
    def __init__(self, file_name):
        self.file_name = file_name
        """Reads in image from file name and returns as an array"""
        img = Image.open(file_name).convert('L')
        print("Reading image: '" + file_name + "'")
        arr = np.array(img)
        (self.width, self.height) = arr.shape
        self.array = arr
        for x in range(0, self.width):
            for y in range(0, self.height):
                if(arr[x][y] not in [128, 0, 255]):
                    print("IMAGE CONTAINS INVALID VALUE", arr[x][y])
                    exit()

    def get_transparent_img(self):
        """ makes white image pixels transparent """
        img = Image.open(self.file_name).convert('RGBA')
        pixdata = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (255, 255, 255, 0)
        arr = np.array(img)
        return arr

    def get_walls(self):
        """ gets black pixel walls from image, stores in array 'walls'
            contains start and end point of all walls """
        print("Getting Walls")
        width = self.width
        height = self.height
        walls = []
        fig3, axis3 = plt.subplots()
        axis3.axis([0, height, 0, width])
        arr_copy = self.array
        for x in range(1, width-1):
            for y in range(1,height - 1):
                if(arr_copy[x][y]==0):
                    start = [x, y]
                    parse_y = y + 1
                    go_y = False
                    while(parse_y < height and arr_copy[x][parse_y] == 0):
                        go_y = True
                        arr_copy[x][parse_y] = 255
                        parse_y = parse_y+1
                    if go_y:
                        end = [x, parse_y - 1]
                        start[1] += -0.999999
                        end[1] += 0.99999999
                        walls.append([start, end])
                        axis3.plot([start[1], end[1]], [start[0], end[0]])
        for x in range(1, width-1):
            for y in range(1, height-1):
                if arr_copy[x][y] == 0:
                    start = [x, y]
                    parse_x = x + 1
                    go_x = False
                    while(parse_x < width and arr_copy[parse_x][y] == 0):
                        go_x = True
                        arr_copy[parse_x][y] = 255
                        parse_x = parse_x+1
                    if go_x:
                        end = [parse_x-1, y]
                        start[0] += -0.999999
                        end[0] += 0.99999999
                        walls.append([start, end])
                        axis3.plot([start[1], end[1]], [start[0], end[0]])
        plt.show()  
        return walls
