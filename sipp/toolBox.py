# -*- coding: utf-8 -*-
# @Author   : Coolister
# @Time     : 2022/10/26 14:43
# @Function ：

from itertools import chain

def tuple_minus(tuple1, tuple2, is_abs=False, is_reduce=False):

    assert len(tuple1) == len(tuple2), 'Invalid input length.'
    if is_abs:
        re = tuple(abs(i[0] - i[1]) for i in zip(tuple1, tuple2))
    else:
        re = tuple(i[0] - i[1] for i in zip(tuple1, tuple2))
    return sum(re) if is_reduce else re


def get_position(plans, i=0):
    re = {}
    for id, plan in plans.items():
        if i < len(plan):
            re[id] = (plan[i]['x'], plan[i]['y'])
        else:
            re[id] = (plan[-1]['x'], plan[-1]['y'])
    return re


def get_max_t(plans):
    re = 0
    for id, plan in plans.items():
        re = max(re, len(plan))
    return re


def check_conflict(plans, safe_interval=0):
    max_t, queue = get_max_t(plans), [get_position(plans)]
    conflicts = {}
    for t in range(1, max_t):
        if len(queue) > safe_interval:
            queue.pop(0)
        conflicts_t = []
        pos_current = get_position(plans, t)
        for name, pos in pos_current.items():
            all_obs = []
            for plan in queue:
                all_obs.extend([v for k, v in plan.items() if k != name])
            if pos in set(all_obs):
                conflicts_t.append(pos)
        if len(conflicts_t) > 0:
            conflicts[t] = conflicts_t
        queue.append(pos_current)
    return conflicts


