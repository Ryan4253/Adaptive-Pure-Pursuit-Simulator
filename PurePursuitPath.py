from DiscretePath import DiscretePath
from PurePursuitGains import PurePursuitGains
import math
import copy
import matplotlib.pyplot as plt

class PurePursuitPath:
    def __init__(self, path, gains):
        self.path = copy.deepcopy(path)
        self.velocity = []
        self.acceleration = []

        self.velocity.append(0)
        for i in range(1, path.size()-1):
            self.velocity.append(min(gains.maxVelocity, gains.maxAngularVelocity / path.getCurvature(i)))
        self.velocity.append(0)

        for i in range(len(self.velocity)-2, -1, -1):
            dist = self.path[i].distTo(self.path[i+1])
            self.velocity[i] = min(self.velocity[i], math.sqrt(self.velocity[i+1]*self.velocity[i+1] + 2 * gains.maxAcceleration * dist))
        

        for i in range(0, len(self.velocity)-1, 1):
            dist = self.path[i].distTo(self.path[i+1]);
            self.velocity[i+1] = min(self.velocity[i+1], math.sqrt(self.velocity[i]*self.velocity[i] + 2 * gains.maxAcceleration * dist));
            self.acceleration.append((self.velocity[i+1] * self.velocity[i+1] - self.velocity[i] * self.velocity[i]) / 2 / dist);

        self.acceleration.append(0)
        self.acceleration[0] = 0
        self.velocity[0] = self.velocity[1]

    def size(self):
        return self.path.size()
    
    def __getitem__(self, index):
        return self.path[index]
    
    def getPoint(self, index):
        return self[index]

    def getVelocity(self, index):
        return self.velocity[index]
    
    def getAcceleration(self, index):
        return self.acceleration[index]
    
    def getCurvature(self, index):
        return self.path.getCurvature(index)

    def draw(self):
        x = []
        y = []
        for i in range(self.path.size()):
            x.append(self.path[i].x)
            y.append(self.path[i].y)

        plt.plot(x, y)
