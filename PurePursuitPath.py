from DiscretePath import DiscretePath
from PurePursuitGains import PurePursuitGains
import math
import copy

class PurePursuitPath:
    def __init__(self, path, gains):
        self.path = copy.deepcopy(path)
        self.velocity = []
        self.acceleration = []

        self.velocity.append(0)
        for i in range(1, len(path)-1):
            self.velocity.append(min(gains.maxVelocity, gains.maxAngularVelocity / path.getCurvature(i)))
        self.velocity.append(0)

        for i in range(len(self.velocity)-1, -1, -1):
            dist = self.path[i].distTo(self.path[i+1])
            self.velocity[i] = min(self.velocity[i], math.sqrt(self.velocity[i+1]*self.velocity[i+1] + 2 * gains.maxAcceleration * dist))
        

        for i in range(0, len(self.velocity)-1, 1):
            dist = self.path[i].distTo(self.path[i+1]);
            self.velocity[i+1] = min(self.velocity[i+1], math.sqrt(self.velocity[i]*self.velocity[i] + 2 * gains.maxAcceleration * dist));
            self.acceleration.emplace_back((self.velocity[i+1] * self.velocity[i+1] - self.velocity[i] * self.velocity[i]) / 2 / dist);

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