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
        self.scale_factor = max(view_width / field_width, view_height / field_height)
        self.end_zone_left = 0
        self.end_zone_right = field_width

    def updateCamera(self, ball_x, ball_y):
        #calculate the camera's top-left corner to center the ball
        half_view_width = (self.view_width / self.scale_factor) / 2
        half_view_height = (self.view_height / self.scale_factor) / 2

        self.camera_x = ball_x - half_view_width
        self.camera_y = ball_y - half_view_height

        self.camera_x = max(0, min(self.camera_x, self.field_width - self.view_width / self.scale_factor))
        self.camera_y = max(0, min(self.camera_y, self.field_height - self.view_height / self.scale_factor))



    def drawField(self):
        drawImage(
            self.field_image_path,
            -self.camera_x * self.scale_factor,
            -self.camera_y * self.scale_factor,
            width=self.field_width * self.scale_factor,
            height=self.field_height * self.scale_factor
        )

    def isTouchdown(self, ball_x):
        return ball_x <= self.end_zone_left or ball_x >= self.end_zone_right
