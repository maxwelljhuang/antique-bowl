import random
from Player import *

def setupFormation(ballX, ballY, quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite, isDefense=False):
    players = []

    # Linemen setup (horizontal line at the line of scrimmage)
    linemenSpacing = 30
    linemenYStart = ballY - 90  # Line of scrimmage is vertically aligned
    linemenX = ballX - 50 if not isDefense else ballX + 50

    for i in range(7):  # 7 linemen
        yOffset = i * linemenSpacing  # Offset each lineman vertically
        players.append(Player(linemenX, linemenYStart + yOffset, spritePath=linemanSprite))

    # Offensive skill players (quarterback, running back, receivers)
    if not isDefense:
        # Quarterback positioned behind the linemen
        qbX = linemenX - 50
        qbY = ballY  # Centered behind the line of scrimmage
        players.append(Player(qbX, qbY, isQuarterback=True, spritePath=quarterbackSprite))

        # Running back positioned further behind the quarterback
        rbX = qbX - 30
        rbY = qbY
        players.append(Player(rbX, rbY, spritePath=runningBackSprite))

        # Wide receivers positioned to the far left and right of the linemen
        wr1X = linemenX - 70
        wr1Y = linemenYStart - 40  # Above the top lineman
        wr2X = linemenX - 70
        wr2Y = linemenYStart + 210  # Below the bottom lineman
        players.append(Player(wr1X, wr1Y, spritePath=receiverSprite))  # Receiver 1
        players.append(Player(wr2X, wr2Y, spritePath=receiverSprite))  # Receiver 2

    return players



