from cmu_graphics import *
from Field import Field
from Ball import Ball
from Formation import setupFormation
from Player import Player
import math
from RPO import *
from Defense import *
from GameState import *

'''
Image Citations:
Field: https://ia802208.us.archive.org/26/items/retro-bowl/RetroBowl_texture_0.png
Player Sprites (including animation frames and stationary frames): https://www.spriters-resource.com/mobile/retrobowl/sheet/200221/
'''

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
    
    app.startButtonHovered = False
    app.passButtonHovered = False
    app.runButtonHovered = False
    app.resetButtonHovered = False

    # print field
    app.field = Field(
        'other_sprites/field.png',
        field_width=2458,
        field_height=446,
        view_width=app.width,
        view_height=app.height
    )

    app.ball = Ball(
        positionX=650,
        positionY=app.field.field_height / 2,
        velocityX=0,
        velocityY=0
    )
    app.gameState = GameState(app.ball.positionX)
    quarterbackSprite = 'other_sprites/stance.png'
    linemanSprite = 'linemen-animation/linestance.png'
    receiverSprite = 'run-animation/run1_cleaned.png'
    runningBackSprite = 'other_sprites/stance.png'

    app.players = setupFormation(
        app.ball.positionX, app.ball.positionY,
        quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite
    )
    app.quarterback = app.players[7]
    app.runningBack = app.players[8]
    app.receivers = app.players[9:]

    app.receiverFrames = [
        f'run-animation/run{i}_cleaned.png' for i in range(1, 7)
    ]
    for receiver in app.receivers:
        receiver.animationFrame = 0
        receiver.animationCounter = 0
        receiver.frameDelay = 3
        receiver.speed = 5

    app.runningBackFrames = [
        f'run-animation/run{i}_cleaned.png' for i in range(1, 7)
    ]

    app.runningBack.animationFrame = 0
    app.runningBack.animationCounter = 0
    app.runningBack.frameDelay = 3
    app.runningBack.speed = 5

    defenderSprite = 'defender.png'  
    app.defense = Defense(app.ball.positionX, app.ball.positionY, defenderSprite)

def drawStartScreen(app):
    #background with field overlay and dimming
    drawImage('other_sprites/field.png', 0, 0, width=app.width, height=app.height)
    drawRect(0, 0, app.width, app.height, fill='black', opacity=70)
    
    #title with shadow effect
    drawLabel('ANTIQUE', 960, 150, size=80, bold=True, fill='black')
    drawLabel('ANTIQUE', 957, 147, size=80, bold=True, fill='gold')
    drawLabel('BOWL', 960, 230, size=80, bold=True, fill='black')
    drawLabel('BOWL', 957, 227, size=80, bold=True, fill='gold')
    
    #main control panel
    drawRect(610, 300, 700, 400, fill=rgb(0, 40, 0), border='gold', borderWidth=3)
    
    #game controls header
    drawLabel("GAME CONTROLS", 960, 340, size=35, bold=True, fill='gold')
    drawLine(660, 370, 1260, 370, fill='gold', lineWidth=2)
    
    #two-column layout for controls
    #pass plays
    drawRect(635, 390, 325, 290, fill=rgb(0, 60, 0), border='white')
    drawLabel("PASSING GAME", 797, 420, size=25, bold=True, fill='white')
    drawLabel("1. Select Pass Play", 797, 460, size=20, fill='white')
    drawLabel("2. Wait for snap", 797, 490, size=20, fill='white')
    drawLabel("3. Click QB to begin throw", 797, 520, size=20, fill='white')
    drawLabel("4. Drag to aim and release", 797, 550, size=20, fill='white')
    drawLabel("5. Use arrow keys after catch", 797, 580, size=20, fill='white')
    
    #run plays
    drawRect(960, 390, 325, 290, fill=rgb(0, 60, 0), border='white')
    drawLabel("RUNNING GAME", 1122, 420, size=25, bold=True, fill='white')
    drawLabel("1. Select Run Play", 1122, 460, size=20, fill='white')
    drawLabel("2. Wait for snap", 1122, 490, size=20, fill='white')
    drawLabel("3. Control with arrow keys:", 1122, 520, size=20, fill='white')
    drawLabel("↑ up  ↓ down  ← left  → right", 1122, 550, size=20, fill='white')
    drawLabel("4. Find running lanes!", 1122, 580, size=20, fill='white')

    #start button with hover effect
    buttonColor = rgb(0, 150, 0) if app.startButtonHovered else 'darkGreen'
    drawRect(860, 730, 200, 60, fill=buttonColor, border='gold', borderWidth=3)
    drawLabel('START GAME', 960, 760, size=30, bold=True, fill='white')

