import math
import time
from Point import Point
from DifferentialDrive import DifferentialDrive
from PurePursuitPath import PurePursuitPath
from PurePursuitGains import PurePursuitGains

class AdaptivePurePursuitController:
    def __init__(self, chassis, gains, lookAhead):
        self.chassis = chassis
        self.gains = gains
        self.lookAhead = lookAhead

        self.isReversed = False
        self.path = None
        self.isSettled = True

        self.prevClosest = None
        self.prevLookAheadIndex = 0
        self.prevLookAheadT = 0


    def initialize(self):
        self.settled = False
        self.prevClosest = None
        self.prevLookAheadIndex = 0
        self.prevLookAheadT = 0

    def followPath(self, path):
        self.initialize()
        self.path = PurePursuitPath(path, self.gains)
    
    def setGains(self, gains):
        self.gains = gains

    def setLookAhead(self, lookAhead):
        self.lookAhead = lookAhead

    def getT(self, start, end, pos):
        d = end - start
        f = start - pos.translation

        a = d * d
        b = 2 * (f * d)
        c = f * f - self.lookAhead * self.lookAhead
        discriminant = b * b - 4 * a * c

        if discriminant > 0:
            dis = math.sqrt(discriminant)
            t1 = ((-b - dis) / (2 * a))
            t2 = ((-b + dis) / (2 * a))

            if t2 >= 0 and t2 <= 1:
                return t2
            
            elif t1 >= 0 and t1 <= 1:
                return t1

        return None

    def getClosestPoint(self, currentPos):
        minDist = 10000000
        closest = 0 if prevClosest == None else 0

        for i in range(self.path.size()):
            dist = currentPos.translation.distTo(self.ath.getPoint(i))
            if(dist < minDist):
                minDist = dist
                closest = i
            
        

        prevClosest = closest
        return closest
            
    def getLookAheadPoint(self, currentPos):
        closestIndex = 0 if self.prevClosest == 0 else None


        for i in range(math.max(closestIndex, self.prevLookAheadIndex), self.path.size()-1):
            start = self.path.getPoint(i)
            end = self.path.getPoint(i+1)

            t = self.getT(start, end, currentPos)

            if(t != None):
                if(i > self.prevLookAheadIndex or t > self.prevLookAheadT):
                    self.prevLookAheadIndex = i
                    self.prevLookAheadT = t
                    break
            
        return self.path[self.prevLookAheadIndex] + (self.path[self.prevLookAheadIndex+1] - self.path[self.prevLookAheadIndex]) * self.prevLookAheadT
    
    def calcCurvature(self, iPos, lookAheadPt):
        a = -math.tan(iPos.Theta())
        b = 1
        c = math.tan(iPos.Theta())*iPos.X() - iPos.Y()

        x = abs(lookAheadPt.X() * a + lookAheadPt.Y() * b + c) / math.sqrt(a * a + b * b)
        sideL = math.sin(iPos.Theta()) * (lookAheadPt.X() - iPos.X()) - math.cos(iPos.Theta()) * (lookAheadPt.Y() - iPos.Y())
        side = sideL / abs(sideL)

        if(sideL == 0):
            return 0
        
        return (2 * x) / (self.lookAhead * self.lookAhead) * side

    def calcVelocity(self, iCurvature, iClosestPt):
        vel =  -self.path.getVelocity(iClosestPt) if self.isReversed else self.path.getVelocity(iClosestPt)
        vl = vel * (2+iCurvature*self.chassis.wheelTrack) / 2
        vr = vel * (2-iCurvature*self.chassis.wheelTrack) / 2

        if(self.isReversed):
            return (vr, vl)
        
        else:
            return (vl, vr)
    
    def calcAcceleration(self, iCurvature, iClosestPt):
        accel = -self.path.getAcceleration(iClosestPt) if self.isReversed else self.path.getAcceleration(iClosestPt)
        al = accel * (2 + iCurvature * self.chassis.wheelTrack) / 2
        ar = accel * (2 - iCurvature * self.chassis.wheelTrack) / 2

        if(self.isReversed):
            return (ar, al)
        else:
            return (al, ar)
        
    def isSettled(self):
        return self.settled

    def waitUntilSettled(self):
        while not self.settled:
            time.sleep(0.01)
        
    def loop(self):
        while(True):
            pos = self.chassis.getState()
            closest = self.getClosestPoint(pos)
            lookAheadPt = self.getLookAheadPoint(pos)

            projectedLookAheadPt = pos.translation + Point((lookAheadPt-pos.getTranslation()).norm() * self.lookAhead)
            curvature = self.calcCurvature(pos, projectedLookAheadPt)

            targetVel = self.calcVelocity(curvature, closest)
            targetAccel = self.calcAcceleration(curvature, closest)

            self.chassis.setAcceleration(targetAccel[0], targetAccel[1])
            self.chassis.setVelocity(targetVel[0], targetVel[1])

            endInLook = False
            endInPath = False
        
            if endInLook and endInPath:
                self.settled = False
                    