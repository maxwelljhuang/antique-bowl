class GameState:
    def __init__(self, initial_ball_position):
        self.down = 1
        self.first_down_line = initial_ball_position + (200)  
        self.initial_ball_position = initial_ball_position
        self.yards_to_go = 10
        self.game_clock = 60
        self.score = {'Team A': 0, 'Team B': 0}
        self.game_over = False
        
    def update_down(self, current_ball_position):
        # If made it to first down
        if current_ball_position >= self.first_down_line:
            # Reset down to 1 and set new first down line
            self.down = 1
            self.first_down_line = current_ball_position + (200)
            self.yards_to_go = 10
            self.initial_ball_position = current_ball_position
            return 'continue'
        else:
            pixels_to_go = self.first_down_line - current_ball_position
            self.yards_to_go = int(pixels_to_go / 20)
            if self.down >= 4:
                self.game_over = True
                return 'game_over'
            return 'continue'
            
    def next_down(self, current_ball_position):
        # Only increment down if we haven't reached first down
        if current_ball_position < self.first_down_line:
            self.down += 1
            if self.down > 4:
                self.game_over = True
                return 'game_over'
        self.initial_ball_position = current_ball_position
        return 'continue'

    def get_down_text(self):
        suffix = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th'}
        return f"{self.down}{suffix[self.down]} Down & {self.yards_to_go}"

    def reset_game(self, initial_ball_position):
        self.down = 1
        self.first_down_line = initial_ball_position + (200)
        self.initial_ball_position = initial_ball_position
        self.yards_to_go = 10
        self.game_over = False
        
    def reset_touchdown(self, initial_ball_position):
        self.down = 1
        self.first_down_line = initial_ball_position + (200)
        self.initial_ball_position = initial_ball_position
        self.yards_to_go = 10
        self.game_over = False