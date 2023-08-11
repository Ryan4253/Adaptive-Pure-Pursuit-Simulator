import math
import time
from Point import circleLineIntersection
from Pose import curvatureToReachPoint
from PurePursuitPath import PurePursuitPath
from DiscretePath import closestPoint
from Math import wheelInverseKinematics
import matplotlib.pyplot as plt

class AdaptivePurePursuitController:
    def __init__(self, chassis, gains, lookAhead):
        self.chassis = chassis
        self.gains = gains
        self.lookAhead = lookAhead
    
    def setGains(self, gains):
        self.gains = gains

    def setLookAhead(self, lookAhead):
        self.lookAhead = lookAhead
            
    def getLookAheadPoint(self, path, minIndex, position):
        for i in range(int(minIndex[0]), path.size()-1):
            start = path[i]
            end = path[i+1]

            t = circleLineIntersection(start, end, position, self.lookAhead)

            if(t and i+t > minIndex[0]):
                minIndex[0] = i+t
                return start + (end - start) * t
            
        return None
     
    def followPath(self, path, reversed =  False, visualize = True):
        ppPath = PurePursuitPath(path, self.gains)
        closestPointIndex = 0
        lookaheadPointT = [0]
        lookAheadPoint = path[0]

        while(closestPointIndex is not path.size()-1):
            pos = self.chassis.getState()
            closestPointIndex = closestPoint(path, closestPointIndex, path.size(), pos.translation)
            lookAheadCandidate = self.getLookAheadPoint(path, lookaheadPointT, pos.translation)
            lookAheadPoint = lookAheadCandidate if lookAheadCandidate is not None else lookAheadPoint
            
            curvature = curvatureToReachPoint(pos, lookAheadPoint)
            velocity = ppPath.getVelocity(closestPointIndex)
            acceleration = ppPath.getAcceleration(closestPointIndex)

            if reversed:
                velocity *= -1
                acceleration *= -1

            vl, vr = wheelInverseKinematics(velocity, curvature, self.chassis.trackWidth)
            al, ar = wheelInverseKinematics(acceleration, curvature, self.chassis.trackWidth) 

            self.chassis.setAccel(al, ar) 
            self.chassis.setVel(vl, vr)
            self.chassis.move(0.01)

            # visualize
            plt.clf()
            plt.title("Adaptive Pure Pursuit")
            plt.xlabel('x (feet)')
            plt.ylabel('y (feet)')
            plt.gca().set_aspect('equal', adjustable='box')
            path.draw()
            plt.plot(pos.translation.x, pos.translation.y, 'ro')
            plt.plot(lookAheadPoint.x, lookAheadPoint.y, 'go')
            plt.pause(0.01)

                    