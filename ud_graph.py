# Course: CS 261
# Author: Perrin Chhagan
# Assignment: Assignment 6
# Description: This project will create an undirected graph and methods to alter the graph


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v in self.adj_list.keys():
            return
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        if u not in self.adj_list.keys():
            self.adj_list[u] = []
        if v not in self.adj_list.keys():
            self.adj_list[v] = []
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            self.adj_list[u].sort()
            self.adj_list[v].sort()

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if u == v:
            return
        if u not in self.adj_list.keys():
            return
        if v not in self.adj_list.keys():
            return
        if v in self.adj_list[u]:
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list.keys():
            return
        del self.adj_list[v]
        for values in self.adj_list.values():
            if v in values:
                values.remove(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        list = []
        for values in self.adj_list.values():
            for v in values:
                if v not in list:
                    list.append(v)

        return list


    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        list = []
        for key in self.adj_list.keys():
            for vertex in self.adj_list[key]:
                if (key, vertex) not in list and (vertex, key) not in list:
                    list.append((key, vertex))

        return list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        length = len(path)
        if length == 1:
            if path[0] in self.adj_list.keys():
                return True
            else:
                return False

        for i in range(0, length-1):
            if path[i] in self.adj_list.keys():
                if path[i+1] not in self.adj_list[path[i]]:
                    return False
            else:
                return False

        return True

    def dfs(self, v_start, v_end=None,) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        path = []

        if v_start not in self.adj_list.keys():
            return path

        vertices =[]
        vertices.append(v_start)

        while vertices:
            vertex = vertices.pop()

            if vertex == v_end:
                path.append(vertex)
                return path
            if vertex not in path:
                path.append(vertex)
                for neighbor in self.adj_list[vertex][::-1]:
                    vertices.append(neighbor)

        return path


    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        list = []
        queue = []

        if v_start not in self.adj_list.keys():
            return list

        list.append(v_start)
        queue.append(v_start)

        while queue:
            vertex = queue.pop(0)

            for node in self.adj_list[vertex]:
                if v_end == v_start:
                    return list
                elif v_end == node:
                    list.append(node)
                    return list
                elif node not in list:
                    queue.append(node)
                    list.append(node)

        return list


    def count_connected_components(self):
        """
        Return number of connected compenents in the graph
        """
        list = []
        count = 0

        for v in self.adj_list.keys():
            if v not in list:
                self.recursive_count_connected(v, list)
                count += 1

        return count

    def recursive_count_connected(self, v_start, list=None):
        """This is a recursive helper method for count_connected_components"""
        if list == None:
            list = []

        if v_start not in self.adj_list.keys():
            return list

        list.append(v_start)

        for vertex in self.adj_list[v_start]:
            if vertex not in list:
                self.recursive_count_connected(vertex, list)

        return list


    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        list = []

        for node in self.adj_list.keys():
            if node not in list:
                if self.helper_has_cycle(node, list, -1) == True:
                    return True
        return False


    def helper_has_cycle(self, node, list=None, parent=None):
        """This is a recursive helper method for has_cycle"""
        list.append(node)

        for vertex in self.adj_list[node]:
            if vertex not in list:
                if self.helper_has_cycle(vertex,list,node):
                    return True
            elif vertex != parent:
                return True

        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    edges = ['BC', 'BI', 'BD', 'BF', 'IB', 'IG', 'HD', 'DG', 'FK', 'KJ', ]
    g = UndirectedGraph(edges)
    print(g.dfs("K","G"))





    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
