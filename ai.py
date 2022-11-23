import random


class AI:
    possible_moves = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    def __init__(self):
        pass

    def get_move(self):
        rand = random.uniform(0, 1)
        return random.choice(self.possible_moves)

