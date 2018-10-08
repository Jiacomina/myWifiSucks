from PIL import Image
import numpy as np

# draws floor plans as 256 x 256 arrays then saves as png
# 0 = black, 255 = white

w, h = 256, 256
data = np.full((h, w), 255, dtype=np.uint8)

# wall thickness
wall = 5 

# room 1, just outer walls
data[:, w-wall:256] = 0
data[:, 0:wall] = 0
data[0:wall, :] = 0
data[h-wall:h, :] = 0
img = Image.fromarray(data, 'L') # L ---  black and white 0 = black 255 white 
img.save('wall1.png')

# room 2, one middle wall
data[:, 150:150+wall] = 0
img = Image.fromarray(data, 'L')
img.save('wall2.png')

# room 3, 2 cross middle walls
data[150:150+wall,:] = 0
img = Image.fromarray(data, 'L')
img.save('wall3.png')
img.show()