Geodesic Voronoi Diagrams
====

This is a Python code for the two-dimensional geodesic Voronoi diagrams:
- Voronoi diagrams of points in a polygon
- Voronoi diagrams in a bounded plane contains obstacles.


<div align="center">
<img src="https://github.com/satemochi/geodesic_voronoi/blob/main/examples/ex_ipe.png" width=45%><img src="https://github.com/satemochi/geodesic_voronoi/blob/main/examples/ex1.png" width=45%></div>


## Description
- We consider the following problem in computational geometry:

> **Given a (bounded) polygon $P \subset \mathbb{R}^2$ and a
set $S \subset P$ of points, compute the Voronoi diagram of $S$ in
the interior of $P$.**

Computing the geodesic Voronoi diagram is equivalent to constructing
the oracle $f$ mapping $P \to S,$
such that $\forall p \in P ~:~ f(p) = \mathrm{argmin}_{s \in S} \|p - s\|_P$
where $\|\cdot\|_P$ is the
[geodesic distance](https://en.wikipedia.org/wiki/Distance_(graph_theory))
with respect to (the visibiity graph of) $P$.

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
- [Numpy](https://numpy.org)
- [PyOpenGL](https://pypi.org/project/PyOpenGL/)
- [PyVisiLibity](https://github.com/tsaoyu/PyVisiLibity)
- [Shapely](https://shapely.readthedocs.io/en/stable/)


## Installation
1. `pip install glfw matplotlib networkx PyOpenGL visilibity shapely`
1. Download `geodesic_voronoi.py` file, and
1. Copy and place it in any directory included in `sys.path` or the `PYTHONPATH` variable.



## Usage
See, python codes in [examples](https://github.com/satemochi/geodesic_voronoi/tree/main/examples) directory.


A simple sample code `examples/ex1.py` is shown as follows:
```python
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
from geodesic_voronoi import geodesic_voronoi, plot_polygon


if __name__ == '__main__':
    shell = [(0, 0), (1600, 0), (1600, 1600), (0, 1600)]
    holes = [[(800, 800), (800, 1000), (1500, 1000), (1500, 800)],
             [(200, 900), (200, 1200), (900, 1200), (900, 1100), (300, 1100),
              (300, 900)],
             [(100, 100), (100, 200), (400, 200), (400, 100)],]
    poly = Polygon(shell=shell, holes=holes)
    gvd = geodesic_voronoi(poly)
    # gvd.draw_visibility_graph(edge_color='g', alpha=0.5)

    sites = [(120, 50), (1290, 400), (350, 1322), (1150, 10), (750, 420)]
    cmap = [(153, 0, 0), (175, 97, 16), (191, 144, 0), (56, 118, 29),
            (19, 79, 92)]
    f = gvd.voronoi_regions(sites)
    for i, (s, b) in enumerate(f.items()):
        c = ('#' + hex(cmap[i][0])[2:].zfill(2) + hex(cmap[i][1])[2:].zfill(2)
             + hex(cmap[i][2])[2:].zfill(2))
        plot_polygon(b, fc=c, ec='k', lw=1.5)
    plt.scatter([x for x, _ in sites], [y for _, y in sites],
                s=25, c='w', ec='k', zorder=5)

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
    # plt.savefig('ex1.png', bbox_inches='tight')
    plt.show()
```
When declaring the input polygon in Shapely,
its exterior must be CCW and each hole must be CW.

---
Copyright (c) 2026, <br/>
satemochi: [satemochi1@yahoo.co.jp](satemochi1@yahoo.co.jp) <br/>
All rights reserved.
