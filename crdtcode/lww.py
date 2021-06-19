# Author : Yeung Kam Kwan (Stefan)
# Date: 18/06/2021

from datetime import datetime


class SBLWWFunctions:
    """
    This is a class to construct the LWWElementGraph
    """

    @staticmethod
    def update(graph, vertex):
        """
        This function will add an vertex to graph
        graph : type = list
        vertex : the vertex we will be adding to the list

        Result:
            return graph after a vertex is added
        """
        vertex_in_graph = False

        for i in range(len(graph)):
            # if vertex is in the graph, update the timestamp
            if graph[i]['vertex'] == vertex:
                graph[i]['timestamp'] = datetime.now()
                vertex_in_graph = True

        # if not in the graph, append it into the graph list
        if not vertex_in_graph:
            graph.append({'vertex': vertex, 'timestamp': datetime.now()})

        graph.sort(key=lambda i: i['vertex'])

        return graph

    @staticmethod
    def compare(graph1, graph2):
        """
        This function will compare two graph list

        Result:
            bool: True if two list are equal, False otherwise
        """

        for element_1 in graph1:
            if element_1 not in graph2:
                return False
        return True

    @staticmethod
    def merge(graph1, graph2):
        """
        This function will merge graph 2 to graph 1

        Result:
            return graph1 after the merging process
        """
        for element2 in graph2:

            # check if vertex is in graph 1
            vertex_found = False

            for i, element1 in enumerate(graph1):
                # If element2's vertex is present and its timestamp is greater than that of element1,
                # update the timestamp
                if element1['vertex'] == element2['vertex']:
                    vertex_found = True

                    if element1['timestamp'] < element2['timestamp']:
                        graph1[i]['timestamp'] = element2['timestamp']

            # If element2 is not in the list, append it to graph1
            if not vertex_found:
                graph1.append(element2)

        graph1.sort(key=lambda i: i['vertex'])
        return graph1

    @staticmethod
    def display(name, graph):
        """
        This function will print graph

        """

        print("{}: ".format(name), end="")
        # Prints vertex with timestamps in microseconds
        for item in graph:
            print("{}:{}".format(item["vertex"], item["timestamp"].microsecond), end=", ")

        # print an empty line
        print()


class LWWElementSet:

    def __init__(self, id):
        self.W = []
        self.R = []
        self.id = id
        self.lwwf = SBLWWFunctions()

    def add(self, elem):
        """
        This function will add the vertex to graph W
        """

        self.W = self.lwwf.update(self.W, elem)

    def remove(self, elem):
        """
        This function will remove the vertex from graph R
        """

        self.R = self.lwwf.update(self.R, elem)

    def query(self, elem):
        """
        This function will check if the element is in the graph

        Result: bool: True if element is in the graph 'W'' with latest timestamp when compared to the one in
        graph 'R', False otherwise.
        """

        elem_in_a = [item for item in self.W if item['vertex'] == elem]
        if len(elem_in_a) != 0:
            elem_in_r = [item for item in self.R if item['vertex'] == elem]
            if len(elem_in_r) == 0 or elem_in_r[-1]["timestamp"] < elem_in_a[-1]["timestamp"]:
                return True
        return False

    def compare(self, lww):
        """
        This function is to compare the two graph W and R

        Result:
            return true if both graph are the same, else return false
        """

        return self.lwwf.compare(self.W, lww.W) and self.lwwf.compare(self.R, lww.R)

    def merge(self, lww):
        """
        This function will merge two graph W and R
        """

        # Merge graph 'W'
        self.W = self.lwwf.merge(self.W, lww.W)

        # Merge graph 'R'
        self.R = self.lwwf.merge(self.R, lww.R)

    def display(self):
        """
        This function will print/ display the two graph
        """

        # print graph 'W'
        self.lwwf.display('W', self.W)

        # print graph 'R'
        self.lwwf.display('R', self.R)
