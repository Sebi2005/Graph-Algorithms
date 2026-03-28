from collections import deque
class NeighborIterator:
    """Custom iterator to iterate over neighbors of a vertex."""
    def __init__(self, neighbors_list):
        self.iterator = iter(neighbors_list)
    def __iter__(self):
        return self
    def __next__(self):
        return next(self.iterator)

class BFSIterator:
    """Iterator that iterates through all vertices reachable from starting vertex using BFS"""
    def __init__(self, graph, start):
        if start not in graph.out_neighbors:
            raise ValueError("Starting vertex does not exist")
        self.graph = graph
        self.visited = set()
        self.queue = deque([(start, 0)])
        self.visited.add(start)
        self.last_distance = 0

    def __iter__(self):
        return self

    def __next__(self):
        if not self.queue:
            raise StopIteration
        current, dist = self.queue.popleft()
        self.last_distance = dist

        for neighbor in self.graph.neighbors(current):
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.queue.append((neighbor, dist + 1))
        return current, dist
    #O(E)

    def get_path_length(self):
        return self.last_distance  # Theta(1)

class DFSIterator:
    """Iterator that iterates through all vertices reachable from starting vertex using dfs"""
    def __init__(self, graph, start):
        if start not in graph.out_neighbors:
            raise ValueError("Starting vertex does not exist")
        self.visited = set()
        self.graph = graph
        self.stack = [(start,0)]
        self.current_distance = 0
    def __iter__(self):
        return self
    def __next__(self):
        while self.stack:
            current, dist = self.stack.pop()
            if current not in self.visited:
                self.visited.add(current)
                self._last_distance=dist
                for neighbor in reversed(list(self.graph.neighbors(current))):
                    if neighbor not in self.visited:
                        self.stack.append((neighbor, dist + 1))
                return current, dist
        raise StopIteration
    #O(E)
    def get_path_length(self):
        return self.current_distance
    #Theta(1)



