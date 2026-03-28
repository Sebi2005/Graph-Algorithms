from domain import *
import time
import heapq
class Stats:
    """Tracks the number of key operations for comparing efficiency"""
    def __init__(self):
        self.cost_calls = 0
        self.pq_push = 0
        self.pq_pop = 0
        self.other_calls = 0
    def __str__(self):
        return (f"cost_calls: {self.cost_calls}, "
                f"pq_push: {self.pq_push}, "
                f"pq_pop: {self.pq_pop}, "
                f"other_calls: {self.other_calls}")

def dijkstra(graph, start, end, stats = None):
    if stats is None:
        stats = Stats()
    dist = {}
    parent = {}
    for v in graph.get_vertices(): #Theta(V)
        dist[v] = float('inf')
    dist[start] = 0
    parent[start] = None
    pq = []
    heapq.heappush(pq, (0, start))
    stats.pq_push += 1
    start_time = time.perf_counter()
    while pq: #O(V)
        current_dist, u = heapq.heappop(pq) #O(log V)
        stats.pq_pop += 1
        if u == end:
            break
        if current_dist > dist[u]:
            continue
        for neighbor in graph.out_neighbors[u]: #O(E)
            if stats:
                stats.cost_calls += 1
            w = graph.get_weight(u, neighbor) #Theta(1)
            new_dist = dist[u] + float(w)
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = u
                heapq.heappush(pq, (new_dist, neighbor)) #O(log V)
                stats.pq_push += 1
    end_time = time.perf_counter()
    path = []
    if dist[end] < float('inf'):
        node = end
        while node is not None:
            path.append(node)
            node = parent[node] if node in parent else None
        path.reverse()
    time_ms = (end_time - start_time) * 1000.0
    return dist[end], path, time_ms, stats
    #O(V log V + E log V) = O((V+E) log V)

def bellman_ford(graph, start, end, stats = None):
    if stats is None:
        stats = Stats()
    dist = {}
    parent = {}
    for v in graph.get_vertices(): #Theta(V)
        dist[v] = float('inf')
        parent[v] = None
    dist[start] = 0
    start_time = time.perf_counter()
    V = graph.get_v() #Theta(1)
    for _ in range(V-1): #O(V-1)
        changed = False
        for u in graph.get_vertices(): #we check every edge -> O(E)
            for n in graph.out_neighbors[u]:
                stats.cost_calls += 1
                w = float(graph.get_weight(u,n))
                if dist[u] != float('inf') and dist[u] + w < dist[n]:
                    dist[n] = dist[u] + w
                    parent[n] = u
                    changed = True
        if not changed:
            break
    end_time = time.perf_counter()
    time_ms = (end_time - start_time) * 1000.0
    path = []
    if dist[end] <float('inf'):
        node = end
        while node is not None:
            path.append(node)
            node = parent[node] if node in parent else None
        path.reverse()
    return dist[end], path, time_ms, stats
    #we check every edge at possible maximum V-1 times => O(V*E)
def compare_dijkstra_bellman(graph_file, start, end):
    g = Graph.create_from_file(graph_file)
    #Dijkstra
    dist_d, path_d, time_d, stats_d = dijkstra(g, start, end, Stats())
    print("Dijkstra: ")
    print(f"Distance: {dist_d}")
    print(f"Path: {path_d}")
    print(f"Time: {time_d:.2f} ms")
    print(f"Stats: {stats_d}\n")
    dist_b, path_b, time_b, stats_b = bellman_ford(g, start, end, Stats())
    print("Bellman-Ford: ")
    print(f"Distance: {dist_b}")
    print(f"Path: {path_b}")
    print(f"Time: {time_b:.2f} ms")
    print(f"Stats: {stats_b}\n")

#if __name__ == "__main__":
    #compare_dijkstra_bellman("graph.txt", "619", "437")

