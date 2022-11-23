import random
import pygame
import ai

SNAKE_COLOR = (255, 0, 0)
FOOD_COLOR = (0, 255, 0)

BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (255, 255, 255)

BLOCK_SIZE = 40
GRID_SIZE = 15

WINDOW_SIZE = (BLOCK_SIZE * GRID_SIZE, BLOCK_SIZE * GRID_SIZE)

GAMETICK = pygame.USEREVENT + 1


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
        self.body.insert(0, self.pos[:])
        self.pos[0] += move[0]
        self.pos[1] += move[1]

        if self.pos in self.body or self.outOfBounds():
            self.game.close()

        self.body = self.body[:self.length]

    def eat(self):
        self.length += 1

    def outOfBounds(self):
        return (self.pos[0] < 0 or self.pos[0] >= WINDOW_SIZE[0] / BLOCK_SIZE) or \
               (self.pos[1] < 0 or self.pos[1] >= WINDOW_SIZE[1] / BLOCK_SIZE)


class Food:
    def __init__(self, game):
        self.game = game
        self.pos = [1, 1]

    def draw(self):
        pygame.draw.rect(self.game.window, FOOD_COLOR,
                         [self.pos[0] * BLOCK_SIZE, self.pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])

    def random(self, snake):
        while True:
            x = random.randint(0, Game.getGrid()[0])
            y = random.randint(0, Game.getGrid()[1])
            if [x, y] not in snake.body and snake.pos != [x, y]:
                self.pos = [x, y]
                break

    def collide(self, snake):
        return snake.pos == self.pos


class Game:
    def __init__(self, window, ai):
        self.window = window
        self.ai = ai
        self.active = True

        self.snake = Snake(self, [round(Game.getGrid()[0] / 2), round(Game.getGrid()[1] / 2)], 3)
        self.food = Food(self)

        if random.randint(0, 1) == 0:
            self.move = [0, random.choice((-1, 1))]
        else:
            self.move = [random.choice((-1, 1)), 0]

    @staticmethod
    def getGrid():
        return [int(WINDOW_SIZE[0] / BLOCK_SIZE) - 1, int(WINDOW_SIZE[1] / BLOCK_SIZE) - 1]

    def loop(self):
        while self.active:
            self.run()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    self.move = [1, 0]
                elif event.key == pygame.K_UP:
                    self.move = [0, -1]
                elif event.key == pygame.K_DOWN:
                    self.move = [0, 1]
                elif event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_SPACE:
                    self.close()
            elif event.type == GAMETICK:
                self.update()

    def update(self):
        self.move = self.ai.get_move()

        self.snake.move(self.move)

        if self.food.collide(self.snake):
            self.snake.eat()
            self.food.random(self.snake)

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)

        self.food.draw()
        self.snake.draw()

        for x in range(0, WINDOW_SIZE[0], BLOCK_SIZE):
            for y in range(0, WINDOW_SIZE[1], BLOCK_SIZE):
                pygame.draw.rect(window, GRID_COLOR, [x, y, BLOCK_SIZE, BLOCK_SIZE], 1)

        pygame.display.update()

    def run(self):
        self.event()
        self.draw()

    def close(self):
        self.active = False


pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake Game")

AI = ai.AI()

for i in range(100):
    if i % 50 == 0:
        pygame.time.set_timer(GAMETICK, 100)
    else:
        pygame.time.set_timer(GAMETICK, 100)

    Game(window, AI).loop()
