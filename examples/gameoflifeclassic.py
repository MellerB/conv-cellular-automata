import numpy as np


def update(cur):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))

    for r, c in np.ndindex(cur.shape):
        num_alive = np.sum(cur[r - 1 : r + 2, c - 1 : c + 2]) - cur[r, c]

        if (cur[r, c] == 1 and 2 <= num_alive <= 3) or (
            cur[r, c] == 0 and num_alive == 3
        ):
            nxt[r, c] = 1

    return nxt


def run(img, epochs):
    img = [img]
    for i in range(epochs):
        img.append(update(img[-1]))
    return img
