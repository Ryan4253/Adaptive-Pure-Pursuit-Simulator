def wheelInverseKinematics(kinematics, curvature, trackWidth):
    left = kinematics * (2 + curvature * trackWidth) / 2
    right = kinematics * (2 - curvature * trackWidth) / 2
    return (left, right)
