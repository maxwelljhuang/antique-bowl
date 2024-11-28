from cmu_graphics import *
from Field import Field
from Ball import Ball
from Formation import setupFormation
from Player import Player
import math
from RPO import *

def onAppStart(app):
    app.state = 'playSelection'
    app.currentPlay = None
    app.timer = 60
    app.score = {'Team A': 0, 'Team B': 0}
    app.draggingBall = False
    app.trajectoryDots = []
    app.qbSelected = False  # Track if QB has been selected
    app.rpo = RPO(app)

    # Initialize the field
    app.field = Field(
        'other_sprites/field.png',
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

    # Load sprites
    quarterbackSprite = 'stance.png'
    linemanSprite = 'linemen-animation/linestance.png'
    receiverSprite = 'run-animation/run1_cleaned.png'
    runningBackSprite = 'stance.png'

    # Set up formations
    app.players = setupFormation(
        app.ball.positionX, app.ball.positionY,
        quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite
    )
    app.quarterback = app.players[7]  # QB is explicitly tracked
    app.runningBack = app.players[8]
    app.receivers = app.players[9:]


    # Animation settings for receivers
    app.receiverFrames = [
        f'/Users/max/Desktop/run-animation/run{i}_cleaned.png' for i in range(1, 7)
    ]
    for receiver in app.receivers:
        receiver.animationFrame = 0
        receiver.animationCounter = 0
        receiver.frameDelay = 5  # Controls animation speed
        
    # Load running back animation frames
    app.runningBackFrames = [
        f'/Users/max/Desktop/run-animation/run{i}_cleaned.png' for i in range(1, 7)
    ]

    # Initialize running back animation settings
    app.runningBack.animationFrame = 0
    app.runningBack.animationCounter = 0
    app.runningBack.frameDelay = 5  # Controls animation speed


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
    ball_image = 'other_sprites/ball.png'
    ball_screen_x = (app.ball.positionX - app.field.camera_x) * app.field.scale_factor
    ball_screen_y = (app.ball.positionY - app.field.camera_y) * app.field.scale_factor
    drawImage(ball_image, ball_screen_x, ball_screen_y, width=60, height=35)

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
    if app.state == 'runPlay':
        if key == 'up':
            app.runningBack.y -= 10  # Move running back up
        elif key == 'down':
            app.runningBack.y += 10  # Move running back down

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
    # Ensure the camera is updated to center the ball
    app.field.updateCamera(app.ball.positionX, app.ball.positionY)

    # Handle ball snapping and handoff logic
    if app.state == 'hiking':
        if app.ball.holder is None:
            # Snap ball to quarterback
            app.ball.reset(app.quarterback.x, app.quarterback.y)
            app.ball.holder = app.quarterback  # Assign ball to QB
        else:
            # Hand off to running back after snapping
            app.ball.holder = app.runningBack
            app.ball.positionX = app.runningBack.x
            app.ball.positionY = app.runningBack.y
            app.state = 'runPlay'  # Transition to run play

    # Automatically move running back forward during run play
    if app.state == 'runPlay':
        # Move the running back forward
        app.runningBack.x += 3  # Forward movement
        app.ball.positionX = app.runningBack.x  # Ball moves with the running back
        app.ball.positionY = app.runningBack.y

        # Update animation frame
        app.runningBack.animationCounter += 1
        if app.runningBack.animationCounter >= app.runningBack.frameDelay:
            app.runningBack.animationFrame = (app.runningBack.animationFrame + 1) % len(app.runningBackFrames)
            app.runningBack.spritePath = app.runningBackFrames[app.runningBack.animationFrame]
            app.runningBack.animationCounter = 0  # Reset counter

    # Update ball position
    app.ball.updatePosition(app.state)

    if app.timer > 0 and app.state != 'playSelection':
        app.timer -= 1 / 30  # Countdown timer

def onMousePress(app, mouseX, mouseY):
    if app.state == 'playSelection':
        # Handle Pass Play selection
        if 50 <= mouseX <= 250 and 50 <= mouseY <= 150:
            app.currentPlay = 'pass'
            app.state = 'hiking'  # Transition to hiking state
            app.qbSelected = False  # Reset QB selection
        elif 50 <= mouseX <= 250 and 200 <= mouseY <= 300:
            app.currentPlay = 'run'
            app.state = 'hiking'  # Transition to hiking state
    if app.state == 'postSnap' and app.currentPlay == 'pass':
        # Map mouse coordinates to field coordinates
        try:
            fieldMouseX, fieldMouseY = screenToField(app, mouseX, mouseY)
        except Exception as e:
            print(f"Error mapping screen to field coordinates: {e}")
            return
        
        # Check if the user clicked on the quarterback
        qbX, qbY = app.quarterback.x, app.quarterback.y
        qbWidth, qbHeight = 60, 35  # Match QB sprite dimensions
        print(f"Mouse (Screen): ({mouseX}, {mouseY})")
        print(f"Mouse (Field): ({fieldMouseX}, {fieldMouseY})")
        print(f"QB Position: ({qbX}, {qbY})")
        
        if qbX - qbWidth / 2 <= fieldMouseX <= qbX + qbWidth / 2 and qbY - qbHeight / 2 <= fieldMouseY <= qbY + qbHeight / 2:
            app.qbSelected = True  # QB is selected
            print("Quarterback selected.")

def onMouseDrag(app, mouseX, mouseY):
    if app.state == 'postSnap' and app.currentPlay == 'pass' and app.qbSelected:
        # Map mouse coordinates to field coordinates
        fieldMouseX, fieldMouseY = screenToField(app, mouseX, mouseY)
        app.rpo.handleMouseDrag(fieldMouseX, fieldMouseY)

def onMouseRelease(app, mouseX, mouseY):
    if app.state == 'postSnap' and app.currentPlay == 'pass' and app.qbSelected:
        # Map mouse coordinates to field coordinates
        fieldMouseX, fieldMouseY = screenToField(app, mouseX, mouseY)
        app.rpo.handleMouseRelease()

def resetGame(app):
    app.state = 'playSelection'  # Reset to play selection
    app.ball.reset(app.field.field_width // 2, app.field.field_height // 2)  # Reset ball to the center
    app.center = {'x': app.ball.positionX, 'y': app.ball.positionY}

    # Reset player positions
    quarterbackSprite = 'stance.png'
    linemanSprite = 'linemen-animation/linestance.png'
    receiverSprite = 'run-animation/run1_cleaned.png'
    runningBackSprite = 'stance.png'
    app.players = setupFormation(
        app.ball.positionX, app.ball.positionY,
        quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite
    )
    app.quarterback = app.players[7]
    app.runningBack = app.players[8]
    app.receivers = app.players[9:]

def screenToField(app, screenX, screenY):
    if not hasattr(app, 'field') or app.field.scale_factor == 0: #
        print("Field or scale factor is not initialized!")
        return screenX, screenY  # Return screen coordinates as-is

    # Map screen coordinates to field coordinates
    fieldX = (screenX / app.field.scale_factor) + app.field.camera_x
    fieldY = (screenY / app.field.scale_factor) + app.field.camera_y
    return fieldX, fieldY

def main():
    runApp(width=2500, height=1250)

if __name__ == "__main__":
    main()
