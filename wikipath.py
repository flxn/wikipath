# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import collections
from collections import defaultdict
import time

ROWS_MAX = 0

""" Queue Class to queue nodes when searching the graph """
class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

""" Simple Directed Graph """
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

nodenames = dict()
G = SimpleDiGraph()

def main():
    """ Main entry point """
    if len(sys.argv) < 3:
        print 'missing arguments'
        print 'Usage: wikipath.py [graphfile] [nodefile]'
        sys.exit(1)

    graphfile = sys.argv[1]
    nodenamefile = sys.argv[2]

    loadNames(nodenamefile)
    loadNodes(graphfile)

    print "Total number of nodes: %i" % G.number_of_nodes()

    while True:
        print "\n--- Shortest Path ---"
        node_from = raw_input("From: ").decode(sys.stdin.encoding)
        startnode = findNodeByName(node_from)
        if startnode == -1:
            print node_from + " not found"
            continue

        node_to = raw_input("To: ").decode(sys.stdin.encoding)
        endnode = findNodeByName(node_to)
        if endnode == -1:
            print node_to + " not found"
            continue

        try:
            #print "[1]:", startnode, "[2]:", endnode, "\n"
            start = time.time()
            shortest_path = find_path(G, startnode, endnode)
            end = time.time()
            #print end - start
            print ""
            print " -> ".join([nodenames[elem] for elem in shortest_path])
        except Exception as e:
            print "Error"
            print e
            pass

def loadNames(nodenamefile):
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

def loadNodes(graphfile):
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

def search(graph, start, goal):
    """ Search shortest path between nodes """
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
    """ Wrapper for the search function """
    raw_path = search(graph, start, goal)
    current = goal
    path = [current]
    while current != start:
        current = raw_path[current]
        path.append(current)
    path.reverse()
    return path

def findNodeByName(searchname):
    """ Get numeric node id by article name """
    for nodenumber, name in nodenames.iteritems():
        if name.decode('utf-8').lower() == searchname.lower():
            return nodenumber
    return -1

if __name__ == '__main__':
    sys.exit(main())
