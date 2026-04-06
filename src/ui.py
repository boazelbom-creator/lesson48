"""UI Components for Q-Learning Visualization"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from environment import GRID_SIZE, START, GOAL, ACTION_ARROWS, state_to_pos, pos_to_state


class GridUI:
    def __init__(self, root, env, agent):
        self.root = root
        self.env = env
        self.agent = agent
        self.cell_size = 50
        self.running = False
        self.refresh_rate = 100
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Q-Learning Grid World")
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Grid canvas
        canvas_size = GRID_SIZE * self.cell_size
        self.canvas = tk.Canvas(main_frame, width=canvas_size, height=canvas_size, bg='white')
        self.canvas.grid(row=0, column=0, rowspan=4)
        self.canvas.bind('<Button-1>', self.on_cell_click)

        # Control panel
        ctrl_frame = tk.Frame(main_frame)
        ctrl_frame.grid(row=0, column=1, padx=10, sticky='n')

        tk.Label(ctrl_frame, text="Refresh Rate (ms):").pack()
        self.rate_entry = tk.Entry(ctrl_frame, width=10)
        self.rate_entry.insert(0, "100")
        self.rate_entry.pack(pady=5)

        self.start_btn = tk.Button(ctrl_frame, text="Start", command=self.start, width=10)
        self.start_btn.pack(pady=5)
        self.stop_btn = tk.Button(ctrl_frame, text="Stop", command=self.stop, width=10)
        self.stop_btn.pack(pady=5)

        self.status_label = tk.Label(ctrl_frame, text="Episode: 0")
        self.status_label.pack(pady=10)
        self.reachable_label = tk.Label(ctrl_frame, text="Goal: Reachable", fg='green')
        self.reachable_label.pack()

        # Graph
        graph_frame = tk.Frame(main_frame)
        graph_frame.grid(row=1, column=1, padx=10)
        self.fig = Figure(figsize=(3, 2), dpi=80)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Last 10 Scores", fontsize=9)
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.graph_canvas.get_tk_widget().pack()

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                if self.env.is_blocked(row, col):
                    color = '#444444'
                elif (row, col) == START:
                    color = '#90EE90'
                elif (row, col) == GOAL:
                    color = '#FFD700'
                else:
                    color = 'white'

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')

                if not self.env.is_blocked(row, col):
                    state = pos_to_state(row, col)
                    best_action = self.agent.get_best_action(state)
                    q_val = self.agent.get_best_q_value(state)
                    arrow = ACTION_ARROWS[best_action]
                    cx, cy = x1 + self.cell_size // 2, y1 + self.cell_size // 2
                    self.canvas.create_text(cx, cy - 8, text=arrow, font=('Arial', 14))
                    self.canvas.create_text(cx, cy + 10, text=f"{q_val:.1f}", font=('Arial', 8))

        # Draw agent
        ar, ac = self.env.agent_pos
        ax1 = ac * self.cell_size + 5
        ay1 = ar * self.cell_size + 5
        ax2 = ax1 + self.cell_size - 10
        ay2 = ay1 + self.cell_size - 10
        self.canvas.create_oval(ax1, ay1, ax2, ay2, fill='red', outline='darkred', width=2)

    def update_graph(self):
        scores = self.agent.get_last_scores(10)
        self.ax.clear()
        self.ax.set_title("Last 10 Scores", fontsize=9)
        if scores:
            self.ax.plot(range(len(scores)), scores, 'b-o', markersize=4)
            self.ax.set_xlim(-0.5, 9.5)
        self.graph_canvas.draw()

    def on_cell_click(self, event):
        if self.running:
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            self.env.toggle_blocked(row, col)
            self.update_reachable()
            self.draw_grid()

    def update_reachable(self):
        if self.env.is_goal_reachable():
            self.reachable_label.config(text="Goal: Reachable", fg='green')
        else:
            self.reachable_label.config(text="Goal: Unreachable!", fg='red')

    def start(self):
        try:
            self.refresh_rate = max(10, int(self.rate_entry.get()))
        except ValueError:
            self.refresh_rate = 100
        if not self.env.is_goal_reachable():
            return
        self.running = True
        self.agent.start_training()
        self.update_loop()

    def stop(self):
        self.running = False
        self.agent.stop_training()

    def update_loop(self):
        if not self.running and not self.agent.training_done:
            return
        self.draw_grid()
        self.update_graph()
        self.status_label.config(text=f"Episode: {self.agent.episode}")
        if self.running or self.agent.training:
            self.root.after(self.refresh_rate, self.update_loop)
