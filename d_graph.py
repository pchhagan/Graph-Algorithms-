# Course: CS261 - Data Structures
# Author: Perrin Chhagan
# Assignment: Assignment 6
# Description: This project will create a directed graph and methods to alter the graph

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        This method will add a vertex to the graph
        """

        for i in range(0, self.v_count):
            self.adj_matrix[i].append(0)
        self.v_count += 1
        self.adj_matrix.append([0]*self.v_count)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        This method adds a new edge to the graph, connecting the provided indices
        """
        if src >= self.v_count or dst >= self.v_count or src == dst or weight < 0:
            return

        self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        This method will remove an edge between two given indices
        """
        if src >= self.v_count or dst >= self.v_count or self.adj_matrix[src][dst] == 0 or src < 0 or dst < 0:
            return

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        This method returns the vertices in the list
        """
        list = []
        for i in range(0, self.v_count):
            list.append(i)

        return list

    def get_edges(self) -> []:
        """
        This method returns a list of the edges in the graph
        """
        list = []

        for i in range(0, self.v_count):
            for j in range(0, len(self.adj_matrix[i])):
                if self.adj_matrix[i][j] != 0:
                    list.append((i, j, self.adj_matrix[i][j]))

        return list
    def is_valid_path(self, path: []) -> bool:
        """
        This method takes a list of indices and returns True if the path is valid
        """
        if path == []:
            return True

        length = len(path)

        for i in range(0, length-1):
            if self.adj_matrix[path[i]][path[i+1]] == 0:
                return False
        return True


    def dfs(self, v_start, v_end=None, list = None) -> []:
        """
        This method performs a depth-first search and returns a list of vertices visited during the search
        """
        if list == None:
            list = []

        if v_start > self.v_count:
            return list

        list.append(v_start)
        length = len(self.adj_matrix[v_start])

        for i in range(0, length):
            if v_end == v_start:
                return list
            elif v_end != None and self.adj_matrix[i][v_end] != 0:
                list.append(i)
                list.append(v_end)
                return list

            elif self.adj_matrix[v_start][i] != 0 and i not in list:
                self.dfs(i,v_end, list)
            else:
                continue

        return list

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method performs a breadth first search and returns a list of vertices visited during the search.
        """
        list = []
        queue = []

        if v_start > self.v_count:
            return list

        list.append(v_start)
        queue.append(v_start)

        while queue:
            vertex = queue.pop(0)
            vertex_length = len(self.adj_matrix[vertex])

            for j in range(0, vertex_length):
                if v_end == v_start:
                    return list
                elif v_end == j:
                    list.append(j)
                    return list
                elif self.adj_matrix[vertex][j] != 0 and j not in list :
                    queue.append(j)
                    list.append(j)

        return list

    def recursivecycle(self, node, path=None, stack =None):
        """
        This method will return True if a cycle is detected and false otherwise
        """
        path.append(node)
        stack.append(node)
        length = len(self.adj_matrix[node])

        for vertex in range(0, length):
            if self.adj_matrix[node][vertex] != 0:
                if vertex not in path:
                    if self.recursivecycle(vertex, path, stack) == True:
                        return True
                elif vertex in stack:
                    return True

        stack.remove(node)
        return False


    def has_cycle(self):
        """
        This method will return True if a cycle is detected and false otherwise
        """
        path = []
        stack = []

        for node in range(0, self.v_count):
            if node not in path:
                if self.recursivecycle(node, path, stack) == True:
                    return True

        return False



    def dijkstra(self, src: int) -> []:
        """
        This method implements the Dijkstra algorithm to compute the length of the shortest path from a given vertex
        to all other vertices
        """
        distance = [float("inf")]*self.v_count
        visited = []
        visited.append((src, 0))
        marked = []

        while visited:
            values = visited.pop(0)
            vertex = values[0]
            cur_distance = values[1]

            if vertex in marked and cur_distance < distance[vertex]:
                distance[vertex] = cur_distance
                marked.remove(vertex)

            if vertex not in marked:
                marked.append(vertex)
                distance[vertex] = cur_distance

                length = len(self.adj_matrix[vertex])
                for i in range(0, length):
                    if self.adj_matrix[vertex][i] == 0:
                        continue
                    else:
                        new_distance = cur_distance + self.adj_matrix[vertex][i]

                        visited.append((i, new_distance))

        return distance




if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(12):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (12, 3, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')

