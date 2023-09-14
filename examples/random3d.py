import sys

sys.path.append("..")
from automaton import Automaton
from display import Display3D
import numpy as np
import math


kernel = np.random.uniform(low=-1, high=1, size=(3, 3, 3))
print(kernel)
kersum = np.sum(kernel)


def rule(x):
    return (np.sin(x / kersum) + 1) / 2


n = 20
prop = 0.01

matrix = np.random.choice([0, 1], size=(n, n, n), p=[1 - prop, prop])

n_iters = 50
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)


disp = Display3D(
    record, offscreen=True, mode="alternative", color="b4", fps=5, clarity_scale=0.7
)
disp.draw_all()
