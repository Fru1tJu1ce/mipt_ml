import game.wrapped_flappy_bird as game
from game.settings import Settings
import game.ai_bird as ai

import sys
import pygame
from pygame.locals import *
import numpy as np


def main():
    st = Settings()
    action_terminal = game.GameState(st)

    # AI Q_table generate
    #Q = ai.generate_q_table() # Uncomment this line to start fresh Q_learning and comment next line
    Q = np.loadtxt('Q_tables_working/Q_table.txt').reshape((288, 512, 2)) # LOAD EXISTING Q_TABLE!!!

    while True:
        # input_actions[0] == 1: do nothing
        # input_actions[1] == 1: flap the bird
        #input_actions = [1, 0]

        # Берем значение из Q_table: нужно ли прыгать в данной ситуации?
        x1, y1 = ai.convert(action_terminal.playerx, action_terminal.playery,
                            action_terminal.lowerPipes)
        jump = ai.ai_jump(x1, y1, Q)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):

                # Saving progress
                Q_reshaped = Q.reshape(Q.shape[0], -1)
                np.savetxt('Q_table.txt', Q_reshaped)

                pygame.quit()
                sys.exit()
            #if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
        if jump:
            input_actions = [0, 1]
        else:
            input_actions = [1, 0]

        action_terminal.frame_step(input_actions, x1, y1, Q)


if __name__ == '__main__':
    # ручная игра
    main()
