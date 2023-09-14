import sys

sys.path.append("..")
from automaton import Automaton
from display import Display4D
import numpy as np

center = -81
kernel = np.full((3, 3, 3, 3), 1)
kernel[1, 1, 1, 1] = center

REMAIN = [2, 3]
SPAWN = [3]


def rule(x):
    if x > 0:  # cell is dead
        if x in SPAWN:
            return 1
        return 0
    else:  # cell is alive
        x -= center
        if x in REMAIN:
            return 1
        return 0


n = 5
size = 30
prop = 0.1

matrix = np.random.choice([0, 1], size=(n, n, n, n), p=[1 - prop, prop])

matrix = np.pad(matrix, (size - n) // 2, mode="constant", constant_values=(0))

n_iters = 20
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule)
record = automaton.run(n_iters)

disp = Display4D(record, offscreen=False, fps=2, mode="regular", clarity_scale=0.8)
disp.draw_all()