def drawGameHUD(app):
    #score, down, and time display overlay
    drawRect(20, 10, 280, 50, fill='black', opacity=80, border='gold')
    drawRect(320, 10, 180, 50, fill='black', opacity=80, border='gold')
    drawRect(520, 10, 180, 50, fill='black', opacity=80, border='gold')
    
    #down and distance with color coding
    downColor = 'red' if app.gameState.down >= 3 else 'white'
    drawLabel(app.gameState.get_down_text(), 160, 35, size=22, bold=True, fill=downColor)
    
    #score display
    drawLabel(f"SCORE: {app.gameState.score['Team A']}", 410, 35, 
             size=22, bold=True, fill='white')
    
    #time with color warnings
    if app.timer <= 10:
        timeColor = 'red'
    elif app.timer <= 30:
        timeColor = 'yellow'
    else:
        timeColor = 'white'
    drawLabel(f"TIME: {int(app.timer)}s", 610, 35, size=22, bold=True, fill=timeColor)
    
def drawPlaySelection(app):
    #play selection panel moved lower
    drawRect(30, 100, 240, 300, fill=rgb(0, 30, 60), border='white', borderWidth=2)
    drawLabel("SELECT PLAY", 150, 130, size=26, bold=True, fill='gold')
    
    #pass play button with hover
    passColor = rgb(0,80,160) if app.passButtonHovered else 'darkBlue'
    drawRect(50, 160, 200, 100, fill=passColor, border='white', borderWidth=2)
    drawLabel("PASS PLAY", 150, 210, fill='white', size=24, bold=True)
    
    #run play button with hover
    runColor = rgb(0,120,0) if app.runButtonHovered else 'darkGreen'
    drawRect(50, 280, 200, 100, fill=runColor, border='white', borderWidth=2)
    drawLabel("RUN PLAY", 150, 330, fill='white', size=24, bold=True)

def drawGameOver(app):
    #full screen overlay
    drawRect(0, 0, app.width, app.height, fill='black', opacity=60)
    
    #game over panel
    drawRect(app.width/2 - 250, app.height/2 - 150, 500, 300, 
            fill=rgb(0, 40, 0), border='gold', borderWidth=4)
    
    drawLabel('GAME OVER', app.width/2, app.height/2 - 80, 
             size=50, bold=True, fill='gold')
    drawLabel(f'Final Score: {app.gameState.score["Team A"]}', 
             app.width/2, app.height/2, size=35, fill='white', bold=True)
    
    #reset button with hover effect
    buttonColor = rgb(0,100,0) if app.resetButtonHovered else 'darkGreen'
    drawRect(app.width/2 - 100, app.height/2 + 60, 200, 60, 
            fill=buttonColor, border='white', borderWidth=3)
    drawLabel('PLAY AGAIN', app.width/2, app.height/2 + 90, 
             size=30, bold=True, fill='white')

