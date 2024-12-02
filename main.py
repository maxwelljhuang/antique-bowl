from cmu_graphics import *
from Field import Field
from Ball import Ball
from Formation import setupFormation
from Player import Player
import math
from RPO import *
from Defense import *
def onAppStart(app):
    app.state = 'startScreen'
    app.timer = 60
    app.score = {'Team A': 0, 'Team B': 0}
    app.draggingBall = False
    app.trajectoryDots = []
    app.qbSelected = False
    app.rpo = RPO(app)
    app.ballSnapped = False
    app.snapTimer = 0
    app.receiversMoving = False
    
    # Initialize field
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
        receiver.speed = 5

    app.runningBackFrames = [
        f'/Users/max/Desktop/run-animation/run{i}_cleaned.png' for i in range(1, 7)
    ]

    app.runningBack.animationFrame = 0
    app.runningBack.animationCounter = 0
    app.runningBack.frameDelay = 3
    app.runningBack.speed = 5

    defenderSprite = 'stance.png'  
    app.defense = Defense(app.ball.positionX, app.ball.positionY, defenderSprite)
def drawStartScreen(app):
    # Draw field background
    drawImage('other_sprites/field.png', 0, 0, width=app.width, height=app.height)
    
    # Semi-transparent black overlay
    drawRect(0, 0, app.width, app.height, fill='black', opacity=60)
    
    # Title container at x=960 (center), y=200
    drawRect(660, 160, 600, 80, fill='darkGreen', border='white', borderWidth=3)
    drawLabel('FOOTBALL SIMULATOR', 960, 200, size=50, bold=True, fill='white', font='monospace')
    
    # Main instructions container centered at x=960, y=500
    drawRect(610, 350, 700, 300, fill=rgb(0, 50, 0), border='white', borderWidth=2)
    
    # Instructions header
    drawLabel("GAME CONTROLS", 960, 380, size=30, bold=True, fill='gold', font='monospace')
    
    # Divider line
    drawLine(660, 410, 1260, 410, fill='white', lineWidth=2)
    
    # Step 1 - Play Selection
    drawLabel("1. Select your play type: Pass Play or Run Play", 960, 440, 
             size=22, bold=True, fill='white', font='monospace')
    
    # Step 2 - Pass Play Controls
    drawLabel("2. Pass Play Controls:", 960, 480, 
             size=22, bold=True, fill='white', font='monospace')
    drawLabel("• Ball snaps to quarterback", 960, 500, 
             size=22, fill='white', font='monospace')
    drawLabel("• Click on quarterback to start throwing", 960, 520, 
             size=22, fill='white', font='monospace')
    drawLabel("• Drag to aim and release to throw", 960, 540, 
             size=22, fill='white', font='monospace')
    
    # Step 3 - Run Play Controls
    drawLabel("3. Run Play Controls:", 960, 580, 
             size=22, bold=True, fill='white', font='monospace')
    drawLabel("• Ball snaps to running back", 960, 600, 
             size=22, fill='white', font='monospace')
    drawLabel("• Use arrow keys to move in any direction", 960, 620, 
             size=22, fill='white', font='monospace')
    
    # Start button centered at x=960, y=800
    drawRect(860, 770, 200, 60, fill='darkGreen', border='white', borderWidth=3)
    drawLabel('START GAME', 960, 800, size=30, bold=True, fill='white', font='monospace')

def redrawAll(app):
    if app.state == 'startScreen':
        drawStartScreen(app)
    else:
        app.field.updateCamera(app.ball.positionX, app.ball.positionY)
        app.field.drawField()

        for player in app.players:
            # Handle receiver animations
            if player in app.receivers and app.receiversMoving:
                player.animationCounter += 1
                if player.animationCounter >= player.frameDelay:
                    player.animationFrame = (player.animationFrame + 1) % len(app.receiverFrames)
                    player.animationCounter = 0
                player.spritePath = app.receiverFrames[player.animationFrame]
            
            # Handle running back animation
            if player == app.runningBack and app.state == 'runPlay':
                player.animationCounter += 1
                if player.animationCounter >= player.frameDelay:
                    player.animationFrame = (player.animationFrame + 1) % len(app.runningBackFrames)
                    player.animationCounter = 0
                player.spritePath = app.runningBackFrames[player.animationFrame]
            
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
            # Play selection buttons with improved styling
            drawRect(50, 50, 200, 100, fill='darkBlue', border='white', borderWidth=2)
            drawRect(50, 200, 200, 100, fill='darkGreen', border='white', borderWidth=2)
            drawLabel("Pass Play", 150, 100, fill='white', size=24, bold=True)
            drawLabel("Run Play", 150, 250, fill='white', size=24, bold=True)

        # Score and timer display with improved visibility
        drawRect(30, 10, 150, 40, fill='black', opacity=50)
        drawRect(330, 10, 150, 40, fill='black', opacity=50)
        drawLabel(f"Score: {app.score['Team A']}", 50, 30, size=20, fill="white", bold=True)
        drawLabel(f"Time: {int(app.timer)}s", 350, 30, size=20, fill="white", bold=True)
        
        for defender in app.defense.players:
            defender.draw(app.field.camera_x, app.field.camera_y, app.field.scale_factor)
def onMousePress(app, mouseX, mouseY):
    if app.state == 'startScreen':
        # Check if Start Game button was clicked
        buttonY = app.height * 0.8
        if (app.width/2 - 100 <= mouseX <= app.width/2 + 100 and
            buttonY - 30 <= mouseY <= buttonY + 30):
            app.state = 'playSelection'
            return

    elif app.state == 'playSelection':
        if 50 <= mouseX <= 250 and 50 <= mouseY <= 150:
            app.currentPlay = 'pass'
            app.state = 'hiking'
            app.qbSelected = False
            app.ballSnapped = False
            app.receiversMoving = True
            print("Pass Play selected.")

        elif 50 <= mouseX <= 250 and 200 <= mouseY <= 300:
            app.currentPlay = 'run'
            app.state = 'hiking'
            app.ballSnapped = False
            app.receiversMoving = False
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
                elif app.currentPlay == 'run':
                    app.ball.holder = app.runningBack
                    app.state = 'runPlay'
                app.snapTimer = 0

    if app.state in ['postSnap', 'runPlay', 'receiverControl']:
        app.defense.update(app.ball, app.players)

    if app.state == 'postSnap' and app.currentPlay == 'pass':
        for receiver in app.receivers:
            if app.receiversMoving:
                receiver.moveForward()
            
            if app.ball.canBeCaught(receiver):
                app.ball.holder = receiver
                app.ball.velocityX = 0
                app.ball.velocityY = 0
                app.ball.inFlight = False
                app.state = 'receiverControl'
                print(f"Ball caught by receiver at ({receiver.x}, {receiver.y})")

    app.ball.updatePosition(app.state)

    if app.timer > 0 and app.state != 'playSelection' and app.state != 'startScreen':
        app.timer -= 1 / 30

def onKeyHold(app, keys):
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