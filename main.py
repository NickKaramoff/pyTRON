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

width, height = 600, 660  # window dimensions
offset = height - width  # vertical space at top of window
wall_size = 15
caption = "pyTRON"
fps = 60

pygame.init()


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


def new_game():
    new_p1 = Player(poz[0], poz[1], (2, 0), P1_COLOR)
    new_p2 = Player(width - poz[0], poz[1], (-2, 0), P2_COLOR)
    return new_p1, new_p2


# Options
screen = pygame.display.set_mode((width, height))  # creates window
pygame.display.set_caption(caption)  # sets window title
font = pygame.font.Font(None, 72)
boosts_font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
check_time = time.time()
poz = [50, (height - offset) / 2]

# create players and add to list
objects = list()
path = list()
p1, p2 = new_game()
objects.append(p1)
path.append((p1.rect, '1'))
objects.append(p2)
path.append((p2.rect, '2'))

player_score = [0, 0]  # current player score

walls = [pygame.Rect([0, offset, wall_size, height]),
         pygame.Rect([0, offset, width, wall_size]),
         pygame.Rect([width - wall_size, offset, wall_size, height]),
         pygame.Rect([0, height - wall_size, width, wall_size])]

finish = False
new = False

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

    for wall in walls:
        pygame.draw.rect(screen, (42, 42, 42), wall, 0)  # draws the walls

    for o in objects:
        if time.time() - o.start_boost >= 0.5:  # limits boost to 0.5s
            o.boost = False

        if (o.rect, '1') in path or (o.rect, '2') in path \
                or o.rect.collidelist(walls) > -1:

            if (time.time() - check_time) >= 0.1:
                check_time = time.time()
                if o.color == P1_COLOR:
                    player_score[1] += 1
                else:
                    player_score[0] += 1
                new = True
                p1, p2 = new_game()
                objects = [p1, p2]
                path = [(p1.rect, '1'), (p2.rect, '2')]
                break

        else:  # not yet traversed
            path.append(
                (o.rect, '1')) if o.color == P1_COLOR else path.append(
                (o.rect, '2'))
        o.__draw__()
        o.__move__()

    for wall in path:
        if new is True:
            path = []
            new = False
            break
        if wall[1] == '1':
            pygame.draw.rect(screen, P1_COLOR, wall[0], 0)
        else:
            pygame.draw.rect(screen, P2_COLOR, wall[0], 0)

    # if len(path) > 50:
    #     path.pop(0)

    score_text = font.render(
        '{0} : {1}'.format(player_score[0], player_score[1]), 1, (255, 255, 51))
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = int(width / 2)
    score_text_pos.centery = int(offset / 2)
    screen.blit(score_text, score_text_pos)

    boosts_p1 = boosts_font.render("%d boosts" % objects[0].boosts, 1, P1_COLOR)
    boosts_p1_pos = boosts_p1.get_rect()
    boosts_p1_pos.centerx = int(boosts_p1.get_width() / 2) + wall_size + 10
    boosts_p1_pos.centery = \
        offset + int(boosts_p1.get_height() / 2) + wall_size + 10
    screen.blit(boosts_p1, boosts_p1_pos)

    boosts_p2 = boosts_font.render("%d boosts" % objects[1].boosts, 1, P2_COLOR)
    boosts_p2_pos = boosts_p2.get_rect()
    boosts_p2_pos.centerx = \
        width - int(boosts_p2.get_width() / 2) - wall_size - 10
    boosts_p2_pos.centery = \
        offset + int(boosts_p2.get_height() / 2) + wall_size + 10
    screen.blit(boosts_p2, boosts_p2_pos)

    if player_score[0] >= 10 or player_score[1] >= 10:
        finish = True

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
