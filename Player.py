import math
from cmu_graphics import *

class Player:
    def __init__(self, x, y, isQuarterback=False, spritePath=None):
        self.x = x
        self.y = y
        self.isQuarterback = isQuarterback
        self.spritePath = spritePath
        self.rotation = 0
        self.speed = 2 if not isQuarterback else 3  # Defensive players are slower

    def moveTowards(self, targetX, targetY):
        dx = targetX - self.x
        dy = targetY - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:  # Prevent division by zero
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def rotateToFace(self, targetX, targetY):
        dx = targetX - self.x
        dy = targetY - self.y
        self.rotation = math.degrees(math.atan2(dy, dx))

    def draw(self, cameraX, cameraY, scaleFactor):
    
        if self.spritePath:
            drawImage(
                self.spritePath,
                (self.x - cameraX) * scaleFactor,
                (self.y - cameraY) * scaleFactor,
                width=40 * scaleFactor,
                height=40 * scaleFactor,
                rotateAngle=self.rotation
            )
    def moveForward(self):
        self.x += self.speed  # Simple forward movement

