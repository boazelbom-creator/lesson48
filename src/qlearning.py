"""Q-Learning Algorithm"""
import numpy as np
import random
import threading
from environment import NUM_STATES, NUM_ACTIONS, pos_to_state, GOAL

# Hyperparameters
ALPHA = 0.1
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_DECAY = 0.99
EPSILON_MIN = 0.05
MAX_STEPS = 200
TOTAL_EPISODES = 2000


class QLearning:
    def __init__(self, env):
        self.env = env
        self.q_table = np.zeros((NUM_STATES, NUM_ACTIONS))
        self.epsilon = EPSILON_START
        self.episode = 0
        self.episode_scores = []
        self.training = False
        self.training_done = False
        self.lock = threading.Lock()

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, NUM_ACTIONS - 1)
        return int(np.argmax(self.q_table[state]))

    def update(self, state, action, reward, next_state):
        best_next = np.max(self.q_table[next_state])
        self.q_table[state, action] += ALPHA * (reward + GAMMA * best_next - self.q_table[state, action])

    def run_episode(self):
        state = self.env.reset()
        total_reward = 0

        for _ in range(MAX_STEPS):
            action = self.choose_action(state)
            next_state, reward, done = self.env.step(action)
            self.update(state, action, reward, next_state)
            total_reward += reward
            state = next_state
            if done:
                break

        return total_reward

    def train(self):
        self.training = True
        self.training_done = False
        self.episode = 0
        self.epsilon = EPSILON_START
        self.q_table = np.zeros((NUM_STATES, NUM_ACTIONS))
        self.episode_scores = []

        if not self.env.is_goal_reachable():
            self.training = False
            self.training_done = True
            return

        for ep in range(TOTAL_EPISODES):
            if not self.training:
                break
            score = self.run_episode()
            with self.lock:
                self.episode_scores.append(score)
                self.episode = ep + 1
            self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)

        self.training = False
        self.training_done = True

    def start_training(self):
        thread = threading.Thread(target=self.train, daemon=True)
        thread.start()

    def stop_training(self):
        self.training = False

    def get_best_action(self, state):
        return int(np.argmax(self.q_table[state]))

    def get_best_q_value(self, state):
        return np.max(self.q_table[state])

    def get_last_scores(self, n=10):
        with self.lock:
            return list(self.episode_scores[-n:])