def drawTouchdown(app):
    #celebration overlay
    drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
    
    #touchdown banner
    bannerWidth, bannerHeight = 600, 300
    centerX, centerY = app.width/2, app.height/2
    
    #banner background with glow effect
    drawRect(centerX - bannerWidth/2 - 10, centerY - bannerHeight/2 - 10,
            bannerWidth + 20, bannerHeight + 20, fill='gold', opacity=30)
    drawRect(centerX - bannerWidth/2, centerY - bannerHeight/2,
            bannerWidth, bannerHeight, fill='darkGreen', opacity=90)
    drawRect(centerX - bannerWidth/2 + 10, centerY - bannerHeight/2 + 10,
            bannerWidth - 20, bannerHeight - 20, fill=None, border='gold', borderWidth=4)
    
    #touchdown text with shadow
    drawLabel('TOUCHDOWN!', centerX + 3, centerY - 47, size=60, bold=True, fill='black')
    drawLabel('TOUCHDOWN!', centerX, centerY - 50, size=60, bold=True, fill='gold')
    
    #score update
    drawLabel(f'Score: {app.gameState.score["Team A"]}', centerX, centerY + 20, 
             size=40, fill='white', bold=True)
    
    #continue prompt
    drawLabel('Click anywhere to continue', centerX, centerY + 80, 
             size=25, fill='white')

def onMouseMove(app, mouseX, mouseY):
    #start button hover detection
    app.startButtonHovered = (860 <= mouseX <= 1060 and 
                            730 <= mouseY <= 790)
    
    #play selection button hover
    if app.state == 'playSelection':
        app.passButtonHovered = (50 <= mouseX <= 250 and 
                               160 <= mouseY <= 260)
        app.runButtonHovered = (50 <= mouseX <= 250 and 
                              280 <= mouseY <= 380)
def redrawAll(app):
    if app.state == 'startScreen':
        drawStartScreen(app)
    else:
        app.field.updateCamera(app.ball.positionX, app.ball.positionY)
        app.field.drawField()

        #draw first down line
        first_down_x = (app.gameState.first_down_line - app.field.camera_x) * app.field.scale_factor
        drawLine(first_down_x, 0, first_down_x, app.height, fill='yellow', lineWidth=2)

        #draw players and animations
        for player in app.players:
            #receiver animation
            if player in app.receivers and app.receiversMoving:
                player.animationCounter += 1
                if player.animationCounter >= player.frameDelay:
                    player.animationFrame = (player.animationFrame + 1) % len(app.receiverFrames)
                    player.animationCounter = 0
                player.spritePath = app.receiverFrames[player.animationFrame]
            
            #running back animation
            if player == app.runningBack and app.state == 'runPlay':
                player.animationCounter += 1
                if player.animationCounter >= player.frameDelay:
                    player.animationFrame = (player.animationFrame + 1) % len(app.runningBackFrames)
                    player.animationCounter = 0
                player.spritePath = app.runningBackFrames[player.animationFrame]
            
            player.draw(app.field.camera_x, app.field.camera_y, app.field.scale_factor)

        #draw trajectory dots for passing
        for dot in app.trajectoryDots:
            dotX = (dot[0] - app.field.camera_x) * app.field.scale_factor
            dotY = (dot[1] - app.field.camera_y) * app.field.scale_factor
            drawCircle(dotX, dotY, 4, fill='yellow', border='black', borderWidth=1)

        #draw ball
        ball_image = 'other_sprites/ball.png'
        ball_screen_x = (app.ball.positionX - app.field.camera_x) * app.field.scale_factor
        ball_screen_y = (app.ball.positionY - app.field.camera_y) * app.field.scale_factor
        drawImage(ball_image, ball_screen_x, ball_screen_y, width=60, height=35)

        #draw defenders
        for defender in app.defense.players:
            defender.draw(app.field.camera_x, app.field.camera_y, app.field.scale_factor)

        #draw UI elements
        drawGameHUD(app)

        #rraw state-specific UI
        if app.state == 'playSelection':
            drawPlaySelection(app)
        elif app.state == 'gameOver':
            drawGameOver(app)
        elif app.state == 'touchdown':
            drawTouchdown(app)

def onKeyPress(app, key):
    if key == 'r' and app.gameState.game_over:
        #reset the game
        app.gameState.reset_game(650)
        resetPlay(app)
        app.state = 'playSelection'

