MyWifiSucks is a program that predicts the best location of wifi nodes within a floor or room map. 
Optimal locations are found using Particle Swarm Optimization. 
Floor maps can be read in as an image file.

Running the program
There are several different python scripts available to use:

main.py: Generates a solution from an image
* python main.py <image_file.py>

main_with_parameters.py: Generates paramater testing data for a provided image
* python main_with_parameters.py <image_file.py>

brute_force.py: Generates a brute force solution from an image
* python brute_force.py <image_file.py>

Input Image Array Specifications (as an Integer):
* 0 - Wall
* 255 - Free Space
* 128 - No go Zone (grey)
* 149 - Green
* 76 - Red

Requirements:
- matplotlib
- numpy
- pyswarm
- Python image library


Credit:
* Uses Pyswarm library (included localy)
* Uses Intersections python script taken from: https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
