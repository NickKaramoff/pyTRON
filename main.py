import pygame
import time

pygame.init()
BLACK = (0, 0, 0)  # colours for use in window
P1_COLOUR = (255, 255, 0)  # player 1 trail colour
P2_COLOUR = (255, 0, 255)  # player 2 trail colour


class Player:
    def __init__(self, x, y, b, c):
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.speed = 1  # player speed
        self.bearing = b  # player direction
        self.colour = c
        self.boost = False  # is boost active
        self.start_boost = time.time()  # used to control boost length
        self.boosts = 3
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2,
                                2)  # player rect object

    def __draw__(self):
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  # redefines rect
        pygame.draw.rect(screen, self.colour, self.rect,
                         0)  # draws player onto screen

    def __move__(self):
        if not self.boost:  # player isn't currently boosting
            self.x += self.bearing[0]
            self.y += self.bearing[1]
        else:
            self.x += self.bearing[0] * 2
            self.y += self.bearing[1] * 2

    def __boost__(self):
        if self.boosts > 0:
            self.boosts -= 1
            self.boost = True
            self.start_boost = time.time()


def new_game():
    new_p1 = Player(poz[0], poz[1], (0, 2), P1_COLOUR)
    new_p2 = Player(poz[0] + 50, poz[1], (0, 2), P2_COLOUR)
    return new_p1, new_p2


# Options
width, height = 600, 660  # window dimensions
offset = height - width  # vertical space at top of window
screen = pygame.display.set_mode((width, height))  # creates window
pygame.display.set_caption("Tron")  # sets window title
font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()
check_time = time.time()
poz = [50, (height - offset) / 2]
# creates player and add it to list
objects = list()
path = list()
p1 = Player(poz[0], poz[1], (0, 2), P1_COLOUR)
p2 = Player(poz[0] + 50, poz[1], (0, 2), P2_COLOUR)
objects.append(p1)
path.append((p1.rect, '1'))
objects.append(p2)
path.append((p2.rect, '2'))
# current player score
player_score = [0, 0]
wall_rects = [pygame.Rect([0, offset, 15, height]),
              pygame.Rect([0, offset, width, 15]),
              pygame.Rect([width - 15, offset, 15, height]),
              pygame.Rect([0, height - 15, width, 15])]
done = False
new = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            # === Player 1 === #
            if event.key == pygame.K_w:
                objects[0].bearing = (0, -2)
            elif event.key == pygame.K_s:
                objects[0].bearing = (0, 2)
            elif event.key == pygame.K_a:
                objects[0].bearing = (-2, 0)
            elif event.key == pygame.K_d:
                objects[0].bearing = (2, 0)
            elif event.key == pygame.K_TAB:
                objects[0].__boost__()
            if event.key == pygame.K_UP:
                objects[1].bearing = (0, -2)
            elif event.key == pygame.K_DOWN:
                objects[1].bearing = (0, 2)
            elif event.key == pygame.K_LEFT:
                objects[1].bearing = (-2, 0)
            elif event.key == pygame.K_RIGHT:
                objects[1].bearing = (2, 0)
            elif event.key == pygame.K_RSHIFT:
                objects[1].__boost__()
    screen.fill(BLACK)
    for r in wall_rects: pygame.draw.rect(screen, (42, 42, 42), r,
                                          0)  # draws the walls
    for o in objects:
        if time.time() - o.start_boost >= 0.5:  # limits boost to 0.5s
            o.boost = False
        if (o.rect, '1') in path or (o.rect, '2') in path \
                or o.rect.collidelist(wall_rects) > -1:
            if (time.time() - check_time) >= 0.1:
                check_time = time.time()
                if o.colour == P1_COLOUR:
                    player_score[1] += 1
                else:
                    player_score[0] += 1
                new = True
                new_p1, new_p2 = new_game()
                objects = [new_p1, new_p2]
                path = [(p1.rect, '1'), (p2.rect, '2')]
                break
        else:  # not yet traversed
            path.append(
                (o.rect, '1')) if o.colour == P1_COLOUR else path.append(
                (o.rect, '2'))
        o.__draw__()
        o.__move__()
    for r in path:
        if new is True:
            path = []
            new = False
            break
        if r[1] == '1':
            pygame.draw.rect(screen, P1_COLOUR, r[0], 0)
        else:
            pygame.draw.rect(screen, P2_COLOUR, r[0], 0)
    if len(path) > 50:
        path.pop(0)
    score_text = font.render(
        '{0} : {1}'.format(player_score[0], player_score[1]), 1, (255, 255, 51))
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = int(width / 2)
    score_text_pos.centery = int(offset / 2)
    screen.blit(score_text, score_text_pos)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
