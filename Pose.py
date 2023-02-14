from Rotation import Rotation
from Point import Point
import copy

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