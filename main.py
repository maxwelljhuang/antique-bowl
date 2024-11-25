from cmu_graphics import *
from Field import Field
from Ball import Ball
from Formation import setupFormation
from Player import Player
import math
#player sprites https://www.spriters-resource.com/mobile/retrobowl/sheet/200221/
#field sprite 
def onAppStart(app):
    # Game state and settings
    app.state = 'playSelection'  # Initial state
    app.currentPlay = None  # Tracks the current play ('pass' or 'run')
    app.timer = 60  # 60-second game timer
    app.score = {'Team A': 0, 'Team B': 0}
    app.draggingBall = False
    app.trajectoryDots = []  # List of dots for the trajectory

    # Initialize the field
    app.field = Field(
        '/Users/max/antique-bowl/other_sprites/field.png',  # Path to field image
        field_width=2458,
        field_height=446,
        view_width=app.width,
        view_height=app.height
    )

    # Initialize the ball
    app.ball = Ball(
        positionX=app.field.field_width // 2,
        positionY=app.field.field_height // 2,
        velocityX=0,
        velocityY=0
    )
    app.center = {'x': app.ball.positionX, 'y': app.ball.positionY}

    # Load sprites
    quarterbackSprite = '/Users/max/antique-bowl/stance.png'
    linemanSprite = '/Users/max/antique-bowl/linemen-animation/linestance.png'
    receiverSprite = '/Users/max/antique-bowl/run-animation/run1_cleaned.png'  # Initial frame for animation
    runningBackSprite = '/Users/max/antique-bowl/stance.png'

    # Set up formations
    app.players = setupFormation(
        app.ball.positionX, app.ball.positionY,
        quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite
    )
    app.quarterback = app.players[7]
    app.runningBack = app.players[8]
    app.receivers = app.players[9:]

    # Animation settings for receivers
    app.receiverFrames = [
        f'/Users/max/antique-bowl/run-animation/run{i}_cleaned.png' for i in range(1, 7)
    ]
    for receiver in app.receivers:
        receiver.animationFrame = 0
        receiver.animationCounter = 0
        receiver.frameDelay = 5  # Controls animation speed

def redrawAll(app):
    # Update the camera to center on the ball
    app.field.updateCamera(app.ball.positionX, app.ball.positionY)

    # Draw the field
    app.field.drawField()

    # Draw offensive players (receivers animated)
    for player in app.players:
        if player in app.receivers:
            player.animationCounter += 1
            if player.animationCounter >= player.frameDelay:
                player.animationFrame = (player.animationFrame + 1) % len(app.receiverFrames)
                player.animationCounter = 0
            player.spritePath = app.receiverFrames[player.animationFrame]
        player.draw(app.field.camera_x, app.field.camera_y, app.field.scale_factor)

    # Draw ball trajectory (if any)
    for dot in app.trajectoryDots:
        drawCircle(
            (dot[0] - app.field.camera_x) * app.field.scale_factor,
            (dot[1] - app.field.camera_y) * app.field.scale_factor,
            3, fill='yellow'
        )

    # Draw the ball
    ball_image = '/Users/max/antique-bowl/other_sprites/ball.png'
    ball_screen_x = (app.ball.positionX - app.field.camera_x) * app.field.scale_factor
    ball_screen_y = (app.ball.positionY - app.field.camera_y) * app.field.scale_factor
    drawImage(ball_image, ball_screen_x, ball_screen_y, width=20, height=20)

    # Draw play selection menu
    if app.state == 'playSelection':
        drawRect(50, 50, 200, 100, fill='blue')
        drawLabel("Pass Play", 150, 100, fill='white', size=20)
        drawRect(50, 200, 200, 100, fill='green')
        drawLabel("Run Play", 150, 250, fill='white', size=20)

    # Draw scores and timer
    drawLabel(f"Team A: {app.score['Team A']}", 50, 30, size=20, fill="white")
    drawLabel(f"Time Left: {int(app.timer)}s", 350, 30, size=20, fill="white")

def onKeyPress(app, key):
    if app.state == 'hiking' and key == 'space':
        # Throw the ball to the closest receiver
        closestReceiver = min(
            app.receivers, key=lambda r: math.sqrt((r.x - app.quarterback.x) ** 2 + (r.y - app.quarterback.y) ** 2)
        )
        app.ball.throw(closestReceiver.x, closestReceiver.y, power=10)

        # Calculate the ball trajectory and display dots
        app.trajectoryDots = calculateTrajectory(app.ball.positionX, app.ball.positionY, closestReceiver.x, closestReceiver.y, power=10)

def calculateTrajectory(startX, startY, targetX, targetY, power=10):
    trajectory = []
    dx = targetX - startX
    dy = targetY - startY
    distance = math.sqrt(dx ** 2 + dy ** 2)
    velocityX = (dx / distance) * power
    velocityY = (dy / distance) * power

    # Simulate the trajectory
    x, y = startX, startY
    while y < 446:  # Ground level
        trajectory.append((x, y))
        x += velocityX
        y += velocityY
        velocityY += 0.5  # Gravity effect
    return trajectory

def onStep(app):
    if app.timer > 0 and app.state != 'playSelection':
        app.timer -= 1 / 30  # Countdown timer

    # Update ball position based on game state
    app.ball.updatePosition(app.state)

def resetGame(app):
    app.state = 'playSelection'  # Reset to play selection
    app.ball.reset(app.field.field_width // 2, app.field.field_height // 2)  # Reset ball to the center
    app.center = {'x': app.ball.positionX, 'y': app.ball.positionY}

    # Reset player positions
    quarterbackSprite = '/Users/max/antique-bowl/stance.png'
    linemanSprite = '/Users/max/antique-bowl/linemen-animation/linestance.png'
    receiverSprite = '/Users/max/antique-bowl/run-animation/run1_cleaned.png'
    runningBackSprite = '/Users/max/antique-bowl/stance.png'
    app.players = setupFormation(
        app.ball.positionX, app.ball.positionY,
        quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite
    )

def main():
    runApp(width=1000, height=500)

if __name__ == "__main__":
    main()
