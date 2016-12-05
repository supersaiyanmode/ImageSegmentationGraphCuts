from bidirectional import min_cut
from node import Node
from edge import Edge

def main():
    node1 = Node((1,1), None, None)
    node2 = Node((2,2), None, None)
    node3 = Node((3,3), None, None)
    node4 = Node((4,4), None, None)
    node5 = Node((5,5), None, None)
    node6 = Node((6,6), None, None)

    edge12 = Edge(node1, node2, 10)
    edge13 = Edge(node1, node3, 10)
    edge23 = Edge(node2, node3, 2)
    edge24 = Edge(node2, node4, 4)
    edge25 = Edge(node2, node5, 8)
    edge34 = Edge(node3, node5, 9)
    edge45 = Edge(node4, node5, 6)
    edge46 = Edge(node4, node6, 10)
    edge56 = Edge(node5, node6, 10)

    graph = {y.coord:y for x,y in locals().items() if "node" in x}

    src, tar = min_cut(graph, node1, node6)
    print "Source: ", src
    print "target: ", tar

if __name__ == '__main__':
    main()
