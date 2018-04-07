""" A basic link-path formulation of the capacitated network design problem.
    This is a single script version that reads in graph, demands, and candidate paths
    from JSON files.
"""
from networkx.readwrite import json_graph
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum
import Utilities.jsonconverter as jc
from Utilities.utilities import link_in_path
import json


if __name__ == '__main__':
    # Get the network from a JSON file
    g = json_graph.node_link_graph(json.load(open("linkPathEx1.json")))
    print (g.edges(data=True))
    demands = jc.j_to_demands(json.load(open("demandLinkPathEx1.json")))
    # Get candidate paths
    paths = jc.j_to_paths(json.load(open("pathsLinkPathEx1.json")))
    # Set up Node Link Formulation Linear Program
    # First some nice lists to help us stay organized
    demand_list = sorted(demands.keys())
    link_list = sorted(g.edges())
    print("g.edges(): ", g.edges())
    print("g.nodes(): ", g.nodes())
    node_list = list((g.nodes()))
    node_list = sorted(node_list[0:7])
    #print("debug: ",node_list[0])
    print("demand_list: ", demand_list)
    print("link_list; ", link_list)
    print("node_list: ", node_list)
    prob = LpProblem("Basic Link Path Formulation", LpMinimize)
    # Create a dictionary to hold demand path variables
    # these will be indexed by a tuple of (demand, path_num) pairs.
    demand_paths = {}
    for d in demand_list:
        for p in range(len(paths[d])):
            name = "xD{}_{}P_{}".format(d[0], d[1], str(p))
            demand_paths[d, p] = LpVariable(name, 0)
    # Add the objective function which for now is the sum of all the
    # demand path variables times their respective path length.
    tmp_list = []
    for d in demand_list:
        for p in range(len(paths[d])):
            tmp_list.append((len(paths[d][p]) - 1)*demand_paths[d, p])
    prob += lpSum(tmp_list)
    # Now lets include the link capacity constraints
    # we have one to add for each lin
    for link in link_list:
        tmp_list = []
        for d in demand_list:
            for p in range(len(paths[d])):
                if link_in_path(link, paths[d][p]):
                    tmp_list.append(demand_paths[d, p])
        link_name = "L{}_{}".format(link[0], link[1])
        prob += lpSum(tmp_list)<= g[link[0]][link[1]]['capacity'], "LinkCap|" + link_name

    # Now for the demand satisfaction constraints
    # We one for demand pair.
    for d in demand_list:
        tmp_list = []
        for p in range(len(paths[d])):
            tmp_list.append(demand_paths[d, p])
        constraint_name = "DemandSat_{}_{}".format(d[0], d[1])
        prob += lpSum(tmp_list) == demands[d], constraint_name

    prob.writeLP("basicLinkPathEx1.lpt")
    prob.solve()
    print("Status:", LpStatus[prob.status])
    for v in prob.variables():
        print(v.name, "=", v.varValue)


