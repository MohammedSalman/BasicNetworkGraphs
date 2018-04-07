# Copyright 2014 Dr. Greg M. Bernstein
""" This file shows how to generate the LP problem for the capacitated
    network design problem (multi-commodity routing) in the node-link
    formulation. The sample main program uses example 2.1 from Pioro and Medhi for
    network and demands.
"""

import networkx as nx
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum


def basic_capacitated_node_link(g, demands):
    """ Creates a basic capacitated network design problem in node-link formulation

        Parameters
        ----------
        g : networkx.DiGraph
            a directed network graph g,
        d : dictionary
            a dictionary of demands indexed by node pairs
        Returns
        -------
        pulp.LpProblem
            a PuLP problem instance suitable for solving or writing.
    """
    # Set up Node Link Formulation Linear Program
    # First some nice lists to help us stay organized
    demand_list = sorted(demands.keys())
    link_list = sorted(g.edges())
    node_list = sorted(g.nodes())
    # print demand_list
    # print link_list
    # print node_list
    prob = LpProblem("Basic Node Link Formulation", LpMinimize)
    # Create a dictionary to hold link flow variables
    # these will be indexed by a tuple of (link, demand) pairs.
    # remember that these are each tuples themselves
    link_flows = {}
    for link in link_list:
        for demand in demand_list:
            name = "xL{}_{}_D{}_{}".format(link[0], link[1], demand[0], demand[1])
            link_flows[(link, demand)] = LpVariable(name, 0)
    # Add the objective function which is the sum of all the
    # link flow variables times their respective link weights.
    tmp_list = []
    for link in link_list:
        for demand in demand_list:
            tmp_list.append(g[link[0]][link[1]]["weight"]*link_flows[(link, demand)])
    prob += lpSum(tmp_list)
    # Now lets include the link capacity constraints
    # we have one to add for each
    for link in link_list:
        tmp_list = []
        for demand in demand_list:
            tmp_list.append(link_flows[(link, demand)])
        link_name = "L{}_{}".format(link[0], link[1])
        prob += lpSum(tmp_list)<= g[link[0]][link[1]]['capacity'], "LinkCap|" + link_name
    # Now for the node flow conservation constraints
    # We have one of these for each node and demand pair.
    for node in node_list:
        for demand in demand_list:
            tmp_list = []
            in_edges = g.in_edges(node)
            out_edges = g.out_edges(node)
            for link in out_edges:
                tmp_list.append(link_flows[(link, demand)])
            for link in in_edges:
                tmp_list.append(-1.0*link_flows[(link, demand)])
            rhs = 0.0  # Default transit node, but check if source or sink
            if node == demand[0]:  # Is node the source of the demand
                rhs = demands[demand]
            if node == demand[1]:  # Is node the sink of the demand
                rhs = -demands[demand]
            constraint_name = "NodeCons|{}D{}_{}".format(node, demand[0], demand[1])
            prob += lpSum(tmp_list) == rhs, constraint_name
    return prob, link_flows

if __name__ == "__main__":
    # Define the network, we'll start with an undirected version and use a
    # convenient utility function to convert it to a directed graph.
    g_temp = nx.Graph()
    # Don't need to add nodes separately.
    g_temp.add_edge(1, 2, capacity=10, weight=1)  # add a "capacity" parameter
    g_temp.add_edge(1, 3, capacity=10, weight=1)  # can have any name you like
    g_temp.add_edge(2, 3, capacity=7, weight=1)
    print(g_temp.edges(data=True))
    g = g_temp.to_directed()  # Nice function to produce a directed version
    print(g.edges(data=True))
    # Here we define demands using a Python dictionary. A Python tuple (a,b)
    # is used for the demand pair, and its dictionary value represents its
    # volume.
    demands = {(1, 2): 5, (2, 1): 5, (1, 3): 7, (3, 1): 7, (2, 3): 8, (3, 2): 8}
    print(demands)
    print(demands[(2, 1)])
    prob, flow_vars = basic_capacitated_node_link(g, demands)
    prob.writeLP("basicNodeLink2_1.lpt")
    prob.solve()
    print("Status:", LpStatus[prob.status])
    for v in prob.variables():
        print(v.name, "=", v.varValue)

