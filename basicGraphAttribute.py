# Copyright 2014 Dr. Greg M. Bernstein
""" Simple graph construction example with NetworkX along with link attributes.
"""

import networkx as nx

if __name__ == '__main__':
    g = nx.Graph()
    # Don't need to add nodes separately.
    g.add_edge(1,2, capacity=10)  # add a "capacity" parameter
    g.add_edge(1,3, capacity=10)  # can have any name you like
    g.add_edge(2,3, capacity=15)
    print "Graph nodes are: {}".format(g.nodes())
    print "Graph edges are: {}".format(g.edges(data=True))
    print "Is edge (2,1) in the graph? {}".format(g.has_edge(2,1))
    print "Is edge (3,2) in the graph? {}".format(g.has_edge(3,2))
    print "The capacity of edge (2,3) is {}".format(g[2][3]["capacity"])