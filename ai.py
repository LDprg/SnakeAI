import random


class AI:
    possible_moves = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    def __init__(self):
        self.game = None

    def setGame(self, game):
        self.game = game

    def getMove(self):
        return random.choice(self.possible_moves)