class Graph:
    def __init__(self, directed = True, weighted = False):
        """Initialize an empty graph.
        Args:
           directed (bool): True if the graph is directed, false otherwise.
        """
        self.directed = directed
        self.weighted = weighted
        self.out_neighbors={} #Outbound adjacency list
        self.in_neighbors={} if directed else self.out_neighbors #If undirected we use the same list
        self.weights={} if weighted else None

        #Theta(1)

    def add_vertex(self,vertex):
        """Adds a vertex to the graph."""
        if vertex in self.out_neighbors:
            raise ValueError("Vertex already exists")
        self.out_neighbors[vertex] = []
        if self.directed:
            self.in_neighbors[vertex] = []
        #Theta(1)
    def add_edge(self,start,end, weight = None):
        """Adds an edge from vertex 'start' to vertex 'end'"""
        if start == end:
            raise ValueError("Self-loops are not available")
        if start not in self.out_neighbors:
            raise ValueError(f"Vertex {start} does not exist")
        if end not in self.out_neighbors:
            raise ValueError(f"Vertex {end} does not exist")
        if end in self.out_neighbors[start]:
            raise ValueError("Edge already exists")
        self.out_neighbors[start].append(end)
        self.in_neighbors[end].append(start)
        if not self.directed:
            if start not in self.out_neighbors[end]:
                self.out_neighbors[end].append(start)
            if end not in self.out_neighbors[start]:
                self.out_neighbors[start].append(end)
        if self.weighted:
            self.weights[(start,end)] = weight if weight is not None else 0
            if not self.directed:
                self.weights[(end,start)] = weight if weight is not None else 0
        #Theta(1)
    def remove_edge(self,initial_vertex, terminal_vertex):
        if initial_vertex not in self.out_neighbors or terminal_vertex not in self.out_neighbors[initial_vertex]:
            raise ValueError("Edge does not exist")
        self.out_neighbors[initial_vertex].remove(terminal_vertex) #O(E/V)
        self.in_neighbors[terminal_vertex].remove(initial_vertex) #O(E/V)
        if not self.directed:
          if initial_vertex in self.out_neighbors[terminal_vertex]:
            self.out_neighbors[terminal_vertex].remove(initial_vertex)
          if terminal_vertex in self.in_neighbors[initial_vertex]:
            self.in_neighbors[initial_vertex].remove(terminal_vertex)
        if self.weighted:
            self.weights.pop((initial_vertex, terminal_vertex), None)
            if not self.directed:
                self.weights.pop((terminal_vertex,initial_vertex), None)
        #O(E/V)+O(E/V) = O(E/V)
    def remove_vertex(self, vertex):
        if vertex not in self.out_neighbors:
            raise ValueError("Vertex does not exist")
        del self.out_neighbors[vertex]
        if self.directed:
            del self.in_neighbors[vertex]
        for v in self.out_neighbors: #O(V)
            if vertex in self.out_neighbors[v]: #O(E)
                self.out_neighbors[v].remove(vertex) #O(E)
            if vertex in self.in_neighbors[v] and self.directed: #O(E)
                self.in_neighbors[v].remove(vertex) #O(E)
        #O(V+E)
    def get_v(self):
        """Returns the number of vertices."""
        return len(self.out_neighbors)
        #Theta(1)
    def get_e(self):
        """Returns the number of edges in the graph."""
        nr_of_edges=0
        for v in self.out_neighbors: #O(V)
            if len(self.out_neighbors[v] )>0:
                nr_of_edges+=len(self.out_neighbors[v]) #Theta(1)
        return nr_of_edges if self.directed else nr_of_edges / 2
        #O(V)
    def is_edge(self, start, end):
        if start not in self.out_neighbors:
            raise ValueError(f"Vertex {start} does not exist")
        if end not in self.out_neighbors:
            raise ValueError(f"Vertex {end} does not exist")
        return end in self.out_neighbors[start]
        #O(E) (O(E/V))
    def neighbors(self,vertex):
        """Returns the list of outbound neighbors of a vertex if directed. If not, of all neighbors.
        """
        if vertex not in self.out_neighbors:
            raise ValueError("Vertex does not exist")
        iterator = NeighborIterator(self.out_neighbors[vertex])
        return iterator
        #  Theta(1)

    def inbound_neighbors(self, vertex):
        if vertex not in self.out_neighbors:
            raise ValueError("Vertex does not exist")
        list_inbound_neighbors=[]
        for v in self.in_neighbors[vertex]:
            list_inbound_neighbors.append(v)
        return list_inbound_neighbors
        # O(d_in) (O(E/V))
    def change_if_directed(self, new_directed):
        if self.directed == new_directed:
            return
        if new_directed:
            self.in_neighbors = {v: [] for v in self.out_neighbors}
            for start in self.out_neighbors:
                for end in self.out_neighbors[start]:
                        self.in_neighbors[end].append(start)
        else:
            for start in self.out_neighbors:
                for end in self.out_neighbors[start]:
                    if start not in self.out_neighbors[end]:
                        self.out_neighbors[end].append(start)
            self.in_neighbors = self.out_neighbors
        self.directed = new_directed
        #O(V+E)
    def change_if_weighted(self, new_weighted):
        if self.weighted == new_weighted:
            return
        if new_weighted:
            self.weights = {}
            for v in self.out_neighbors:
                for u in self.out_neighbors[v]:
                    self.weights[(v,u)] = 0
        else:
            self.weights = None
        self.weighted = new_weighted
    def set_weight(self, start, end, weight):
        if not self.weighted:
            raise ValueError("Graph is not weighted")
        if (start, end) not in self.weights:
            raise ValueError("Edge does not exist")
        self.weights[(start,end)] = weight
        if not self.directed:
            self.weights[(end,start)] = weight

    def get_weight(self, start, end):
        if not self.weighted:
            raise ValueError("Graph is not weighted")
        if (start, end) not in self.weights:
            raise ValueError("Edge does not exist")
        return self.weights[(start,end)]
        #Theta(1)

    def get_vertices(self):
        return list(self.out_neighbors.keys())
        # Theta(V)
    def DFS_iter(self, start):
        return DFSIterator(self, start)
    def BFS_iter(self, start):
        return BFSIterator(self, start)
    def __str__(self):
        first_line= "directed " if self.directed else "undirected "
        first_line+="weighted" if self.weighted else "unweighted"
        output=[first_line]
        printed_edges = set()
        for v in self.out_neighbors:
            if self.out_neighbors[v]:
                for n in self.out_neighbors[v]:
                    if self.directed or ((v,n) not in printed_edges and (n,v) not in printed_edges):
                        edge_str = f"{v} {n}"
                        if self.weighted:
                            edge_str+=f" {self.get_weight(v,n)}"
                        output.append(edge_str)
                        if not self.directed:
                            printed_edges.add((v,n))
                            printed_edges.add((n,v))
            if not self.out_neighbors[v] and not self.in_neighbors[v]:
                output.append(f"{v}")
        return "\n".join(output)
        # O(V+E)

    @staticmethod
    def create_from_file(filename):
        with open(filename, "r") as file:
            lines = file.read().splitlines()
        if not lines:
            raise ValueError("Empty file")
        first_line = lines[0].strip().lower().split()
        if len(first_line) != 2:
            raise ValueError("First line must contain two words: directed/undirected and weighted/unweighted")
        directed = first_line[0] == "directed"
        weighted = first_line[1] == "weighted"
        graph = Graph(directed=directed, weighted=weighted)
        for line in lines[1:]:
            parts = line.strip().split()
            if not parts:
                continue
            if len(parts) == 1:
                graph.add_vertex(parts[0])
            elif len(parts) == 2:
                start, end = parts[0], parts[1]
                if start not in graph.out_neighbors:
                    graph.add_vertex(start)
                if end not in graph.out_neighbors:
                    graph.add_vertex(end)
                graph.add_edge(start, end)
            elif len(parts) == 3:
                start, end, weight = parts[0], parts[1], parts[2]
                if start not in graph.out_neighbors:
                    graph.add_vertex(start)
                if end not in graph.out_neighbors:
                    graph.add_vertex(end)
                graph.add_edge(start, end, weight)
            else:
                raise ValueError(f"Invalid line format: {line}")

        return graph

