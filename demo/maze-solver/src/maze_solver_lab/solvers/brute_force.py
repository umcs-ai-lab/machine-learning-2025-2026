from __future__ import annotations

from collections import deque

from maze_solver_lab.maze import Cell, Maze
from maze_solver_lab.solvers.base import BaseSolver, SolverSnapshot, reconstruct_path


class DepthFirstSearchSolver(BaseSolver):
    name = "DFS brute-force"

    def _reset_impl(self, maze: Maze) -> None:
        self._stack: list[Cell] = [maze.start]
        self._frontier: set[Cell] = {maze.start}
        self._visited: set[Cell] = set()
        self._came_from: dict[Cell, Cell] = {}

    def step(self) -> SolverSnapshot:
        assert self.maze is not None

        if self._snapshot.done:
            return self._snapshot

        if not self._stack:
            self._snapshot = SolverSnapshot(
                visited=set(self._visited),
                frontier=set(),
                done=True,
                success=False,
                info={"visited": len(self._visited)},
            )
            return self._snapshot

        current = self._stack.pop()
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
            if neighbor in self._visited or neighbor in self._frontier:
                continue
            self._came_from[neighbor] = current
            self._stack.append(neighbor)
            self._frontier.add(neighbor)

        self._snapshot = SolverSnapshot(
            visited=set(self._visited),
            frontier=set(self._frontier),
            current=current,
            info={"visited": len(self._visited), "frontier": len(self._frontier)},
        )
        return self._snapshot


class BreadthFirstSearchSolver(BaseSolver):
    name = "BFS brute-force"

    def _reset_impl(self, maze: Maze) -> None:
        self._queue: deque[Cell] = deque([maze.start])
        self._frontier: set[Cell] = {maze.start}
        self._visited: set[Cell] = set()
        self._came_from: dict[Cell, Cell] = {}

    def step(self) -> SolverSnapshot:
        assert self.maze is not None

        if self._snapshot.done:
            return self._snapshot

        if not self._queue:
            self._snapshot = SolverSnapshot(
                visited=set(self._visited),
                frontier=set(),
                done=True,
                success=False,
                info={"visited": len(self._visited)},
            )
            return self._snapshot

        current = self._queue.popleft()
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
            if neighbor in self._visited or neighbor in self._frontier:
                continue
            self._came_from[neighbor] = current
            self._queue.append(neighbor)
            self._frontier.add(neighbor)

        self._snapshot = SolverSnapshot(
            visited=set(self._visited),
            frontier=set(self._frontier),
            current=current,
            info={"visited": len(self._visited), "frontier": len(self._frontier)},
        )
        return self._snapshot
