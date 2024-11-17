from cmu_graphics import *
from Field import Field  # Ensure Field is in the same directory or properly imported

def onAppStart(app):
    app.field = Field(
        '/Users/max/antique-bowl/other_sprites/field.png',  # Replace with the correct path to your image
        field_width=2048,
        field_height=1024,
        view_width=800,
        view_height=400
        )
    app.ball = {'x': 400, 'y': 200, 'radius': 10}

def redrawAll(app):
    """
    Redraws the field and the ball, centering the camera on the ball.
    """
    # Update the camera to follow the ball
    app.field.updateCamera(app.ball['x'], app.ball['y'])

    # Draw the field
    app.field.drawField()

    # Draw the ball
    drawCircle(
        app.ball['x'] - app.field.camera_x,
        app.ball['y'] - app.field.camera_y,
        app.ball['radius'],
        fill="red"
    )

def onKeyHold(app, keys):
    """
    Handles key press events to move the ball.
    """
    if 'up' in keys:
        app.ball['y'] -= 5
    if 'down' in keys:
        app.ball['y'] += 5
    if 'left' in keys:
        app.ball['x'] -= 5
    if 'right' in keys:
        app.ball['x'] += 5

def main():
    runApp(width=800, height = 400)

main()
