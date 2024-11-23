from cmu_graphics import *
from Field import Field  # Ensure Field class is in the same directory or properly imported

def onAppStart(app):
    # Initialize the field
    app.field = Field(
        '/Users/max/antique-bowl/other_sprites/field.png',  # Path to the field image
        field_width=2458,       # Field width in pixels
        field_height=446,      # Field height in pixels
        view_width=app.width,   # Screen width
        view_height=app.height  # Screen height
    )
    app.ball = {'x': app.field.field_width // 2, 'y': app.field.field_height // 2, 'radius': 10}

def redrawAll(app):
    # Update the camera to follow the ball
    app.field.updateCamera(app.ball['x'], app.ball['y'])

    # Draw the field with the updated camera position
    app.field.drawField()

    # Draw the ball as an image
    ball_image_path = '/Users/max/antique-bowl/other_sprites/ball.png'  # Replace with the correct path
    ball_screen_x = (app.ball['x'] - app.field.camera_x) * app.field.scale_factor
    ball_screen_y = (app.ball['y'] - app.field.camera_y) * app.field.scale_factor
    ball_scaled_width = 50 * app.field.scale_factor  # Scale the ball's width
    ball_scaled_height = 25 * app.field.scale_factor  # Scale the ball's height

    # Draw the ball
    drawImage(ball_image_path,
              ball_screen_x - ball_scaled_width / 2,  # Center horizontally
              ball_screen_y - ball_scaled_height / 2,  # Center vertically
              width=ball_scaled_width,
              height=ball_scaled_height)

def onKeyHold(app, keys):
    if 'up' in keys:
        app.ball['y'] -= 5
    if 'down' in keys:
        app.ball['y'] += 5
    if 'left' in keys:
        app.ball['x'] -= 5
    if 'right' in keys:
        app.ball['x'] += 5

def main():
    runApp(width=2500, height=1200)  # Replace with your desired dimensions

main()
