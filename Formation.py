from Player import Player

def setupFormation(ball_x, ball_y):
    """
    Set up an offensive formation with 7 linemen, 2 wide receivers, 1 quarterback, and 1 running back.
    :param ball_x: X-coordinate of the ball (line of scrimmage center).
    :param ball_y: Y-coordinate of the ball (line of scrimmage).
    :return: A list of Player objects in their formation.
    """
    players = []

    # 7 Linemen: Horizontally aligned around the ball
    linemen_y_offsets = [-90, -60, -30, 0, 30, 60, 90]  # Vertical offsets from the ball
    for i, offset in enumerate(linemen_y_offsets):
        players.append(Player(ball_x, ball_y + offset, f'/Users/max/antique-bowl/linemen-animation/linestance.png'))

    # Quarterback directly behind the center lineman
    players.append(Player(ball_x - 50, ball_y, '/Users/max/antique-bowl/stance.png'))  # QB sprite

    # Running Back further behind the quarterback
    players.append(Player(ball_x - 90, ball_y, '/Users/max/antique-bowl/stance.png'))  # RB sprite

    # 2 Wide Receivers: Far left and far right, at the same y-coordinate as linemen
    players.append(Player(ball_x - 25, ball_y - 110, '/Users/max/antique-bowl/stance.png'))  # Left receiver
    players.append(Player(ball_x - 25, ball_y + 110, '/Users/max/antique-bowl/stance.png'))  # Right receiver

    return players
