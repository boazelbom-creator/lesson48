"""Grid World Environment for Q-Learning"""
from collections import deque

GRID_SIZE = 12
NUM_STATES = GRID_SIZE * GRID_SIZE
NUM_ACTIONS = 4
START = (0, 0)
GOAL = (11, 11)

# Actions: 0=Up, 1=Down, 2=Left, 3=Right
ACTIONS = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
ACTION_ARROWS = {0: '↑', 1: '↓', 2: '←', 3: '→'}


def state_to_pos(state):
    return (state // GRID_SIZE, state % GRID_SIZE)


def pos_to_state(row, col):
    return row * GRID_SIZE + col


def is_valid_pos(row, col):
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE


class GridWorld:
    def __init__(self):
        self.blocked = set()
        self.agent_pos = START
        self.reset()

    def reset(self):
        self.agent_pos = START
        return pos_to_state(*self.agent_pos)

    def toggle_blocked(self, row, col):
        if (row, col) == START or (row, col) == GOAL:
            return
        pos = (row, col)
        if pos in self.blocked:
            self.blocked.remove(pos)
        else:
            self.blocked.add(pos)

    def is_blocked(self, row, col):
        return (row, col) in self.blocked

    def step(self, action):
        dr, dc = ACTIONS[action]
        new_row = self.agent_pos[0] + dr
        new_col = self.agent_pos[1] + dc

        if is_valid_pos(new_row, new_col) and not self.is_blocked(new_row, new_col):
            self.agent_pos = (new_row, new_col)

        done = self.agent_pos == GOAL
        reward = 100 if done else -1
        return pos_to_state(*self.agent_pos), reward, done

    def is_goal_reachable(self):
        if START in self.blocked or GOAL in self.blocked:
            return False
        visited = set()
        queue = deque([START])
        visited.add(START)

        while queue:
            row, col = queue.popleft()
            if (row, col) == GOAL:
                return True
            for dr, dc in ACTIONS.values():
                nr, nc = row + dr, col + dc
                if is_valid_pos(nr, nc) and (nr, nc) not in visited and (nr, nc) not in self.blocked:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return False

    def get_valid_actions(self, state):
        row, col = state_to_pos(state)
        valid = []
        for action, (dr, dc) in ACTIONS.items():
            nr, nc = row + dr, col + dc
            if is_valid_pos(nr, nc) and not self.is_blocked(nr, nc):
                valid.append(action)
        return valid if valid else list(ACTIONS.keys())
