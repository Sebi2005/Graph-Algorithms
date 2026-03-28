"""from domain import *
from collections import deque
def is_bip(graph):
    color = {}
    for v in graph.get_vertices():
        if v not in color:
            color[v] = 0
            queue = deque([v])
            while queue:
                current = queue.popleft()
                for neighbor in graph.neighbors(current):
                    if neighbor not in color:
                        color[neighbor] = 1 - color[current]
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        return False, None, None
    part1=[v  for v in color if color[v]==0]
    part2=[v for v in color if color[v]==1]
    return True, part1, part2

def try_match(u,graph, visited, match_g1,match_g2):
    if u in visited:
        return False
    visited.add(u)
    for v in graph.neighbors(u):
        if match_g2[v] is None or try_match(match_g2[v], graph, visited, match_g1, match_g2):
            match_g2[v] = u
            match_g1[u] = v
            return True
    return False

def kuhn(graph):
    bip, g1, g2 = is_bip(graph)
    if not bip:
        raise ValueError("Graph is not bipartite")
    match_g1 = {u: None for u in g1}
    match_g2 = {v: None for v in g2}
    changed = True
    while changed:
        changed = False
        visited = set()
        for u in g1:
            if match_g1[u] is None:
                if try_match(u, graph, visited, match_g1, match_g2):
                    changed = True
    return {(u,v) for u,v in match_g1.items() if v is not None}

if __name__ == "__main__":
    g = Graph.create_from_file("graph.txt")
    matching = kuhn(g)
    print("Maximum matching is: ", matching)"""




"""        for u in g1:
            visited = set()
            try_match(u, graph, visited, match_g1, match_g2)
    return {(u,v) for u,v in match_g1.items() if v is not None}"""
