import pygame
import time

#
# PARAMETERS
#

# Colors

BLACK = (0, 0, 0)
YELLOW = (229, 226, 71)
CYAN = (118, 214, 202)

BG_COLOR = BLACK
P1_COLOR = CYAN  # player 1 trail color
P2_COLOR = YELLOW  # player 2 trail color

# Window

WIDTH, HEIGHT = 600, 660  # window dimensions
OFFSET = HEIGHT - WIDTH  # vertical space at top of window
WALL_WIDTH = 15
WINDOW_CAPTION = "pyTRON"
GAME_FPS = 60

pygame.init()


#
# PLAYER
#

class Player:
    def __init__(self, x, y, direction, color):
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.speed = 1  # player speed
        self.direction = direction  # player direction
        self.color = color
        self.boost = False  # is boost active
        self.start_boost = time.time()  # used to control boost length
        self.boosts = 3
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2,
                                2)  # player rect object

    def __draw__(self):
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  # redefines rect
        pygame.draw.rect(screen, self.color, self.rect,
                         0)  # draws player onto screen

    def __move__(self):
        if not self.boost:  # player isn't currently boosting
            self.x += self.direction[0]
            self.y += self.direction[1]
        else:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2

    def __boost__(self):
        if self.boosts > 0:
            self.boosts -= 1
            self.boost = True
            self.start_boost = time.time()


#
# SETUP
#


# Options
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # creates window
pygame.display.set_caption(WINDOW_CAPTION)  # sets window title
SCORE_FONT = pygame.font.Font(None, 72)
BOOSTS_FONT = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
check_time = time.time()
start_pos = [50, (HEIGHT - OFFSET) / 2]


def new_game():
    new_p1 = Player(start_pos[0], start_pos[1], (2, 0), P1_COLOR)
    new_p2 = Player(WIDTH - start_pos[0], start_pos[1], (-2, 0), P2_COLOR)
    return new_p1, new_p2


# create players and add to list
objects = list()
tails = list()
p1, p2 = new_game()
objects.append(p1)
tails.append((p1.rect, '1'))
objects.append(p2)
tails.append((p2.rect, '2'))

players_score = [0, 0]  # current players score

SCREEN_FRAME = [pygame.Rect([0, OFFSET, WALL_WIDTH, HEIGHT]),
                pygame.Rect([0, OFFSET, WIDTH, WALL_WIDTH]),
                pygame.Rect([WIDTH - WALL_WIDTH, OFFSET, WALL_WIDTH, HEIGHT]),
                pygame.Rect([0, HEIGHT - WALL_WIDTH, WIDTH, WALL_WIDTH])]

finish = False
new = False

#
# GAME
#

while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finish = True

            # === Player 1 === #
            if event.key == pygame.K_w:
                objects[0].direction = (0, -2)
            elif event.key == pygame.K_s:
                objects[0].direction = (0, 2)
            elif event.key == pygame.K_a:
                objects[0].direction = (-2, 0)
            elif event.key == pygame.K_d:
                objects[0].direction = (2, 0)
            elif event.key == pygame.K_TAB:
                objects[0].__boost__()

            # === Player 2 === #
            if event.key == pygame.K_UP:
                objects[1].direction = (0, -2)
            elif event.key == pygame.K_DOWN:
                objects[1].direction = (0, 2)
            elif event.key == pygame.K_LEFT:
                objects[1].direction = (-2, 0)
            elif event.key == pygame.K_RIGHT:
                objects[1].direction = (2, 0)
            elif event.key == pygame.K_RSHIFT:
                objects[1].__boost__()

    screen.fill(BG_COLOR)

    for tail_wall in SCREEN_FRAME:
        pygame.draw.rect(screen, (42, 42, 42), tail_wall, 0)  # draws the walls

    for o in objects:
        if time.time() - o.start_boost >= 0.5:  # limits boost to 0.5s
            o.boost = False

        if (o.rect, '1') in tails or (o.rect, '2') in tails \
                or o.rect.collidelist(SCREEN_FRAME) > -1:

            if (time.time() - check_time) >= 0.1:
                check_time = time.time()
                if o.color == P1_COLOR:
                    players_score[1] += 1
                else:
                    players_score[0] += 1
                new = True
                p1, p2 = new_game()
                objects = [p1, p2]
                tails = [(p1.rect, '1'), (p2.rect, '2')]
                break

        else:  # not yet traversed
            tails.append(
                (o.rect, '1')) if o.color == P1_COLOR \
                else tails.append((o.rect, '2'))
        o.__draw__()
        o.__move__()

    for tail_wall in tails:
        if new is True:
            tails = []
            new = False
            break
        if tail_wall[1] == '1':
            pygame.draw.rect(screen, P1_COLOR, tail_wall[0], 0)
        else:
            pygame.draw.rect(screen, P2_COLOR, tail_wall[0], 0)

    # if len(path) > 50:
    #     path.pop(0)

    score_text = SCORE_FONT.render('%d : %d' % (players_score[0],
                                                players_score[1]),
                                   1,
                                   (255, 255, 51))
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = int(WIDTH / 2)
    score_text_pos.centery = int(OFFSET / 2)
    screen.blit(score_text, score_text_pos)

    boosts_p1 = BOOSTS_FONT.render("%d boosts" % objects[0].boosts, 1, P1_COLOR)
    boosts_p1_pos = boosts_p1.get_rect()
    boosts_p1_pos.centerx = int(boosts_p1.get_width() / 2) + WALL_WIDTH + 10
    boosts_p1_pos.centery = \
        OFFSET + int(boosts_p1.get_height() / 2) + WALL_WIDTH + 10
    screen.blit(boosts_p1, boosts_p1_pos)

    boosts_p2 = BOOSTS_FONT.render("%d boosts" % objects[1].boosts, 1, P2_COLOR)
    boosts_p2_pos = boosts_p2.get_rect()
    boosts_p2_pos.centerx = \
        WIDTH - int(boosts_p2.get_width() / 2) - WALL_WIDTH - 10
    boosts_p2_pos.centery = \
        OFFSET + int(boosts_p2.get_height() / 2) + WALL_WIDTH + 10
    screen.blit(boosts_p2, boosts_p2_pos)

    if players_score[0] >= 10 or players_score[1] >= 10:
        finish = True

    pygame.display.flip()
    clock.tick(GAME_FPS)

pygame.quit()
