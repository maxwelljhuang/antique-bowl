from Player import Player  # Ensure Player is defined in Player.py or adjust the import path

def setupFormation(ball_x, ball_y):
    """
    Set up player positions horizontally relative to the ball placement.
    :param ball_x: X-coordinate of the ball.
    :param ball_y: Y-coordinate of the ball.
    :return: A list of Player objects in their formation.
    """
    players = []

    # 7 Linemen (horizontal line centered around the ball, same y-coordinate)
    linemen_x_offsets = [-120, -90, -60, -30, 30, 60, 90]
    for i, offset in enumerate(linemen_x_offsets):
        players.append(Player(ball_x + offset, ball_y, f'/Users/max/antique-bowl/linemen-animation/linestance.png'))

    # Quarterback (directly behind the center lineman)
    players.append(Player(ball_x, ball_y + 50, '/Users/max/antique-bowl/stance.png'))  # QB sprite

    # Running Back (further behind the quarterback)
    players.append(Player(ball_x, ball_y + 100, '/Users/max/antique-bowl/stance.png'))  # RB sprite

    # Wide Receivers (far left and right of the linemen line)
    players.append(Player(ball_x - 200, ball_y, '/Users/max/antique-bowl/stance.png'))  # Left receiver
    players.append(Player(ball_x + 200, ball_y, '/Users/max/antique-bowl/stance.png'))  # Right receiver

    return players
