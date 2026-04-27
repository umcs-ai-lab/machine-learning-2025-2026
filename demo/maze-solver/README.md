# Maze Solver Lab

Interactive maze pathfinding laboratory built with Python, pygame, and uv.

The project compares four families of maze-solving methods:

1. Brute-force search: DFS and BFS
2. Heuristic search: A*
3. Reinforcement learning: tabular Q-learning
4. Evolutionary optimization: a genetic algorithm over movement sequences

The main design goal is to keep every solver step-based. Each algorithm exposes the same interface, so the UI can animate one decision at a time and new algorithms can be added without rewriting the application.

## Demo controls

| Key | Action |
| --- | --- |
| `1` | DFS brute-force solver |
| `2` | BFS brute-force solver |
| `3` | A* solver |
| `4` | Q-learning solver |
| `5` | Evolutionary solver |
| `Space` | Pause / resume |
| `N` | Execute one step |
| `R` | Reset current solver |
| `M` | Generate a new maze |
| `+` / `-` | Change animation speed |
| `Esc` | Quit |

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Quick start

```bash
uv sync
uv run maze-solver-lab
```

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

## GitHub setup

```bash
git init
git add .
git commit -m "Initial Maze Solver Lab application"
git branch -M main
git remote add origin git@github.com:<your-user>/maze-solver-lab.git
git push -u origin main
```

## Project structure

```text
maze-solver-lab/
├── src/
│   └── maze_solver_lab/
│       ├── app.py
│       ├── config.py
│       ├── main.py
│       ├── maze.py
│       ├── rendering.py
│       └── solvers/
│           ├── astar.py
│           ├── base.py
│           ├── brute_force.py
│           ├── evolutionary.py
│           └── q_learning.py
├── tests/
├── pyproject.toml
└── README.md
```

## Development roadmap

- Add a maze editor with mouse-based wall toggling.
- Save and load mazes from JSON files.
- Add charts for Q-learning rewards and evolutionary fitness.
- Add experiment export to CSV.
- Add more algorithms: Dijkstra, Greedy Best-First Search, Bidirectional BFS, Ant Colony Optimization.
