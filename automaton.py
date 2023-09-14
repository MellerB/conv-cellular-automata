import numpy as np
from scipy import ndimage


class Automaton:
    def __init__(self, init_matrix, kernel, rule, wrap=False):
        self.record = []
        self.rule = np.vectorize(rule)
        self.kernel = np.array(kernel)
        self.matrix = np.array(init_matrix)
        self.record.append(self.matrix)

        self.pad = None
        if not wrap:
            self.pad = "constant"
        else:
            self.pad = "wrap"

    def run(self, n_iters):
        for i in range(n_iters):
            self.matrix = ndimage.convolve(self.matrix, self.kernel, mode=self.pad)
            self.matrix = self.rule(self.matrix)
            self.record.append(self.matrix)
        return self.record
