class PurePursuitGains:
    def __init__(self, maxVelocity, maxAcceleration, trackWidth):
        self.maxVelocity = maxVelocity
        self.maxAcceleration = maxAcceleration
        self.maxAngularVelocity = 2 * maxVelocity / trackWidth