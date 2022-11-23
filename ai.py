import random
import numpy as np
import os
import torch
import torch.nn as nn
import torch.optim as optim


class Brain(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.stack = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.stack(x)

    def save(self, file_name='brain.pth'):
        model_folder_path = 'nn'
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class BrainTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        pred = self.model(state)
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action).item()] = Q_new

        self.optimer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimer.step()


class AI:
    possible_moves = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])

    def __init__(self):
        self.move = None
        self.state_old = None
        self.state = None
        self.game = None
        self.totalReward = 0.0
        self.reward = 0.0

        self.learningRate = 0.1
        self.discount = 0.9
        self.epsilon = 0.1

        self.model = Brain(6, 256, 2)
        self.trainer = BrainTrainer(self.model, lr=self.learningRate, gamma=self.discount)

    def setGame(self, game):
        self.game = game

    def getMove(self):
        self.state_old = self.getState()
        self.move = self.get_action(self.state_old)
        return self.move

    def update(self):
        self.state = self.getState()

        self.train_short_memory(self.state_old, self.move, self.reward, self.state, self.game.active)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def getState(self):
        state = [
            self.game.snake.pos[0],
            self.game.snake.pos[1],
            self.game.food.pos[0],
            self.game.food.pos[1],
        ]

        return np.array(state, dtype=int)

    def get_action(self, state):
        if random.randint(0, 1) < self.epsilon:
            move = random.choice(self.possible_moves)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        return move
