import pygame
import game.flappy_bird_utils as flappy_bird_utils
from itertools import cycle


class Settings:
    FPS = 50
    SCREENWIDTH = 288
    SCREENHEIGHT = 512

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    IMAGES, HITMASKS = flappy_bird_utils.load()
    PIPEGAPSIZE = 100  # gap between upper and lower part of pipe
    BASEY = SCREENHEIGHT * 0.79

    PLAYER_WIDTH = IMAGES['player'][0].get_width()
    PLAYER_HEIGHT = IMAGES['player'][0].get_height()
    PIPE_WIDTH = IMAGES['pipe'][0].get_width()
    PIPE_HEIGHT = IMAGES['pipe'][0].get_height()
    BACKGROUND_WIDTH = IMAGES['background'].get_width()

    PLAYER_INDEX_GEN = cycle([0, 1, 2, 1])
