import game.game_functions as gf
import pygame
import game.ai_bird as ai


class GameState:
    def __init__(self, settings):
        self.st = settings
        self.score = self.playerIndex = self.loopIter = 0
        self.playerx = int(self.st.SCREENWIDTH * 0.2)
        self.playery = int((self.st.SCREENHEIGHT - self.st.PLAYER_HEIGHT) / 2)
        self.basex = 0
        self.baseShift = self.st.IMAGES['base'].get_width() - self.st.BACKGROUND_WIDTH

        newPipe1 = gf.getRandomPipe(self.st)
        newPipe2 = gf.getRandomPipe(self.st)
        self.upperPipes = [
            {'x': self.st.SCREENWIDTH, 'y': newPipe1[0]['y']},
            {'x': self.st.SCREENWIDTH + (self.st.SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]
        self.lowerPipes = [
            {'x': self.st.SCREENWIDTH, 'y': newPipe1[1]['y']},
            {'x': self.st.SCREENWIDTH + (self.st.SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        # player velocity, max velocity, downward accleration, accleration on flap
        self.pipeVelX = -4  # player's velocity along Y, default same as playerFlapped
        self.playerVelY = -0  # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10  # max vel along Y, max descend speed
        self.playerMinVelY = -8  # min vel along Y, max ascend speed
        self.playerAccY = 1  # players downward acceleration
        self.playerFlapAcc = -9  # players speed on flapping  # FIXME придумайте, как оптимизировать шаг
        self.playerFlapped = False  # True when player flaps
        self.playerRot = 45  # player's rotation
        self.playerVelRot = 3  # angular speed
        self.playerRotThr = 20  # rotation threshold

    def frame_step(self, input_actions, x1, y1, Q):
        pygame.event.pump()

        reward = 0  # FIXME придумайте стратегию награды/наказания
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        # input_actions[0] == 1: do nothing
        # input_actions[1] == 1: flap the bird
        if input_actions[1] == 1:
            if self.playery > -2 * self.st.PLAYER_HEIGHT:
                self.playerVelY = self.playerFlapAcc
                self.playerFlapped = True

        # check for score
        playerMidPos = self.playerx + self.st.PLAYER_WIDTH / 2
        for pipe in self.upperPipes:
            pipeMidPos = pipe['x'] + self.st.PIPE_WIDTH / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                self.score += 1
                reward += 100  # FIXME придумайте стратегию награды/наказания

        # playerIndex basex change
        if (self.loopIter + 1) % 3 == 0:
            self.playerIndex = next(self.st.PLAYER_INDEX_GEN)
        self.loopIter = (self.loopIter + 1) % 30
        self.basex = -((-self.basex + 100) % self.baseShift)

        # rotate player
        if self.playerRot > -90:
            self.playerRot -= self.playerVelRot

        # player's movement
        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False
            self.playerRot += 45
        self.playery += min(self.playerVelY, self.st.BASEY - self.playery - self.st.PLAYER_HEIGHT)
        if self.playery < 0:
            self.playery = 0

        # move pipes to left
        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            uPipe['x'] += self.pipeVelX
            lPipe['x'] += self.pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < self.upperPipes[0]['x'] < 5:
            newPipe = gf.getRandomPipe(self.st)
            self.upperPipes.append(newPipe[0])
            self.lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if self.upperPipes[0]['x'] < -self.st.PIPE_WIDTH:
            self.upperPipes.pop(0)
            self.lowerPipes.pop(0)

        x2, y2 = ai.convert(self.playerx, self.playery, self.lowerPipes)

        # check if crash here
        isCrash = gf.checkCrash({'x': self.playerx, 'y': self.playery,
                              'index': self.playerIndex},
                             self.upperPipes, self.lowerPipes, self.st)
        if isCrash:
            reward = -5000
            ai.Q_update(Q, x1, y1, input_actions, reward, x2, y2)
            terminal = True
            self.__init__(self.st)
            #reward = -1000  # FIXME придумайте стратегию награды/наказания

        reward = 5

        ai.Q_update(Q, x1, y1, input_actions, reward, x2, y2)

        # draw sprites
        self.st.SCREEN.blit(self.st.IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            self.st.SCREEN.blit(self.st.IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            self.st.SCREEN.blit(self.st.IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        self.st.SCREEN.blit(self.st.IMAGES['base'], (self.basex, self.st.BASEY))

        # Showing score
        gf.showScore(self.score, self.st)

        # Player rotation has a threshold
        visibleRot = self.playerRotThr
        if self.playerRot <= self.playerRotThr:
            visibleRot = self.playerRot
        playerSurface = pygame.transform.rotate(self.st.IMAGES['player'][self.playerIndex], visibleRot)
        self.st.SCREEN.blit(playerSurface, (self.playerx, self.playery))

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        self.st.FPSCLOCK.tick(self.st.FPS)

        return image_data, reward, terminal