def onMousePress(app, mouseX, mouseY):
    if app.state == 'startScreen':
        buttonY = app.height * 0.8
        if (app.width/2 - 100 <= mouseX <= app.width/2 + 100 and
            buttonY - 30 <= mouseY <= buttonY + 30):
            app.state = 'playSelection'
            return
        
    elif app.state == 'playSelection':
        if 50 <= mouseX <= 250:
            if 160 <= mouseY <= 260:  #pass play
                app.currentPlay = 'pass'
                app.state = 'hiking'
                app.qbSelected = False
                app.ballSnapped = False
                app.receiversMoving = True
            elif 280 <= mouseY <= 380:  #run play
                app.currentPlay = 'run'
                app.state = 'hiking'
                app.ballSnapped = False
                app.receiversMoving = False

    elif app.state == 'postSnap' and app.currentPlay == 'pass':
        fieldMouseX, fieldMouseY = screenToField(app, mouseX, mouseY)
        qbX, qbY = app.quarterback.x, app.quarterback.y
        qbWidth, qbHeight = 60, 35

        if (qbX - qbWidth/2 <= fieldMouseX <= qbX + qbWidth/2 and 
            qbY - qbHeight/2 <= fieldMouseY <= qbY + qbHeight/2):
            app.qbSelected = True
            app.ball.beingDragged = True
    if app.state == 'touchdown':
        app.state = 'playSelection'
        #reset formations when leaving touchdown screen
        starting_position = 650
        quarterbackSprite = 'other_sprites/stance.png'
        linemanSprite = 'linemen-animation/linestance.png'
        receiverSprite = 'run-animation/run1_cleaned.png'
        runningBackSprite = 'other_sprites/stance.png'
        defenderSprite = 'defender.png'
        
        app.players = setupFormation(
            starting_position, app.ball.positionY,
            quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite
        )
        app.quarterback = app.players[7]
        app.runningBack = app.players[8]
        app.receivers = app.players[9:]
        app.defense = Defense(starting_position, app.ball.positionY, defenderSprite)
        return
        
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
                    app.ball.initial_throw_position = app.ball.positionX
                elif app.currentPlay == 'run':
                    app.ball.holder = app.runningBack
                    app.state = 'runPlay'
                app.snapTimer = 0

    if app.state in ['postSnap', 'runPlay', 'receiverControl']:
        #check for touchdown
        if app.ball.positionX >= app.field.field_width * 0.9:
            app.state = 'touchdown'
            app.gameState.score['Team A'] += 7
            app.gameState.reset_touchdown(650)
            resetPlayAfterTouchdown(app)
            return

        app.defense.update(app.ball, app.players)
        
        for player in app.players:
            player.updateTackleAnimation()
            if player in app.receivers and app.receiversMoving and app.currentPlay == 'pass':
                player.moveForward()
        
        if any(player.tackleAnimationComplete for player in app.players):
            #here's the key change: Check for first down before updating downs
            if app.ball.positionX >= app.gameState.first_down_line:
                #reset down and update first down line
                app.gameState.down = 1
                app.gameState.initial_ball_position = app.ball.positionX
                app.gameState.first_down_line = app.ball.positionX + 200
                app.gameState.yards_to_go = 10
                resetPlay(app)
            else:
                #if not a first down, then update down count
                result = app.gameState.update_down(app.ball.positionX)
                if result == 'game_over':
                    app.state = 'gameOver'
                else:
                    result = app.gameState.next_down(app.ball.positionX)
                    if result == 'game_over':
                        app.state = 'gameOver'
                    else:
                        resetPlay(app)

        if app.state == 'postSnap' and app.currentPlay == 'pass':
            if app.ball.inFlight:
                for receiver in app.receivers:
                    if app.ball.canBeCaught(receiver):
                        app.ball.holder = receiver
                        app.ball.velocityX = 0
                        app.ball.velocityY = 0
                        app.ball.inFlight = False
                        app.state = 'receiverControl'
                        break
            
            #if ball hits ground (incomplete pass)
            elif not app.ball.inFlight and not app.ball.holder and not app.ball.beingDragged:
                #reset ball to where play started
                app.ball.positionX = app.ball.initial_throw_position
                result = app.gameState.next_down(app.ball.initial_throw_position)
                if result == 'game_over':
                    app.state = 'gameOver'
                else:
                    resetPlay(app)

        app.ball.updatePosition(app.state)

        if app.timer > 0 and app.state != 'playSelection' and app.state != 'startScreen':
            app.timer -= 1 / 30

