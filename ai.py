import random
import numpy as np

class AI:
    possible_moves = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]
    learning = True

    def __init__(self):
        self.game = None
        self.history = []
        self.oldDistance = 0.0
        self.totalReward = 0.0
        self.reward = 0.0

        self.epsilon = 0.2
        self.learningRate = 0.1
        self.discount = 0.9

        self.qTable = {}

    def setGame(self, game):
        self.game = game

    def getMove(self):
        if random.uniform(0, 1) < self.epsilon and self.learning:
            move = random.choice(self.possible_moves)
        else:
            move = self.possible_moves[np.argmax([self.getQ(self.getStateStr(), x) for x in self.possible_moves])]

        self.history.append(move)
        return move

    def setReward(self, reward):
        self.totalReward += reward
        self.reward = reward

    def updateQ(self):
        if len(self.history) > 1 and self.learning:
            oldState = self.getStateStr()
            oldMove = self.history[-2]
            oldQ = self.getQ(oldState, oldMove)

            self.qTable[str(oldState) + str(oldMove)] = oldQ + self.learningRate * (self.reward + self.discount * max([self.getQ(self.getStateStr(), x) for x in self.possible_moves]) - oldQ)

    def getQ(self, state, move):
        if str(state) + str(move) not in self.qTable:
            self.qTable[str(state) + str(move)] = 0.0
        return self.qTable[str(state) + str(move)]

    def getState(self):
        return [self.game.snake.pos, self.game.food.pos]

    def getStateStr(self):
        return [str(x) for x in self.getState()]
