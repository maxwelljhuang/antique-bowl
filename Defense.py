from Player import Player
import math
import random

''' 
Refernces: 
Rule Based AI - https://realpython.com/tic-tac-toe-ai-python/ , https://stackoverflow.com/questions/53421492/python-rule-based-engine 
'''

class Defense:
    def __init__(self, ballX, ballY, defenderSprite):
        self.players = self.setup_formation(ballX, ballY, defenderSprite)
        self.tackle_distance = 30
        self.pursuit_speed = 3
        self.chase_mode = "contain"
        self.running_frames = [f'run-animation/run{i}_cleaned.png' for i in range(1, 7)]
        self.setup_animations()
        
    def setup_animations(self):
        for defender in self.players:
            defender.animationFrame = 0
            defender.animationCounter = 0
            defender.frameDelay = 3
            defender.isRunning = False
            
    def setup_formation(self, ballX, ballY, defenderSprite):
        linemenSpacing = 30
        linemenX = ballX  
        linemenYStart = ballY - 90 
        defenders = []
        
        # Create different types of defenders with increased speeds
        # 3 linemen
        for i in range(3):  
            yOffset = i * linemenSpacing + 30
            defender = Player(linemenX + 35, ballY + yOffset - 90, spritePath=defenderSprite)
            defender.type = "lineman"
            defender.speed = 2.5
            defender.pursuit_range = 50
            defenders.append(defender)
            
        # 2 linebackers
        for i in range(2):
            yOffset = i * linemenSpacing * 2 + 15
            defender = Player(linemenX + 85, ballY + yOffset - 90, spritePath=defenderSprite)
            defender.type = "linebacker"
            defender.speed = 3.5
            defender.pursuit_range = 100
            defenders.append(defender)
            
        # 2 safeties
        for i in range(2):
            yOffset = i * linemenSpacing * 3
            defender = Player(linemenX + 135, ballY + yOffset - 90, spritePath=defenderSprite)
            defender.type = "safety"
            defender.speed = 4.0
            defender.pursuit_range = 150
            defenders.append(defender)
        
        return defenders

    def update(self, ball, offensive_players):
        ball_carrier = ball.holder
        
        for defender in self.players:
            # Update animation when moving
            prev_x = defender.x
            prev_y = defender.y
            
            if ball_carrier:
                if defender.type == "lineman":
                    self.pursue_aggressively(defender, ball_carrier)
                elif defender.type == "linebacker":
                    self.contain_strategy(defender, ball_carrier)
                else:  # safety
                    self.deep_contain(defender, ball_carrier)
                
                if self.can_tackle(defender, ball_carrier):
                    self.tackle(ball, ball_carrier)
            else:
                self.return_to_position(defender, ball)
            
            # Check if defender is moving to update animation
            is_moving = abs(prev_x - defender.x) > 0.1 or abs(prev_y - defender.y) > 0.1
            if is_moving:
                defender.isRunning = True
                defender.animationCounter += 1
                if defender.animationCounter >= defender.frameDelay:
                    defender.animationFrame = (defender.animationFrame + 1) % len(self.running_frames)
                    defender.animationCounter = 0
                defender.spritePath = self.running_frames[defender.animationFrame]
            else:
                defender.isRunning = False
                defender.spritePath = 'stance.png'

    def pursue_aggressively(self, defender, target):
        # Direct pursuit at maximum speed
        dx = target.x - defender.x
        dy = target.y - defender.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            speed = defender.speed * 1.2  # Extra speed for aggressive pursuit
            defender.x += (dx/distance) * speed
            defender.y += (dy/distance) * speed

    def contain_strategy(self, defender, target):
        dx = target.x - defender.x
        dy = target.y - defender.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Try to get ahead of the ball carrier
            anticipation_x = target.x + 50
            
            dx = anticipation_x - defender.x
            speed = defender.speed
            
            # Faster if behind ball carrier
            if defender.x > target.x:
                speed *= 1.2
                
            defender.x += (dx/distance) * speed
            defender.y += (dy/distance) * speed

    def deep_contain(self, defender, target):
        # Safeties stay deeper and wider
        dx = target.x - defender.x + 100  # Stay further ahead
        dy = target.y - defender.y
        if abs(dy) < 50:  # Maintain minimum lateral spacing
            dy = 50 * (1 if dy > 0 else -1)
        
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            speed = defender.speed
            defender.x += (dx/distance) * speed
            defender.y += (dy/distance) * speed

    def return_to_position(self, defender, ball):
        # Return to initial defensive positions
        target_x = ball.positionX + (35 if defender.type == "lineman" else
                                   85 if defender.type == "linebacker" else 135)
        target_y = ball.positionY
        
        dx = target_x - defender.x
        dy = target_y - defender.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            defender.x += (dx/distance) * defender.speed
            defender.y += (dy/distance) * defender.speed

    def can_tackle(self, defender, ball_carrier):
        dx = defender.x - ball_carrier.x
        dy = defender.y - ball_carrier.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < self.tackle_distance
    
    def tackle(self, ball, ball_carrier):
        ball_carrier.startTackle()
        ball.holder = None
        ball.inFlight = False
        ball.velocityX = 0
        ball.velocityY = 0