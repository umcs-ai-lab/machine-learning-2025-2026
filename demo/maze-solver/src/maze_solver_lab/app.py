from __future__ import annotations

from collections.abc import Callable

import pygame

from maze_solver_lab.config import AppConfig
from maze_solver_lab.maze import Maze, generate_maze
from maze_solver_lab.rendering import Renderer
from maze_solver_lab.solvers import (
    AStarSolver,
    BreadthFirstSearchSolver,
    DepthFirstSearchSolver,
    EvolutionarySolver,
    QLearningSolver,
)
from maze_solver_lab.solvers.base import BaseSolver

SolverFactory = Callable[[], BaseSolver]


class MazeSolverApp:
    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or AppConfig()
        self.maze_seed = self.config.random_seed
        self.maze: Maze = generate_maze(self.config.rows, self.config.cols, self.maze_seed)
        self.solver_factories: dict[int, SolverFactory] = {
            pygame.K_1: DepthFirstSearchSolver,
            pygame.K_2: BreadthFirstSearchSolver,
            pygame.K_3: AStarSolver,
            pygame.K_4: QLearningSolver,
            pygame.K_5: EvolutionarySolver,
        }
        self.solver: BaseSolver = AStarSolver()
        self.solver.reset(self.maze)
        self.paused = False
        self.speed = self.config.solver_steps_per_tick

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("Maze Solver Lab")
        screen = pygame.display.set_mode((self.config.window_width, self.config.window_height))
        clock = pygame.time.Clock()
        renderer = Renderer(screen, self.config)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self._handle_key(event.key)

            if not self.paused and not self.solver.is_finished:
                self._advance_solver(self.speed)

            renderer.draw(
                maze=self.maze,
                snapshot=self.solver.snapshot(),
                solver_name=self.solver.name,
                paused=self.paused,
                speed=self.speed,
            )
            pygame.display.flip()
            clock.tick(self.config.frames_per_second)

        pygame.quit()

    def _handle_key(self, key: int) -> bool:
        if key == pygame.K_ESCAPE:
            return False

        if key in self.solver_factories:
            self.solver = self.solver_factories[key]()
            self.solver.reset(self.maze)
            self.paused = False
            return True

        if key == pygame.K_SPACE:
            self.paused = not self.paused
        elif key == pygame.K_n:
            self._advance_solver(1)
        elif key == pygame.K_r:
            self.solver.reset(self.maze)
            self.paused = False
        elif key == pygame.K_m:
            self._new_maze()
        elif key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            self.speed = min(500, self.speed + 1)
        elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            self.speed = max(1, self.speed - 1)

        return True

    def _advance_solver(self, steps: int) -> None:
        for _ in range(steps):
            if self.solver.is_finished:
                break
            self.solver.step()

    def _new_maze(self) -> None:
        if self.maze_seed is None:
            next_seed = None
        else:
            next_seed = self.maze_seed + 1
            self.maze_seed = next_seed

        self.maze = generate_maze(self.config.rows, self.config.cols, next_seed)
        self.solver.reset(self.maze)
        self.paused = False
