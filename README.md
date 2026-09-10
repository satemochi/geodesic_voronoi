Geodesic Voronoi Diagrams
====

This is a Python code for the two-dimensional geodesic Voronoi diagrams:
- Voronoi diagrams of points in a polygon
- Voronoi diagrams in a bounded plane contains obstacles.


<div align="center">
<img src="https://github.com/satemochi/geodesic_voronoi/blob/main/examples/ex_ipe.png" width=45%><img src="https://github.com/satemochi/geodesic_voronoi/blob/main/examples/ex1.png" width=45%></div>


## Description
- We consider the following problem in computational geometry:

** Given a (bounded) polygon $P \subset \mathbb{R}^2$ and a
set $S \subset P$ of points, compute the Voronoi diagram of $S$ in
the interior of $P$.**

- Our implementation solves this problem in the following naive way:
1. [Visibility graphs](https://en.wikipedia.org/wiki/Visibility_graph) / [visibility polygons](https://en.wikipedia.org/wiki/Visibility_polygon)
1. [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
1. [Additively weighted Voronoi diagrams](https://en.wikipedia.org/wiki/Weighted_Voronoi_diagram) (drawing with the hidden surface elimination)
1. [Boundary tracing](https://en.wikipedia.org/wiki/Boundary_tracing) / [Boolean operations on polygons](https://en.wikipedia.org/wiki/Boolean_operations_on_polygons)

- There are a lot of bugs, so it's still under-coded.


## Requirements
- [Python](https://www.python.org)
- [GLFW](https://www.glfw.org)
- [Matplotlib](https://matplotlib.org)
- [NetworkX](https://networkx.github.io)
- [PyOpenGL](https://pypi.org/project/PyOpenGL/)
- [PyVisiLibity](https://github.com/tsaoyu/PyVisiLibity)
- [Shapely](https://shapely.readthedocs.io/en/stable/)


## Installation
1. `pip install glfw matplotlib networkx PyOpenGL visilibity shapely`
1. Download `geodesic_voronoi.py` file, and
1. Copy and place it in any directory included in `sys.path` or the `PYTHONPATH` variable.



## Usage
See, python codes in [examples](https://github.com/satemochi/geodesic_voronoi/tree/main/examples) directory.



---
Copyright (c) 2026, <br/>
satemochi: [satemochi1@yahoo.co.jp](satemochi1@yahoo.co.jp) <br/>
All rights reserved.
