def weight(node1, node2):
    # calculate energy
    pass

def isValidMove(move, nrow, ncol):
    x, y = move
    return x >= 0 and y >= 0 and x < nrow and y < ncol
