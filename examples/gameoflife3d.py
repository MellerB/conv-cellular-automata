import sys

sys.path.append("..")
from automaton import Automaton
from display import Display3D
import numpy as np


center = -27
kernel = np.full((3, 3, 3), 1)
kernel[1, 1, 1] = center

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


n = 10
size = 50
prop = 0.1

matrix = np.random.choice([0, 1], size=(n, n, n), p=[1 - prop, prop])
matrix = np.pad(matrix, (size - n) // 2, mode="constant", constant_values=(0))

n_iters = 50
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule)
record = automaton.run(n_iters)


disp = Display3D(
    record, offscreen=False, fps=5, mode="regular", color="b4", clarity_scale=0.8
)
disp.draw_all()
