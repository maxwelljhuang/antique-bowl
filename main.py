from cmu_graphics import *
from Game import Game

game = Game()
    # Run the app
runApp(
    width=800,
    height=400,
    redrawAll=game.redrawAll,
    onKeyHold=game.onKeyHold
)
