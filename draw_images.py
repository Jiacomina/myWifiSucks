from PIL import Image
import numpy as np

# draws floor plans as 256 x 256 arrays then saves as png
# 0 = black, 255 = white

w, h = 100, 100
data = np.full((h, w), 255, dtype=np.uint8)

# wall thickness
wall = 1

def room1():
    # room 1, just outer walls
    data[:, w-wall:256] = 0
    data[:, 0:wall] = 0
    data[0:wall, :] = 0
    data[h-wall:h, :] = 0
    img = Image.fromarray(data, 'L') # L ---  black and white 0 = black 255 white 
    img.save('wall1small.png')

def room2():
    # room 2, one middle wall
    data[:, 40:40+wall] = 0
    img = Image.fromarray(data, 'L')
    img.save('wall2small.png')

def room3():
    # room 3, 2 cross middle walls
    data[:, 40:40+wall] = 0
    data[40:40+wall,:] = 0
    img = Image.fromarray(data, 'L')
    img.save('wall3small.png')
    img.show()

def room3gap():
    # room 3, 2 cross middle walls
    data[:, 40:40+wall] = 0
    data[40:40+wall,:] = 0
    data[:, 39] = 255
    img = Image.fromarray(data, 'L')
    img.save('wall3small.png')
    img.show()