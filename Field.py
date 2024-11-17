from cmu_graphics import *

class Field:
    def __init__(self, field_image_path, field_width, field_height, view_width, view_height):
        self.field_image_path = field_image_path
        self.field_width = field_width
        self.field_height = field_height
        self.view_width = view_width
        self.view_height = view_height
        self.camera_x = 0
        self.camera_y = 0

    def updateCamera(self, ball_x, ball_y):
        self.camera_x = max(0, min(ball_x - self.view_width // 2, self.field_width - self.view_width))
        self.camera_y = max(0, min(ball_y - self.view_height // 2, self.field_height - self.view_height))

    def drawField(self):
        if self.field_image_path:
            try:
                drawImage(
                    self.field_image_path,
                    -self.camera_x, -self.camera_y,
                    width=self.field_width,
                    height=self.field_height
                )
            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            drawRect(
                -self.camera_x, -self.camera_y,
                self.field_width, self.field_height,
                fill="green"
            )
