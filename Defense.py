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
        defenders = []
        
        # Create 7 defenders in a basic formation
        for i in range(3):
            x = ballX + 60 + (i * 40)
            y = ballY - 20
            defenders.append(Player(x, y, spritePath=defenderSprite))
        
        for i in range(4):
            x = ballX + 40 + (i * 50)
            y = ballY - 80
            defenders.append(Player(x, y, spritePath=defenderSprite))
        
        return defenders
    
    def update(self, ball, offensive_players):
        ball_carrier = ball.holder
        
        for defender in self.players:
            if ball_carrier:
                self.move_to_target(defender, ball_carrier.x, ball_carrier.y)
                
                # Check for tackle
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
        # Start the tackle animation for the ball carrier
        ball_carrier.startTackle()
        
        # Reset ball
        ball.holder = None
        ball.inFlight = False
        ball.velocityX = 0
        ball.velocityY = 0