from collections import deque 
class node():
    def __init__(self,value, weight):
        self.value=value
        self.weight=weight
        self.next=None

class graph:
    def __init__(self):
        self.graph={}            

    def add_edge(self,source,dest, weight): 
        vert=node(dest, weight)
        if source in self.graph:
            vert.next=self.graph[source]
            self.graph[source]=self.graph[source].append(vert)
        else:
            self.graph[source]=[vert]
        vertice.next=self.graph[source]
        self.graph[source]= vertice

#class dijkstra:
#    def __init__(self):