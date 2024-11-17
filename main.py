from cmu_graphics import *
import Game
import Field
import Ball
import Player
import Team

# Instantiate the game
game = Game.Game()
field = Field.Field('./other_sprites/field.png', 2048, 1024, 800, 400)
ball = {'x': 400, 'y': 200}

# Run the app

def redrawAll(app):
    print("redrawAll running: Field test")
    field.updateCamera(ball['x'], ball['y'])
    field.drawField()
    drawCircle(ball['x'] - field.camera_x, ball['y'] - field.camera_y, 20, fill="red")

runApp(width=800, height=400, redrawAll=redrawAll)
