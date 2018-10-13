"""
Reads in image from file name and returns as an array
"""
from PIL import Image
import numpy as np

class FloorMap():
    def __init__(self, file_name):
        self.file_name = file_name
        """Reads in image from file name and returns as an array"""
        img = Image.open(file_name).convert('L')
        print("Reading image: '" + file_name + "'")
        arr = np.array(img)
        (self.width, self.height) = arr.shape
        self.array = arr

    def get_array(self):
        return self.array

    def get_transparent_img(self):
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
        print("Getting Walls")
        width = self.width
        #walls = [[[0,0],[width,0]], [[0,0],[0,width]],[[0,width],[width,width]],[[width,0],[width,width]]]
        walls = []
        for x in range(1, width-1):
            for y in range(1, width-1):
                arr_copy = self.array
                if(arr_copy[x][y] == 0):
                    start = [x,y]
                    parse_x = x + 1
                    go_x = False
                    while(parse_x < width and arr_copy[parse_x][y] == 0):
                        go_x = True
                        arr_copy[parse_x][y] = 255
                        parse_x = parse_x+1
                    if(go_x):
                        end = [parse_x-1,y]
                        walls.append([start, end])
                    
                    parse_y = y + 1
                    go_y = False
                    while(parse_y < width and arr_copy[x][parse_y] == 0):
                        go_y = True
                        arr_copy[x][parse_y] = 255
                        parse_y = parse_y+1
                    if(go_y):
                        end = [x,parse_y - 1]
                        walls.append([start, end])
        return walls