from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from random import Random
from typing import Final

from maze_solver_lab.maze import Cell, Maze
from maze_solver_lab.solvers.base import BaseSolver, SolverSnapshot

_ACTIONS: Final[tuple[tuple[int, int], ...]] = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
)
_OPPOSITE_ACTION: Final[dict[int, int]] = {
    0: 2,
    1: 3,
    2: 0,
    3: 1,
}


@dataclass(frozen=True)
class IndividualResult:
    genome: list[int]
    path: list[Cell]
    fitness: float
    reached_goal: bool
    best_distance_to_goal: int


class EvolutionarySolver(BaseSolver):
    name = "Evolutionary search"

    def __init__(
        self,
        *,
        population_size: int = 120,
        genome_length: int | None = None,
        elite_size: int = 12,
        mutation_rate: float = 0.05,
        max_generations: int = 1000,
        immigrant_rate: float = 0.02,
        seed: int | None = 21,
    ) -> None:
        super().__init__()
        self.population_size = population_size
        self.requested_genome_length = genome_length
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.immigrant_rate = immigrant_rate
        self._rng = Random(seed)

    def _reset_impl(self, maze: Maze) -> None:
        self._generation = 0
        self._best_generation = 0
        self._distance_to_goal = self._compute_distance_to_goal(maze)
        self._start_distance = self._distance_to_goal.get(maze.start, maze.rows * maze.cols)
        self._genome_length = self._resolve_genome_length(maze)
        self._population = [self._random_genome() for _ in range(self.population_size)]
        self._best: IndividualResult | None = None
        self._visited: set[Cell] = set()

    def step(self) -> SolverSnapshot:
        assert self.maze is not None

        if self._snapshot.done:
            return self._snapshot

        evaluated = [self._evaluate(genome) for genome in self._population]
        evaluated.sort(key=lambda item: item.fitness, reverse=True)
        best = evaluated[0]

        if self._best is None or best.fitness > self._best.fitness:
            self._best = best
            self._best_generation = self._generation + 1

        display_best = self._best if self._best is not None else best
        self._visited.update(display_best.path)
        self._generation += 1

        success = display_best.reached_goal
        done = success or self._generation >= self.max_generations

        self._snapshot = SolverSnapshot(
            visited=set(self._visited),
            path=list(display_best.path),
            current=display_best.path[-1],
            done=done,
            success=success,
            info={
                "generation": self._generation,
                "best_generation": self._best_generation,
                "fitness": round(display_best.fitness, 2),
                "distance_left": display_best.best_distance_to_goal,
                "path_length": len(display_best.path),
            },
        )

        if not done:
            self._population = self._next_generation(evaluated)

        return self._snapshot

    def _resolve_genome_length(self, maze: Maze) -> int:
        if self.requested_genome_length is not None:
            return self.requested_genome_length

        # The previous fixed length was too tight for larger generated mazes.
        # The shortest path may be over 200 cells, while evolutionary candidates
        # often need extra moves because they wander before finding useful turns.
        return max(self._start_distance + maze.rows + maze.cols, 260)

    def _compute_distance_to_goal(self, maze: Maze) -> dict[Cell, int]:
        """Compute graph distance to the goal for every reachable cell.

        This distance map is used only as a fitness signal. It gives the genetic
        algorithm a smoother learning signal than raw Manhattan distance, because
        Manhattan distance ignores walls and often rewards paths that enter dead
        ends close to the goal.
        """

        distances: dict[Cell, int] = {maze.goal: 0}
        queue: deque[Cell] = deque([maze.goal])

        while queue:
            current = queue.popleft()
            for neighbor in maze.neighbors(current):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        return distances

    def _random_genome(self) -> list[int]:
        return [self._rng.randrange(len(_ACTIONS)) for _ in range(self._genome_length)]

    def _random_valid_walk_genome(self) -> list[int]:
        """Create a diversity immigrant by performing a random valid walk.

        This is not a guaranteed solution. It simply prevents the population from
        spending most of its time bumping into walls. Random immigrants are a
        standard way to keep a genetic algorithm from getting stuck too early.
        """

        assert self.maze is not None

        current = self.maze.start
        previous_action: int | None = None
        genome: list[int] = []

        for _ in range(self._genome_length):
            candidates: list[tuple[int, Cell]] = []
            current_row, current_col = current

            for action, (delta_row, delta_col) in enumerate(_ACTIONS):
                candidate = (current_row + delta_row, current_col + delta_col)
                if self.maze.is_walkable(candidate):
                    candidates.append((action, candidate))

            if previous_action is not None and len(candidates) > 1:
                non_reversing_candidates = [
                    item for item in candidates if item[0] != _OPPOSITE_ACTION[previous_action]
                ]
                if non_reversing_candidates:
                    candidates = non_reversing_candidates

            action, current = self._rng.choice(candidates)
            genome.append(action)
            previous_action = action

            if current == self.maze.goal:
                break

        while len(genome) < self._genome_length:
            genome.append(self._rng.randrange(len(_ACTIONS)))

        return genome

    def _evaluate(self, genome: list[int]) -> IndividualResult:
        assert self.maze is not None

        current = self.maze.start
        raw_path = [current]
        collisions = 0
        repeated = 0
        seen = {current}
        reached_goal = False
        best_distance = self._distance_to_goal.get(current, self.maze.rows * self.maze.cols)
        best_index = 0

        for action in genome:
            delta_row, delta_col = _ACTIONS[action]
            candidate = (current[0] + delta_row, current[1] + delta_col)

            if not self.maze.is_walkable(candidate):
                collisions += 1
                continue

            current = candidate
            raw_path.append(current)

            if current in seen:
                repeated += 1
            seen.add(current)

            distance = self._distance_to_goal.get(current, self.maze.rows * self.maze.cols)
            if distance < best_distance:
                best_distance = distance
                best_index = len(raw_path) - 1

            if current == self.maze.goal:
                reached_goal = True
                best_distance = 0
                best_index = len(raw_path) - 1
                break

        display_path = raw_path[: best_index + 1]
        progress = self._start_distance - best_distance
        unique_cells = len(seen)

        fitness = (
            100.0 * progress
            - 0.8 * best_index
            + 0.15 * unique_cells
            - 1.2 * collisions
            - 0.05 * repeated
        )

        if reached_goal:
            fitness += 15_000.0 - 3.0 * len(display_path)

        return IndividualResult(
            genome=list(genome),
            path=display_path,
            fitness=fitness,
            reached_goal=reached_goal,
            best_distance_to_goal=best_distance,
        )

    def _next_generation(self, evaluated: list[IndividualResult]) -> list[list[int]]:
        elites = [result.genome for result in evaluated[: self.elite_size]]
        next_population = [list(genome) for genome in elites]

        immigrant_count = max(1, int(self.population_size * self.immigrant_rate))
        while len(next_population) < self.elite_size + immigrant_count:
            next_population.append(self._random_valid_walk_genome())

        while len(next_population) < self.population_size:
            parent_a = self._tournament(evaluated).genome
            parent_b = self._tournament(evaluated).genome
            child = self._crossover(parent_a, parent_b)
            self._mutate(child)
            next_population.append(child)

        return next_population

    def _tournament(self, evaluated: list[IndividualResult], size: int = 5) -> IndividualResult:
        candidates = self._rng.sample(evaluated, k=min(size, len(evaluated)))
        return max(candidates, key=lambda item: item.fitness)

    def _crossover(self, parent_a: list[int], parent_b: list[int]) -> list[int]:
        if len(parent_a) <= 1:
            return list(parent_a)

        split = self._rng.randrange(1, len(parent_a))
        return list(parent_a[:split]) + list(parent_b[split:])

    def _mutate(self, genome: list[int]) -> None:
        for index in range(len(genome)):
            if self._rng.random() < self.mutation_rate:
                genome[index] = self._rng.randrange(len(_ACTIONS))

        if self._rng.random() < 0.10:
            start = self._rng.randrange(len(genome))
            stop = min(len(genome), start + self._rng.randrange(4, 24))
            for index in range(start, stop):
                genome[index] = self._rng.randrange(len(_ACTIONS))
