class Ball:
    def __init__(self, positionX, positionY, velocityX=0, velocityY=0, holder=None, radius=15):
        self.positionX = positionX
        self.positionY = positionY
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.holder = holder  # Determines if the ball is held by a player
        self.radius = radius

    def updatePosition(self, gameState):
        # Ball remains stationary in non-play states
        if gameState not in ['hiking', 'pass']:
            self.velocityX = 0
            self.velocityY = 0
            return

        # Apply velocity changes
        self.positionX += self.velocityX
        self.positionY += self.velocityY

        # Apply gravity if the ball is above the ground level
        if self.positionY + self.radius < 446:  # Ground level
            self.velocityY += 0.5  # Simulate gravity
        else:
            # Stop gravity and reset the ball to ground level
            self.velocityY = 0
            self.positionY = 446 - self.radius

    def reset(self, x, y):
        self.positionX = x
        self.positionY = y
        self.velocityX = 0
        self.velocityY = 0
        self.holder = None  # Ball is not held

    def throw(self, targetX, targetY, power=10):

        dx = targetX - self.positionX
        dy = targetY - self.positionY
        distance = (dx**2 + dy**2)**0.5
        self.velocityX = (dx / distance) * power
        self.velocityY = (dy / distance) * power

    def isHeld(self):

        return self.holder is not None
