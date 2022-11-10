# -*- coding: utf-8 -*-
# @Author   : Coolister
# @Time     : 2022/10/24 11:32
# @Function ：

import bisect
from sipp.constants import SAFE_DURATION

class Interval(object):
    def __init__(self, start=0, end=float('inf')):
        self.start = start
        self.end = end

    def __lt__(self, other):
        assert type(other) == Interval, 'Comparison input type is wrong'
        return self.start < other.start

    def __eq__(self, other):
        assert type(other) in (int, float, Interval), 'Comparison input type is wrong'
        if type(other) in (int, float):
            return other == self.start
        elif type(other) == Interval:
            return self.start == other.start and self.end == self.end

    def __len__(self):
        return self.end - self.start + 1

    def __getitem__(self, item):
        assert type(item) == slice, 'Invalid argument type.'
        start = item.start if item.start is not None else self.start
        end = item.stop if item.stop is not None else self.end
        return Interval(start, end)

    def contain(self, t):
        return self.start <= t <= self.end

    def add_start(self, other):
        pass


class Grid(object):
    def __init__(self, position):
        self.position = position
        self.timeline = [Interval()]
        self.movement = {}

    def split_interval(self, t, p=None, last_t=False):

        if p:
            self.movement[t] = p
        for interval in self.timeline:
            if last_t:
                if t <= interval.start:
                    self.timeline.remove(interval)
                elif t > interval.end:
                    continue
                else:
                    self.timeline.remove(interval)
                    bisect.insort_left(self.timeline, interval[:t - 1])
                    break
            else:
                if not interval.contain(t + SAFE_DURATION):
                    continue
                elif t == interval:
                    self.timeline.remove(interval)
                    if interval.contain(t + SAFE_DURATION + 1):
                        bisect.insort_left(self.timeline, interval[t + SAFE_DURATION + 1:])
                    break
                elif t == interval.end:
                    self.timeline.remove(interval)
                    if interval.contain(t - 1):
                        bisect.insort_left(self.timeline, interval[:t - 1])
                    break
                elif interval.contain(t):
                    self.timeline.remove(interval)
                    bisect.insort_left(self.timeline, interval[:t - 1])
                    if interval.contain(t + SAFE_DURATION + 1):
                        bisect.insort_left(self.timeline, interval[t + SAFE_DURATION + 1:])
                    break


class Map(object):
    def __init__(self, dimension, obstacles, dyn_obstacles):
        self.dimension = dimension
        self.obstacles = obstacles
        self.dyn_obstacles = dyn_obstacles

    def get_width(self):
        return self.dimension[0]

    def get_height(self):
        return self.dimension[1]


class Graph(object):
    def __init__(self, map):
        self.map = map
        self.graph = {}
        self.init_graph()
        self.init_interval()

    def init_graph(self):
        for i in range(self.map.get_width()):
            for j in range(self.map.get_height()):
                self.graph[(i, j)] = Grid((i, j))

    def init_interval(self):
        if not self.map.dyn_obstacles:
            return
        for name, plan in self.map.dyn_obstacles.items():
            for i in range(len(plan)):
                state = plan[i]
                last_t = i == len(plan) - 1
                position = (state.get('x'), state.get('y'))
                t = state.get('t')
                p = None
                if i > 0:
                    state_prev = plan[i - 1]
                    p = (state_prev.get('x'), state_prev.get('y'))
                self.graph[position].split_interval(t, p, last_t)

    def is_valid_position(self, position):
        dim_check = position[0] in range(self.map.get_width()) and position[1] in range(self.map.get_height())
        obs_check = position not in self.map.obstacles
        return dim_check and obs_check

    def get_valid_neighbours(self, position):
        neighbour_list = []

        up = (position[0], position[1] + 1)
        if self.is_valid_position(up): neighbour_list.append(up)

        down = (position[0], position[1] - 1)
        if self.is_valid_position(down): neighbour_list.append(down)

        left = (position[0] - 1, position[1])
        if self.is_valid_position(left): neighbour_list.append(left)

        right = (position[0] + 1, position[1])
        if self.is_valid_position(right): neighbour_list.append(right)

        return neighbour_list
