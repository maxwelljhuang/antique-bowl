import math

class RPO:
    def __init__(self, app):
        self.app = app

    def handleMouseDrag(self, mouseX, mouseY):
        if self.app.state == 'postSnap':
            self.app.dragStartX = self.app.ball.positionX
            self.app.dragStartY = self.app.ball.positionY
            self.app.dragEndX = mouseX
            self.app.dragEndY = mouseY
            self.calculateTrajectory(mouseX, mouseY)

    def handleMouseRelease(self):
        if self.app.state == 'postSnap' and self.app.currentPlay == 'pass':
            #calculate direction and power of throw
            dx = self.app.dragEndX - self.app.dragStartX
            dy = self.app.dragEndY - self.app.dragStartY
            distance = math.sqrt(dx ** 2 + dy ** 2)
            
            if distance > 0:  
                power = min(10, distance / 50)  
                self.app.ball.throw(self.app.dragEndX, self.app.dragEndY, power=power)
                self.app.ball.holder = None  
                self.app.state = 'ballInMotion'  

    
    def calculateTrajectory(self, mouseX, mouseY):
        startX = self.app.ball.positionX
        startY = self.app.ball.positionY
        dx = mouseX - startX
        dy = mouseY - startY
        distance = math.sqrt(dx ** 2 + dy ** 2)
        power = min(10, distance / 50)  
        velocityX = (dx / distance) * power
        velocityY = (dy / distance) * power

        #trajectory simulation
        trajectory = []
        x, y = startX, startY
        #ground level
        while y < 446: 
            trajectory.append((x, y))
            x += velocityX
            y += velocityY
            #add gravity
            velocityY += 0.5  
        self.app.trajectoryDots = trajectory