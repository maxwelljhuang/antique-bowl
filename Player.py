from cmu_graphics import *

class Player:
    def __init__(self, x, y, sprite_path, width=40, height=40):
        self.x = x
        self.y = y
        self.sprite_path = sprite_path
        self.width = width
        self.height = height

    def draw(self, camera_x, camera_y, scale_factor):
        # Calculate screen position relative to the camera
        screen_x = (self.x - camera_x) * scale_factor
        screen_y = (self.y - camera_y) * scale_factor
        # Scale the sprite size
        scaled_width = self.width * scale_factor
        scaled_height = self.height * scale_factor
        # Draw the player's sprite
        drawImage(self.sprite_path,
                  screen_x - scaled_width / 2,  # Center horizontally
                  screen_y - scaled_height / 2,  # Center vertically
                  width=scaled_width,
                  height=scaled_height)
    