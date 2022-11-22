import random
import pygame
import torch.nn as nn

WINDOW_SIZE = (600, 600)
BLOCK_SIZE = 60

SNAKE_COLOR = (255, 0, 0)
FOOD_COLOR = (0, 255, 0)

BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (255, 255, 255)

START_LENGTH = 3
START_POS = [1, 1]

SPEED = 250

pygame.init()

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake Game")


def getFoodPos(snakeBody):
    while True:
        maxX = int(WINDOW_SIZE[0] / BLOCK_SIZE) - 1
        maxY = int(WINDOW_SIZE[1] / BLOCK_SIZE) - 1

        x = random.randint(0, maxX)
        y = random.randint(0, maxY)
        if [x, y] not in snakeBody:
            return [x, y]


def gameLoop():
    SNAKE_POS = START_POS
    SNAKE_LENGTH = START_LENGTH

    SNAKE_BODY = []
    SNAKE_BODY.insert(0, list(SNAKE_POS))

    STATE = ""

    MOVE = [1, 0]

    FOOD_POS = getFoodPos(SNAKE_BODY)

    gametick = pygame.USEREVENT + 1
    pygame.time.set_timer(gametick, SPEED)

    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    MOVE = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    MOVE = [1, 0]
                elif event.key == pygame.K_UP:
                    MOVE = [0, -1]
                elif event.key == pygame.K_DOWN:
                    MOVE = [0, 1]
                elif event.key == pygame.K_ESCAPE:
                    active = False
            elif event.type == gametick:
                SNAKE_POS[0] += MOVE[0]
                SNAKE_POS[1] += MOVE[1]

                while len(SNAKE_BODY) > SNAKE_LENGTH - 1:
                    SNAKE_BODY.pop()

                for pos in SNAKE_BODY:
                    if pos == SNAKE_POS:
                        STATE = "GAME OVER"
                        active = False
                        break

                for pos in SNAKE_BODY:
                    if pos == FOOD_POS:
                        SNAKE_LENGTH += 1
                        FOOD_POS = getFoodPos(SNAKE_BODY)

                SNAKE_BODY.insert(0, list(SNAKE_POS))

                for pos in SNAKE_BODY:
                    if pos[0] < 0 or pos[0] > (WINDOW_SIZE[0] / BLOCK_SIZE) - 1 or \
                            pos[1] < 0 or pos[1] > (WINDOW_SIZE[1] / BLOCK_SIZE) - 1:
                        STATE = "GAME OVER"
                        active = False

                if SNAKE_LENGTH >= (WINDOW_SIZE[0] / BLOCK_SIZE) * (WINDOW_SIZE[1] / BLOCK_SIZE):
                    STATE = "YOU WIN"
                    active = False

        window.fill(BACKGROUND_COLOR)

        for x in range(0, WINDOW_SIZE[0], BLOCK_SIZE):
            x_pos = x / BLOCK_SIZE
            for y in range(0, WINDOW_SIZE[1], BLOCK_SIZE):
                y_pos = y / BLOCK_SIZE

                if x_pos == FOOD_POS[0] and y_pos == FOOD_POS[1]:
                    pygame.draw.rect(window, FOOD_COLOR, [x, y, BLOCK_SIZE, BLOCK_SIZE])

                for pos in SNAKE_BODY:
                    if x_pos == pos[0] and y_pos == pos[1]:
                        pygame.draw.rect(window, SNAKE_COLOR, [x, y, BLOCK_SIZE, BLOCK_SIZE])

                pygame.draw.rect(window, GRID_COLOR, [x, y, BLOCK_SIZE, BLOCK_SIZE], 1)

        pygame.display.update()

    return [STATE, SNAKE_LENGTH]


STATE, SNAKE_LENGTH = gameLoop()

if STATE == "":
    exit()

STATE += " - " + str(SNAKE_LENGTH)

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                active = False

    window.fill(BACKGROUND_COLOR)

    window.blit(pygame.font.SysFont('freesanbold.ttf', 50).render(STATE, True, GRID_COLOR),
                (WINDOW_SIZE[0] / 2 - 100, WINDOW_SIZE[1] / 2 - 25))

    pygame.display.update()
