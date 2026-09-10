from itertools import combinations, groupby
from math import ceil, dist
import glfw
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
from OpenGL.GL import *
from shapely import intersection
from shapely.geometry import Polygon
import visilibity as vis


class geodesic_voronoi:
    def __init__(self, poly):
        self.poly = poly
        self.eps = 1.e-6
        self.__set_width_height()
        self.vg, self.env = self.__get_visibility_graph()
        self.__comp_bases()

    def __set_width_height(self):
        x1, y1, x2, y2 = self.poly.bounds
        mag = max(x2 - x1, y2 - y1)
        self.w, self.h = int(mag), int(mag * (y2 - y1) / (x2 - x1))

    def __get_visibility_graph(self):
        env, rv = self.__const_environment(self.poly)
        vis_vg = vis.Visibility_Graph(env, self.eps)
        nx_vg = nx.Graph()
        for ui, vi in combinations((i for i in range(vis_vg.n())
                                    if (env(i).x(), env(i).y()) in rv), 2):
            if vis_vg(ui, vi):
                u, v = (env(ui).x(), env(ui).y()), (env(vi).x(), env(vi).y())
                nx_vg.add_edge(u, v, weight=dist(u, v))
        return nx_vg, env

    def __const_environment(self, p, delta=1.0):
        assert p.exterior.is_ccw
        assert all(not h.is_ccw for h in p.interiors)
        simp = p.exterior.coords[:-1]
        boundaries = [vis.Polygon([vis.Point(x, y) for x, y in simp])]
        reflex = [simp[i] for i in range(-1, len(simp)-1)
                  if not self.__ccw(simp[i-1], simp[i], simp[i+1])]
        for h in p.interiors:
            simp = h.coords[:-1]
            boundaries.append(vis.Polygon([vis.Point(x, y) for x, y in simp]))
            reflex += [simp[i] for i in range(-1, len(simp)-1)
                       if not self.__ccw(simp[i-1], simp[i], simp[i+1])]
        return vis.Environment(boundaries), reflex

    @staticmethod
    def __ccw(p, q, r):
        (px, py), (qx, qy), (rx, ry) = p, q, r
        return ((qx - px) * (ry - py) - (qy - py) * (rx - px)) > 0

    def __comp_bases(self):
        for v in self.vg:
            self.vg.nodes[v]['base'] = self.__get_base_coordinates(v)

    def __get_base_coordinates(self, s):
        cpts = self.__get_circum_points(s)
        return [(p[0], p[1], dist(s, p)) for p in cpts]

    def __get_circum_points(self, p, minlen=10):
        vertices = self.__get_snapped_vertices(self.__get_isovist(p))
        n, o, points = len(vertices), np.array(p), []
        for i in range(n):
            _p, _q = vertices[i], vertices[(i+1) % n]
            if p == _p or p == _q:
                if p == _q:
                    points.append(p)
                continue
            sdiv_count = int(ceil(dist(_p, _q) / minlen))
            pts = zip(np.linspace(_p[0], _q[0], sdiv_count),
                      np.linspace(_p[1], _q[1], sdiv_count))
            points += pts
        return (a := [p[0] for p in groupby(points)]) + [a[0]]

    def __get_isovist(self, p):
        v = vis.Point(*p)
        v.snap_to_boundary_of(self.env, self.eps)
        v.snap_to_vertices_of(self.env, self.eps)
        return vis.Visibility_Polygon(v, self.env, self.eps)

    def __get_snapped_vertices(self, isovist):
        vertices = []
        for i in range(isovist.n()):
            p = isovist[i]
            p.snap_to_vertices_of(self.env, self.eps)
            p.snap_to_boundary_of(self.env, self.eps)
            vertices.append((p.x(), p.y()))
        return vertices + [vertices[0]]

    def voronoi_regions(self, sites):
        glfw.init()
        glfw.window_hint(glfw.VISIBLE, False)
        window = glfw.create_window(self.w, self.h,
                                    "hidden window", None, None)
        glfw.make_context_current(window)
        self.__setup()
        cmap = [(i+1, i+1, i+1) for i in range(len(sites))]
        for s, c in zip(sites, cmap):
            glColor3ubv(c)
            self.__draw_site(s)
            self.__draw_reflexes(s)

        regions = {sites[i]: intersection(Polygon(b), self.poly)
                   for i, b in enumerate(self.__get_boundaries(sites, cmap))}

        glfw.destroy_window(window)
        glfw.terminate()
        return regions

    def __setup(self):
        x1, y1, x2, y2 = self.poly.bounds
        glViewport(0, 0, self.w, self.h)
        glOrtho(x1, x2, y1, y2, (_ := max(x2-x1, y2-y1)), -_)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def __draw_site(self, s):
        bases = self.__get_base_coordinates(s)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*s)
        for p in bases:
            glVertex3f(*p)
        glEnd()

    def __draw_reflexes(self, s):
        dist = self.__geodesic_distances(s)
        for v in self.vg:
            glPushMatrix()
            glTranslatef(0, 0, dist[v])
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(*v)
            for p in self.vg.nodes[v]['base']:
                glVertex3f(*p)
            glEnd()
            glPopMatrix()

    def __geodesic_distances(self, s):
        vertices = self.__get_snapped_vertices(self.__get_isovist(s))
        for v in vertices:
            if v in self.vg:
                self.vg.add_edge(v, s, weight=dist(v, s))
        lengths = nx.single_source_dijkstra_path_length(self.vg, s)
        self.vg.remove_node(s)
        return lengths

    def __get_boundaries(self, sites, cmap):
        buf = glReadPixels(0, 0, self.w, self.h, GL_RED, GL_UNSIGNED_BYTE)
        image = np.frombuffer(buf, dtype=np.uint8).reshape(self.h, self.w)
        for s, c in zip(sites, cmap):
            yield self.__boundary_tracing(s, c, image)

    def __boundary_tracing(self, s, c, img):
        x, y = s
        x1, y1, x2, y2 = self.poly.bounds
        aw, ah = x2 - x1, y2 - y1

        gx = int(self.w * (x - x1) / aw)
        gy = int(self.h * (y - y1) / ah)
        assert img[gy][gx] == c[0]

        boundaries, d = [self.__find_left_most(img, c, gx, gy)], 4
        while True:
            d = (d + 6) & 7 if d & 1 else (d + 7) & 7
            while True:
                next_x, next_y = boundaries[-1]
                if d == 0:
                    next_y += 1
                elif d == 1:
                    next_x, next_y = next_x - 1, next_y + 1
                elif d == 2:
                    next_x -= 1
                elif d == 3:
                    next_x, next_y = next_x - 1, next_y - 1
                elif d == 4:
                    next_y -= 1
                elif d == 5:
                    next_x, next_y = next_x + 1, next_y - 1
                elif d == 6:
                    next_x += 1
                elif d == 7:
                    next_x, next_y = next_x + 1, next_y + 1
                if self.__check_valid_image_boundaries(img, c, next_x, next_y):
                    boundaries.append((next_x, next_y))
                    break
                d = (d + 1) & 7
            if len(boundaries) >= 4:
                if (boundaries[-1] == boundaries[1] and
                        boundaries[-2] == boundaries[0]):
                    break

        return [(gx * aw / self.w + x1, gy * ah / self.h + y1)
                for gx, gy in boundaries]

    def __find_left_most(self, img, c, gx, gy):
        for x in range(gx, -1, -1):
            if img[gy][x] != c[0]:
                return (x+1, gy)
        return (0, gy)

    def __check_valid_image_boundaries(self, img, c, next_x, next_y):
        if (next_y >= self.h or next_x < 0 or next_y < 0 or next_x >= self.w):
            return False
        if img[next_y][next_x] == c[0]:
            return True

    def draw_visibility_graph(self, **kwargs):
        nx.draw_networkx_edges(self.vg, {v: v for v in self.vg}, **kwargs)


def plot_polygon(poly, **kwargs):
    if poly.geom_type == 'Polygon':
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch
        from matplotlib.collections import PatchCollection
        path = Path.make_compound_path(
            Path(np.asarray(poly.exterior.coords)[:, :2]),
            *[Path(np.asarray(r.coords)[:, :2]) for r in poly.interiors])
        patch = PathPatch(path, **kwargs)
        collection = PatchCollection([patch], **kwargs)
        plt.gca().add_collection(collection, autolim=True)
