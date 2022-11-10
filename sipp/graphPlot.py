# -*- coding: utf-8 -*-
# @Author   : Coolister
# @Time     : 2022/11/3 17:36
# @Function ：

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sipp.toolBox import get_max_t, get_position, check_conflict


class GraphPlot(object):
    def __init__(self, config=None, plan=None):
        self.config = config
        self.plan = plan if plan else {}
        self.color = {
            'white': (248, 248, 255),
            'red': (178, 34, 34),
            'green': '#00CD66',
            'orange': '#FF7F00'
        }
        self.plans = {**self.plan, **self.config.dyn_obstacles}

    def draw(self, save_gif_fn=None):
        width, height = self.config.dimension
        plans = self.plans
        obs = [[self.color['white'] for _ in range(width)] for _ in range(height)]
        for i in self.config.obstacles:
            obs[i[1]][i[0]] = self.color['red']
        agv = get_position(plans)
        agv_x, agv_y = zip(*agv.values())
        max_t = get_max_t(plans)
        conflicts = check_conflict(self.plans)

        if len(conflicts) > 0:
            print('@There are conflicts in plans!!!')
            print(conflicts)

        fig, ax = plt.subplots()
        ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
        ax.yaxis.set_major_locator(plt.MultipleLocator(1.0))

        obs_img = ax.imshow(obs, origin='lower')
        xy = ax.transData.transform([(0, 1), (1, 0)]) - ax.transData.transform([(0, 0)])
        agv_img = ax.scatter(agv_x, agv_y, c=self.color['green'], s=(min(xy[0,1], xy[1,0])*0.6)**2)
        annotate_img = []
        for k, v in agv.items():
            annotate_img.append(ax.annotate(k, v, va="center", ha="center"))

        def animate(i):
            agv = get_position(plans, i)
            agv_pos = list(agv.values())
            agv_img.set_offsets(agv_pos)
            colors = None
            if i in conflicts:
                conflict = conflicts.get(i)
                colors = [self.color['green'] if i in conflict else self.color['orange'] for i in agv_pos]
                agv_img.set_color(colors)
            for annotate in annotate_img:
                id = annotate.get_text()
                pos = agv.get(id)
                annotate.set_position(pos)
            return (agv_img,*annotate_img,)

        ani = animation.FuncAnimation(fig, animate, repeat=False, frames=max_t, interval=800, blit=True)
        plt.grid()

        if save_gif_fn:
            if save_gif_fn.split('.')[-1] != 'gif':
                raise ValueError('File must be gif format!!')
            writer = animation.PillowWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
            ani.save(save_gif_fn, writer=writer)
        plt.show()




