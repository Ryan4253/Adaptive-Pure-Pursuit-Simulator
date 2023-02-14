from re import S
import matplotlib.pyplot as plt
from SimplePath import SimplePath
from DiscretePath import DiscretePath
from Bezier import Bezier
from Point import Point
import math
from DifferentialDrive import DifferentialDrive
from PurePursuitGains import PurePursuitGains
from Pose import Pose
from AdaptivePurePursuitController import AdaptivePurePursuitController

path = Bezier([Bezier.Knot(0, 0, 0, 2), Bezier.Knot(4, 2, 0, 2)]).generate_by_length(0.5)
chassis = DifferentialDrive(Pose(0, 0, 0), 1, 3, 3)
gains = PurePursuitGains(3, 3, 1)
controller = AdaptivePurePursuitController(chassis, gains, 1)

controller.followPath(path)