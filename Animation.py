class Animation:
    def __init__(self, framePaths, frameDelay):
    
        self.frames = framePaths
        self.frameDelay = frameDelay
        self.currentFrameIndex = 0
        self.stepCounter = 0
        self.paused = False

    def update(self):
        if self.paused:
            return
        self.stepCounter += 1
        if self.stepCounter >= self.frameDelay:
            self.currentFrameIndex = (self.currentFrameIndex + 1) % len(self.frames)
            self.stepCounter = 0

    def getCurrentFrame(self):
        return self.frames[self.currentFrameIndex]

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def reset(self):
        self.currentFrameIndex = 0
        self.stepCounter = 0
