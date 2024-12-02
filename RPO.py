import math

class RPO:
    def __init__(self, app):
        self.app = app  # Reference to the app for managing state and game objects

    def handleMouseDrag(self, mouseX, mouseY):
        if self.app.state == 'postSnap':
            # Calculate drag direction and power for visual feedback
            self.app.dragStartX = self.app.ball.positionX
            self.app.dragStartY = self.app.ball.positionY
            self.app.dragEndX = mouseX
            self.app.dragEndY = mouseY
            self.calculateTrajectory(mouseX, mouseY)

    def handleMouseRelease(self):
        if self.app.state == 'postSnap' and self.app.currentPlay == 'pass':
            # Calculate the direction and power of the throw
            dx = self.app.dragEndX - self.app.dragStartX
            dy = self.app.dragEndY - self.app.dragStartY
            distance = math.sqrt(dx ** 2 + dy ** 2)
            
            if distance > 0:  # Avoid division by zero
                power = min(10, distance / 50)  # Scale the power
                self.app.ball.throw(self.app.dragEndX, self.app.dragEndY, power=power)
                self.app.ball.holder = None  # Release the ball
                self.app.state = 'ballInMotion'  # Transition to ball motion state

    
    def calculateTrajectory(self, mouseX, mouseY):
        startX = self.app.ball.positionX
        startY = self.app.ball.positionY
        dx = mouseX - startX
        dy = mouseY - startY
        distance = math.sqrt(dx ** 2 + dy ** 2)
        power = min(10, distance / 50)  # Adjust power scaling
        velocityX = (dx / distance) * power
        velocityY = (dy / distance) * power

        # Simulate the trajectory for visual feedback
        trajectory = []
        x, y = startX, startY
        while y < 446:  # Ground level
            trajectory.append((x, y))
            x += velocityX
            y += velocityY
            velocityY += 0.5  # Gravity effect
        self.app.trajectoryDots = trajectory