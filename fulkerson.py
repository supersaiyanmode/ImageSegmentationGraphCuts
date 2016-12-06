from random import shuffle
import config
from utils import print_path
from utils import reachable_bfs

# Edmonds-Karp Algorithm implementation
def bfs(source, target):
    visited = set()
    queue = [(source, [])]

    while queue:
        node, path = queue.pop(0)
        visited.add(node.coord)
        if node.coord == target.coord:
            return path

        edges = [x for x in node.edges if x.residual > config.residue_thresh and
                 x.get_other(node).coord not in visited]
        if config.randomized_bfs:
            shuffle(edges)
        for edge in edges:
            neigh_node = edge.get_other(node)
            queue.append((neigh_node, path + [edge]))

    return None


def min_cut(graph, source, target):
    max_flow = 0
    while True:
        path = bfs(source, target)
        if path is None:
            break
        if config.verbose:
            print_path(path)

        min_edge = min(path, key=lambda x: x.residual)
        mid_edge_val = min_edge.residual
        max_flow += mid_edge_val

        for p in path:
            p.residual -= mid_edge_val

        if config.verbose >= 2:
            print "Minimum edge: ", min_edge
            print "Updated path: ", path
            print ""

    if config.verbose:
        print "Max flow:", max_flow

    fg_coords = reachable_bfs(target)
    bg_coords = [x for x in graph if x not in fg_coords]

    return fg_coords, bg_coords
