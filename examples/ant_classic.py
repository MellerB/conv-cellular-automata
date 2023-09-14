import numpy as np


clockwise = np.matrix([[0, 1], [-1, 0]])
counter_clockwise = np.matrix([[0, -1], [1, 0]])


def run(matrix, n_iters, positions):
    agents = range(len(positions))
    directions = [np.matrix([[1], [0]]) for i in agents]
    matrix = np.array(matrix)
    dim = matrix.shape[0]
    record = []
    for i in range(n_iters):
        record.append(np.array(matrix))
        for a in agents:
            pos = positions[a]
            direction = directions[a]
            pos[:] = pos + direction
            pos %= dim
            if matrix[pos[0, 0], pos[1, 0]] == 0:
                matrix[pos[0, 0], pos[1, 0]] = 1
                direction[:] = clockwise * direction
            else:
                matrix[pos[0, 0], pos[1, 0]] = 0
                direction[:] = counter_clockwise * direction
    return record
