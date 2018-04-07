# Copyright 2014 Dr. Greg M. Bernstein
""" Simple graph construction example with NetworkX along with
    path validity checking function.
"""

import networkx as nx

def path_valid(g, p):
    """ Checks whether the list nodes p is a valid path in g.

        Parameters
        ----------
        g : networkx.Graph
            Some type of directed or undirected graph
        p : list
            The path given as a list of nodes.
    """
    plen = len(p)
    for i in range(plen-1):
     if not g.has_edge(p[i],p[i+1]):
         return False
    return True

if __name__ == '__main__':
    # Try creating an undirected graph
    g = nx.Graph()
    g.add_node(1); g.add_node(2); g.add_node(3)
    g.add_edge(1,2); g.add_edge(1,3); g.add_edge(2,3)
    print "Graph nodes are: {}".format(g.nodes())
    print "Graph edges are: {}".format(g.edges())
    print "Is edge (2,1) in the graph? {}".format(g.has_edge(2,1))
    print "Is edge (3,2) in the graph? {}".format(g.has_edge(3,2))
    print "Is path [1,3,2] valid? {}".format(path_valid(g, [1,3,2]))
    print "Is path [1,4,2] valid? {}".format(path_valid(g, [1,4,2]))
