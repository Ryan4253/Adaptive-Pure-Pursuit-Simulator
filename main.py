from re import S
import matplotlib.pyplot as plt
from SimplePath import SimplePath
from DiscretePath import DiscretePath
from Bezier import Bezier
from Point import Point
import math

def test():
    #a = SimplePath([Point(0, 0), Point(4, 4), Point(8, 4)]).generate_by_length(0.25).smoothen(0.8, 0.001)
    a = Bezier([Bezier.Knot(0, 0, 0, 2), Bezier.Knot(4, 2, 0, 2)]).generate_by_length(0.5)
    #
    #, Bezier.Knot(6, 0, -math.pi/2, 2), Bezier.Knot(3, -2, 5 * math.pi/4), Bezier.Knot(1, -4, -math.pi), Bezier.Knot(0, 0, math.pi/2)
    #for i in range(len(a.p1)):
        #print(a.c2[i].x, a.c2[i].y)

    plt.xlabel('x (feet)')
    plt.ylabel('y (feet)')
    x = []
    y = []
    for i in range(a.size()):
        x.append(a[i].x)
        y.append(a[i].y)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot(x, y, 'bo')
    #plt.show()

test()