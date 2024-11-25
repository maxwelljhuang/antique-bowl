class RPO:
    def __init__(self, quarterback, receivers, runningBack):
        self.quarterback = quarterback
        self.receivers = receivers
        self.runningBack = runningBack

    def decide(self):
 
        # Simple logic: pass if no defender nearby, otherwise run
        if all(abs(receiver.x - self.quarterback.x) > 100 for receiver in self.receivers):
            return 'pass'
        else:
            return 'run'
