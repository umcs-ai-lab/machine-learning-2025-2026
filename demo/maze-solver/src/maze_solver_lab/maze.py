from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Iterable, TypeAlias

import numpy as np

Cell: TypeAlias = tuple[int, int]


@dataclass(frozen=True)
class Maze:
    grid: np.ndarray
    start: Cell
    goal: Cell

    @property
    def rows(self) -> int:
        return int(self.grid.shape[0])

    @property
    def cols(self) -> int:
        return int(self.grid.shape[1])

    def is_inside(self, cell: Cell) -> bool:
        row, col = cell
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_wall(self, cell: Cell) -> bool:
        row, col = cell
        return bool(self.grid[row, col])

    def is_walkable(self, cell: Cell) -> bool:
        return self.is_inside(cell) and not self.is_wall(cell)

    def neighbors(self, cell: Cell) -> Iterable[Cell]:
        row, col = cell
        candidates = (
            (row - 1, col),
            (row, col + 1),
            (row + 1, col),
            (row, col - 1),
        )
        for candidate in candidates:
            if self.is_walkable(candidate):
                yield candidate


def _make_odd(value: int) -> int:
    value = max(5, value)
    return value if value % 2 == 1 else value + 1


def generate_maze(rows: int, cols: int, seed: int | None = None) -> Maze:
    """Generate a perfect maze with recursive backtracking."""

    rows = _make_odd(rows)
    cols = _make_odd(cols)
    rng = Random(seed)

    grid = np.ones((rows, cols), dtype=np.uint8)
    start = (1, 1)
    goal = (rows - 2, cols - 2)

    stack = [start]
    grid[start] = 0

    while stack:
        current_row, current_col = stack[-1]
        candidates: list[tuple[Cell, Cell]] = []

        for delta_row, delta_col in ((-2, 0), (0, 2), (2, 0), (0, -2)):
            next_cell = (current_row + delta_row, current_col + delta_col)
            wall_between = (current_row + delta_row // 2, current_col + delta_col // 2)

            if 1 <= next_cell[0] < rows - 1 and 1 <= next_cell[1] < cols - 1:
                if grid[next_cell] == 1:
                    candidates.append((next_cell, wall_between))

        if not candidates:
            stack.pop()
            continue

        next_cell, wall_between = rng.choice(candidates)
        grid[wall_between] = 0
        grid[next_cell] = 0
        stack.append(next_cell)

    grid[start] = 0
    grid[goal] = 0
    return Maze(grid=grid, start=start, goal=goal)


def simple_test_maze() -> Maze:
    grid = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ],
        dtype=np.uint8,
    )
    return Maze(grid=grid, start=(1, 1), goal=(5, 5))
