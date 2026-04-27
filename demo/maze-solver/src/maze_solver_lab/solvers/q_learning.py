from __future__ import annotations

from random import Random

import numpy as np

from maze_solver_lab.maze import Cell, Maze
from maze_solver_lab.solvers.base import BaseSolver, SolverSnapshot

_ACTIONS: tuple[tuple[int, int], ...] = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
)


class QLearningSolver(BaseSolver):
    name = "Q-learning"

    def __init__(
        self,
        *,
        episodes: int = 450,
        max_steps_per_episode: int = 600,
        learning_rate: float = 0.35,
        discount_factor: float = 0.94,
        epsilon: float = 0.35,
        epsilon_decay: float = 0.992,
        min_epsilon: float = 0.03,
        seed: int | None = 13,
    ) -> None:
        super().__init__()
        self.episodes = episodes
        self.max_steps_per_episode = max_steps_per_episode
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.initial_epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self._rng = Random(seed)

    def _reset_impl(self, maze: Maze) -> None:
        self._q = np.zeros((maze.rows, maze.cols, len(_ACTIONS)), dtype=np.float64)
        self._episode = 1
        self._step_in_episode = 0
        self._epsilon = self.initial_epsilon
        self._current = maze.start
        self._visited: set[Cell] = {maze.start}
        self._episode_path: list[Cell] = [maze.start]
        self._best_path: list[Cell] = []
        self._best_steps = 10**9
        self._success_count = 0
        self._policy_path: list[Cell] = []

    def step(self) -> SolverSnapshot:
        assert self.maze is not None

        if self._snapshot.done:
            return self._snapshot

        if self._episode > self.episodes:
            self._policy_path = self._build_policy_path()
            self._snapshot = SolverSnapshot(
                visited=set(self._visited),
                path=list(self._policy_path),
                current=self._policy_path[-1] if self._policy_path else self.maze.start,
                done=True,
                success=bool(self._policy_path and self._policy_path[-1] == self.maze.goal),
                info={
                    "episodes": self.episodes,
                    "successes": self._success_count,
                    "path_length": len(self._policy_path),
                    "epsilon": round(self._epsilon, 3),
                },
            )
            return self._snapshot

        action = self._choose_action(self._current)
        next_cell, reward = self._transition(self._current, action)

        row, col = self._current
        next_row, next_col = next_cell
        old_value = self._q[row, col, action]
        next_best = float(np.max(self._q[next_row, next_col]))
        new_value = old_value + self.learning_rate * (
            reward + self.discount_factor * next_best - old_value
        )
        self._q[row, col, action] = new_value

        self._current = next_cell
        self._visited.add(next_cell)
        self._episode_path.append(next_cell)
        self._step_in_episode += 1

        reached_goal = next_cell == self.maze.goal
        episode_timed_out = self._step_in_episode >= self.max_steps_per_episode

        if reached_goal:
            self._success_count += 1
            if self._step_in_episode < self._best_steps:
                self._best_steps = self._step_in_episode
                self._best_path = list(self._episode_path)

        if reached_goal or episode_timed_out:
            self._episode += 1
            self._step_in_episode = 0
            self._epsilon = max(self.min_epsilon, self._epsilon * self.epsilon_decay)
            self._current = self.maze.start
            self._episode_path = [self.maze.start]

        display_path = self._best_path if self._best_path else self._episode_path
        self._snapshot = SolverSnapshot(
            visited=set(self._visited),
            path=list(display_path),
            current=self._current,
            info={
                "episode": self._episode,
                "successes": self._success_count,
                "epsilon": round(self._epsilon, 3),
                "best_path": len(self._best_path),
            },
        )
        return self._snapshot

    def _choose_action(self, cell: Cell) -> int:
        if self._rng.random() < self._epsilon:
            return self._rng.randrange(len(_ACTIONS))

        row, col = cell
        return int(np.argmax(self._q[row, col]))

    def _transition(self, cell: Cell, action: int) -> tuple[Cell, float]:
        assert self.maze is not None

        row, col = cell
        delta_row, delta_col = _ACTIONS[action]
        candidate = (row + delta_row, col + delta_col)

        if not self.maze.is_walkable(candidate):
            return cell, -10.0

        if candidate == self.maze.goal:
            return candidate, 100.0

        return candidate, -1.0

    def _build_policy_path(self) -> list[Cell]:
        assert self.maze is not None

        current = self.maze.start
        path = [current]
        seen = {current}

        for _ in range(self.maze.rows * self.maze.cols * 2):
            if current == self.maze.goal:
                return path

            row, col = current
            ordered_actions = list(np.argsort(self._q[row, col])[::-1])
            moved = False

            for action in ordered_actions:
                next_cell, _ = self._transition(current, int(action))
                if next_cell == current or next_cell in seen:
                    continue
                current = next_cell
                path.append(current)
                seen.add(current)
                moved = True
                break

            if not moved:
                break

        if self._best_path:
            return self._best_path
        return path
