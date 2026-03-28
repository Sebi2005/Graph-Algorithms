from domain import *
def find_hamiltonian_cycle(graph):
    vertices = graph.get_vertices()
    if not vertices:
        return None
    path = [vertices[0]]
    visited = set(path)
    def backtrack(n):
        if len(path) == len(vertices):
            if graph.is_edge(path[-1],path[0]):
                path.append(path[0])
                return True
            return False
        for neighbor in graph.neighbors(path[-1]):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                if backtrack(n+1):
                    return True
                visited.remove(neighbor)
                path.pop()
        return False
    if backtrack(1):
        return path
    else:
        return None
if __name__ == "__main__":
    g = Graph.create_from_file("graph.txt")
    print(find_hamiltonian_cycle(g))