# Q-Learning Grid World

A reinforcement learning project that trains an agent using Q-learning on a 12x12 grid world with an interactive visualization UI.

## Features

- **12x12 Grid Environment**: Agent navigates from top-left (0,0) to bottom-right (11,11)
- **Q-Learning Algorithm**: Classical Q-learning with epsilon-greedy exploration
- **Interactive UI**: Click cells to create obstacles, watch the agent learn in real-time
- **Live Visualization**: See Q-values and optimal action arrows update as training progresses
- **Performance Graph**: Sliding window showing scores of the last 10 episodes
- **Fast Training**: 2000 episodes complete in ~0.3 seconds

## Requirements

- Python 3.8+
- Tkinter (usually included with Python)
- numpy
- matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/boazelbom-creator/lesson48.git
cd lesson48
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
cd src
python main.py
```

## How to Use

### Grid Display
- **Green cell** (top-left): Start position
- **Gold cell** (bottom-right): Goal position
- **Gray cells**: Blocked/obstacle cells
- **Red circle**: Agent's current position
- **Arrows** (↑↓←→): Best action for each cell based on Q-values
- **Numbers**: Q-value of the best action for each cell

### Controls

| Control | Description |
|---------|-------------|
| **Click on cell** | Toggle cell as blocked/unblocked |
| **Refresh Rate field** | Set UI update interval in milliseconds (default: 100ms) |
| **Start button** | Begin training and visualization |
| **Stop button** | Pause the visualization |

### Status Indicators
- **Episode counter**: Shows current training episode (0-2000)
- **Goal status**: Shows if the goal is reachable with current obstacles
- **Score graph**: Displays the last 10 episode scores

## Algorithm Parameters

| Parameter | Value |
|-----------|-------|
| Learning rate (α) | 0.1 |
| Discount factor (γ) | 0.95 |
| Initial epsilon (ε) | 1.0 |
| Epsilon decay | × 0.99 per episode |
| Minimum epsilon | 0.05 |
| Max steps per episode | 200 |
| Total episodes | 2000 |

## Reward Structure

| Event | Reward |
|-------|--------|
| Reaching goal | +100 |
| Each step | -1 |
| Blocked cell | Cannot enter |

## Project Structure

```
lesson48/
├── src/
│   ├── environment.py   # Grid world environment
│   ├── qlearning.py     # Q-learning algorithm
│   ├── ui.py            # Tkinter UI components
│   └── main.py          # Entry point
├── requirements.txt
├── PRD.md               # Product requirements document
└── README.md
```

## Notes

- Training runs at full speed in a separate thread
- UI updates independently based on the refresh rate setting
- If you block all paths to the goal, the system will detect it and prevent training
- After training completes, the UI shows the final learned policy
