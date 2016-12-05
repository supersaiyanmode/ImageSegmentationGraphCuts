from data import construct_graph
from data import suppress_pixels


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


def segment_image(algorithm, image, seed):
    graph, fg_node, bg_node = construct_graph(image, seed)
    print "Graph constructed"

    fg_coords, bg_coords = algorithm(graph, fg_node, bg_node)
    fg_nodes = [graph[x] for x in fg_coords]
    bg_nodes = [graph[x] for x in bg_coords]

    fg_img = suppress_pixels(image, bg_nodes)
    bg_img = suppress_pixels(image, fg_nodes)

    return fg_img, bg_img
