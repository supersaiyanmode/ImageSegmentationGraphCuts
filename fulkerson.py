from data import construct_graph
from data import suppress_pixels
import config


def bfs(source, target):
    visited = set()
    queue = [(source,[])]

    while queue:
        node, path = queue.pop(0)
        visited.add(node.coord)
        if node.coord == target.coord:
            return path

        for edge in node.edges:
            neigh_node = edge.get_other(node)
            if neigh_node.coord not in visited and edge.residual > config.residue_thresh:
                queue.append((neigh_node, path + [edge]))

    return None

def reachable_bfs(source):
    visited = set()
    queue = [source]

    while queue:
        node = queue.pop(0)

        if node.coord in visited:
            continue

        visited.add(node.coord)

        for edge in node.edges:
            neigh = edge.get_other(node)
            if edge.residual <= config.residue_thresh:
                continue
            queue.append(neigh)
    return visited

def print_path(path):
    s = str(path[0].node1) + "".join("-" + str(p.residual) + "-" + str(p.node2) for p in path[:-1])
    s += "-" + str(path[-1].residual) + "-" + str(path[-1].node1)
    print "Got path(%d)"%len(path), s

def min_cut(graph, source, target):
    while True:
        path = bfs(source, target)
        if path is None:
            break
        print_path(path)
        #print path

        min_edge = min(path, key=lambda x: x.residual)
        mid_edge_val = min_edge.residual
        #print "Minimum edge: ", min_edge
        for p in path:
            p.residual -= mid_edge_val
        #print "Updated path: ", path
        #print ""

    fg_coords = reachable_bfs(source)
    bg_coords = [x for x in graph if x not in fg_coords]

    return fg_coords, bg_coords

def naive_segment_image(image, seed):
    graph, fg_node, bg_node = construct_graph(image, seed)
    print "Graph constructed"

    fg_nodes = []
    bg_nodes = []

    for coord, node in graph.iteritems():
        if node is fg_node or node is bg_node:
            continue
        fg_edge = [x for x in node.edges if x.get_other(node).is_fg()][0]
        bg_edge = [x for x in node.edges if x.get_other(node).is_bg()][0]
        if fg_edge.capacity > bg_edge.capacity:
            bg_nodes.append(node)
        else:
            fg_nodes.append(node)
    fg_image = suppress_pixels(image, bg_nodes)
    bg_image = suppress_pixels(image, fg_nodes)
    return fg_image, bg_image

def segment_image(image, seed):
    graph, fg_node, bg_node = construct_graph(image, seed)
    print "Graph constructed"

    fg_coords, bg_coords = min_cut(graph, fg_node, bg_node)
    fg_nodes = [graph[x] for x in fg_coords]
    bg_nodes = [graph[x] for x in bg_coords]

    fg_img = suppress_pixels(image, bg_nodes)
    bg_img = suppress_pixels(image, fg_nodes)

    return fg_img, bg_img



