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
