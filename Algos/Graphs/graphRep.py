from collections import deque, defaultdict

class GraphRep:
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

        self.nodes.add(node1)
        self.nodes.add(node2)

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
                u = parent[node]
                v = node
                w = self.weights[(u, v)]
                dij_edges.append((u, v, w))
        # Extracting nodes
        nodes_in_tree = set()
        for u, v, w in dij_edges:
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

        return list(nodes_in_tree), [(u, v, w) for u, v, w in min_tree], min_tree

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
                path_edges.add((parent[v], v, self.weights[(parent[v], v)]))

        # Getting the nodes
        nodes_in_tree = set()
        for u, v, w in path_edges:
            nodes_in_tree.add(u)
            nodes_in_tree.add(v)

        return list(nodes_in_tree), path_edges, parent, distance
    
    def kruskal(self):

        ds = DisjointSet()
        for node in self.nodes:
            ds.parent[node] = node
            ds.rank[node] = 0

        # Sorting edges by weight
        sorted_edges = sorted(self.edges, key=lambda edge: edge[2])

        mst_edges = []
        total_weight = 0

        for u, v, w in sorted_edges:
            # If u and v are in different groups, then it is safe to add edge
            if ds.find(u) != ds.find(v):
                ds.union(u, v)
                mst_edges.append((u, v, w))
                total_weight += self.weights[(u, v)]

        return self.nodes, mst_edges, total_weight
    
    def graph_coloring(self):
        colors = {}
        for node in self.adj_list:
            used_colors = set(colors[neighbor] for neighbor in self.adj_list[node] if neighbor in colors)
            color = 0
            while color in used_colors:
                color += 1
            colors[node] = color
        return colors
    
    def ford_fulkerson(self, source, sink):
        residual = GraphHelper.build_residual_graph(self)
        parent = {}
        max_flow = 0

        # Initialize flow dict (for final output)
        flow_dict = {(u, v): 0 for u, v, _ in self.edges}

        while GraphHelper.bfs(residual, source, sink, parent):
            # Find bottleneck
            path_flow = float('inf')
            v = sink
            while v != source:
                u = parent[v]
                capacity = residual.weights[(u, v)]
                path_flow = min(path_flow, capacity)
                v = parent[v]

            # Update residual capacities
            v = sink
            while v != source:
                u = parent[v]
                residual.weights[(u, v)] -= path_flow
                residual.weights[(v, u)] += path_flow
                v = parent[v]

            max_flow += path_flow
            parent.clear()

        # After all flow pushed → compute flow on each original edge
        edges_with_flow = []
        for u, v, _ in self.edges:
            original_capacity = self.weights[(u, v)]
            residual_capacity = residual.weights[(u, v)]
            flow_sent = original_capacity - residual_capacity
            edges_with_flow.append((u, v, flow_sent))

        return max_flow, list(self.nodes), edges_with_flow
    



class DisjointSet:
    def __init__(self):
         # each node is the parent of itself "each node in its own group"
        self.parent = {}
        # The rank is like the height of the tree, at first is 0
        self.rank = {}

    # Finding the leader of the group the node belongs to, in order to merge after
    def find(self, node):
        if self.parent[node] != node:
            # Recursively check for the leader node of the group
            self.parent[node] = self.find(self.parent[node])
        
        return self.parent[node]
    
    def union(self, u, v):
        # Getting the leader of both the nodes
        root_u = self.find(u)
        root_v = self.find(v)

        # Merging only in the case where they don't belong the same group
        if root_u != root_v:
            # We will attach the smaller tree under the bigger tree
            if self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            elif self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

class GraphHelper:
    @staticmethod
    def build_residual_graph(graph):
        residual = GraphRep(directed=True)
        residual.nodes = set(graph.nodes)
        residual.adj_list = {u: [] for u in graph.nodes}
        residual.edges = []
        residual.weights = {}

        for u, v, _ in graph.edges:
            capacity = graph.weights[(u, v)]

            # Forward edge
            residual.adj_list[u].append(v)
            residual.edges.append((u, v, capacity))
            residual.weights[(u, v)] = capacity

            # Reverse edge with 0 capacity
            if (v, u) not in residual.weights:
                residual.adj_list[v].append(u)
                residual.edges.append((v, u, 0))
                residual.weights[(v, u)] = 0

        return residual

    @staticmethod
    def bfs(residual, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v in residual.adj_list[u]:
                capacity = residual.weights[(u, v)]
                if v not in visited and capacity > 0:
                    parent[v] = u
                    if v == sink:
                        return True
                    visited.add(v)
                    queue.append(v)
        return False 


# The Unit tests
""" myapp = GraphRep()
myapp.add_edge('A', 'B', 10)
myapp.add_edge('B', 'C', 5)
myapp.add_edge('B', 'D', 2)
myapp.add_edge('C', 'D', 6)
myapp.add_edge('D', 'A', 12)
myapp.add_edge('D', 'X', 12)
myapp.add_edge('X', 'A', 12)
myapp.adjacency_list()

nodes_in_tree, result, total_weight = myapp.kruskal()
nodes_in_tree1, result1, total_weight1 = myapp.Prim("B")
print(result)
print(result1)


graphView.plot_graph(nodes_in_tree, result, True, False, "kruskal")
graphView.plot_graph(nodes_in_tree1, result1, True, False, "Prim") """
