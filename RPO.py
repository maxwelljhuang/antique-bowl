import math

class RPO:
    def __init__(self, app):
        self.app = app  # Reference to the app for managing state and game objects

    def handleMouseDrag(self, mouseX, mouseY):
        """
        Handles the dragging motion to calculate the direction and power for the throw.
        """
        if self.app.currentPlay == 'pass' and self.app.state == 'preSnap':
            # Calculate drag distance for pass trajectory
            self.app.dragStartX = self.app.ball.positionX
            self.app.dragStartY = self.app.ball.positionY
            self.app.dragEndX = mouseX
            self.app.dragEndY = mouseY
            self.calculateTrajectory(mouseX, mouseY)

    def handleMouseRelease(self):
        """
        Handles releasing the mouse to execute the pass or toss.
        """
        if self.app.currentPlay == 'pass' and self.app.state == 'preSnap':
            # Throw the ball based on the drag direction
            dx = self.app.dragEndX - self.app.dragStartX
            dy = self.app.dragEndY - self.app.dragStartY
            distance = math.sqrt(dx ** 2 + dy ** 2)
            power = min(10, distance / 50)  # Adjust power scaling
            self.app.ball.throw(self.app.dragEndX, self.app.dragEndY, power=power)
            self.app.state = 'hiking'
        elif self.app.currentPlay == 'run' and self.app.state == 'preSnap':
            # Toss the ball to the running back
            runningBack = self.app.runningBack
            self.app.ball.throw(runningBack.x, runningBack.y, power=5)
            self.app.state = 'hiking'

    def calculateTrajectory(self, mouseX, mouseY):
        """
        Calculate the trajectory of the ball based on the drag direction and power.
        """
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
