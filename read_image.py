"""
Reads in image from file name and returns as an array
"""
from PIL import Image
import numpy as np

def load_floor_plan(file_name):
    """Reads in image from file name and returns as an array"""
    img = Image.open(file_name).convert('RGB')
    arr = np.array(img)
    print("Reading image: '" + file_name + "'")
    return arr
