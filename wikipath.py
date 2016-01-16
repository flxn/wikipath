# -*- coding: utf-8 -*-
#!/usr/bin/env python

import networkx as nx
import sys
import collections
from collections import defaultdict
import time

USE_NX = False
ROWS_MAX = 0

if len(sys.argv) < 3:
    print 'missing arguments'
    sys.exit(1)

graphfile = sys.argv[1]
nodenamefile = sys.argv[2]
nodenames = dict()

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

class SimpleDiGraph:
    def __init__(self):
        self.edges = defaultdict(list)

    def add_edge(self, node_from, node_to):
        self.edges[node_from].append(node_to)

    def neighbours(self, id):
        try:
            return self.edges[id]
        except:
            return []

    def number_of_nodes(self):
        return len(self.edges)

def search(graph, start, goal):
    queue = Queue()
    queue.put(start)
    visited = {}
    visited[start] = True
    path = {}
    path[start] = None

    while not queue.empty():
        current = queue.get()

        if current == goal:
            break

        for next in graph.neighbours(current):
            if next not in visited:
                queue.put(next)
                visited[next] = True
                path[next] = current

    return path

def find_path(graph, start, goal):
    raw_path = search(graph, start, goal)
    current = goal
    path = [current]
    while current != start:
        current = raw_path[current]
        path.append(current)
    path.reverse()
    return path

if USE_NX:
    G = nx.DiGraph()
else:
    G = SimpleDiGraph()

def findNodeByName(searchname):
    for nodenumber, name in nodenames.iteritems():
        if name.decode('utf-8') == searchname:
            return nodenumber
    return -1

start = time.time()
linecount = 0
with open(nodenamefile) as f:
    for line in f:
        linecount += 1
        if linecount % 1000 == 0:
            sys.stdout.write("\rLoading Names: %i loaded" % linecount)
            sys.stdout.flush()
        (nodenumber, name) = [col.strip() for col in line.split('|')]
        nodenames[int(nodenumber)] = name

end = time.time()
print " - elapsed time: %is" % (end - start)

start = time.time()
linecount = 0
with open(graphfile) as f:
    for line in f:
        linecount += 1
        if linecount % 1000 == 0:
            sys.stdout.write("\rLoading Connections: %i loaded" % linecount)
            sys.stdout.flush()

        (title,links) = [col.strip() for col in line.split(';')]
        links = links.split('|')
        for link in links:
            G.add_edge(int(title), int(link))

        if ROWS_MAX > 0 and linecount == ROWS_MAX:
            break

end = time.time()
print " - elapsed time: %is" % (end - start)

print "\nTotal number of nodes: %i" % G.number_of_nodes()

while True:
    print "\n--- Shortest Path ---"
    node_from = raw_input("From: ").decode(sys.stdin.encoding)
    node_to = raw_input("To: ").decode(sys.stdin.encoding)
    try:
        startnode = findNodeByName(node_from)
        endnode = findNodeByName(node_to)
        print "Node1: %i" % startnode
        print "Node2: %i\n" % endnode

        if USE_NX:
            shortest_path = nx.shortest_path(G, startnode, endnode)
        else:
            shortest_path = find_path(G, startnode, endnode)

        print " -> ".join([nodenames[elem] for elem in shortest_path])
    except Exception as e:
        print "Error"
        print e
        pass
