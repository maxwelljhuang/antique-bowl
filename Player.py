from cmu_graphics import *

class Player:
    def __init__(self, x, y, spritePath='stance.png', isQuarterback=False):
        #player attributes
        self.x = x
        self.y = y
        self.spritePath = spritePath
        self.isQuarterback = isQuarterback
        self.speed = 5
        self.animationFrame = 0
        self.animationCounter = 0
        self.frameDelay = 3
        
        #tackle animation
        self.isTackled = False
        self.tackleFrames = [
            'tackle-animation/tackle1.png',
            'tackle-animation/tackle2.png',
            'tackle-animation/tackle3.png'
        ]
        self.currentTackleFrame = 0
        self.tackleAnimationDelay = 5
        self.tackleAnimationCounter = 0
        self.tackleAnimationComplete = False
    
    def startTackle(self):
        self.isTackled = True
        self.currentTackleFrame = 0
        self.tackleAnimationCounter = 0
        self.tackleAnimationComplete = False
        self.speed = 0
    
    def updateTackleAnimation(self):
        if self.isTackled and not self.tackleAnimationComplete:
            self.tackleAnimationCounter += 1
            if self.tackleAnimationCounter >= self.tackleAnimationDelay:
                self.currentTackleFrame += 1
                self.tackleAnimationCounter = 0
                
                if self.currentTackleFrame >= len(self.tackleFrames):
                    self.tackleAnimationComplete = True
                    self.currentTackleFrame = len(self.tackleFrames) - 1
    
    def draw(self, camera_x, camera_y, scale_factor):
        screen_x = (self.x - camera_x) * scale_factor
        screen_y = (self.y - camera_y) * scale_factor
        
        if self.isTackled:
            sprite = self.tackleFrames[self.currentTackleFrame]
        else:
            sprite = self.spritePath
            
        drawImage(sprite, screen_x, screen_y, width=65, height=110) 
    
    def moveForward(self):
        if not self.isTackled:
            self.x += self.speed