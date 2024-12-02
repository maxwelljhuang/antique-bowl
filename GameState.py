class GameState:
    def __init__(self, initial_ball_position):
        self.down = 1
        # 10 yards = 2000ish pixels?
        self.first_down_line = initial_ball_position + (10 * 200)  
        self.initial_ball_position = initial_ball_position
        self.yards_to_go = 10
        self.game_clock = 60
        self.score = {'Team A': 0, 'Team B': 0}
        
    def update_down(self, current_ball_position):
        #if made to first down
        if current_ball_position >= self.first_down_line:
            #reset down
            self.down = 1
            self.first_down_line = current_ball_position + (10 * 200)
            self.yards_to_go = 10
            self.initial_ball_position = current_ball_position
        else:
            pixels_to_go = self.first_down_line - current_ball_position
            #pixels to yards conversion
            self.yards_to_go = int(pixels_to_go / 200)  
            
    def next_down(self, current_ball_position):
        self.down += 1
        if self.down > 4:
            return 'turnover'
        self.initial_ball_position = current_ball_position
        return 'continue'

    def get_down_text(self):
        suffix = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th'}
        return f"{self.down}{suffix[self.down]} Down & {self.yards_to_go}"