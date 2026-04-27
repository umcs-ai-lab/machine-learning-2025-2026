from __future__ import annotations

from typing import Final

import pygame

from maze_solver_lab.config import AppConfig
from maze_solver_lab.maze import Maze
from maze_solver_lab.solvers.base import SolverSnapshot

Color = tuple[int, int, int]

BACKGROUND: Final[Color] = (18, 18, 24)
WALL: Final[Color] = (26, 28, 34)
EMPTY: Final[Color] = (236, 236, 230)
GRID_LINE: Final[Color] = (205, 205, 198)
VISITED: Final[Color] = (125, 173, 214)
FRONTIER: Final[Color] = (91, 204, 155)
PATH: Final[Color] = (244, 202, 92)
CURRENT: Final[Color] = (109, 92, 245)
START: Final[Color] = (80, 190, 120)
GOAL: Final[Color] = (232, 93, 117)
TEXT: Final[Color] = (241, 241, 245)
MUTED_TEXT: Final[Color] = (190, 190, 200)
PANEL: Final[Color] = (32, 33, 42)


class Renderer:
    def __init__(self, screen: pygame.Surface, config: AppConfig) -> None:
        self.screen = screen
        self.config = config
        self.font = pygame.font.SysFont("consolas", 18)
        self.small_font = pygame.font.SysFont("consolas", 15)

    def draw(
        self,
        *,
        maze: Maze,
        snapshot: SolverSnapshot,
        solver_name: str,
        paused: bool,
        speed: int,
    ) -> None:
        self.screen.fill(BACKGROUND)
        self._draw_maze(maze, snapshot)
        self._draw_panel(maze, snapshot, solver_name, paused, speed)

    def _draw_maze(self, maze: Maze, snapshot: SolverSnapshot) -> None:
        cell_size = self.config.cell_size

        visited = snapshot.visited
        frontier = snapshot.frontier
        path = set(snapshot.path)

        for row in range(maze.rows):
            for col in range(maze.cols):
                cell = (row, col)
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)

                if maze.is_wall(cell):
                    color = WALL
                elif cell in path:
                    color = PATH
                elif cell in frontier:
                    color = FRONTIER
                elif cell in visited:
                    color = VISITED
                else:
                    color = EMPTY

                if cell == maze.start:
                    color = START
                elif cell == maze.goal:
                    color = GOAL
                elif cell == snapshot.current:
                    color = CURRENT

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_LINE, rect, 1)

    def _draw_panel(
        self,
        maze: Maze,
        snapshot: SolverSnapshot,
        solver_name: str,
        paused: bool,
        speed: int,
    ) -> None:
        panel_top = maze.rows * self.config.cell_size
        panel_rect = pygame.Rect(0, panel_top, self.config.window_width, self.config.panel_height)
        pygame.draw.rect(self.screen, PANEL, panel_rect)

        status = "PAUSED" if paused else "RUNNING"
        success = "success" if snapshot.success else "working"
        if snapshot.done and not snapshot.success:
            success = "failed"

        first_line = f"{solver_name} | {status} | {success} | speed={speed} step(s)/tick"
        second_line = self._format_info(snapshot)
        controls = "1 DFS  2 BFS  3 A*  4 Q-learning  5 Evolutionary | Space pause | N step | R reset | M maze | +/- speed | Esc quit"

        self._blit_text(first_line, 12, panel_top + 12, TEXT, self.font)
        self._blit_text(second_line, 12, panel_top + 40, MUTED_TEXT, self.small_font)
        self._blit_text(controls, 12, panel_top + 70, MUTED_TEXT, self.small_font)

    def _format_info(self, snapshot: SolverSnapshot) -> str:
        if not snapshot.info:
            return "No metrics yet."

        return " | ".join(f"{key}: {value}" for key, value in snapshot.info.items())

    def _blit_text(
        self,
        text: str,
        x: int,
        y: int,
        color: Color,
        font: pygame.font.Font,
    ) -> None:
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
