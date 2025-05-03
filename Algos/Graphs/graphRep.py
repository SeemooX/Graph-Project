
class graph_representation:
    def __init__(self, directed=False):
        self.nodes = set()
        self.adj_list = {}
        self.edges = []
        self.weights = {} 
        self.directed = directed

    def add_edge(self, node1, node2, weight=None):
        if node1 not in self.adj_list:
            self.adj_list[node1] = []
        if node2 not in self.adj_list:
            self.adj_list[node2] = []

        self.adj_list[node1].append(node2)
        if not self.directed:
            self.adj_list[node2].append(node1)

        self.edges.append((node1, node2, weight))

        if weight != None:
            self.weights[(node1, node2)] = weight
            if not self.directed:
                self.weights[(node2, node1)] = weight

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.adj_list:
            self.adj_list[node] = []

    def adjacency_list(self):
        for index in self.adj_list:
            print(index, "->", self.adj_list[index])


    def BFS(self, source):
        File = [source]
        explored = []
        visited = set()
        bfs_tree = []

        while File:
            node = File.pop(0)
            if node not in visited:
                visited.add(node)
                for neighbor in self.adj_list[node]:
                    if neighbor not in visited and neighbor not in explored:
                        File.append(neighbor)
                        explored.append(neighbor)
                        bfs_tree.append((node, neighbor))
        nodes_in_tree = list(visited)
        
        return nodes_in_tree, bfs_tree
    
    
    def DFS(self, start):
        visited = set()
        dfs_tree = []

        def dfs_recursive(node):
            visited.add(node)
            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    dfs_tree.append((node, neighbor))
                    dfs_recursive(neighbor)

        dfs_recursive(start)
        nodes_in_tree = list(visited)
        return nodes_in_tree, dfs_tree
    
    # The graph has to be directed
    def Dijkstra(self, source):
        # Initialization
        distance = {}
        parent = {}
        File = set()

        for node in self.adj_list.keys():
            distance[node] = float('inf')
            parent[node] = None
            File.add(node)

        distance[source] = 0

        while File:
            # Pick node with smallest distance
            node = min(File, key=lambda x: distance[x])
            File.remove(node)

            for neighbor in self.adj_list[node]:
                weight = self.weights[(node, neighbor)]
                if distance[neighbor] > distance[node] + weight:
                    distance[neighbor] = distance[node] + weight
                    parent[neighbor] = node
        # Extracting the edges
        dij_edges = []
        for node in parent:
            if parent[node] is not None:
                dij_edges.append((parent[node], node))
        # Extracting nodes
        nodes_in_tree = set()
        for u, v in dij_edges:
            nodes_in_tree.add(u)
            nodes_in_tree.add(v)

        return list(nodes_in_tree), dij_edges, parent, distance
    
    def Prim(self, source):
        explored = {source}
        min_tree = []

        while len(explored) != len(self.nodes):
            min_weight = float('inf')
            selected_edge = None
            for node in explored:
                for neighbor in self.adj_list[node]:
                    if neighbor not in explored and self.weights[(node, neighbor)] < min_weight:
                        min_weight = self.weights[(node, neighbor)]
                        selected_edge = (node, neighbor, min_weight)

            if selected_edge is None:
                break

            explored.add(selected_edge[1])
            min_tree.append(selected_edge)
        
        # Extracting nodes from edges
        nodes_in_tree = set()
        for u, v, w in min_tree:
            nodes_in_tree.add(u)
            nodes_in_tree.add(v)

        return list(nodes_in_tree), [(u, v) for u, v, w in min_tree], min_tree

    def Bellman_Ford(self, source):
        # Initialization
        distance = {}
        parent = {}

        for node in self.adj_list.keys():
            distance[node] = float('inf')
            parent[node] = None

        distance[source] = 0
        v = len(self.adj_list)

        # Relaxing all the |v| - 1 times
        for i in range(v - 1):
            for(u, neighbors) in self.adj_list.items():
                for v in neighbors:
                    weight = self.weights[(u, v)]
                    if distance[v] > distance[u] +  weight:
                        distance[v] = distance[u] +  weight
                        parent[v] = u
    
        # Checking for an absorbent cycle
        for (u, neighbors) in self.adj_list.items():
            for v in neighbors:
                weight = self.weights[(u, v)]
                if distance[u] + weight < distance[v]:
                    print("There exist an absorbant cycle in the Graph")
                    return None, None, None, None
            
        # Getting the edges
        path_edges = set()
        for v in self.adj_list.keys():
            if parent[v] is not None:
                path_edges.add((parent[v], v))

        # Getting the nodes
        nodes_in_tree = set()
        for u, v in path_edges:
            nodes_in_tree.add(u)
            nodes_in_tree.add(v)

        return list(nodes_in_tree), path_edges, parent, distance
    
    def graph_coloring(self):
        colors = {}
        for node in self.adj_list:
            used_colors = {colors[neighbor] for neighbor in self.adj_list[node] if neighbor in colors}
            for color in range(len(self.adj_list)):
                if color not in used_colors:
                    colors[node] = color
                    break
        return colors

    
# The Unit tests
myapp = graph_representation()
myapp.add_edge('A', 'B', 10)
myapp.add_edge('B', 'C', 5)
myapp.add_edge('B', 'D', 2)
myapp.add_edge('C', 'D', 6)
myapp.add_edge('D', 'A', 12)
myapp.adjacency_list()

nodes_in_tree, dfs_tree = myapp.DFS('A')
print(nodes_in_tree)
print(dfs_tree)

print(myapp.graph_coloring())


"""  elements = [source]
        explored = set()
        min_tree = []
        min_weight = float('inf')

        for element in elements:
            min_weight = float('inf')
            for neighbor in self.adj_list[element]:
                if min_weight > self.weights[(element, neighbor)] and neighbor not in explored:
                    min_weight = self.weights[(element, neighbor)]
                    elements.append(neighbor)
                    explored.add(neighbor)
                    min_tree.append((element, neighbor, min_weight))
            
        return min_tree
         """