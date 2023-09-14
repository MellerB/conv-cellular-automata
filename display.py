from vedo import *
from itertools import product
import math
import time
import numpy as np

FilenameException = Exception("Filename should end with '.mp4'")
np.seterr(all="raise")


class Display:
    def plotter_open(self):
        settings.use_fxaa = True
        self.plotter = Plotter(
            size=self.size, interactive=False, offscreen=self.offscreen
        )
        self.plotter.background(c1="black")

    def draw_all(self):
        self.t = 0
        self.plotter_open()
        self._init_cubes()
        video = Video(name=self.filename, fps=self.fps, backend="cv")
        pb = ProgressBar(0, len(self.record), c="r")
        draw = self._draw_next
        if self.mode == "slice":
            draw = self._draw_next_slice_mode
        if self.mode == "alternative":
            draw = self._draw_next_alt_mode
        for i in pb.range():
            draw()
            video.add_frame()
            pb.print()
        video.close()
        self.plotter.close()


class Display2D(Display):
    def __init__(
        self,
        record,
        color="r4",
        color_map="rainbow",
        mode="regular",
        size=(1080, 1080),
        offscreen=False,
        fps=10,
        filename="video.mp4",
        clarity_scale=0.9,
        min_value_displayed=0.1,
        cut_invariant=False,
    ):
        self.min_value_displayed = min_value_displayed
        self.clarity_scale = clarity_scale
        self.size = size
        self.mode = mode
        self.record = np.array(record)
        if mode != "alternative":
            self.record[self.record < min_value_displayed] = 0
        self.fps = fps
        self.t = 0
        self.xd = record[0].shape[0]
        self.yd = record[0].shape[1]
        self.cubes = np.empty(shape=(self.xd, self.yd), dtype=Cube)
        self.offscreen = offscreen
        if cut_invariant:
            for i in range(len(self.record) - 1):
                if np.all(self.record[i - 1] == self.record[i]):
                    self.record = self.record[:i]
                    print(
                        "length after cutting invariant iterations:", len(self.record)
                    )
                    break
        if filename.endswith(".mp4"):
            self.filename = filename
        else:
            raise FilenameException

        self.vars = list(product(range(self.xd), range(self.yd)))
        self.color = color
        self.color_map = color_map

    def _init_cubes(self):
        self.border = (
            Box(
                pos=(self.xd / 2 - 0.5, self.yd / 2 - 0.5, 0.5),
                length=self.xd,
                width=self.yd,
                height=1,
                alpha=1,
            )
            .color(self.color)
            .wireframe()
        )
        start = time.perf_counter()
        sums = [np.count_nonzero(t) for t in self.record]
        max = np.max(sums)
        print(
            "max:",
            max,
            "of:",
            self.xd * self.yd,
            "percentage:",
            round(max * 100 / (self.xd * self.yd)),
        )
        self.cubes = np.empty(max, dtype=Cube)
        for i in range(len(self.cubes)):
            c = Cube(
                pos=(0, 0, 0),
                side=1,
                alpha=1,
            )
            self.cubes[i] = c
        self.plotter.add(self.border)
        self.plotter.add(*list(self.cubes))
        print("Initialisation completed in:", time.perf_counter() - start, "s")

    def _draw_next(self):
        i = 0
        for x, y in np.ndindex(self.record[self.t].shape):
            value = self.record[self.t][x, y]

            if value:
                self.cubes[i].on()
                self.cubes[i].scale(value * self.clarity_scale, reset=True)
                self.cubes[i].pos(x, y, 0)
                self.cubes[i].color(self.color)
                i += 1
        for j in range(i, len(self.cubes)):
            self.cubes[j].off()
        self.plotter.show()
        self.t += 1

    def _draw_next_alt_mode(self):
        i = 0
        for x, y in np.ndindex(self.record[self.t].shape):
            value = self.record[self.t][x, y]

            if value:
                self.cubes[i].on()
                self.cubes[i].scale(self.clarity_scale, reset=True)
                self.cubes[i].pos(x, y, 0)
                self.cubes[i].color(
                    color_map(value, name=self.color_map, vmin=0, vmax=1)
                )
                i += 1
        for j in range(i, len(self.cubes)):
            self.cubes[j].off()
        self.plotter.show()
        self.t += 1


