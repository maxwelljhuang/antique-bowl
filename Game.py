from cmu_graphics import *
from Field import Field  # Ensure the Field module is imported correctly

class Game:
    def __init__(self):
        """
        Initializes the game.
        """
        self.state = "main_menu"  # Current game state
        self.teams = []  # List of Team objects
        self.currentMatch = None  # Placeholder for the current match object
        self.field = Field(
            '/Users/max/antique-bowl/field.png',  # Path to the field image
            field_width=2048,
            field_height=1024,
            view_width=800,
            view_height=400
        )
        self.ball = {'x': 400, 'y': 200, 'radius': 10}  # Ball position and size

    def redrawAll(self, app):
        """
        Redraws the entire screen, including the field and ball.
        """
        # Update the camera to follow the ball
        self.field.updateCamera(self.ball['x'], self.ball['y'])

        # Draw the field
        self.field.drawField()

        # Draw the ball
        drawCircle(
            self.ball['x'] - self.field.camera_x,
            self.ball['y'] - self.field.camera_y,
            self.ball['radius'],
            fill="brown"
        )

    def onKeyHold(self, app, keys):
        """
        Handles key press events to move the ball.
        """
        if 'up' in keys:
            self.ball['y'] -= 5
        if 'down' in keys:
            self.ball['y'] += 5
        if 'left' in keys:
            self.ball['x'] -= 5
        if 'right' in keys:
            self.ball['x'] += 5
