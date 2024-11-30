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
    app.qbSelected = False
    app.rpo = RPO(app)
    app.ballSnapped = False
    app.snapTimer = 0
    app.receiversMoving = False  # New flag to control receiver movement

    app.field = Field(
        'other_sprites/field.png',
        field_width=2458,
        field_height=446,
        view_width=app.width,
        view_height=app.height
    )

    app.ball = Ball(
        positionX=app.field.field_width * 0.2,
        positionY=app.field.field_height / 2,
        velocityX=0,
        velocityY=0
    )

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

    app.receiverFrames = [
        f'/Users/max/Desktop/run-animation/run{i}_cleaned.png' for i in range(1, 7)
    ]
    for receiver in app.receivers:
        receiver.animationFrame = 0
        receiver.animationCounter = 0
        receiver.frameDelay = 3
        receiver.speed = 5  # Increased receiver speed

    app.runningBackFrames = [
        f'/Users/max/Desktop/run-animation/run{i}_cleaned.png' for i in range(1, 7)
    ]

    app.runningBack.animationFrame = 0
    app.runningBack.animationCounter = 0
    app.runningBack.frameDelay = 3
    app.runningBack.speed = 5  # Set running back speed

def redrawAll(app):
    app.field.updateCamera(app.ball.positionX, app.ball.positionY)
    app.field.drawField()

    for player in app.players:
        if player in app.receivers and app.receiversMoving:
            player.animationCounter += 1
            if player.animationCounter >= player.frameDelay:
                player.animationFrame = (player.animationFrame + 1) % len(app.receiverFrames)
                player.animationCounter = 0
            player.spritePath = app.receiverFrames[player.animationFrame]
        player.draw(app.field.camera_x, app.field.camera_y, app.field.scale_factor)

    for dot in app.trajectoryDots:
        dotX = (dot[0] - app.field.camera_x) * app.field.scale_factor
        dotY = (dot[1] - app.field.camera_y) * app.field.scale_factor
        drawCircle(dotX, dotY, 4, fill='yellow', border='black', borderWidth=1)

    ball_image = 'other_sprites/ball.png'
    ball_screen_x = (app.ball.positionX - app.field.camera_x) * app.field.scale_factor
    ball_screen_y = (app.ball.positionY - app.field.camera_y) * app.field.scale_factor
    drawImage(ball_image, ball_screen_x, ball_screen_y, width=60, height=35)

    if app.state == 'playSelection':
        drawRect(50, 50, 200, 100, fill='blue')
        drawLabel("Pass Play", 150, 100, fill='white', size=20)
        drawRect(50, 200, 200, 100, fill='green')
        drawLabel("Run Play", 150, 250, fill='white', size=20)

    drawLabel(f"Team A: {app.score['Team A']}", 50, 30, size=20, fill="white")
    drawLabel(f"Time Left: {int(app.timer)}s", 350, 30, size=20, fill="white")

def onMousePress(app, mouseX, mouseY):
    if app.state == 'playSelection':
        if 50 <= mouseX <= 250 and 50 <= mouseY <= 150:
            app.currentPlay = 'pass'
            app.state = 'hiking'
            app.qbSelected = False
            app.ballSnapped = False
            app.receiversMoving = True  # Start receiver movement for pass play
            print("Pass Play selected.")

        elif 50 <= mouseX <= 250 and 200 <= mouseY <= 300:
            app.currentPlay = 'run'
            app.state = 'hiking'
            app.ballSnapped = False
            app.receiversMoving = False  # Keep receivers stationary for run play
            print("Run Play selected.")

    elif app.state == 'postSnap' and app.currentPlay == 'pass':
        fieldMouseX, fieldMouseY = screenToField(app, mouseX, mouseY)
        qbX, qbY = app.quarterback.x, app.quarterback.y
        qbWidth, qbHeight = 60, 35

        if (qbX - qbWidth/2 <= fieldMouseX <= qbX + qbWidth/2 and 
            qbY - qbHeight/2 <= fieldMouseY <= qbY + qbHeight/2):
            app.qbSelected = True
            app.ball.beingDragged = True

def onMouseDrag(app, mouseX, mouseY):
    if app.state == 'postSnap' and app.currentPlay == 'pass' and app.qbSelected:
        fieldMouseX, fieldMouseY = screenToField(app, mouseX, mouseY)
        if app.ball.beingDragged:
            app.ball.positionX = fieldMouseX
            app.ball.positionY = fieldMouseY
            app.trajectoryDots = calculateTrajectory(
                app.quarterback.x, 
                app.quarterback.y,
                fieldMouseX,
                fieldMouseY,
                power=15
            )

