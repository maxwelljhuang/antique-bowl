from cmu_graphics import *

def onAppStart(app):
    # Load the animation frames
    baseUrl = '/Users/max/Desktop/run-animation/run'
    app.runFrames = [f'{baseUrl}{i}_cleaned.png' for i in range(1,7)]

    # Animation state
    app.currentFrame = 0  # Start with the first frame
    app.frameDelay = 5    # Number of steps before advancing to the next frame
    app.stepCounter = 0   # Counter to track steps between frame changes

    # Player position
    app.playerX = 400
    app.playerY = 300

def onStep(app):
    # Increment the step counter
    app.stepCounter += 1

    # Change the frame after every 'frameDelay' steps
    if app.stepCounter >= app.frameDelay:
        app.currentFrame = (app.currentFrame + 1) % len(app.runFrames)  # Cycle through frames
        app.stepCounter = 0  # Reset step counter

def redrawAll(app):
    # Draw the current frame of the running animation
    drawImage(
        app.runFrames[app.currentFrame],
        app.playerX - 20,  # Adjust X to center the sprite
        app.playerY - 40,  # Adjust Y to center the sprite
        width=40,  # Adjust size as needed
        height=80  # Adjust size as needed
    )

def main():
    runApp(width=800, height=600)

main()

#f'/mnt/data/run_cleaned_{(i % 6) + 1}.png'