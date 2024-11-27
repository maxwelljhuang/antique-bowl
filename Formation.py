import random
from Player import *

def setupFormation(ballX, ballY, quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite, isDefense=False):
    players = []

    # Defensive or offensive line setup
    linemenSpacing = 30
    linemenYStart = ballY - 90  # Ensure stable y-coordinates
    linemenX = ballX - 100 if isDefense else ballX - 50

    for i in range(7):
        yOffset = i * linemenSpacing  # Offset each lineman vertically
        players.append(Player(linemenX, linemenYStart + yOffset, spritePath=linemanSprite))

    # Quarterback and skill players (offense only)
    if not isDefense:
        qbX = ballX + 30
        qbY = ballY  # Place QB behind the ball
        players.append(Player(qbX, qbY, isQuarterback=True, spritePath=quarterbackSprite))  # QB
        players.append(Player(ballX, ballY + 50, spritePath=runningBackSprite))  # Running Back
        players.append(Player(ballX + 150, ballY - 50, spritePath=receiverSprite))  # Receiver 1
        players.append(Player(ballX + 150, ballY + 50, spritePath=receiverSprite))  # Receiver 2

    return players