def onMouseRelease(app, mouseX, mouseY):
    if app.state == 'postSnap' and app.currentPlay == 'pass' and app.qbSelected:
        fieldMouseX, fieldMouseY = screenToField(app, mouseX, mouseY)
        if app.ball.beingDragged:
            app.ball.throw(fieldMouseX, fieldMouseY)
            app.qbSelected = False
            app.trajectoryDots = []

def onStep(app):
    app.field.updateCamera(app.ball.positionX, app.ball.positionY)

    if app.state == 'hiking':
        if not app.ballSnapped:
            app.snapTimer += 1
            if app.snapTimer < 10:
                app.ball.positionX += (app.quarterback.x - app.ball.positionX) / 5
                app.ball.positionY += (app.quarterback.y - app.ball.positionY) / 5
            else:
                app.ballSnapped = True
                app.ball.holder = app.quarterback
                if app.currentPlay == 'pass':
                    app.state = 'postSnap'
                    print("Ball snapped to quarterback for Pass Play.")
                elif app.currentPlay == 'run':
                    app.ball.holder = app.runningBack
                    app.state = 'runPlay'
                    print("Ball handed off to running back.")
                app.snapTimer = 0

    if app.state == 'postSnap' and app.currentPlay == 'pass':
        for receiver in app.receivers:
            if app.receiversMoving:
                receiver.moveForward()  # Receivers move faster now
            
            if app.ball.canBeCaught(receiver):
                app.ball.holder = receiver
                app.ball.velocityX = 0
                app.ball.velocityY = 0
                app.ball.inFlight = False
                app.state = 'receiverControl'
                print(f"Ball caught by receiver at ({receiver.x}, {receiver.y})")

    if app.state == 'runPlay':
        app.runningBack.animationCounter += 1
        if app.runningBack.animationCounter >= app.runningBack.frameDelay:
            app.runningBack.animationFrame = (app.runningBack.animationFrame + 1) % len(app.runningBackFrames)
            app.runningBack.spritePath = app.runningBackFrames[app.runningBack.animationFrame]
            app.runningBack.animationCounter = 0

    app.ball.updatePosition(app.state)

    if app.timer > 0 and app.state != 'playSelection':
        app.timer -= 1 / 30

def onKeyHold(app, keys):
    # Handle movement for both running back and receiver with ball
    if app.state in ['runPlay', 'receiverControl']:
        ballCarrier = app.ball.holder
        if ballCarrier:
            if 'up' in keys:
                ballCarrier.y -= ballCarrier.speed
            if 'down' in keys:
                ballCarrier.y += ballCarrier.speed
            if 'right' in keys:
                ballCarrier.x += ballCarrier.speed
            if 'left' in keys:
                ballCarrier.x -= ballCarrier.speed
            
            # Update ball position to follow carrier
            app.ball.positionX = ballCarrier.x
            app.ball.positionY = ballCarrier.y

def calculateTrajectory(startX, startY, targetX, targetY, power=10):
    trajectory = []
    dx = targetX - startX
    dy = targetY - startY
    distance = math.sqrt(dx ** 2 + dy ** 2)
    
    if distance == 0:
        return trajectory
        
    velocityX = (dx / distance) * power
    velocityY = (dy / distance) * power

    x, y = startX, startY
    gravity = 0.5
    steps = 30
    
    for _ in range(steps):
        trajectory.append((x, y))
        x += velocityX
        y += velocityY
        velocityY += gravity
        
        if y >= 446:
            break

    return trajectory

def resetGame(app):
    app.state = 'playSelection'
    app.ball.reset(app.field.field_width // 2, app.field.field_height // 2)
    app.center = {'x': app.ball.positionX, 'y': app.ball.positionY}
    app.receiversMoving = False

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
    if not hasattr(app, 'field') or app.field.scale_factor == 0:
        print("Field or scale factor is not initialized!")
        return screenX, screenY

    fieldX = (screenX / app.field.scale_factor) + app.field.camera_x
    fieldY = (screenY / app.field.scale_factor) + app.field.camera_y
    return fieldX, fieldY

def main():
    runApp(width=1920, height=1080)

if __name__ == "__main__":
    main()