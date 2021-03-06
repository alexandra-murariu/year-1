import copy
import math
import random
from collections import defaultdict

INFINITY = math.inf


class Graph:
    """
    Class for the bidirectional graph
    """

    def __init__(self, n=0, m=0, nodes=None, dict_in=None, dict_out=None, dict_cost=None, dict_un=None):
        if dict_cost is None:
            dict_cost = {}
        if dict_out is None:
            dict_out = {}
        if dict_in is None:
            dict_in = {}
        if nodes is None:
            nodes = []
        self._nr_of_vertices = n
        self._nr_of_edges = m
        self._list_of_nodes = nodes
        self._dict_in = dict_in
        self._dict_out = dict_out
        self.graph = defaultdict(list)
        self._dict_cost = dict_cost
        self.Time = 0
        self.count = 0
        self.min = 10000
        self.j_min = 10000
        self.visited = [0 for i in range(self._nr_of_vertices)]
        self.edges = []

    def copy_graph(self):
        """
        Function that returns a copy of the graph

        :return (Graph) an exact deepcopy of this graph
        """
        return Graph(self._nr_of_vertices, self._nr_of_edges, self.parse_vertices(), copy.deepcopy(self.get_dict_in()),
                     copy.deepcopy(self.get_dict_out()), copy.deepcopy(self.get_dict_cost()))

    def parse_vertices(self):
        """
        Function that returns an iterator to the vertices list

        :return an iterator through the list of vertices
        """
        return iter(self._list_of_nodes)

    def is_edge(self, node_in, node_out):
        """
        Function that checks if (node_in, node_out) is an edge
        Complexity: Theta(1)
        :param node_in: the first vertex
        :param node_out: the second vertex
        :return true if (node_1, node_2) is a vertex, false otherwise
        """
        if (node_in, node_out) in self._dict_cost.keys():
            return True
        return False

    def in_degree(self, node):
        """
        Function that returns the in-degree of the given vertex
        Complexity: Theta(1)
        :param node: the node to compute the in-degree of
        :raise Exception: if the node doesn't exist
        :return: the in-degree of the given node (int)
        """
        if node in self._dict_in.keys():
            return len(self._dict_in[node])
        elif node not in self._list_of_nodes:
            raise Exception("This is not a node.")
        return 0

    def out_degree(self, node):
        """
        Function that returns the out-degree of the given vertex
        Complexity: Theta(1)
        :param node: the node to compute the out-degree of
        :raise Exception: if the node doesn't exist
        :return: the out-degree of the given node (int)
        """
        if node in self._dict_out.keys():
            return len(self._dict_out[node])
        elif node not in self._list_of_nodes:
            raise Exception("This is not a node.")
        return 0

    def parse_outbound_edges(self, vertex):
        """
        Function that returns an iterator through the outbound edges of the vertex
        Complexity: Theta(1)
        :param vertex: the node to parse through
        :raise Exception: if the node doesn't exist
        :return: an iterator through the list of vertices that are outbound connected to the vertex
        """
        if vertex not in self._dict_out.keys():
            raise Exception("No outbound edges for this vertex")
        return iter(self._dict_out[vertex])

    def parse_inbound_edges(self, vertex):
        """
        Function that returns an iterator through the inbound edges of the vertex
        Complexity: Theta(1)
        :param vertex: the node to parse through
        :raise Exception: if the node doesn't exist
        :return: an iterator through the list of vertices that are inbound connected to the vertex
        """
        if vertex not in self._dict_in.keys():
            raise Exception("No inbound edges for this vertex")
        return iter(self._dict_in[vertex])

    def modify_cost(self, node_in, node_out, new_cost):
        """
        Function that modifies the cost of the given edge
        Complexity: Theta(1)
        :param node_in: the first vertex
        :param node_out: the second vertex
        :param new_cost: the new cost of the edge (int)
        :raise Exception: if the edge doesn't exist
        :return: -
        """
        if not self.is_edge(node_in, node_out):
            raise Exception("The edge doesn't exist")
        self._dict_cost[(node_in, node_out)] = new_cost

    def add_edge(self, node_in, node_out, cost):
        """
        Function that adds an edge to the graph
        Complexity: Theta(1)
        :param node_in: the first vertex
        :param node_out: the second vertex
        :param cost: the cost of the new edge (int)
        :raise Exception: if the edge already exists, or if the nodes don't exist
        :return: -
        """
        if (node_in, node_out) in self._dict_cost.keys():
            raise Exception("This edge already exists.")
        elif node_in not in self.parse_vertices() or node_out not in self.parse_vertices():
            raise Exception("The nodes don't exist.")
        else:
            if node_in not in self._dict_out.keys():
                self._dict_out[node_in] = [node_out]
            else:
                self._dict_out[node_in].append(node_out)
            if node_out not in self._dict_in.keys():
                self._dict_in[node_out] = [node_in]
            else:
                self._dict_in[node_out].append(node_in)
            self._dict_cost[(node_in, node_out)] = cost
            self._nr_of_edges += 1

    def remove_edge(self, node_in, node_out):
        """
        Function that removes an edge from the graph
        Complexity: Theta(1)
        :param node_in: the first vertex
        :param node_out: the second vertex
        :raise Exception: if the edge doesn't exist
        :return: -
        """
        if (node_in, node_out) not in self._dict_cost.keys():
            raise Exception("This edge can't be removed, it doesn't exist.")
        self._dict_in[node_out].remove(node_in)
        self._dict_out[node_in].remove(node_out)
        del self._dict_cost[(node_in, node_out)]
        self._nr_of_edges -= 1

    def add_node(self, vertex):
        """
        Function that adds a node to the graph
        Complexity: Theta(1)
        :param vertex: the node to be added
        :raise Exception: the node is invalid (it already exists)
        :return: -
        """

        if vertex not in self._list_of_nodes:
            self._nr_of_vertices += 1
            self._list_of_nodes.append(vertex)
            return
        else:
            raise Exception("The vertex to add is not valid.")

    def remove_node(self, vertex):
        """
        Function that removes a node from the graph
        Complexity: O(n)
        :param vertex: the node to be removed
        :raise Exception: if the vertex doesn't exist
        :return: -
        """

        if vertex not in self._list_of_nodes:
            raise Exception("The vertex to remove doesn't exist.")

        else:
            if vertex in self._dict_in.keys():
                inbound_edges = [i for i in self._dict_in[vertex]]
                for node in inbound_edges:

                    self._dict_in[vertex].remove(node)
                    if node in self._dict_out.keys():
                        self._dict_out[node].remove(vertex)
                    del self._dict_cost[(node, vertex)]
                    self._nr_of_edges -= 1
            if vertex in self._dict_out.keys():
                outbound_edges = [i for i in self._dict_out[vertex]]
                for node in outbound_edges:
                    if node in self._dict_in.keys():
                        self._dict_in[node].remove(vertex)
                    self._dict_out[vertex].remove(node)
                    del self._dict_cost[(vertex, node)]
                    self._nr_of_edges -= 1
            self._nr_of_vertices -= 1
            self._list_of_nodes.remove(vertex)

    def read_from_file(self, file_name):
        """
        Function that reads a graph from a file
        Complexity: O(n)
        :param file_name: the file to read from
        :return: -
        """
        with open(file_name) as f:
            content = f.read().splitlines()

        self._nr_of_vertices = int(content[0].split()[0])
        self._nr_of_edges = int(content[0].split()[1])

        for index in range(1, len(content)):
            node_1 = int(content[index].split()[0])
            node_2 = int(content[index].split()[1])
            cost = int(content[index].split()[2])
            self.edges.append([node_1, node_2, cost])
            self.graph[node_1].append(node_2)
            self.graph[node_2].append(node_1)
            if node_2 not in self._dict_in.keys():
                self._dict_in[node_2] = [node_1]
            else:
                self._dict_in[node_2].append(node_1)

            if node_1 not in self._dict_out.keys():
                self._dict_out[node_1] = [node_2]
            else:
                self._dict_out[node_1].append(node_2)

            self._dict_cost[(node_1, node_2)] = cost
        self._list_of_nodes = [i for i in range(self._nr_of_vertices)]

    def write_to_file(self, file_name):
        """
        Function that writes to a file the graph
        Complexity: O(n)
        :param file_name: the file to write into
        :return: -
        """
        f = open(file_name, "w")
        f.write(str(self._nr_of_vertices) + " " + str(self._nr_of_edges) + "\n")

        for key, value in self._dict_out.items():
            for vertex in value:
                f.write(str(key) + " " + str(vertex) + " " + str(self._dict_cost[(key, vertex)]) + "\n")

    def get_cost(self, n1, n2):
        if not self.is_edge(n1, n2):
            raise Exception("The edge doesn't exist")
        else:
            return self._dict_cost[(n1, n2)]

    def get_nr_of_vertices(self):
        return self._nr_of_vertices

    def get_nr_of_edges(self):
        return self._nr_of_edges

    def set_nr_of_vertices(self, n):
        self._nr_of_vertices = n

    def set_nr_of_edges(self, m):
        self._nr_of_edges = m

    def get_dict_in(self):
        return self._dict_in

    def get_dict_out(self):
        return self._dict_out

    def get_dict_cost(self):
        return self._dict_cost

    def __str__(self):
        graph_str = str(self._nr_of_vertices) + " " + str(self._nr_of_edges) + "\n"
        for key, value in self._dict_out.items():
            for node in value:
                graph_str += str(key) + " " + str(node) + " " + str(self._dict_cost[(key, node)]) + "\n"
        graph_str += "Remaining nodes: "
        for node in self._list_of_nodes:
            graph_str += str(node) + " "
        return graph_str

    @staticmethod
    def random_graph(n, m):
        """
        Function that creates a random graph
        :param n: the number of vertices
        :param m: the number of edges
        :return: a graph
        """
        if int(m) > int(n) * int(n):
            raise Exception("The graph cannot be constructed.")
        h = Graph(n, 0, [i for i in range(int(n))])
        all_edges = [[i, j] for i in range(n) for j in range(n)]

        while m > 0:
            edge = random.choice(all_edges)
            all_edges.remove(edge)
            cost = random.randint(1, 50)
            h.add_edge(edge[0], edge[1], cost)
            m -= 1
        return h

    def shortest_path(self, start, end):
        """
        Function that calculates the shortest path between two vertices
        :param start: the starting vertex
        :param end: the ending vertex
        :return: the length and path
        """
        visited = {end}
        queue = [end]
        dist_dictionary = {end: 0}
        next_dictionary = {}
        while len(queue) != 0:
            x = queue.pop(0)
            try:
                for y in self.parse_inbound_edges(x):
                    if y not in visited:
                        queue.append(y)
                        visited.add(y)
                        dist_dictionary[y] = dist_dictionary[x] + 1
                        next_dictionary[y] = x
                        # print(queue)
            except Exception:
                continue
        x = start
        y = -1
        path = [start]
        while y != end:
            y = next_dictionary[x]
            x = y
            path.append(x)
        if start in dist_dictionary:
            return dist_dictionary[start], path
        else:
            raise Exception("No path")

    def DFS(self, x, visited=[], processed=[]):
        """
        Function that performs a depth first search
        :param x: the node that is currently analyzed
        :param visited: the list of visited nodes
        :param processed: the list of processed nodes
        :return: -
        """
        if x in self._dict_out.keys():
            for y in self.parse_outbound_edges(x):
                if y not in visited:
                    visited.append(y)
                    self.DFS(y, visited, processed)
        processed.append(x)

    def kosaraju(self):
        """
        Function that determines the strongly connected components of a graph
        :return: dictionary of strongly connected components (keys are nodes, values are the indices of the components)
        """
        processed = []
        visited = []
        for s in self.parse_vertices():
            if s not in visited:
                visited.append(s)
                self.DFS(s, visited, processed)
        visited.clear()
        c = 0
        comp = {}
        q = []
        while not len(processed) == 0:
            s = processed.pop()
            if s not in visited:
                c += 1
                comp[s] = c
                q.append(s)
                visited.append(s)
                while len(q) != 0:
                    x = q.pop()
                    try:
                        for y in self.parse_inbound_edges(x):
                            if y not in visited:
                                visited.append(int(y))
                                q.append(int(y))
                                comp[int(y)] = c
                    except Exception:
                        continue
        return comp

    def BCCUtil(self, u, parent, low, disc, st):
        """
        A recursive function that finds and prints strongly connected
        components using DFS traversal
        :param u: The vertex to be visited next
        :param parent: the parent of the vertex
        :param low: earliest visited vertex (the vertex with minimum
                   discovery time) that can be reached from subtree
                   rooted with current vertex
        :param disc: Stores discovery times of visited vertices
        :param st: To store visited edges
        :return:-
        """

        # Count of children in current node
        children = 0

        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        # Recur for all the vertices adjacent to this vertex
        for v in self.graph[u]:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if disc[v] == -1:
                parent[v] = u
                children += 1
                st.append((u, v))  # store the edge in stack
                self.BCCUtil(v, parent, low, disc, st)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 -- per Strongly Connected Components Article
                low[u] = min(low[u], low[v])

                # If u is an articulation point, pop
                # all edges from stack till (u, v)
                if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                    self.count += 1  # increment count
                    w = -1
                    while w != (u, v):
                        w = st.pop()

            elif v != parent[u] and low[u] > disc[v]:
                '''Update low value of 'u' only of 'v' is still in stack
                (i.e. it's a back edge, not cross edge).
                Case 2 
                -- per Strongly Connected Components Article'''

                low[u] = min(low[u], disc[v])

                st.append((u, v))

    # The function to do DFS traversal.
    # It uses recursive BCCUtil()
    def BCC(self):
        """
        Function that finds the number of biconnected components in the graph
        :return: -
        """
        # Initialize disc and low, and parent arrays
        disc = [-1] * (self._nr_of_vertices)
        low = [-1] * (self._nr_of_vertices)
        parent = [-1] * (self._nr_of_vertices)
        st = []

        # Call the recursive helper function to
        # find articulation points
        # in DFS tree rooted with vertex 'i'
        for i in range(self._nr_of_vertices):
            if disc[i] == -1:
                self.BCCUtil(i, parent, low, disc, st)

            # If stack is not empty, pop all edges from stack
            if st:
                self.count = self.count + 1

                while st:
                    w = st.pop()

    def floyd_warshall(self, x, y):
        d = [[math.inf for i in range(self._nr_of_vertices)] for j in range(self._nr_of_vertices)]
        p = [[-1 for i in range(self._nr_of_vertices)] for j in range(self._nr_of_vertices)]
        for i in range(self._nr_of_vertices):
            d[i][i] = 0
        for key, value in self._dict_cost.items():
            d[key[0]][key[1]] = value

        for i in range(self._nr_of_vertices):
            for j in range(self._nr_of_vertices):
                if i != j and d[i][j] != math.inf:
                    p[i][j] = i
        print(d)
        # print(p)
        print("Intermediate matrices: ")
        for k in range(self._nr_of_vertices):
            for i in range(self._nr_of_vertices):
                for j in range(self._nr_of_vertices):
                    if d[i][j] > d[i][k] + d[k][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        p[i][j] = p[k][j]
            print("k = " + str(k))
            print("p = ")
            for line in p:
                print(line)
            print("d = ")
            for line in d:
                print(line)
        path = []
        cost = p[x][y]
        start = x
        end = y
        path.append(cost)
        if d[start][end] == math.inf:
            raise Exception("No path")
        elif start == end:
            raise Exception("Same node")
        while cost != x:
            y = cost
            cost = p[x][y]
            path.insert(0, cost)
        path.append(end)
        return d[start][end], path

    '''
        def floyd_warshall(self, x, y):
            w = {}
            f = {}
            for i in range(self._nr_of_vertices):
                for j in range(self._nr_of_vertices):
                    if i == j:
                        w[(i, j)] = 0
                    elif (i, j) in self._dict_cost.keys():
                        w[(i, j)] = self._dict_cost[(i, j)]
                        f[(i, j)] = j
                    else:
                        w[(i, j)] = INFINITY

            for k in range(self._nr_of_vertices):
                for i in range(self._nr_of_vertices):
                    for j in range(self._nr_of_vertices):
                        if w[(i, j)] > w[(i, k)] + w[(k, j)]:
                            w[(i, j)] = w[(i, k)] + w[(k, j)]
                            f[(i, j)] = f[(i, k)]

            return w[(x, y)], f
    '''

    def toposortalg(self):
        sorted = []
        fullyProcessed = set()
        inProcess = set()
        for x in self._list_of_nodes:
            if x not in fullyProcessed:
                ok = self.toposortdfs(x, sorted, fullyProcessed, inProcess)
                if not ok:
                    sorted.clear()
                    return False, sorted
        return True, sorted

    def toposortdfs(self, x, sorted, fullyProcessed, inProcess):
        inProcess.add(x)
        if x in self._dict_in:
            for y in self.parse_inbound_edges(x):
                if y in inProcess:
                    return False
                elif y not in fullyProcessed:
                    ok = self.toposortdfs(y, sorted, fullyProcessed, inProcess)
                    if not ok:
                        return False
        inProcess.remove(x)
        sorted.append(x)
        fullyProcessed.add(x)
        return True

    def is_dag(self):
        return self.toposortalg()

    def highest_cost_path(self, c, z):
        dag_answer = self.is_dag()
        if not dag_answer[0]:
            return -1
        dist = [-math.inf for i in range(self._nr_of_vertices)]
        dist[c] = 0

        for u in dag_answer[1]:
            if u == z:
                break
            if u in self._dict_in:
                for v in self.parse_inbound_edges(u):
                    if dist[u] < (dist[v] + self._dict_cost[(v, u)]):
                        dist[u] = dist[v] + self._dict_cost[(v, u)]
            if u in self._dict_out:
                for v in self.parse_outbound_edges(u):
                    if dist[v] < (dist[u] + self._dict_cost[(u, v)]):
                        dist[v] = dist[u] + self._dict_cost[(u, v)]
        return dist[z]

    def sortGraph(self):
        sortedGraph = []
        fullyProcessed = set()
        inProcess = set()
        for x in self.parse_vertices():
            if x not in fullyProcessed:
                ok = self.TopoSortDFS(x, sortedGraph, fullyProcessed, inProcess)
                if not ok:
                    sortedGraph = []
                    return sortedGraph
        return sortedGraph

    def TopoSortDFS(self, x, sortedGraph, fullyProcessed, inProcess):
        inProcess.add(x)
        if x in self._dict_in.keys():
            for y in self.parse_inbound_edges(x):
                if y in inProcess:
                    return False
                if y not in fullyProcessed:
                    ok = self.TopoSortDFS(y, sortedGraph, fullyProcessed, inProcess)
                    if not ok:
                        return False
        inProcess.remove(x)
        sortedGraph.append(x)
        fullyProcessed.add(x)
        return True

    def TSP_greedy(self, node):
        path = []
        self.min = 10000
        self.j_min = 10000
        self.visited.clear()
        path.clear()
        path = [0 for i in range(self._nr_of_vertices + 1)]
        self.visited = [0 for i in range(self._nr_of_vertices)]
        path[0] = node
        self.visited[node] = 1
        count = 1
        cost = 0
        for i in range(self._nr_of_vertices - 1):
            self.choose(path[count - 1])
            print("Connected (" + str(path[count - 1]) + ", " + str(self.j_min) + ") of cost " + str(self.min))
            path[count] = self.j_min
            self.visited[self.j_min] = 1
            count += 1
            cost += self.min
        cost += self.get_cost(path[self._nr_of_vertices - 1], node)
        print("Path has cost " + str(cost) + " and is: ")
        for i in range(self._nr_of_vertices):
            print(str(path[i]), end=' ')
        print(str(node))

    def TSP_heuristic(self):
        save_cost = 10000
        save_path = [0 for i in range(self._nr_of_vertices + 1)]
        path = []
        for index in range(self._nr_of_vertices):
            print("We start at point " + str(index))
            self.min = 10000
            self.j_min = 10000
            self.visited.clear()
            path.clear()
            path = [0 for i in range(self._nr_of_vertices + 1)]
            self.visited = [0 for i in range(self._nr_of_vertices)]
            path[0] = index
            self.visited[index] = 1
            count = 1
            cost = 0
            for i in range(self._nr_of_vertices - 1):
                self.choose(path[count - 1])
                print("Connected (" + str(path[count - 1]) + ", " + str(self.j_min) + ") of cost " + str(self.min))
                path[count] = self.j_min
                self.visited[self.j_min] = 1
                count += 1
                cost += self.min
            cost += self.get_cost(path[self._nr_of_vertices - 1], index)
            print("Path has cost " + str(cost) + " and is: ")
            for i in range(self._nr_of_vertices):
                print(str(path[i]), end=' ')
            print(str(index))
            if cost < save_cost:
                for i in range(self._nr_of_vertices):
                    save_path[i] = path[i]
                save_cost = cost
        print("Shortest path starts at point " + str(save_path[0]) + ", has cost " + str(save_cost) + " and is:")
        for i in range(self._nr_of_vertices):
            print(str(save_path[i]), end=' ')
        print(str(save_path[0]))
        return

    def TSP_sort(self):
        self.edges.sort(key=lambda i: i[2])
        save_cost = 10000
        save_path = [[0, 0, 0] for i in range(self._nr_of_vertices + 1)]
        path = []
        for index in self.edges:
            print("-----We start with edge " + str(index))
            self.min = 10000
            self.j_min = [10000, 10000, 10000]
            self.visited.clear()
            path.clear()
            path = [[0, 0, 0] for i in range(self._nr_of_edges + 1)]
            self.visited = [0 for i in range(self._nr_of_vertices)]
            path[0] = index
            self.visited[index[0]] = 1
            self.visited[index[1]] = 1
            count: int = 1
            cost = index[2]
            for i in range(self._nr_of_vertices - 2):
                self.choose2(path[count - 1])
                print("Connected (" + str(path[count - 1][1]) + ", " + str(self.j_min[1]) + ") of cost " + str(self.min))
                path[count] = self.j_min
                self.visited[self.j_min[0]] = 1
                self.visited[self.j_min[1]] = 1
                count += 1
                cost += self.min
            cost += self.get_cost(path[int(self._nr_of_vertices - 2)][1], index[0])
            #cost += path[self._nr_of_edges - 1]
            print("Path has cost " + str(cost) + " and is: ")
            for i in range(self._nr_of_vertices - 1):
                print(str(path[i]), end=' ')
            print("[" + str(path[self._nr_of_vertices - 2][1]) + ", " + str(index[0]) + ", " + str(self.get_cost(path[self._nr_of_vertices - 2][1], index[0])) + "]")
            if cost < save_cost:
                for i in range(self._nr_of_vertices - 1):
                    save_path[i] = path[i]
                save_path[self._nr_of_vertices - 1] = [path[self._nr_of_vertices - 2][1], index[0], self.get_cost(path[self._nr_of_vertices - 2][1], index[0])]
                save_cost = cost
        print("Shortest path starts at point " + str(save_path[0][0]) + ", has cost " + str(save_cost) + " and is:")
        for i in range(self._nr_of_vertices):
            print(str(save_path[i]), end=' ')
        print()
        return

    def choose(self, last):
        self.min = 10000
        self.j_min = -1
        for j in range(self._nr_of_vertices):
            if not self.visited[j]:
                if self.get_cost(last, j) < self.min:
                    self.min = self.get_cost(last, j)
                    self.j_min = j

    def choose2(self, last):
        self.min = 10000
        self.j_min = [-1, -1, -1]
        for j in range(self._nr_of_vertices):
            if not self.visited[j]:
                if self.get_cost(last[1], j) < self.min:
                    self.min = self.get_cost(last[1], j)
                    self.j_min = [last[1], j, self.get_cost(last[1], j)]

