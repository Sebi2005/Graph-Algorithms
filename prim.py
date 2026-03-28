
from domain import *
import heapq

def prim_mst(graph, start= None):
    """
    Constructs a Minimum Spanning Tree from an undirected, connected, weighted graph
    """
    if graph.directed:
        raise ValueError("Graph expected to be undirected")
    if not graph.weighted:
        raise ValueError("Graph expected to be weighted")
    vertices = graph.get_vertices()
    if not vertices:
        raise ValueError("Graph cannot be empty")
    if start is None:
        start = vertices[0]
    mst = Graph(directed=False, weighted=True)
    for v in vertices: #Theta(V)
        mst.add_vertex(v)
    pq = []
    cost = {}
    visited = set()
    prev = {}
    visited.add(start)
    #initially add all neighbors of start as potential edges
    for n in graph.neighbors(start):
        cost[n] = graph.get_weight(start, n)
        prev[n] = start
        heapq.heappush(pq, (cost[n], n)) #O(log V)
    #O(E log V)
    while mst.get_e() < graph.get_v() - 1: #O(V)
        if not pq:
            break #graph might not be connected
        current_cost, v = heapq.heappop(pq) #O(log V)
        if v not in visited:
            mst.add_edge(prev[v],v,current_cost)
            visited.add(v)
            for n in graph.neighbors(v):
                edge_weight = graph.get_weight(v,n)
                if (n not in cost) or (edge_weight < cost[n]):
                    cost[n] = edge_weight
                    prev[n] = v
                    heapq.heappush(pq, (cost[n], n)) #O(log V)
    #O((V+E) log V)
    return mst


def count_leaves(tree=Graph, root= None ):
    """
    Counts the leaves of the tree using DFS
    """
    if root not in tree.out_neighbors:
        raise ValueError("Root does not exist in the tree")
    visited = set(root)
    stack = [root]
    leaf_count = 0
    while stack:
        u = stack.pop()
        children = 0
        for n in tree.neighbors(u):
            if n not in visited:
                visited.add(n)
                stack.append(n)
                children+= 1
        if children == 0:
            leaf_count+= 1
    return leaf_count
#each vertex is popped and pushed exactly once -> O(V)
#each tree edge is inspected twice -> O(2*E) = O(E)
#O(V+E)
"""if __name__ == "__main__":
    g = Graph.create_from_file("graph.txt")
    root = input("Start vertex for MST (Prim): ")
    mst = prim_mst(g, root)
    print(mst)
    leaf_root = input("Root for leaf count: ")
    leaves = count_leaves(mst, leaf_root)
    print(f"Number of leaves when rooted at {leaf_root}: {leaves}\n")"""
