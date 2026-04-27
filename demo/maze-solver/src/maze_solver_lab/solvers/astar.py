from __future__ import annotations

import heapq

from maze_solver_lab.maze import Cell, Maze
from maze_solver_lab.solvers.base import BaseSolver, SolverSnapshot, reconstruct_path


def manhattan_distance(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class AStarSolver(BaseSolver):
    name = "A* search"

    def _reset_impl(self, maze: Maze) -> None:
        self._counter = 0
        self._open_heap: list[tuple[int, int, Cell]] = []
        self._frontier: set[Cell] = {maze.start}
        self._visited: set[Cell] = set()
        self._came_from: dict[Cell, Cell] = {}
        self._g_score: dict[Cell, int] = {maze.start: 0}
        heapq.heappush(self._open_heap, (0, self._counter, maze.start))

    def step(self) -> SolverSnapshot:
        assert self.maze is not None

        if self._snapshot.done:
            return self._snapshot

        while self._open_heap:
            _, _, current = heapq.heappop(self._open_heap)
            if current not in self._visited:
                break
        else:
            self._snapshot = SolverSnapshot(
                visited=set(self._visited),
                frontier=set(),
                done=True,
                success=False,
                info={"visited": len(self._visited)},
            )
            return self._snapshot

        self._frontier.discard(current)
        self._visited.add(current)

        if current == self.maze.goal:
            path = reconstruct_path(self._came_from, self.maze.start, self.maze.goal)
            self._snapshot = SolverSnapshot(
                visited=set(self._visited),
                frontier=set(self._frontier),
                path=path,
                current=current,
                done=True,
                success=True,
                info={"visited": len(self._visited), "path_length": len(path)},
            )
            return self._snapshot

        for neighbor in self.maze.neighbors(current):
            tentative_g = self._g_score[current] + 1
            if tentative_g >= self._g_score.get(neighbor, 10**9):
                continue

            self._came_from[neighbor] = current
            self._g_score[neighbor] = tentative_g
            f_score = tentative_g + manhattan_distance(neighbor, self.maze.goal)
            self._counter += 1
            heapq.heappush(self._open_heap, (f_score, self._counter, neighbor))
            self._frontier.add(neighbor)

        self._snapshot = SolverSnapshot(
            visited=set(self._visited),
            frontier=set(self._frontier),
            current=current,
            info={"visited": len(self._visited), "frontier": len(self._frontier)},
        )
        return self._snapshot
