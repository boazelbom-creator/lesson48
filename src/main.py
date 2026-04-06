"""Main entry point for Q-Learning Grid World"""
import tkinter as tk
from environment import GridWorld
from qlearning import QLearning
from ui import GridUI


def main():
    root = tk.Tk()
    root.resizable(False, False)

    env = GridWorld()
    agent = QLearning(env)
    ui = GridUI(root, env, agent)

    root.mainloop()


if __name__ == "__main__":
    main()
