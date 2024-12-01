from Player import *
class Defender(Player):
    def __init__(self, x, y, spritePath=None):
        super().__init__(x, y, spritePath=spritePath)
        self.speed = 4
        self.target = None
        self.state = 'zone'
        self.assignedZone = {'x': x, 'y': y}
        self.tackleRadius = 30
        self.tackleProbability = 0.7  # 70% chance of successful tackle when in range
        
    def attemptTackle(self, ballCarrier, app):
        if not ballCarrier:
            return False
            
        # Calculate distance to ball carrier
        dx = self.x - ballCarrier.x
        dy = self.y - ballCarrier.y
        distance = (dx**2 + dy**2)**0.5
        
        # Check if within tackle range
        if distance <= self.tackleRadius:
            # Randomize tackle success based on probability
            if random.random() < self.tackleProbability:
                self.executeTackle(ballCarrier, app)
                return True
                
        return False
        
    def executeTackle(self, ballCarrier, app):
        app.state = 'tackling'
        app.tackler = self
        app.tackled = ballCarrier
        app.tackleAnimationFrame = 0
        app.ball.holder = None
        
        # Calculate tackle direction
        dx = ballCarrier.x - self.x
        dy = ballCarrier.y - self.y
        angle = math.atan2(dy, dx)
        
        # Set tackle animation parameters
        app.tackleStartX = ballCarrier.x
        app.tackleStartY = ballCarrier.y
        app.tackleEndX = ballCarrier.x + math.cos(angle) * 20
        app.tackleEndY = ballCarrier.y + math.sin(angle) * 20

def handleTackle(app):
    if app.state != 'tackling':
        return
        
    # Tackle animation takes 20 frames
    if app.tackleAnimationFrame < 20:
        progress = app.tackleAnimationFrame / 20
        
        # Move players during tackle
        app.tackled.x = app.tackleStartX + (app.tackleEndX - app.tackleStartX) * progress
        app.tackled.y = app.tackleStartY + (app.tackleEndY - app.tackleStartY) * progress
        app.tackler.x = app.tackled.x - 20  # Keep defender close
        app.tackler.y = app.tackled.y
        
        # Update ball position
        app.ball.positionX = app.tackled.x
        app.ball.positionY = app.tackled.y
        
        app.tackleAnimationFrame += 1
    else:
        # Tackle animation complete
        calculateYardsGained(app)
        app.state = 'playOver'
        
def calculateYardsGained(app):
    yardsGained = (app.tackled.x - app.startLineX) / 30  # Approximate yards
    app.yardsGained = round(yardsGained, 1)
    
    # Update down and distance
    app.currentDown += 1
    app.yardsToGo -= app.yardsGained
    
    if app.yardsGained >= app.yardsToGo:
        app.currentDown = 1
        app.yardsToGo = 10
    elif app.currentDown > 4:
        app.state = 'turnover'