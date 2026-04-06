# Product Requirements Document (PRD)
## Q-Learning Grid World with Interactive UI

---

## 1. Overview

### 1.1 Purpose
Build a reinforcement learning application that trains an agent using Q-learning on a 12×12 grid world, with a real-time interactive UI for visualization and control.

### 1.2 Technology Stack
- **Language**: Python
- **Environment**: Virtual environment (venv)
- **UI Framework**: TBD (e.g., Pygame, Tkinter)

### 1.3 Constraints
- Code files must not exceed 150 lines each
- No unnecessary abstractions
- Exact implementation as specified (no simplifications or optimizations unless requested)

---

## 2. Environment Specifications

### 2.1 Grid
| Property | Value |
|----------|-------|
| Dimensions | 12 × 12 |
| Total States | 144 |
| Start State | (0, 0) - Top-left corner |
| Goal State | (11, 11) - Bottom-right corner |

### 2.2 Actions
| Action | Direction |
|--------|-----------|
| 0 | Up |
| 1 | Down |
| 2 | Left |
| 3 | Right |

### 2.3 Blocked States
- User-defined via UI interaction
- Agent cannot enter blocked cells
- Blocked cells excluded from transitions during training
- System must detect unreachable goal and handle gracefully (no crashes)

---

## 3. Q-Learning Algorithm

### 3.1 Parameters
| Parameter | Symbol | Value |
|-----------|--------|-------|
| Learning Rate | α | 0.1 |
| Discount Factor | γ | 0.95 |
| Initial Epsilon | ε₀ | 1.0 |
| Epsilon Decay | - | ε × 0.99 per episode |
| Minimum Epsilon | ε_min | 0.05 |
| Max Steps per Episode | - | 200 |
| Total Episodes | - | 2000 |

### 3.2 Q-Table
- Dimensions: 144 states × 4 actions
- Initialized to zeros

### 3.3 Reward Structure
| Event | Reward |
|-------|--------|
| Reaching goal (11,11) | +100 |
| Every move | -1 |
| Attempting blocked cell | Forbidden (action has no effect) |

### 3.4 Training Behavior
- Training runs at **full speed** with no delays
- No waiting for UI updates
- Training completes after 2000 episodes
- Q-table and agent position accessible to UI during and after training

---

## 4. User Interface Requirements

### 4.1 Live Grid Visualization
- Display 12×12 grid on screen
- Each cell shows:
  - Best action arrow based on current Q-values: ↑ ↓ ← →
  - Q-value of the best action (numeric)
- Blocked states visually distinct (grayed out, X-marked, or different color)
- Start state (0,0) and goal state (11,11) clearly marked

### 4.2 Agent Movement Visualization
- Agent visually represented on the grid
- Movement drawn live at user-defined intervals
- Visualization **decoupled** from training loop:
  - Training runs instantly
  - UI refreshes independently every X ms
  - UI displays latest agent position and current Q-table state

### 4.3 Visualization Timing Control
- Input field for user to set refresh rate in milliseconds
- Example: User enters "20" → UI updates every 20 ms

### 4.4 Unpassable State Controls
- User clicks any cell to toggle blocked/unblocked
- First click → blocked
- Second click → unblocked
- Changes apply immediately before training

### 4.5 Sliding Score Graph
- Displays scores of the **last 10 episodes**
- Updates in real-time based on UI refresh interval
- When buffer exceeds 10 values, oldest value removed (sliding window)

### 4.6 Control Buttons
| Button | Function |
|--------|----------|
| Start | Begin agent movement visualization |
| Stop | Pause agent movement visualization |

---

## 5. Architecture Requirements

### 5.1 Separation of Concerns
```
┌─────────────────┐     ┌─────────────────┐
│  Training Loop  │────▶│    Q-Table      │◀────┐
│  (Full Speed)   │     │  Agent Position │     │
└─────────────────┘     └─────────────────┘     │
                              ▲                 │
                              │ Read            │ Read
                              │                 │
                        ┌─────────────────┐     │
                        │   UI Loop       │─────┘
                        │  (Every X ms)   │
                        └─────────────────┘
```

### 5.2 Module Structure
```
lesson48/
├── venv/
├── src/
│   ├── environment.py    # Grid world environment
│   ├── qlearning.py      # Q-learning algorithm
│   ├── ui.py             # UI components and visualization
│   └── main.py           # Entry point
├── PRD.md
├── prompt.txt
└── requirements.txt
```

### 5.3 Threading Model
- **Training Thread**: Runs Q-learning at full speed
- **UI Thread**: Updates display every X ms, reads shared state

---

## 6. Behavior Specifications

### 6.1 Training Behavior
- Runs without delays or waits
- Completes 2000 episodes
- Updates Q-table continuously
- Tracks episode scores for graph

### 6.2 Visualization Behavior
- Independent from training speed
- Refreshes every X ms (user-defined)
- Displays:
  - Current Q-table values and best actions
  - Agent's current position
  - Last 10 episode scores on graph
- If training finishes early, UI shows final stable policy
- Visualization stops when Stop button clicked

### 6.3 Blocked Cell Behavior
- Cannot be entered by agent
- Agent stays in current position if action would lead to blocked cell
- Path-finding check: system detects if goal is unreachable
- If unreachable, system handles gracefully (no crash, notify user)

---

## 7. Acceptance Criteria

- [ ] 12×12 grid displays correctly with all cells visible
- [ ] Agent starts at (0,0) and can reach (11,11)
- [ ] Q-learning trains for 2000 episodes at full speed
- [ ] Q-table shows 144×4 entries
- [ ] Each cell displays best action arrow and Q-value
- [ ] Blocked cells are visually distinct and non-enterable
- [ ] Click toggles cell blocked status
- [ ] Unreachable goal is detected and handled
- [ ] Refresh rate input field works (ms)
- [ ] Sliding graph shows last 10 episode scores
- [ ] Start/Stop buttons control agent visualization
- [ ] Training and UI are decoupled
- [ ] All code files ≤ 150 lines

---

## 8. Out of Scope
- Saving/loading Q-tables
- Multiple agents
- Different algorithms (SARSA, DQN, etc.)
- Custom grid sizes
- Diagonal movement
