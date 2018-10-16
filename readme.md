MyWifiSucks is a program that predicts the best location of wifi nodes within a floor or room map. 
Optimal locations are found using Particle Swarm Optimization. 
Floor maps can be read in as an image file.

Input Image Array Specifications:
* 0 - Wall
* 255 - Free Space
* 128 - No go Zone

Requirements:
- matplotlib
- numpy

Credit:
* Uses Pyswarm library (included localy)
* Uses Intersections python script taken from: https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
