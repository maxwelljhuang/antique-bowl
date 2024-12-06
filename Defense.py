from Player import Player
import math
import random

''' 
Refernces: 
Rule Based AI - https://realpython.com/tic-tac-toe-ai-python/ , https://stackoverflow.com/questions/53421492/python-rule-based-engine 
'''
class Defense:
    def setup_formation(self, ballX, ballY, defenderSprite):
        #constants for formation setup
        linemenSpacing = 30
        linemenX = ballX  
        linemenYStart = ballY - 90 
        defenders = []
        
        #create defensive linemen (3 players)
        for i in range(3):  
            yOffset = i * linemenSpacing + 30
            defender = Player(linemenX + 35, ballY + yOffset - 90, spritePath=defenderSprite)
            defender.type = "lineman"
            defender.speed = 2.5  #linemen are slowest but closest to line
            defender.pursuit_range = 50
            defenders.append(defender)
            
        # Create linebackers (2 players)
        for i in range(2):
            yOffset = i * linemenSpacing * 2 + 15
            defender = Player(linemenX + 85, ballY + yOffset - 90, spritePath=defenderSprite)
            defender.type = "linebacker"
            defender.speed = 3.5  #linebackers have medium speed
            defender.pursuit_range = 100
            defenders.append(defender)
            
        #create safeties (2 players)
        for i in range(2):
            yOffset = i * linemenSpacing * 3
            defender = Player(linemenX + 135, ballY + yOffset - 90, spritePath=defenderSprite)
            defender.type = "safety"
            defender.speed = 4.0  #safeties are fastest but start furthest back
            defender.pursuit_range = 150
            defenders.append(defender)
        
        return defenders

    def __init__(self, ballX, ballY, defenderSprite):
        #initialize defense with starting positions and sprites
        self.players = self.setup_formation(ballX, ballY, defenderSprite)
        self.tackle_distance = 30
        self.pursuit_speed = 3
        self.chase_mode = "contain"
        
        #load defender-specific animation frames
        self.running_frames = [
            f'defender-animation/defense{i}.png' for i in range(1, 7)
        ]
        self.setup_animations()
        
    def setup_animations(self):
        #setup animation properties for each defender
        for defender in self.players:
            defender.animationFrame = 0
            defender.animationCounter = 0
            defender.frameDelay = 3
            defender.isRunning = False
            #set initial sprite
            defender.spritePath = self.running_frames[0]

    def update(self, ball, offensive_players):
        #main update loop for defensive behavior
        ball_carrier = ball.holder
        
        for defender in self.players:
            #store previous position for animation checks
            prev_x = defender.x
            prev_y = defender.y
            
            if ball_carrier:
                #different pursuit strategies based on defender type
                if defender.type == "lineman":
                    self.pursue_aggressively(defender, ball_carrier)
                elif defender.type == "linebacker":
                    self.contain_strategy(defender, ball_carrier)
                else:  #safety
                    self.deep_contain(defender, ball_carrier)
                
                # Check if close enough to tackle
                if self.can_tackle(defender, ball_carrier):
                    self.tackle(ball, ball_carrier)
            else:
                #return to base positions when no ball carrier
                self.return_to_position(defender, ball)
            
            #update defender animations based on movement
            is_moving = abs(prev_x - defender.x) > 0.1 or abs(prev_y - defender.y) > 0.1
            if is_moving:
                defender.isRunning = True
                defender.animationCounter += 1
                if defender.animationCounter >= defender.frameDelay:
                    # Update to next animation frame
                    defender.animationFrame = (defender.animationFrame + 1) % 6
                    defender.spritePath = self.running_frames[defender.animationFrame]
                    defender.animationCounter = 0
            else:
                defender.isRunning = False
                #reset to first frame when not moving
                defender.spritePath = self.running_frames[0]

    def pursue_aggressively(self, defender, target):
        #direct pursuit at maximum speed
        dx = target.x - defender.x
        dy = target.y - defender.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            speed = defender.speed * 1.2  #extra speed
            defender.x += (dx/distance) * speed
            defender.y += (dy/distance) * speed

    def contain_strategy(self, defender, target):
        #try to get ahead of ball carrier to cut off lanes
        dx = target.x - defender.x
        dy = target.y - defender.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            #attempt to anticipate ball carrier's movement
            anticipation_x = target.x + 50
            
            dx = anticipation_x - defender.x
            speed = defender.speed
            
            #speed boost if defender is behind ball carrier
            if defender.x > target.x:
                speed *= 1.2
                
            defender.x += (dx/distance) * speed
            defender.y += (dy/distance) * speed

    def deep_contain(self, defender, target):
        #safeties stay deeper and wider to prevent big plays
        dx = target.x - defender.x + 100  
        dy = target.y - defender.y
        if abs(dy) < 50:  
            dy = 50 * (1 if dy > 0 else -1)
        
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            speed = defender.speed
            defender.x += (dx/distance) * speed
            defender.y += (dy/distance) * speed

    def return_to_position(self, defender, ball):
        #return defenders to their base positions relative to ball
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
        #check if defender is close enough to make tackle
        dx = defender.x - ball_carrier.x
        dy = defender.y - ball_carrier.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < self.tackle_distance
    
    def tackle(self, ball, ball_carrier):
        #perform tackle - stop ball carrier and reset ball state
        ball_carrier.startTackle()
        ball.holder = None
        ball.inFlight = False
        ball.velocityX = 0
        ball.velocityY = 0