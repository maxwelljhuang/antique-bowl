class Ball:
    def __init__(self, positionX, positionY, velocityX, velocityY, holder):
        self.positionX = positionX
        self.positionY = positionY
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.holder = holder  # The player holding the ball

    def updatePosition(self):
        """
        Updates the ball's position based on its velocity.
        """
        self.positionX += self.velocityX
        self.positionY += self.velocityY
