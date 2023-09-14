import sys

sys.path.append("..")
from automaton import Automaton
from display import Display2D
import numpy as np

kernel = np.random.uniform(low=-1, high=1, size=(3, 3))
print(kernel)
kersum = np.sum(kernel)


def rule(x):
    return (np.sin(x / kersum) + 1) / 2


n = 50
prop = 0.1

matrix = np.random.choice([0, 1], size=(n, n), p=[1 - prop, prop])

n_iters = 150
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=True)
record = automaton.run(n_iters)


disp = Display2D(record, offscreen=True, mode="alternative", color="g4", fps=30)
disp.draw_all()
