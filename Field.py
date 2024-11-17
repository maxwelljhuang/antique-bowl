from cmu_graphics import *

class Field:
    def __init__(self, field_image_path, field_width, field_height, view_width, view_height):
        """
        Initializes the field with the given image and dimensions.
        :param field_image_path: Path to the field image.
        :param field_width: Total width of the field in pixels.
        :param field_height: Total height of the field in pixels.
        :param view_width: Width of the visible portion of the field (viewport).
        :param view_height: Height of the visible portion of the field (viewport).
        """
        self.field_image_path = field_image_path
        self.field_width = field_width
        self.field_height = field_height
        self.view_width = view_width
        self.view_height = view_height
        self.camera_x = 0
        self.camera_y = 0

    def updateCamera(self, ball_x, ball_y):
        """
        Updates the camera position to center on the ball, ensuring the viewport stays within the field bounds.
        :param ball_x: The x-coordinate of the ball.
        :param ball_y: The y-coordinate of the ball.
        """
        # Center the camera on the ball
        self.camera_x = ball_x - self.view_width // 2
        self.camera_y = ball_y - self.view_height // 2

        # Clamp the camera within field boundaries
        self.camera_x = max(0, min(self.camera_x, self.field_width - self.view_width))
        self.camera_y = max(0, min(self.camera_y, self.field_height - self.view_height))

    def drawField(self):
        """
        Draws the portion of the field visible in the current camera view.
        """
        drawImage(self.field_image_path, -self.camera_x, -self.camera_y)
