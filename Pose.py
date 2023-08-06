from Rotation import Rotation
from Point import Point
import copy
import math

class Pose: 

    def __init__(self, a, b = None, c = None):
        if(isinstance(a, Pose)):
            self.translation = copy.deepcopy(a.point)
            self.rotation = copy.deepcopy(a.rotation)

        elif(isinstance(b, Rotation)):
            self.translation = copy.deepcopy(a)
            self.rotation = copy.deepcopy(b)
            
        else:
            self.translation = Point(a, b)
            self.rotation = Rotation(copy.deepcopy(c))

    def X(self):
        return self.translation.x

    def Y(self):
        return self.translation.y

    def Theta(self):
        return self.rotation.theta

    def __eq__(self, rhs):
        return self.translation == rhs.translation and self.rotation == rhs.rotation

    def __ne__(self, rhs):
        return not(self == rhs)
    
def curvatureToReachPoint(position : Pose, point : Point):
    a = -math.tan(position.Theta())
    b = 1
    c = math.tan(position.Theta())*position.X() - position.Y()

    x = abs(point.x * a + point.y * b + c) / math.sqrt(a * a + b * b)
    sideL = math.sin(position.Theta()) * (point.x - position.X()) - math.cos(position.Theta()) * (point.y - position.Y())
    side = sideL / abs(sideL)
    chord = position.translation.distTo(point)

    if(sideL == 0):
        return 0

    return (2 * x) / (chord * chord) * side