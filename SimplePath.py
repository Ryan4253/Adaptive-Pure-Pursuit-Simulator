from DiscretePath import DiscretePath
import copy
import math

class SimplePath:
    def __init__(self, waypoint):
        self.waypoint = copy.deepcopy(waypoint)
    
    def generate_by_size(self, step, end = True):
        path = [];
        for i in range(0, len(self.waypoint)-1):
            diff = self.waypoint[i+1]-self.waypoint[i];
            inc = diff / step;

            for j in range(0, step):
                path.append(self.waypoint[i] + inc * j)
            
        if len(self.waypoint) != 0 and end:
            path.append(self.waypoint[len(self.waypoint)-1])

        self.waypoint = copy.deepcopy(path);

        return self;

    def generate_by_length(self, length, end = True):
        path = [];
        for i in range(0, len(self.waypoint)-1):
            step = math.ceil((self.waypoint[i].distTo(self.waypoint[i+1]) / length)); 
            diff = self.waypoint[i+1]-self.waypoint[i];
            inc = diff/step;

            for j in range(0, step):
                path.append(self.waypoint[i] + inc*j)
            
        if len(self.waypoint) != 0 and end:
            path.append(self.waypoint[len(self.waypoint)-1])

        self.waypoint = copy.deepcopy(path);

        return self;

    def smoothen(self, smoothWeight, tolerance):
        change = tolerance;
        newPath = copy.deepcopy(self.waypoint)
        a = 1-smoothWeight
        b = smoothWeight;
        number = 0
        while change >= tolerance :
            number+=1
            change = 0;
            for i in range(1, len(self.waypoint)-1) : 
                aux = copy.deepcopy(newPath[i]);

                newPath[i].x = ((newPath[i].x + a * (self.waypoint[i].x - newPath[i].x) + 
                                b * (newPath[i-1].x + newPath[i+1].x - (2.0 * newPath[i].x))))
                newPath[i].y = ((newPath[i].y + a * (self.waypoint[i].y - newPath[i].y) + 
                                b * (newPath[i-1].y + newPath[i+1].y - (2.0 * newPath[i].y))))

                change += abs(aux.x + aux.y - newPath[i].x - newPath[i].y);
        print(number)
        return DiscretePath(newPath);

    def noSmoothen(self):
        return DiscretePath(self.waypoint);