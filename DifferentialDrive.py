import pygame
import math
import time
import pygame
from threading import Thread, Lock
from Bezier import Bezier
from Pose import Pose
from Rotation import Rotation
from DiscretePath import DiscretePath


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
        self.dt = 0
        self.lastTime = 0

        self.mutex = Lock()

    def getState(self):
        self.mutex.acquire()
        ret = self.pose
        self.mutex.release()
        return ret

    def getLeftVel(self):
        self.mutex.acquire()
        ret = self.pose.vl
        self.mutex.release()
        return ret
    
    def getRightVel(self):
        self.mutex.acquire()
        ret = self.pose.vr
        self.mutex.release()
        return ret
    
    def getLeftAccel(self):
        self.mutex.acquire()
        ret = self.pose.al
        self.mutex.release()
        return ret

    def getRightAccel(self):
        self.mutex.acquire()
        ret = self.pose.ar
        self.mutex.release()
        return ret

    def setVel(self, vl, vr):
        self.mutex.acquire()
        self.vl = vl
        self.vr = vr
        self.mutex.release()

    def setAccel(self, al, ar):
        self.mutex.acquire()
        self.al = al
        self.ar = ar
        self.mutex.release()

    def move(self):
        self.mutex.acquire()
        self.dt = (pygame.time.get_ticks()-self.lastTime) / 1000
        self.lastTime = pygame.time.get_ticks()
        self.vl += 0.5 * self.al * self.dt
        self.vr += 0.5 * self.ar * self.dt
        self.pose.point.x += (self.vl + self.vr) / 2 * math.cos(self.pose.Theta()) * (self.dt)
        self.pose.point.y -= (self.vl + self.vr) / 2 * math.sin(self.pose.Theta()) * (self.dt)
        self.pose.rotation.theta += (self.vl - self.vr) / self.trackWidth * (self.dt)
        self.vl += 0.5 * self.al * self.dt
        self.vr += 0.5 * self.ar * self.dt
        self.mutex.release()

    def render(self, map):
        self.field.blit(self.rotated, self.rect)

class ChassisRenderer:
    def __init__(self, chassis, field, image):
        self.chassis = chassis
        self.img = pygame.image.load(image)
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center = (self.chassis.getState().X(), self.chassis.getState().Y()))
        self.map = field

    def render(self):
        pos = self.chassis.getState()
        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(pos.Theta()), 1)
        self.rect = self.rotated.get_rect(center = (pos.X(), pos.Y()))
        self.map.blit(self.rotated, self.rect)


class Envir:
    def __init__(self, width, height):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)


        self.width = width
        self.height = height

        pygame.display.set_caption("Differential Drive Simulator")
        self.map = pygame.display.set_mode((self.width, self.height))

def drawPath(map, color, path):
    for i in range(1, path.size()):
        pygame.draw.line(map, color, (path[i-1].x, path[i-1].y), (path[i].x, path[i].y))

pygame.init()
running = True

environment = Envir(1920, 1080)
robot = DifferentialDrive(Pose(400, 300, Rotation(0)), 100, 500, 500)
renderer = ChassisRenderer(robot, environment.map, r"/home/ryan/Documents/Pure-Pursuit-Simulator/SpeVm6L.png")
path = Bezier([Bezier.Knot(100, 100, 0, 300), Bezier.Knot(1200, 600, 0, 300)]).generate_by_length(10)

while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
    drawPath(environment.map, environment.red, path)
    robot.move()
    renderer.render()
    pygame.display.update()
    environment.map.fill(environment.black)
    time.sleep(0.01)


