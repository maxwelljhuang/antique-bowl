from cmu_graphics import *

class Field:
    def __init__(self, field_image_path, field_width, field_height, view_width, view_height):
        """
        Initializes the field with the given image and dimensions.
        """
        self.field_image_path = field_image_path
        self.field_width = field_width
        self.field_height = field_height
        self.view_width = view_width
        self.view_height = view_height
        self.camera_x = 0
        self.camera_y = 0

        # Calculate uniform scale factor to fit the viewport without stretching
        self.scale_factor = max(view_width / field_width, view_height / field_height)

    def updateCamera(self, ball_x, ball_y):
        """
        Updates the camera position to center on the ball while ensuring it stays within bounds.
        """
        # Center the camera on the ball
        self.camera_x = ball_x - (self.view_width / self.scale_factor) / 2
        self.camera_y = ball_y - (self.view_height / self.scale_factor) / 2

        # Clamp the camera to the field's boundaries
        self.camera_x = max(0, min(self.camera_x, self.field_width - self.view_width / self.scale_factor))
        self.camera_y = max(0, min(self.camera_y, self.field_height - self.view_height / self.scale_factor))

    def drawField(self):
        """
        Draws the field, scaled to maintain its aspect ratio.
        """
        drawImage(self.field_image_path,
                  -self.camera_x * self.scale_factor,
                  -self.camera_y * self.scale_factor,
                  width=self.field_width * self.scale_factor,
                  height=self.field_height * self.scale_factor)