from maze_solver_lab.maze import generate_maze, simple_test_maze


def test_simple_test_maze_has_walkable_start_and_goal() -> None:
    maze = simple_test_maze()

    assert maze.is_walkable(maze.start)
    assert maze.is_walkable(maze.goal)


def test_generated_maze_has_walkable_start_and_goal() -> None:
    maze = generate_maze(15, 15, seed=1)

    assert maze.rows == 15
    assert maze.cols == 15
    assert maze.is_walkable(maze.start)
    assert maze.is_walkable(maze.goal)
