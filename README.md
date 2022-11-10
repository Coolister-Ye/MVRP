# MVRP

This project is aiming to solve multiple vehicle routing problems.

## Introduction

This project implemented SIPP algorithm to plan the paths for multiple vehicles in a grid-fashion map.
Originally, SIPP solve the routing once at a time. To get the plan for multiple
vehicles, the algorithm need to be called in a sequential fashion. In this way, the
order of routing can be important. However, ordering the routing(deciding which vehicle to plan first) 
is out of the scope of this project and may be considered in the future.

## Easy run

To use the SIPP algo just follow the example code in [sippExample.py](/sippExample.py).
There are several settings can be used to configure the planner.

- [SAFE_DURATION](/sipp/constants.py): The time need to wait until a position can be defined as totally available (Default=0). 
For example, after a vehicle left position (0, 0), this position need to be locked down for SAFE_DURATION
seconds to avoid potential conflicts.
- config: The configuration of the sipp planner.
  - dimension: (width, height)
  - obstacles: List of positions where are unavailable.
  - dyn_obstacles: List of routing of dynamic obstacles, which can be planned vehicles or other moving items.
  - start: Start position
  - end: Goal position
  - id: Name of the routing vehicle
  - start_t: Start timestamp (Default=0), if this value greater than 0, it means vehicle won't show up in the map until that timestamp 

## Results

To plot the result, can use the code in [graphPlot.py](/sipp/graphPlot.py).
There are several cases showed below, which demonstrate the difference between 0 and 1 SAFE_DURATION setting, 
complex situation/map like single plank.

| SAFE_DURATION==0           | SAFE_DURATION==1           |
|----------------------------|----------------------------|
| ![0](/pic/svrp_0_safe.gif) | ![1](/pic/svrp_1_safe.gif) |


| Single Plank                  | Multiple Vehicle Routing    |
|-------------------------------|-----------------------------|
| ![0](/pic/svrp_sp_1_safe.gif) | ![1](/pic/mvrp_1_safe.gif)  |
