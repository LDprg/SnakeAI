import random
import threading

import pygame
import numpy as np
import ai

SNAKE_COLOR = (255, 0, 0)
FOOD_COLOR = (0, 255, 0)

BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (255, 255, 255)

BLOCK_SIZE = 40
GRID_SIZE = 15

WINDOW_SIZE = (BLOCK_SIZE * GRID_SIZE, BLOCK_SIZE * GRID_SIZE)


def getDistance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


class Snake:
    def __init__(self, game, pos, length):
        self.game = game

        self.pos = pos
        self.length = length

        self.body = []

    def draw(self):
        pygame.draw.rect(self.game.window, SNAKE_COLOR,
                         (self.pos[0] * BLOCK_SIZE, self.pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for i in self.body:
            pygame.draw.rect(self.game.window, SNAKE_COLOR,
                             (i[0] * BLOCK_SIZE, i[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def move(self, move):
        self.body.insert(0, np.copy(self.pos))
        self.pos += move

        if self.selfCollide() or self.outOfBounds():
            self.game.ai.setReward(-100)
            self.game.close()

        self.body = self.body[:self.length]

    def eat(self):
        self.length += 1

    def outOfBounds(self):
        return (self.pos[0] < 0 or self.pos[0] >= WINDOW_SIZE[0] / BLOCK_SIZE) or \
               (self.pos[1] < 0 or self.pos[1] >= WINDOW_SIZE[1] / BLOCK_SIZE)

    def selfCollide(self):
        return True in [(self.pos == x).all() for x in self.body]


class Food:
    def __init__(self, game):
        self.game = game
        self.pos = np.array([1, 1])

    def draw(self):
        pygame.draw.rect(self.game.window, FOOD_COLOR,
                         [self.pos[0] * BLOCK_SIZE, self.pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

    def random(self, snake):
        while True:
            x = random.randint(0, Game.getGrid()[0])
            y = random.randint(0, Game.getGrid()[1])
            if True not in [([x, y] == i).all() for i in snake.body] and ([x, y] != snake.pos).all():
                self.pos = [x, y]
                break

    def collide(self, snake):
        return (snake.pos == self.pos).all()


class Game:
    def __init__(self, window, ai):
        self.window = window

        self.active = True

        self.snake = Snake(self, np.array([round(Game.getGrid()[0] / 2), round(Game.getGrid()[1] / 2)]), 3)
        self.food = Food(self)

        if random.randint(0, 1) == 0:
            self.move = np.array([0, random.choice((-1, 1))])
        else:
            self.move = np.array([random.choice((-1, 1)), 0])

        self.ai = ai
        self.ai.setGame(self)

    @staticmethod
    def getGrid():
        return np.array([int(WINDOW_SIZE[0] / BLOCK_SIZE) - 1, int(WINDOW_SIZE[1] / BLOCK_SIZE) - 1])

    def update(self):
        self.move = self.ai.getMove()

        self.snake.move(self.move)

        if self.food.collide(self.snake):
            self.ai.setReward(100)
            self.snake.eat()
            self.food.random(self.snake)
        else:
            self.ai.setReward(50 / getDistance(self.snake.pos, self.food.pos))

        self.ai.update()

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)

        self.food.draw()
        self.snake.draw()

        for x in range(0, WINDOW_SIZE[0], BLOCK_SIZE):
            for y in range(0, WINDOW_SIZE[1], BLOCK_SIZE):
                pygame.draw.rect(window, GRID_COLOR, [x, y, BLOCK_SIZE, BLOCK_SIZE], 1)

        pygame.display.update()

    def run(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()

            self.draw()

    def close(self):
        self.active = False


pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake Game")

AI = ai.AI()

for i in range(10000000):
    game = Game(window, AI)

    game.run()

    print("Game: " + str(i) + " Score: " + str(AI.totalReward))
