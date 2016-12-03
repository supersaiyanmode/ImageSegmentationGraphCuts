from data import construct_graph
from data import suppress_pixels

def bfs(graph, source, target):
    visited = set(source.coord)
    queue = [(source,[])]

    while queue:
        node, path = queue.pop(0)

        if node.coord == target.coord:
            return path

        for edge in node.edges:
            neigh_node = edge.get_other(node)
            if neigh_node.coord not in visited and edge.residual > 0:
                visited.add(neigh_node.coord)
                queue.append((neigh_node, path + [edge]))

    return None

def reachable_bfs(graph, source):
    visited = set(source.coord)
    queue = [source]

    while queue:
        node = queue.pop(0)

        visited.add(node.coord)
        for edge in node.edges:
            neigh = edge.get_other(node)
            if edge.residual > 0 and neigh.coord in visited:
                continue
            queue.add(neigh)
    return visited


def min_cut(graph, source, target):
    while True:
        path = bfs(graph, source, target)
        if path is None:
            break
        min_edge = min(path, key=lambda x: x.residual)

        for p in path:
            p.residual -= min_edge.residual

    return reachable_bfs(graph, source), \
            reachable_bfs(graph, target)
def naive_segment_image(image, seed):
    graph, fg_node, bg_node = construct_graph(image, seed)
    fg_nodes = []
    bg_nodes = []

    for coord, node in graph.iteritems():
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
    fg_coords, bg_coords = min_cut(graph, fg_node, bg_node)
    fg_nodes = [graph[x] for x in fg_coords]
    bg_nodes = [graph[x] for x in bg_coords]

    fg_img = suppress_pixels(image, bg_nodes)
    bg_img = suppress_pixels(image, fg_nodes)

    return fg_img, bg_img


