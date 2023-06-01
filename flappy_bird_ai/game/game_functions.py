import random
import pygame


def getRandomPipe(st):
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapYs = [20, 30, 40, 50, 60, 70, 80, 90]
    index = random.randint(0, len(gapYs) - 1)
    gapY = gapYs[index]

    gapY += int(st.BASEY * 0.2)
    pipeX = st.SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - st.PIPE_HEIGHT},  # upper pipe
        {'x': pipeX, 'y': gapY + st.PIPEGAPSIZE},  # lower pipe
    ]


def showScore(score, st):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0  # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += st.IMAGES['numbers'][digit].get_width()

    Xoffset = (st.SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        st.SCREEN.blit(st.IMAGES['numbers'][digit],
                       (Xoffset, st.SCREENHEIGHT * 0.1))
        Xoffset += st.IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes, st):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = st.IMAGES['player'][0].get_width()
    player['h'] = st.IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= st.BASEY - 1:
        return True
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                                 player['w'], player['h'])

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], st.PIPE_WIDTH,
                                    st.PIPE_HEIGHT)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], st.PIPE_WIDTH,
                                    st.PIPE_HEIGHT)

            # player and upper/lower pipe hitmasks
            pHitMask = st.HITMASKS['player'][pi]
            uHitmask = st.HITMASKS['pipe'][0]
            lHitmask = st.HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask,
                                      uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask,
                                      lHitmask)

            if uCollide or lCollide:
                return True

    return False

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False
