#https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/

import math

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

def ccw(A,B,C):
	return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

def intersection(A1, A2, B1, B2):
    A = Point(A1[0], A1[1])
    B = Point(A2[0], A2[1])
    C = Point(B1[0], B1[1])
    D = Point(B2[0], B2[1])
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
