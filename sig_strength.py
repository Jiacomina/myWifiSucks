import math
#Signal strength loss equation with distance drop-off and walls (Kelly's paper)

#Assume zero signal at walls

#sig_stren_router = signal strength at the router (dB)
#sig_stren = signal strength at pixel
#L0 = path loss at 1m from router
#dist = straight-line distance from router
#L_exp = path loss exponent (n)
#L_i = Loss of wall type i
#k_i = no. of walls of type i

#r = max. radius of router
#(x_node,y_node) = router location
#(x1,y1) = pixel location

sig_stren_router = 20

#grocery store path loss exp
L_exp = 1.8

#Wall losses (NEED TO FIND GENERAL MODEL FOR FINDING WALL LOSS AT WIFI FREQS AND A WAY TO COUNT NO> OF EACH WALL TYPE)
k_1 = 2
k_2 = 3
L_1 = 3.4
L_2 = 6.9

dist = math.sqrt((x_node - x1)**2 + (y_node - y1)**2)

if dist > r:
	sig_stren = 0
else:
	sig_stren = sig_stren_router - (19.7 + 10**L_exp**log(dist) + k_1**L_1 + k_2**L_2)