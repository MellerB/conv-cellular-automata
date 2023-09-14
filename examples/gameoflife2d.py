import sys

sys.path.append("..")
from automaton import Automaton
from display import Display2D
import numpy as np

center = -9
kernel = [[1, 1, 1], [1, -9, 1], [1, 1, 1]]

REMAIN = [2, 3]
SPAWN = [3]


def rule(x):
    if x > 0:  # cell is dead
        n = x
        if n in SPAWN:
            return 1
        return 0
    else:  # cell is alive
        n = x - center
        if n in REMAIN:
            return 1
        return 0


n = 40
size = 100
prop = 0.4

matrix = np.random.choice([0, 1], size=(n, n), p=[1 - prop, prop])
matrix = np.pad(matrix, (size - n) // 2, mode="constant", constant_values=(0))


n_iters = 100
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)


disp = Display2D(record, offscreen=True, color="b4", fps=10)
disp.draw_all()
