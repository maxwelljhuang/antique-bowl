from cmu_graphics import *
#run, pass, option
class rpo(app):

    # Initialize the game state
    app.stepsPerSecond = 60

    # Ball and player positions
    ball = Circle(200, 300, 10, fill='brown')
    player = Circle(200, 300, 20, fill='blue')
    ball_in_hand = True  # Ball starts with the player

    # Dragging variables
    is_dragging = False
    drag_start = None

    # Function to throw the ball
    def throw_ball(end_x, end_y):
        ball.centerX = player.centerX
        ball.centerY = player.centerY
        ball.dx = (end_x - ball.centerX) / 10
        ball.dy = (end_y - ball.centerY) / 10

    # Function to hand off the ball
    def hand_off_ball():
        global ball_in_hand
        ball_in_hand = True
        ball.centerX = player.centerX
        ball.centerY = player.centerY

    # Mouse press (start dragging)
    def onMousePress(mouseX, mouseY):
        global is_dragging, drag_start
        if ball_in_hand:  # Start dragging only if the player has the ball
            is_dragging = True
            drag_start = (mouseX, mouseY)

    # Mouse release (end dragging)
    def onMouseRelease(mouseX, mouseY):
        global is_dragging, ball_in_hand
        if is_dragging:
            is_dragging = False
            drag_end = (mouseX, mouseY)
            
            if drag_start:  # Check if it was a valid drag
                drag_distance = ((drag_end[0] - drag_start[0])**2 + (drag_end[1] - drag_start[1])**2)**0.5
                if drag_distance > 50:  # Long drag -> throw
                    throw_ball(mouseX, mouseY)
                    ball_in_hand = False
                else:  # Short drag -> hand off
                    hand_off_ball()

    # Run the ball by moving the player
    def onMouseDrag(mouseX, mouseY):
        if ball_in_hand:
            player.centerX = mouseX
            player.centerY = mouseY
            ball.centerX = mouseX
            ball.centerY = mouseY

    # Update ball position for throws
    def onStep():
        if not ball_in_hand:
            ball.centerX += ball.dx
            ball.centerY += ball.dy

    # Draw everything
    def redrawAll():
        drawLabel("Drag player to run or pass the ball.", 200, 20, size=14)
        ball.draw()
        player.draw()
cmu_graphics.run()
