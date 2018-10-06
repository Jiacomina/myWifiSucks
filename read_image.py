from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def load_floor_plan(file_name):
    img = Image.open(file_name).convert('RGB')
    arr = np.array(img)
    print("Reading image: '" + file_name + "'")
    fig, ax = plt.subplots()
    plt.imshow(arr)
    plt.show()


