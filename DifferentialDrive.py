import math

class DifferentialDrive:
    def __init__(self, startPos, trackWidth, maxVel, maxAccel):
        self.pose = startPos
        self.trackWidth = trackWidth
        self.vl = -500
        self.vr = 500
        self.al = 100
        self.ar = 100
        self.maxVel = maxVel
        self.maxAccel = maxAccel

    def getState(self):
        return self.pose

    def getLeftVel(self):
        return self.vl
    
    def getRightVel(self):
        return self.vr
    
    def getLeftAccel(self):
        return self.al

    def getRightAccel(self):
        return self.ar

    def setVel(self, vl, vr):
        self.vl = vl
        self.vr = vr

    def setAccel(self, al, ar):
        self.al = al
        self.ar = ar

    def move(self, dt):
        self.vl += 0.5 * self.al * dt
        self.vr += 0.5 * self.ar * dt
        self.pose.point.x += (self.vl + self.vr) / 2 * math.cos(self.pose.Theta()) * (dt)
        self.pose.point.y -= (self.vl + self.vr) / 2 * math.sin(self.pose.Theta()) * (dt)
        self.pose.rotation.theta += (self.vl - self.vr) / self.trackWidth * (dt)
        self.vl += 0.5 * self.al * dt
        self.vr += 0.5 * self.ar * dt