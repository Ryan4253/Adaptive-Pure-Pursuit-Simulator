from Rotation import Rotation
import math
import copy

class Point:
    def __init__(self, a, b = None):
        if(isinstance(a, Point)):
            self.x = copy.deepcopy(a.x)
            self.y = copy.deepcopy(a.y)

        elif(isinstance(b, Rotation)):
            self.x = a * b.cosine
            self.y = a * b.sine
        else:
            self.x = copy.deepcopy(a)
            self.y = copy.deepcopy(b)

    def __add__(self, rhs):
        return Point(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return self + (-rhs)

    def __mul__(self, scalar):
        if(isinstance(scalar, Point)):
            return self.x * scalar.x + self.y * scalar.y
        return Point(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq___(self, rhs):
        return self.x == rhs.x and self.y == rhs.Y

    def __ne__(self, rhs):
        return not(self == rhs)

    def distTo(self, rhs):
        return math.sqrt((self.x - rhs.x)**2 + (self.y - rhs.y)**2)

    def angleTo(self, rhs):
        return math.atan2(self.x - rhs.x, self.y - rhs.y)

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def norm(self):
        return Point(self.x / self.mag(), self.y / self.mag())

    def rotateBy(self, rhs):
        return Point(self.x * rhs.cosine - self.y * rhs.sine, self.x * rhs.sine + self.y * rhs.cosine)
    
def circumradius(A, B, C):
    a = B.distTo(C)
    b = C.distTo(A)
    c = A.distTo(B)

    a2 = a**2
    b2 = b**2
    c2 = c**2

    pa = A * (a2 * (b2 + c2 - a2) / ((b+c)*(b+c)-a2) / (a2-(b-c)*(b-c)))
    pb = B * (b2 * (a2 + c2 - b2) / ((a+c)*(a+c)-b2) / (b2-(a-c)*(a-c)))
    pc = C * (c2 * (a2 + b2 - c2) / ((a+b)*(a+b)-c2) / (c2-(a-b)*(a-b)))

    center = pa + pb + pc

    return center.distTo(A)

def circleLineIntersection(start, end, pos, radius):
    d = end - start
    f = start - pos

    a = d * d
    b = 2 * (f * d)
    c = f * f - radius * radius
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