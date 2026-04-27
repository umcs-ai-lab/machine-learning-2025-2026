import pytest

from maze_solver_lab.maze import simple_test_maze
from maze_solver_lab.solvers import AStarSolver, BreadthFirstSearchSolver, DepthFirstSearchSolver
from maze_solver_lab.solvers.base import BaseSolver


def run_until_done(solver: BaseSolver, max_steps: int = 500):
    maze = simple_test_maze()
    solver.reset(maze)

    snapshot = solver.snapshot()
    for _ in range(max_steps):
        snapshot = solver.step()
        if snapshot.done:
            break

    return maze, snapshot


@pytest.mark.parametrize(
    "solver",
    [DepthFirstSearchSolver(), BreadthFirstSearchSolver(), AStarSolver()],
)
def test_classic_solvers_find_path(solver: BaseSolver) -> None:
    maze, snapshot = run_until_done(solver)

    assert snapshot.done
    assert snapshot.success
    assert snapshot.path[0] == maze.start
    assert snapshot.path[-1] == maze.goal


def test_bfs_and_astar_find_same_shortest_path_length() -> None:
    _, bfs_snapshot = run_until_done(BreadthFirstSearchSolver())
    _, astar_snapshot = run_until_done(AStarSolver())

    assert len(bfs_snapshot.path) == len(astar_snapshot.path)
