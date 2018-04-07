# Copyright 2014 Dr. Greg M. Bernstein
"""
    Example script showing how to read in graphs, demands, and paths
    from JSON files. Using networkx and our own helper functions.
"""
__author__ = 'Greg Bernstein'
from networkx.readwrite import json_graph
import Utilities.jsonconverter as jc  # This is my custom library
import json
if __name__ == '__main__':
    # Gets the graph. Assumes the file is in the same directory as
    # this python file
    g = json_graph.node_link_graph(json.load(open("linkPathEx1.json")))
    print g.edges(data=True)
    # Gets the demands from a file.
    demands = jc.j_to_demands(json.load(open("demandLinkPathEx1.json")))
    print demands
    # Gets the path candidates from a file.
    paths = jc.j_to_paths(json.load(open("pathsLinkPathEx1.json")))
    print paths