class Display3D(Display):
    def __init__(
        self,
        record,
        color="r4",
        color_map="rainbow",
        size=(1080, 1080),
        offscreen=False,
        fps=10,
        filename="video.mp4",
        mode="regular",
        clarity_scale=0.9,
        min_value_displayed=0.1,
        cut_invariant=False,
    ):
        self.clarity_scale = clarity_scale
        self.mode = mode
        self.record = np.array(record)
        if mode != "alternative":
            self.record[self.record < min_value_displayed] = 0
        self.size = size
        self.fps = fps
        self.t = 0
        self.xd = record[0].shape[0]
        self.yd = record[0].shape[1]
        self.zd = record[0].shape[2]
        self.cubes = None
        self.border = None
        self.offscreen = offscreen
        if cut_invariant:
            for i in range(len(self.record) - 1):
                if np.all(self.record[i - 1] == self.record[i]):
                    self.record = self.record[:i]
                    print(
                        "length after cutting invariant iterations:", len(self.record)
                    )
                    break
        if filename.endswith(".mp4"):
            self.filename = filename
        else:
            raise FilenameException

        self.vars = list(product(range(self.xd), range(self.yd), range(self.zd)))
        self.color = color
        self.color_map = color_map

    def _init_cubes(self):
        self.border = (
            Box(
                pos=(self.xd / 2 - 0.5, self.yd / 2 - 0.5, self.zd / 2 - 0.5),
                length=self.xd,
                width=self.yd,
                height=self.zd,
                alpha=1,
            )
            .color(self.color)
            .wireframe()
        )
        start = time.perf_counter()
        sums = [np.count_nonzero(t) for t in self.record]
        max = np.max(sums)
        print(
            "max:",
            max,
            "of:",
            self.xd * self.yd * self.zd,
            "percentage:",
            round(max * 100 / (self.xd * self.yd * self.zd)),
        )
        self.cubes = np.empty(max, dtype=Cube)
        for i in range(len(self.cubes)):
            c = Cube(
                pos=(0, 0, 0),
                side=1,
                alpha=0.5,
            )
            self.cubes[i] = c
        if self.mode != "slice":
            self.plotter.add(self.border)
        self.plotter.add(*list(self.cubes))
        print("Initialisation completed in:", time.perf_counter() - start, "s")

    def _draw_next(self):
        i = 0
        for x, y, z in np.ndindex(self.record[self.t].shape):
            value = self.record[self.t][x, y, z]

            if value:
                self.cubes[i].on()
                self.cubes[i].scale(value * self.clarity_scale, reset=True)
                self.cubes[i].pos(x, y, z)
                self.cubes[i].color(self.color)
                i += 1
        for j in range(i, len(self.cubes)):
            self.cubes[j].off()
        self.plotter.show(azimuth=0.5, roll=0)
        self.t += 1

    def _draw_next_slice_mode(self):
        i = 0
        k = (self.xd * self.yd) ** 0.5
        r = (k * self.zd) / 4.3
        for x, y, z in np.ndindex(self.record[self.t].shape):
            value = self.record[self.t][x, y, z]

            if value:
                self.cubes[i].on()
                self.cubes[i].scale(value * self.clarity_scale, reset=True)
                t = 2 * math.pi * (z / self.zd)
                self.cubes[i].pos(
                    x + r * math.sin(t) - self.xd / 2,
                    y + (r * math.cos(t)) - self.yd / 2,
                    0,
                )
                self.cubes[i].color(self.color)
                i += 1

        for j in range(i, len(self.cubes)):
            self.cubes[j].off()
        self.plotter.show(
            camera={
                "pos": (0, 0, r + 1.5 * max(self.xd, self.yd) + 1),
                "view_angle": 90.0,
            }
        )
        self.t += 1

    def _draw_next_alt_mode(self):
        i = 0
        for x, y, z in np.ndindex(self.record[self.t].shape):
            value = self.record[self.t][x, y, z]
            if value:
                self.cubes[i].on()
                self.cubes[i].scale(self.clarity_scale, reset=True)
                self.cubes[i].pos(x, y, z)

                self.cubes[i].color(
                    color_map(value, name=self.color_map, vmin=0.0, vmax=1.0)
                )
                i += 1

        for j in range(i, len(self.cubes)):
            self.cubes[j].off()
        self.plotter.show(azimuth=0.5, roll=0)
        self.t += 1


