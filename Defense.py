from Player import Player

class Defense:
    def __init__(self, ballX, ballY, defenderSprite):
        self.players = self.setup_formation(ballX, ballY, defenderSprite)
        self.tackle_distance = 30  # Distance required to tackle ball carrier
    
    def setup_formation(self, ballX, ballY, defenderSprite):
        defenders = []
        
        # Create 7 defenders in a basic formation
        # Three defenders up front, positioned to the right of the ball
        for i in range(3):
            x = ballX + 60 + (i * 40)  # Start 60 pixels to the right of ball, space them 40 pixels apart
            y = ballY - 20  # 20 pixels behind the ball
            defenders.append(Player(x, y, spritePath=defenderSprite))
        
        # Four defenders in the backfield, also to the right
        for i in range(4):
            x = ballX + 40 + (i * 50)  # Start 40 pixels to the right, space them 50 pixels apart
            y = ballY - 80  # 80 pixels back from the line
            defenders.append(Player(x, y, spritePath=defenderSprite))
        
        return defenders
    
    def update(self, ball, offensive_players):
        # Find the ball carrier
        ball_carrier = ball.holder
        
        # Update each defender's position
        for defender in self.players:
            if ball_carrier:
                # Move towards ball carrier
                self.move_to_target(defender, ball_carrier.x, ball_carrier.y)
            else:
                # If ball is in the air, move towards the ball
                self.move_to_target(defender, ball.positionX, ball.positionY)
            
            # Check for tackle
            if ball_carrier and self.can_tackle(defender, ball_carrier):
                self.tackle(ball)
    
    def move_to_target(self, defender, target_x, target_y):
        # Calculate direction to target
        dx = target_x - defender.x
        dy = target_y - defender.y
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 0:
            # Move defender towards target at reduced speed
            speed = 2
            defender.x += (dx/distance) * speed
            defender.y += (dy/distance) * speed
    
    def can_tackle(self, defender, ball_carrier):
        dx = defender.x - ball_carrier.x
        dy = defender.y - ball_carrier.y
        distance = (dx**2 + dy**2)**0.5
        return distance < self.tackle_distance
    
    def tackle(self, ball):
        # Reset ball and ball carrier on tackle
        ball.holder = None
        ball.inFlight = False
        ball.velocityX = 0
        ball.velocityY = 0