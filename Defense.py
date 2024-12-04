from Player import Player
'''
Refernces:
Rule Based AI - https://realpython.com/tic-tac-toe-ai-python/ , https://stackoverflow.com/questions/53421492/python-rule-based-engine
'''
from Player import Player

class Defense:
    def __init__(self, ballX, ballY, defenderSprite):
        self.players = self.setup_formation(ballX, ballY, defenderSprite)
        self.tackle_distance = 30
    
    def setup_formation(self, ballX, ballY, defenderSprite):

        linemenSpacing = 30
        #linemen setup
        linemenX = ballX  
        linemenYStart = ballY - 90 
        #set the center to be directly over the ball
        defenders = []
        for i in range(7):  
            #offset location of linemen
            yOffset = i * linemenSpacing  
            defenders.append(Player(linemenX + 35, ballY + yOffset - 90, spritePath = defenderSprite))
        
        return defenders
    
    def update(self, ball, offensive_players):
        ball_carrier = ball.holder
        
        for defender in self.players:
            if ball_carrier:
                self.move_to_target(defender, ball_carrier.x, ball_carrier.y)
                
                #check for tackle
                if self.can_tackle(defender, ball_carrier) and not ball_carrier.isTackled:
                    self.tackle(ball, ball_carrier)
            else:
                self.move_to_target(defender, ball.positionX, ball.positionY)
    
    def move_to_target(self, defender, target_x, target_y):
        dx = target_x - defender.x
        dy = target_y - defender.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 0:
            speed = 2
            defender.x += (dx/distance) * speed
            defender.y += (dy/distance) * speed
    
    def can_tackle(self, defender, ball_carrier):
        dx = defender.x - ball_carrier.x
        dy = defender.y - ball_carrier.y
        distance = (dx**2 + dy**2)**0.5
        return distance < self.tackle_distance
    
    def tackle(self, ball, ball_carrier):
        #start the tackle animation
        ball_carrier.startTackle()
        #reset the ball
        ball.holder = None
        ball.inFlight = False
        ball.velocityX = 0
        ball.velocityY = 0