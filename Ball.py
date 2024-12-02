class Ball:
    def __init__(self, positionX, positionY, velocityX=0, velocityY=0, holder=None, radius=15):
        self.positionX = positionX
        self.positionY = positionY
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.holder = holder
        self.radius = radius
        self.inFlight = False
        self.beingDragged = False 

    def throw(self, targetX, targetY, power=10):
        self.velocityX = (targetX - self.positionX) * 0.1 
        self.velocityY = (targetY - self.positionY) * 0.1
        self.holder = None
        self.inFlight = True
        self.beingDragged = False

    def updatePosition(self, gameState):
        if self.holder is not None:
            self.positionX = self.holder.x
            self.positionY = self.holder.y
            return

        if self.inFlight and not self.beingDragged:
            self.positionX += self.velocityX
            self.positionY += self.velocityY
            self.velocityY += 0.5  
            if self.positionY + self.radius >= 446:
                self.positionY = 446 - self.radius
                self.velocityY = 0
                self.velocityX *= 0.8
                self.inFlight = False

    def canBeCaught(self, player):
        if not self.inFlight or self.beingDragged:
            return False
        dx = self.positionX - player.x
        dy = self.positionY - player.y
        distance = (dx**2 + dy**2)**0.5
        return distance < 50
    
    def reset(self, x, y):
        self.positionX = x
        self.positionY = y
        self.velocityX = 0
        self.velocityY = 0
        self.holder = None 