"""
if __name__=="__main__":
    print("Welcome!")
    mode = input("Create new graph or load from file? (new/file): ").strip().lower()
    if mode == "file":
        filename = input("Enter filename: ").strip()
        try:
            g = Graph.create_from_file(filename)
            print("Graph loaded successfully.\n")
        except Exception as e:
            print("Error loading graph:", e)
    else:
        directed = input("Should the graph be directed? (yes/no): ").strip().lower() == "yes"
        weighted = input("Should the graph be weighted? (yes/no): ").strip().lower() == "yes"
        g = Graph(directed=directed, weighted=weighted)
        print("Empty graph created.\n")

    while True:
        print("\n=== Menu ===")
        print("1. Add a vertex")
        print("2. Add an edge")
        print("3. Remove an edge")
        print("4. Remove a vertex")
        print("5. Get the number of vertices")
        print("6. Get the number of edges")
        print("7. Check if there is an edge between two vertices")
        print("8. Get the outbound neighbors of a vertex")
        print("9. Get the inbound neighbors of a vertex")
        print("10. Get a list of all vertices")
        print("11. Print the graph")
        print("12. BFS from a vertex (with distances)")
        print("13. DFS from a vertex (with depths)")
        print("14. Change graph to directed/undirected")
        print("15. Change graph to weighted/unweighted")
        print("16. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                v = input("Vertex: ")
                g.add_vertex(v)
                print(f"Vertex '{v}' added.")

            elif choice == "2":
                u = input("Start vertex: ")
                v = input("End vertex: ")
                w = None
                if g.weighted:
                    w = int(input("Weight: "))
                g.add_edge(u, v, w)
                print(f"Edge {u} → {v} added.")

            elif choice == "3":
                u = input("Start vertex: ")
                v = input("End vertex: ")
                g.remove_edge(u, v)
                print(f"Edge {u} → {v} removed.")

            elif choice == "4":
                v = input("Vertex to remove: ")
                g.remove_vertex(v)
                print(f"Vertex '{v}' removed.")

            elif choice == "5":
                print("Number of vertices:", g.get_v())

            elif choice == "6":
                print("Number of edges:", g.get_e())

            elif choice == "7":
                u = input("Start vertex: ")
                v = input("End vertex: ")
                exists = g.is_edge(u, v)
                print("Edge exists." if exists else "Edge does not exist.")

            elif choice == "8":
                v = input("Vertex: ")
                print("Outbound neighbors:", *g.neighbors(v))

            elif choice == "9":
                v = input("Vertex: ")
                print("Inbound neighbors:", g.inbound_neighbors(v))

            elif choice == "10":
                print("Vertices:", g.get_vertices())

            elif choice == "11":
                print("\nGraph:")
                print(g)

            elif choice == "12":
                start = input("Start vertex for BFS: ")
                print("BFS Traversal (vertex, distance):")
                for vertex, dist in g.BFS_iter(start):
                    print(f"{vertex}, distance = {dist}")

            elif choice == "13":
                start = input("Start vertex for DFS: ")
                print("DFS Traversal (vertex, depth):")
                for vertex, dist in g.DFS_iter(start):
                    print(f"{vertex}, depth = {dist}")

            elif choice == "14":
                new_directed = input("Should the graph be directed? (yes/no): ").strip().lower() == "yes"
                g.change_if_directed(new_directed)

            elif choice == "15":
                new_weighted = input("Should the graph be weighted? (yes/no): ").strip().lower() == "yes"
                g.change_if_weighted(new_weighted)

            elif choice == "16":
                print("Exiting program. Goodbye!")
                break

            else:
                print("Invalid option. Please choose again.")
        except Exception as e:
            print("Error: ", e)
"""














