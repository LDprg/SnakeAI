import random


class AI:
    def __init__(self):
        self.epsilon = 0.2
        self.learning_rate = 0.1
        self.discount = 0.7
        self.possible_moves = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.q_table = {}

    def get_move(self, snake, food):
        state = self.get_state(snake, food)

        rand = random.uniform(0, 1)
        if rand < self.epsilon:
            return random.choice(self.possible_moves)
        else:
            return self.get_best_move(state)

    def set_reward(self, snake, food, reward):
        state = self.get_state(snake, food)
        state_str = self.get_str_state(state)

        # print(reward, state_str)

        if state_str not in self.q_table:
            self.q_table[state_str] = [[0.0, 0.0], [0.0, 0.0]]
        else:
            for row in self.q_table[state_str]:
                for item in row:
                    item = self.learning_rate * item + self.learning_rate * (float(-reward) + self.discount*max(row))

    def get_best_move(self, state):
        state_str = self.get_str_state(state)
        if state_str not in self.q_table:
            self.q_table[state_str] = [[0.0, 0.0], [0.0, 0.0]]

        return self.possible_moves[self.q_table[state_str].index(max(self.q_table[state_str]))]

    def get_state(self, snake, food):
        return [snake, food]

    def get_str_state(self, state):
        state_str = ""

        for i in state:
            state_str += str(i)

        return state_str
