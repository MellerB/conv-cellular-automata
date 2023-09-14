import sys

sys.path.append("..")
from automaton import Automaton
from display import Display4D
import numpy as np

kernel = np.random.uniform(low=-1, high=1, size=(3, 3, 3, 3))
print(kernel)
kersum = np.sum(kernel)


def rule(x):
    return (np.sin(x / kersum) + 1) / 2


n = 10
prop = 0.1

matrix = np.random.choice([0, 1], size=(n, n, n, n), p=[1 - prop, prop])


n_iters = 50
automaton = Automaton(init_matrix=matrix, kernel=kernel, rule=rule, wrap=False)
record = automaton.run(n_iters)


disp = Display4D(record, mode="slice", offscreen=True, fps=5)
disp.draw_all()
