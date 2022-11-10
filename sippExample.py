# -*- coding: utf-8 -*-
# @Author   : Coolister
# @Time     : 2022/11/9 14:32
# @Function ：

from sipp.graphPlot import *
from sipp.graphConstruction import *
from sipp.graphSearch import *
from sipp.constants import SAFE_DURATION


def runGraphPlot():
    dyn_obs = {
        '0': [
            {'t': 0, 'x': 2, 'y': 2},
            {'t': 1, 'x': 1, 'y': 2},
            {'t': 2, 'x': 1, 'y': 1},
            {'t': 3, 'x': 1, 'y': 0},
            {'t': 4, 'x': 0, 'y': 0}
        ]
    }

    config = Config(dimension=(3, 3), obstacles=[(0, 1), (2, 1)], dyn_obstacles=dyn_obs, start=(0, 0), end=(2, 2), id='1')
    plotter = GraphPlot(config)
    plotter.draw()

def runGraphSearch():
    dyn_obs = {
        '0': [
            {'t': 0, 'x': 2, 'y': 2},
            {'t': 1, 'x': 1, 'y': 2},
            {'t': 2, 'x': 1, 'y': 1},
            {'t': 3, 'x': 1, 'y': 0},
            {'t': 4, 'x': 0, 'y': 0}
        ]
    }

    config = Config(dimension=(3, 3), obstacles=[(0, 1), (2, 1)], dyn_obstacles=dyn_obs, start=(0, 0), end=(2, 2), id='1')
    planner = Sipp(config)
    plan = planner.graph_search()
    if plan is None:
        print('cannot find feasible solution!!')
    else:
        plotter = GraphPlot(config, {config.id: plan})
        plotter.draw('pic/svrp_{}_safe.gif'.format(SAFE_DURATION))


def runGraphSearchSinglePlank():
    dyn_obs = {
        '0': [
            {'t': 0, 'x': 0, 'y': 1},
            {'t': 1, 'x': 1, 'y': 1},
            {'t': 2, 'x': 2, 'y': 1},
            {'t': 3, 'x': 3, 'y': 1},
            {'t': 4, 'x': 4, 'y': 1},
            {'t': 5, 'x': 5, 'y': 1},
            {'t': 6, 'x': 6, 'y': 1},
            {'t': 7, 'x': 7, 'y': 1},
            {'t': 8, 'x': 8, 'y': 1},
            {'t': 9, 'x': 9, 'y': 1},
        ]
    }
    obstacles = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
                 (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (9, 2)]
    config = Config(dimension=(10, 3), obstacles=obstacles, dyn_obstacles=dyn_obs, start=(6, 1), end=(0, 1), id='1')

    planner = Sipp(config)
    plan = planner.graph_search()
    if plan is None:
        print('cannot find feasible solution!!')
    else:
        plotter = GraphPlot(config, {config.id: plan})
        plotter.draw('pic/svrp_sp_{}_safe.gif'.format(SAFE_DURATION))


def runGraphSearchMulti():

    dyn_obs = {}
    map_config = {
        'dimension': (11, 13),
        'obstacles': [(10, 11), (9, 1), (3, 0), (7, 12), (2, 8), (8, 0), (4, 12), (2, 12), (8, 4),
                      (10, 3), (4, 0), (10, 8), (9, 0), (10, 7), (5, 12), (10, 12),
                      (9, 11), (5, 0), (0, 4), (10, 0), (10, 9), (0, 0), (10, 4), (6, 0), (1, 4),
                      (0, 12), (10, 1), (6, 12), (1, 0), (0, 8), (10, 5), (7, 0),
                      (3, 12), (1, 12), (8, 12), (10, 10), (3, 8), (2, 0), (1, 8), (8, 8), (3, 4),
                      (2, 4), (9, 12), (10, 2)]
    }
    vehicle = [
        {'name': '0', 'start': (9, 3),  'goal': (1, 3)},
        {'name': '1', 'start': (9, 7),  'goal': (2, 7)},
        {'name': '2', 'start': (9, 9),  'goal': (2, 9)},
        {'name': '3', 'start': (9, 5),  'goal': (2, 5)},
        {'name': '4', 'start': (7, 1),  'goal': (2, 3)},
        {'name': '5', 'start': (7, 11), 'goal': (1, 9)},
        {'name': '6', 'start': (8, 1),  'goal': (1, 5)},
        {'name': '7', 'start': (8, 11), 'goal': (1, 7)}
    ]
    for i, v in enumerate(vehicle):
        config = Config(dimension=map_config['dimension'], obstacles=map_config['obstacles'], dyn_obstacles=dyn_obs,
                        start=v['start'], end=v['goal'], id=v['name'])
        planner = Sipp(config)
        plan = planner.graph_search()
        if i < len(vehicle) - 1:
            dyn_obs.update({config.id: plan})
        else:
            plotter = GraphPlot(config, {config.id: plan})
            plotter.draw('pic/mvrp_{}_safe.gif'.format(SAFE_DURATION))


if __name__ == '__main__':
    # runGraphPlot()
    # runGraphSearch()
    # runGraphSearchSinglePlank()
    runGraphSearchMulti()
