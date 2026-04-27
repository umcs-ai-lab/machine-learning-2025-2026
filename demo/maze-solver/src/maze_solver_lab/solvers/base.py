from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from maze_solver_lab.maze import Cell, Maze


@dataclass(frozen=True)
class SolverSnapshot:
    visited: set[Cell] = field(default_factory=set)
    frontier: set[Cell] = field(default_factory=set)
    path: list[Cell] = field(default_factory=list)
    current: Cell | None = None
    done: bool = False
    success: bool = False
    info: dict[str, Any] = field(default_factory=dict)


class BaseSolver(ABC):
    name = "Base solver"

    def __init__(self) -> None:
        self.maze: Maze | None = None
        self._snapshot = SolverSnapshot()

    def reset(self, maze: Maze) -> None:
        self.maze = maze
        self._snapshot = SolverSnapshot()
        self._reset_impl(maze)

    @abstractmethod
    def _reset_impl(self, maze: Maze) -> None:
        raise NotImplementedError

    @abstractmethod
    def step(self) -> SolverSnapshot:
        raise NotImplementedError

    def snapshot(self) -> SolverSnapshot:
        return self._snapshot

    @property
    def is_finished(self) -> bool:
        return self._snapshot.done


def reconstruct_path(came_from: dict[Cell, Cell], start: Cell, goal: Cell) -> list[Cell]:
    if goal != start and goal not in came_from:
        return []

    current = goal
    path = [current]

    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path
