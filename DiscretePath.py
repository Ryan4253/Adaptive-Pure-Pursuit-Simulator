from Point import circumradius
import matplotlib.pyplot as plt
import math
import copy

class DiscretePath:
    def __init__(self, waypoint):
        self.path = copy.deepcopy(waypoint)

    def __add__(self, rhs):
        ret = DiscretePath(self.path)
        if(isinstance(rhs, DiscretePath)):
            for point in rhs.path:
                ret.append(point)
        else:
            ret.append(rhs)
        
        return ret
    
    def __iadd__(self, rhs):
        if(isinstance(rhs, DiscretePath)):
            for point in rhs.path:
                self.path.append(point)
        else:
            self.path.append(rhs)
        
        return self

    def __getitem__(self, i):
        i = max(min(i,len(self.path)-1), 0)
        return self.path[i]

    def size(self):
        return len(self.path)
    
    def getCurvature(self, i):
        if i <= 0 or i > self.size():
            return 0.0

        radius = circumradius(self.path[i-1], self.path[i], self.path[i+1])

        if(math.isnan(radius)):
            return 0.0

        return 1 / radius

    def print(self):
        for point in self.path:
            print("[", point.x, " ", point.y, "]")

    def draw(self):
        x = []
        y = []
        for i in range(len(self.path)):
            x.append(self.path[i].x)
            y.append(self.path[i].y)

        plt.plot(x, y)

def closestPoint(path, begin, end, point):
    minDist = 10000000
    closest = begin

    for i in range(begin, end):
        dist = point.distTo(path[i])
        if(dist < minDist):
            minDist = dist
            closest = i
        
    return closest