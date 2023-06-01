import numpy as np


def generate_q_table():
    """Generates Q-table to make decisions"""
    return np.zeros((288, 512, 2), dtype=float)


def ai_jump(x, y, Q):
    """Checks if it's needed to jump"""
    return Q[x][y][1] > Q[x][y][0]


def convert(birdxpos, birdypos, bttm_pipes):
    """Calculating x and y distances to pipe, then dividing them by 10 to reduce number of possible events"""
    if (bttm_pipes[0]['x'] - birdxpos + 34 + 26) < 0:
        x = bttm_pipes[1]['x'] - birdxpos
        y = bttm_pipes[1]['y'] - birdypos
        if (y < 0):
            y = abs(y) + 412
    else:
        x = bttm_pipes[0]['x'] - birdxpos
        y = bttm_pipes[0]['y'] - birdypos
        if (y < 0):
            y = abs(y) + 412
    return int(x / 10), int(y / 10)


def Q_update(Q, x_prev, y_prev, input_actions, reward, x_new, y_new):
    """
    Updating Q_table with formula:
    Q[s(t), a] = (1 - lr) * Q[s(t), a] + lr * (reward + gamma * max(Q[s(t + 1), a]))
    """
    if input_actions == [0, 1]:
        Q[x_prev][y_prev][1] = 0.4 * Q[x_prev][y_prev][1] + (0.6) * (
                reward + max(Q[x_new][y_new][0], Q[x_new][y_new][1]))
    else:
        Q[x_prev][y_prev][0] = 0.4 * Q[x_prev][y_prev][0] + (0.6) * (
                reward + max(Q[x_new][y_new][0], Q[x_new][y_new][1]))
