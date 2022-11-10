# -*- coding: utf-8 -*-
# @Author   : Coolister
# @Time     : 2022/10/26 10:40
# @Function ：

from sipp.graphConstruction import Map, Graph, Interval
from sipp.toolBox import tuple_minus
import heapq
# from graphPlot import GraphPlot

from sipp.constants import SAFE_DURATION

class Config(Map):
    def __init__(self, dimension, obstacles, dyn_obstacles, start, end, id, start_t=0):
        Map.__init__(self, dimension, obstacles, dyn_obstacles)
        self.id = id
        self.start = start
        self.end = end
        self.start_t = start_t


class State(object):
    def __init__(self, cfg, t=0, g=float('inf'), h=float('inf'), interval=Interval(), parent=None):
        self.cfg = cfg
        self.t = t
        self.g = g
        self.h = h
        self.interval = interval
        self.parent = parent

    @property
    def f(self):
        return self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.cfg == other.cfg and self.interval == other.interval

    def __str__(self):
        return 'cfg:({},{});interval:({},{})'.format(self.cfg[0], self.cfg[1], self.interval.start, self.interval.end)

    def get_json(self):
        return {'t': self.t, 'x': self.cfg[0], 'y': self.cfg[1]}


class Sipp(Graph):
    def __init__(self, config):
        Graph.__init__(self, config)
        self.config = config

    def get_start_interval(self):
        grid = self.graph[self.config.start]
        for interval in grid.timeline:
            if interval.contain(self.config.start_t):
                return interval
        raise ValueError('Start time invalid!!')

    def get_heuristic(self, cfg):
        return tuple_minus(cfg, self.config.end, is_abs=True, is_reduce=True)

    def get_successors(self, s):
        successors = []
        m_time = 1
        neighbour_list = self.get_valid_neighbours(s.cfg)

        for neighbour in neighbour_list:
            start_t = s.t + m_time
            end_t = s.interval.end + m_time
            for interval in self.graph[neighbour].timeline:
                if interval.start > end_t or interval.end < start_t:
                    continue
                t = max(start_t, interval.start)
                cost = t - s.t
                parent = self.graph[s.cfg].movement.get(t)
                if t + SAFE_DURATION > interval.end:
                    continue
                elif parent == neighbour:
                    continue
                successor = State(neighbour, t, s.g + cost, self.get_heuristic(neighbour), interval, s)
                successors.append(successor)
        return successors

    def graph_search(self):
        open = []
        visited = {}
        goal_expanded = False
        goal_node = None

        h_start = self.get_heuristic(self.config.start)
        i_start = self.get_start_interval()
        s_start = State(cfg=self.config.start, g=0, h=h_start, interval=i_start)
        heapq.heappush(open, s_start)
        visited[str(s_start)] = s_start

        while open and not goal_expanded:
            s = heapq.heappop(open)
            successors = self.get_successors(s)
            for successor in successors:
                if successor.cfg == self.config.end:
                    goal_expanded = True
                    goal_node = successor
                    break
                if str(successor) not in visited:
                    visited[str(successor)] = successor
                    heapq.heappush(open, successor)
                elif visited[str(successor)].g > s.g :
                    visited[str(successor)].g = s.g
                    visited[str(successor)].t = successor.t
                    heapq.heappush(open, visited[str(successor)])

        if goal_node is None:
            print('@No feasible solution found for {}!!'.format(self.config.id))
            return None

        plan = []
        current = goal_node
        while current:
            plan.insert(0, current.get_json())
            if current.parent:
                for i in range(current.t - current.parent.t - 1):
                    tmp_json = current.parent.get_json()
                    tmp_json['t'] += i + 1
                    plan.insert(0, tmp_json)
            current = current.parent

        return plan