class Display4D(Display):
    def __init__(
        self,
        record,
        color_map="rainbow",
        size=(1080, 1080),
        offscreen=False,
        fps=10,
        filename="video.mp4",
        mode="regular",
        clarity_scale=0.9,
        min_value_displayed=0.1,
        cut_invariant=False,
    ):
        self.clarity_scale = clarity_scale
        self.mode = mode
        self.record = np.array(record)
        self.size = size
        self.mode = mode
        if mode != "alternative":
            self.record[self.record < min_value_displayed] = 0
        self.fps = fps
        self.t = 0
        self.xd = record[0].shape[0]
        self.yd = record[0].shape[1]
        self.zd = record[0].shape[2]
        self.qd = record[0].shape[3]
        self.sqrtqd = int(math.sqrt(self.qd) * 1.5) + 1
        self.cubes = None
        self.border = None
        self.offscreen = offscreen
        if cut_invariant:
            for i in range(len(self.record) - 1):
                if np.all(self.record[i - 1] == self.record[i]):
                    self.record = self.record[:i]
                    print(
                        "length after cutting invariant iterations:", len(self.record)
                    )
                    break
        if filename.endswith(".mp4"):
            self.filename = filename
        else:
            raise FilenameException

        self.vars = list(
            product(range(self.xd), range(self.yd), range(self.zd), range(self.qd))
        )
        self.color_map = color_map

    def _init_cubes(self):
        self.border = (
            Box(
                pos=(self.xd / 2 - 0.5, self.yd / 2 - 0.5, self.zd / 2 - 0.5),
                length=self.xd,
                width=self.yd,
                height=self.zd,
                alpha=1,
            )
            .color("w")
            .wireframe()
        )
        start = time.perf_counter()
        sums = [np.count_nonzero(t) for t in self.record]
        max = np.max(sums)
        print(
            "max:",
            max,
            "of:",
            self.xd * self.yd * self.zd * self.qd,
            "percentage:",
            round(max * 100 / (self.xd * self.yd * self.zd * self.qd)),
        )
        self.cubes = np.empty(max, dtype=Cube)
        for i in range(len(self.cubes)):
            c = Cube(
                pos=(0, 0, 0),
                side=1,
                alpha=0.3,
            )
            self.cubes[i] = c
        if self.mode != "slice":
            self.plotter.add(self.border)
        self.plotter.add(*list(self.cubes))
        print("Initialisation completed in:", time.perf_counter() - start, "s")

    def _draw_next(self):
        i = 0
        for x, y, z, q in np.ndindex(self.record[self.t].shape):
            value = self.record[self.t][x, y, z, q]

            if value:
                self.cubes[i].on()
                self.cubes[i].scale(value * self.clarity_scale, reset=True)

                self.cubes[i].pos(x, y, z)
                self.cubes[i].color(
                    color_map(q, name=self.color_map, vmin=0, vmax=self.qd - 1)
                )
                i += 1

        for j in range(i, len(self.cubes)):
            self.cubes[j].off()
        self.plotter.show(azimuth=0.5, roll=0)
        self.t += 1

    def _draw_next_slice_mode(self):
        i = 0
        k = (self.xd * self.yd) ** 0.5
        r = (k * self.qd) / 4.3
        for x, y, z, q in np.ndindex(self.record[self.t].shape):
            value = self.record[self.t][x, y, z, q]

            if value:
                self.cubes[i].on()
                self.cubes[i].scale(value * self.clarity_scale, reset=True)
                t = 2 * math.pi * (q / self.qd)
                self.cubes[i].pos(
                    x + r * math.sin(t) - self.xd / 2,
                    y + (r * math.cos(t)) - self.yd / 2,
                    z,
                )
                self.cubes[i].color(
                    color_map(q, name=self.color_map, vmin=0, vmax=self.qd - 1)
                )
                i += 1

        for j in range(i, len(self.cubes)):
            self.cubes[j].off()
        self.plotter.show(
            camera={
                "pos": (0, 0, r + 1.5 * max(self.xd, self.yd) + 1),
                "view_angle": 90.0,
            }
        )
        self.t += 1
