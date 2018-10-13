"""
Reads in image from file name and returns as an array
"""
from PIL import Image
import numpy as np

def load_floor_plan(file_name):
    """Reads in image from file name and returns as an array"""
    img = Image.open(file_name).convert('L')
    img = img.convert('RGBA')

    pixdata = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)

    arr = np.array(img)
    img.save("transparent.png")
    print("Reading image: '" + file_name + "'")
    return arr