def onKeyHold(app, keys):
    if app.state in ['runPlay', 'receiverControl']:
        ballCarrier = app.ball.holder
        if ballCarrier:
            new_x = ballCarrier.x
            new_y = ballCarrier.y
            
            #calculate new position based on input
            if 'up' in keys:
                new_y -= ballCarrier.speed
            if 'down' in keys:
                new_y += ballCarrier.speed
            if 'right' in keys:
                new_x += ballCarrier.speed
            if 'left' in keys:
                new_x -= ballCarrier.speed
            
            #check boundaries before applying movement
            #adding margins for player sprite size
            margin = 30
            field_top = margin
            field_bottom = app.field.field_height - 80
            
            #only update position if within bounds
            if field_top <= new_y <= field_bottom:
                ballCarrier.y = new_y
            app.ball.positionY = ballCarrier.y
            
            #always allow horizontal movement
            ballCarrier.x = new_x
            app.ball.positionX = ballCarrier.x
    
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

def resetPlay(app):
    if app.currentPlay == 'pass' and not app.ball.holder:
        last_ball_x = app.gameState.initial_ball_position
    else:
        last_ball_x = app.ball.positionX
    
    app.state = 'playSelection'
    app.draggingBall = False
    app.trajectoryDots = []
    app.qbSelected = False
    app.ballSnapped = False
    app.snapTimer = 0
    app.receiversMoving = False
    
    #reset ball position
    app.ball.reset(last_ball_x, app.field.field_height / 2)
    
    quarterbackSprite = 'other_sprites/stance.png'
    linemanSprite = 'linemen-animation/linestance.png'
    receiverSprite = 'run-animation/run1_cleaned.png'
    runningBackSprite = 'other_sprites/stance.png'
    defenderSprite = 'defender.png'
    
    #new formation
    app.players = setupFormation(
        last_ball_x, app.ball.positionY,
        quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite
    )
    app.quarterback = app.players[7]
    app.runningBack = app.players[8]
    app.receivers = app.players[9:]
    
    app.defense = Defense(last_ball_x, app.ball.positionY, defenderSprite)

def resetPlayAfterTouchdown(app):
    #20 yard line position
    starting_position = 650
    
    app.state = 'touchdown'
    app.draggingBall = False
    app.trajectoryDots = []
    app.qbSelected = False
    app.ballSnapped = False
    app.snapTimer = 0
    app.receiversMoving = False
    
    #reset ball position
    app.ball.reset(starting_position, app.field.field_height / 2)
    
    #reset game state
    app.gameState.reset_touchdown(starting_position)
    
    #reset all formations
    quarterbackSprite = 'other_sprites/stance.png'
    linemanSprite = 'linemen-animation/linestance.png'
    receiverSprite = 'run-animation/run1_cleaned.png'
    runningBackSprite = 'other_sprites/stance.png'
    defenderSprite = 'defender.png'
    
    #create new formation at starting position
    app.players = setupFormation(
        starting_position, app.ball.positionY,
        quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite
    )
    
    # Update player references
    app.quarterback = app.players[7]
    app.runningBack = app.players[8]
    app.receivers = app.players[9:]
    
    #reset animation states for receivers
    for receiver in app.receivers:
        receiver.animationFrame = 0
        receiver.animationCounter = 0
        receiver.frameDelay = 3
        receiver.speed = 5
    
    #reset animation states for running back
    app.runningBack.animationFrame = 0
    app.runningBack.animationCounter = 0
    app.runningBack.frameDelay = 3
    app.runningBack.speed = 5
    
    #reset defense
    app.defense = Defense(starting_position, app.ball.positionY, defenderSprite)

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