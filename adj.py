
class graph_representions:

    def __init__(self, num_vertices, directed=False):
        self.num_vertices = num_vertices
        self.adj_list = {i: [] for i in range(num_vertices)}
        self.adj_matrix =  [[0] * num_vertices for _ in range(num_vertices)]
        self.inc_matrix = []
        self.directed = directed                                                  

    def add_edge(self, u, v):
        """Add an edge to the graph (directed or undirected)."""
        # For directed graphs
        if self.directed:
            self.adj_list[u].append(v)
        # For undirected graphs
        else:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
        
        self.adj_matrix[u][v] = 1
        if not self.directed:
            self.adj_matrix[v][u] = 1
        

    def disp_adj_list(self):
        for node in self.adj_list:
            print("Node", node , "is connected to:" , self.adj_list[node])
            
    def disp_adj_matrix(self):
        for i in self.adj_matrix:
            print(i)
            
    def disp_incidence_matrix(self):
        for i in self.adj_matrix:
            print(i)
            
    def algo_DFS(self, start):
        visited = set()
        dfs_tree = []
        stack = [start]

        while stack:
            node = stack.pop() # Popping the node needed to work on
            if node not in visited:
                visited.add(node)
                for neighbor in self.adj_list[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
                        dfs_tree.append((node, neighbor))

        return dfs_tree
    
        


                
obj = graph_representions(5, True)
obj.add_edge(0, 1)
obj.add_edge(1, 2)
obj.add_edge(1, 4)
obj.add_edge(2, 3)
obj.add_edge(4, 3)
print(obj.algo_DFS(0))

 

