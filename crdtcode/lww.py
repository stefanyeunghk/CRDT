# Author : Yeung Kam Kwan (Stefan)
# Date: 18/06/2021

from datetime import datetime


class SBLWWFunctions:
    """
    This is a class to construct the LWWElementSet
    """

    @staticmethod
    def update(payload, vertex):
        """
        This function will add an vertex to Payload
        Payload : type = list
        vertex : the vertex we will be adding to the list

        Result:
            return payload after a vertex is added
        """
        vertex_in_graph = False

        for i in range(len(payload)):
            # if vertex is in the graph, update the timestamp
            if payload[i]['vertex'] == vertex:
                payload[i]['timestamp'] = datetime.now()
                vertex_in_graph = True

        # if not in the graph, append it into the payload list
        if not vertex_in_graph:
            payload.append({'vertex': vertex, 'timestamp': datetime.now()})

        payload.sort(key=lambda i: i['vertex'])

        return payload

    @staticmethod
    def compare(payload1, payload2):
        """
        This function will compare two payload list

        Result:
            bool: True if two list are equal, False otherwise
        """

        for element_1 in payload1:
            if element_1 not in payload2:
                return False
        return True

    @staticmethod
    def merge(payload1, payload2):
        """
        This function will merge payload 2 to payload 1

        Result:
            return payload1 after the merging process
        """
        for element2 in payload2:

            # check if vertex is in payload 1
            vertex_found = False

            for i, element1 in enumerate(payload1):
                # If element2's vertex is present and its timestamp is greater than that of element1,
                # update the timestamp
                if element1['vertex'] == element2['vertex']:
                    vertex_found = True

                    if element1['timestamp'] < element2['timestamp']:
                        payload1[i]['timestamp'] = element2['timestamp']

            # If element2 is not in the list, append it to payload1
            if not vertex_found:
                payload1.append(element2)

        payload1.sort(key=lambda i: i['vertex'])
        return payload1

    @staticmethod
    def display(name, payload):
        """
        This function will print payload

        """

        print("{}: ".format(name), end="")
        # Prints vertex with timestamps in microseconds
        for item in payload:
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
        This function will add the vertex to payload W
        """

        self.W = self.lwwf.update(self.W, elem)

    def remove(self, elem):
        """
        This function will remove the vertex from payload R
        """

        self.R = self.lwwf.update(self.R, elem)

    def query(self, elem):
        """
        This function will check if the element is in the graph/payload

        Result: bool: True if element is in the payload 'W'' with latest timestamp when compared to the one in
        payload 'R', False otherwise.
        """

        elem_in_a = [item for item in self.W if item['vertex'] == elem]
        if len(elem_in_a) != 0:
            elem_in_r = [item for item in self.R if item['vertex'] == elem]
            if len(elem_in_r) == 0 or elem_in_r[-1]["timestamp"] < elem_in_a[-1]["timestamp"]:
                return True
        return False

    def compare(self, lww):
        """
        This function is to compare the two payload W and R

        Result:
            return true if both payload are the same, else return false
        """

        return self.lwwf.compare(self.W, lww.W) and self.lwwf.compare(self.R, lww.R)

    def merge(self, lww):
        """
        This function will merge two payload W and R
        """

        # Merge payload 'W'
        self.W = self.lwwf.merge(self.W, lww.W)

        # Merge payload 'R'
        self.R = self.lwwf.merge(self.R, lww.R)

    def display(self):
        """
        This function will print/ display the two payload
        """

        # print payload 'W'
        self.lwwf.display('W', self.W)

        # print payload 'R'
        self.lwwf.display('R', self.R)

