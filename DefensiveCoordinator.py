from Defender import *
class DefensiveCoordinator:
    def __init__(self, app):
        self.app = app
        self.defenders = []
        self.defensiveFormation = 'base43'  # Can be 'base43', 'cover2', 'blitz', etc.
        
    def setupDefense(self):
        # Clear existing defenders
        self.defenders = []
        
        if self.defensiveFormation == 'base43':
            # Create defensive line (4 players)
            for i in range(4):
                x = self.app.ball.positionX + 50  # Line up across from offensive line
                y = self.app.field.field_height/2 - 80 + i*40  # Spread across line
                defender = Defender(x, y, 'defensive_sprite.png')
                self.defenders.append(defender)
            
            # Create linebackers (3 players)
            for i in range(3):
                x = self.app.ball.positionX + 120  # Second level
                y = self.app.field.field_height/2 - 60 + i*60
                defender = Defender(x, y, 'linebacker_sprite.png')
                self.defenders.append(defender)
            
            # Create defensive backs (4 players)
            for i in range(4):
                x = self.app.ball.positionX + 200  # Deep coverage
                y = self.app.field.field_height/2 - 90 + i*60
                defender = Defender(x, y, 'db_sprite.png')
                self.defenders.append(defender)
    
    def updateDefense(self):
        ballCarrier = self.app.ball.holder
        tackles = []
        
        # Update each defender's AI
        for defender in self.defenders:
            tackle = defender.updateAI(ballCarrier, self.app.ball, self.app.receivers)
            if tackle:
                tackles.append(defender)
        
        # Handle any tackles
        if tackles and ballCarrier:
            # Play is over due to tackle
            self.app.state = 'playOver'
            return True
            
        return False
    
    def callDefensivePlay(self, formation):
        self.defensiveFormation = formation
        
        if formation == 'cover2':
            # Assign deep zones to safeties
            self.defenders[-2].assignZone(self.app.ball.positionX + 250, 
                                       self.app.field.field_height/3)
            self.defenders[-1].assignZone(self.app.ball.positionX + 250, 
                                       2*self.app.field.field_height/3)
            
            # Assign man coverage to corners
            self.defenders[-4].assignManCoverage(self.app.receivers[0])
            self.defenders[-3].assignManCoverage(self.app.receivers[1])
        
        elif formation == 'blitz':
            # Send more defenders after QB
            for defender in self.defenders[:6]:  # Front 6 players blitz
                defender.state = 'pursue'
                defender.target = self.app.quarterback