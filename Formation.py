import random
from Player import *

def setupFormation(ballX, ballY, quarterbackSprite, linemanSprite, receiverSprite, runningBackSprite, isDefense=False):
    players = []

    #linemen setup
    linemenSpacing = 30
    linemenYStart = ballY - 90  
    #set the center to be directly over the ball
    linemenX = ballX  


    for i in range(7):  
        #offset location of linemen
        yOffset = i * linemenSpacing  
        players.append(Player(linemenX, linemenYStart + yOffset, spritePath=linemanSprite))

    #offense formation
    if not isDefense:
        qbX = linemenX - 50
        qbY = ballY  
        players.append(Player(qbX, qbY, isQuarterback=True, spritePath=quarterbackSprite))

        #r back positioned further behind the quarterback
        rbX = qbX - 30
        rbY = qbY
        players.append(Player(rbX, rbY, spritePath=runningBackSprite))

        #receivers positioned to the far left and right of the linemen
        wr1X = linemenX - 70
        wr1Y = linemenYStart - 40 
        wr2X = linemenX - 70
        wr2Y = linemenYStart + 210  
        players.append(Player(wr1X, wr1Y, spritePath=receiverSprite))  
        players.append(Player(wr2X, wr2Y, spritePath=receiverSprite))  

    return players





