import numpy as np

# Constants for different cell states
WIRE = 1
HEAD = 2
TAIL = 3

neighborhood = np.array(
    [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
)


def run(matrix, n_iters):
    record = [np.array(matrix)]

    for i in range(n_iters):
        record.append(matrix)
        matrix = next(matrix)
    return record


def next(grid):
    new_grid = np.array(grid)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            cell_state = grid[i, j]

            if cell_state == HEAD:
                new_grid[i, j] = TAIL
            elif cell_state == TAIL:
                new_grid[i, j] = WIRE
            elif cell_state == WIRE:
                heads_count = np.sum(
                    grid[
                        (i + neighborhood[:, 0]) % grid.shape[0],
                        (j + neighborhood[:, 1]) % grid.shape[1],
                    ]
                    == HEAD
                )
                if heads_count == 1 or heads_count == 2:
                    new_grid[i, j] = HEAD
    return new_grid
