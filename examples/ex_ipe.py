from freetype import Face
from matplotlib import pyplot as plt
from matplotlib.path import Path
from shapely import union_all, orient_polygons
from shapely.affinity import scale, translate
from shapely.geometry import Polygon
from geodesic_voronoi import geodesic_voronoi, plot_polygon


def get_path(c, fname='Alice-Regular.ttf'):
    """ This function is presented originally of freetype-py:
        we can refer the source 'glyph-vector.py' in the examples directory.
    """
    face = Face(fname)
    face.set_char_size(24 * 64)
    face.load_char(c)
    slot = face.glyph
    outline = slot.outline

    start, end = 0, 0
    VERTS, CODES = [], []
    for i in range(len(outline.contours)):
        end = outline.contours[i]
        points = outline.points[start:end+1]
        points.append(points[0])
        tags = outline.tags[start:end+1]
        tags.append(tags[0])

        segments = [[points[0], ], ]
        for j in range(1, len(points)):
            segments[-1].append(points[j])
            if tags[j] & (1 << 0) and j < (len(points)-1):
                segments.append([points[j], ])
        verts = [points[0], ]
        codes = [Path.MOVETO, ]
        for segment in segments:
            if len(segment) == 2:
                verts.extend(segment[1:])
                codes.extend([Path.LINETO])
            elif len(segment) == 3:
                verts.extend(segment[1:])
                codes.extend([Path.CURVE3, Path.CURVE3])
            else:
                verts.append(segment[1])
                codes.append(Path.CURVE3)
                for i in range(1, len(segment)-2):
                    A, B = segment[i], segment[i+1]
                    C = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
                    verts.extend([C, B])
                    codes.extend([Path.CURVE3, Path.CURVE3])
                verts.append(segment[-1])
                codes.append(Path.CURVE3)
        VERTS.extend(verts)
        CODES.extend(codes)
        start = end+1
    return Path(VERTS, CODES)


def get_polygon(c):
    path = get_path(c)
    ext, holes = None, []
    for p in path.to_polygons():
        n = len(p)
        if sum(p[i][0] * p[(i+1) % n][1] - p[(i+1) % n][0] * p[i][1]
               for i in range(n)) > 0:  # if hold this then p is hole.
            holes.append(p[::-1])
        else:
            ext = p
    return orient_polygons(Polygon(ext, holes), exterior_cw=False)


if __name__ == '__main__':
    _I = get_polygon('I')
    assert _I.is_valid
    assert _I.exterior.is_ccw
    _p = translate(scale(get_polygon('p'), 0.7, 0.7), xoff=250, yoff=-100)
    assert _p.is_valid
    assert _p.exterior.is_ccw
    _e = translate(scale(get_polygon('e'), 0.7, 0.7), xoff=800, yoff=-130)
    assert _e.is_valid
    assert _e.exterior.is_ccw

    Ipe = orient_polygons(union_all([_I, _p, _e]), exterior_cw=False)
    assert Ipe.is_valid
    assert Ipe.exterior.is_ccw
    sites = [(120, 40), (1290, 400), (350, 322), (1150, 0), (750, 420)]
    cmap = [(153, 0, 0), (175, 97, 16), (191, 144, 0), (56, 118, 29),
            (19, 79, 92)]
    plt.scatter([x for x, _ in sites], [y for _, y in sites],
                s=25, ec='k', color='w', zorder=15)
    gvd = geodesic_voronoi(Ipe)
    # gvd.draw_visibility_graph()

    f = gvd.voronoi_regions(sites)
    for i, (s, b) in enumerate(f.items()):
        c = ('#' + hex(cmap[i][0])[2:].zfill(2) + hex(cmap[i][1])[2:].zfill(2)
             + hex(cmap[i][2])[2:].zfill(2))
        plot_polygon(b, fc=c, ec='k', lw=1.0)

    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.autoscale()
    plt.tight_layout()
    # plt.savefig('ex_ipe.png', bbox_inches='tight')
    plt.show()
