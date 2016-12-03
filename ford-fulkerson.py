import sys
# generic ford-fulkerson

# bfs - returns true, if there is a path from s -> t,
# stores path in parent
def bfs(residualGraph, s, t, parent, nVertices):
    # queue
    isVisited = [False] * nVertices
    queue = [s]
    isVisited[s] = True
    parent[s] = -1

    while len(queue) != 0:
        node = queue[0]
        queue.pop(0)

        for iterIndex in xrange(nVertices):
            if not isVisited[iterIndex] and residualGraph[node][iterIndex] > 0:
                queue.append(iterIndex)
                parent[iterIndex] = node
                isVisited[iterIndex] = True

    return isVisited[t]

def dfs(residualGraph, s, isVisited, nrow):
    isVisited[s] = True
    for iterIndex in xrange(nrow):
        if residualGraph[s][iterIndex] and not isVisited[iterIndex]:
            dfs(residualGraph, iterIndex, isVisited, nrow)

    return isVisited

def minCut(graph, s, t):

    # nrow = ncol = number of vertices
    nrow, ncol = len(graph), len(graph[0])

    residualGraph = [[[] for _ in xrange(ncol)] for _ in xrange(nrow)]

    for rowIndex in xrange(nrow):
        for colIndex in xrange(ncol):
            residualGraph[rowIndex][colIndex] = graph[rowIndex][colIndex]

    # bfs with storing the parent path
    parent = [None] * nrow

    # bfs till there is no augmenting path
    while(bfs(residualGraph, s, t, parent, nrow)):
        # iterate over the parent path to get the residual
        minPathFlow = sys.maxint
        iterNode = t

        # starting from terminal node find the path with minimum flow
        while iterNode != s:
            fromPath = parent[iterNode]
            minPathFlow = min(minPathFlow, residualGraph[fromPath][iterNode])
            iterNode = fromPath

        iterNode = t
        while iterNode != s:
            fromPath = parent[iterNode]
            residualGraph[fromPath][iterNode] -= minPathFlow
            #residualGraph[iterNode][fromPath] += minPathFlow
            iterNode = fromPath

    isVisited = [False] * nrow
    # find all the paths which are reachable from source
    isVisited = dfs(residualGraph, s, isVisited, nrow)

    reachableNodes = []
    # technically we don't need the cut, we only need the
    for iterIndex in xrange(nrow):
       if isVisited[iterIndex]:
           reachableNodes.append(iterIndex)

    print "Vertices reachable from source", reachableNodes

    print "Cuts"
    for rowIndex in xrange(nrow):
        for colIndex in xrange(ncol):
            if isVisited[rowIndex] and not isVisited[colIndex] and graph[rowIndex][colIndex]:
                print rowIndex, colIndex

def main():
    graph = [  [0 , 16, 13,  0, 0, 0],
               [16,  0, 10, 12, 0, 0],
               [13, 10,  0,  9,14, 0],
               [0,  12,  9,  0, 7, 20],
               [0,   0, 14,  7, 0, 4],
               [0,   0,  0, 20, 4, 0]]

    minCut(graph, 0, 5)

    pass

if __name__ == '__main__':
    main()
