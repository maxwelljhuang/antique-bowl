from cmu_graphics import *

# Load the original image

original_sprite = Image('field.png', 0, 0)

# Set the display (window) size and desired zoom level
display_width, display_height = 800, 600
zoom_factor = 2  # Increase to zoom in more (higher values show less of the field)

# Set the canvas to the display size
app.width = display_width
app.height = display_height

# Create a scaled image by applying the zoom factor to its width and height
sprite = Image('field.png', 0, 0, width=original_sprite.width * zoom_factor, height=original_sprite.height * zoom_factor)

# Initial view center (starting position)
view_center_x = sprite.width // 2
view_center_y = sprite.height // 2

def update_view():
    # Position the sprite so that the view center is centered in the display
    sprite.centerX = display_width // 2 - (view_center_x - display_width // 2)
    sprite.centerY = display_height // 2 - (view_center_y - display_height // 2)

def onKeyHold(keys):
    global view_center_x, view_center_y
    # Arrow keys to move the view
    if 'left' in keys:
        view_center_x = max(view_center_x - 10, display_width // 2)
    if 'right' in keys:
        view_center_x = min(view_center_x + 10, sprite.width - display_width // 2)
    if 'up' in keys:
        view_center_y = max(view_center_y - 10, display_height // 2)
    if 'down' in keys:
        view_center_y = min(view_center_y + 10, sprite.height - display_height // 2)

    update_view()

# Set up the initial view
update_view()

# Run the app
app.run()
