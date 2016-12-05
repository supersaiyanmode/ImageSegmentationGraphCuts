import config


def print_path(path):
    s = str(path[0].node1) + "".join("-" + str(p.residual) + "-" + str(p.node2) for p in path[:-1])
    s += "-" + str(path[-1].residual) + "-" + str(path[-1].node1)
    if config.verbose:
        print "Got path(%d)" % len(path), s


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
