class GameState:
    def __init__(self, initial_ball_position):
        self.down = 1
        self.first_down_line = initial_ball_position + (10 * 200)  # 10 yards = 2000 pixels
        self.initial_ball_position = initial_ball_position
        self.yards_to_go = 10
        self.game_clock = 60
        self.score = {'Team A': 0, 'Team B': 0}
        
    def update_down(self, current_ball_position):
        # If we passed the first down line
        if current_ball_position >= self.first_down_line:
            # Reset downs and set new first down line
            self.down = 1
            self.first_down_line = current_ball_position + (10 * 200)  # New first down 10 yards ahead
            self.yards_to_go = 10
            self.initial_ball_position = current_ball_position
        else:
            # Update yards to go based on current position
            pixels_to_go = self.first_down_line - current_ball_position
            self.yards_to_go = int(pixels_to_go / 200)  # Convert pixels to yards
            
    def next_down(self, current_ball_position):
        self.down += 1
        if self.down > 4:
            return 'turnover'
        self.initial_ball_position = current_ball_position
        return 'continue'

    def get_down_text(self):
        suffix = {1: 'st', 2: 'nd', 3: 'rd', 4: 'th'}
        return f"{self.down}{suffix[self.down]} Down & {self.yards_to_go}"