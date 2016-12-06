from itertools import izip
from random import shuffle

import config
from utils import print_path
from utils import reachable_bfs


def bfs_level_order(source):
    queue = [(source, [])]
    visited = set()
    all_paths = {}

    while queue:
        next_level_successors = []
        for node, path in queue:
            visited.add(node.coord)
            all_paths[node.coord] = path

            edges = [x for x in node.edges if x.residual > config.residue_thresh and
                     x.get_other(node).coord not in visited]
            if config.randomized_bfs:
                shuffle(edges)
            for edge in edges:
                neigh_node = edge.get_other(node)
                next_level_successors.append((neigh_node, path + [edge]))

        yield all_paths

        queue = next_level_successors


def bidirectional_search(source, target):
    paths = []
    for s, t in izip(bfs_level_order(source), bfs_level_order(target)):
        for key in s.viewkeys() & t.viewkeys():
            paths.append(s[key] + t[key][::-1])
    return sorted(paths, key=len)


def min_cut(graph, source, target):
    max_flow = 0
    while True:
        paths = bidirectional_search(source, target)
        if not paths:
            break
        for path in paths:
            min_edge = min(path, key=lambda x: x.residual)
            mid_edge_val = min_edge.residual

            if mid_edge_val <= config.residue_thresh:
                continue

            if config.verbose:
                print_path(path)

            max_flow += mid_edge_val

            for p in path:
                p.residual -= mid_edge_val

            if config.verbose >= 2:
                print "Minimum edge: ", mid_edge_val
                print "Updated path: ", path
                print ""

    if config.verbose:
        print "Max flow:", max_flow

    fg_coords = reachable_bfs(target)
    bg_coords = [x for x in graph if x not in fg_coords]

    return fg_coords, bg_coords
