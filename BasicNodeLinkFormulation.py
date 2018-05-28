# Copyright 2014 Dr. Greg M. Bernstein
""" This file shows how to generate the LP problem for the capacitated
    network design problem (multi-commodity routing) in the node-link
    formulation. The sample main program uses example 2.1 from Pioro and Medhi for
    network and demands.
"""
import time

import pandas as pd
import networkx as nx
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum
import random

# df = pd.DataFrame()
start_time = time.time()


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
            name = "D{}_{}_xL{}_{}".format(demand[0], demand[1], link[0], link[1])
            link_flows[(link, demand)] = LpVariable(name, 0)
    # Add the objective function which is the sum of all the
    # link flow variables times their respective link weights.
    tmp_list = []
    for link in link_list:
        for demand in demand_list:
            tmp_list.append(g[link[0]][link[1]]["weight"] * link_flows[(link, demand)])
    prob += lpSum(tmp_list)
    # Now lets include the link capacity constraints
    # we have one to add for each
    for link in link_list:
        tmp_list = []
        for demand in demand_list:
            tmp_list.append(link_flows[(link, demand)])
        link_name = "L{}_{}".format(link[0], link[1])
        prob += lpSum(tmp_list) <= g[link[0]][link[1]]['capacity'], "LinkCap|" + link_name
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
                tmp_list.append(-1.0 * link_flows[(link, demand)])
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
    g_temp.add_edge(1, 2, capacity=1, weight=1)  # add a "capacity" parameter
    g_temp.add_edge(1, 3, capacity=1, weight=1)  # can have any name you like
    g_temp.add_edge(2, 3, capacity=1, weight=1)

    print(g_temp.edges(data=True))
    g = g_temp.to_directed()  # Nice function to produce a directed version
    print(g.edges(data=True))
    # Here we define demands using a Python dictionary. A Python tuple (a,b)
    # is used for the demand pair, and its dictionary value represents its
    # volume.
    # demands = {(1, 2): 5, (2, 1): 5, (1, 3): 7, (3, 1): 7, (2, 3): 8, (3, 2): 8}
    min_cut = 2
    d0 = random.uniform(0, min_cut)
    d1 = random.uniform(0, min_cut)
    d2 = random.uniform(0, min_cut)
    d3 = random.uniform(0, min_cut)
    d4 = random.uniform(0, min_cut)
    d5 = random.uniform(0, min_cut)
    import numpy as np

    steps = 0.2
    fr = 0.0
    to = 2.0
    d = np.arange(fr, to + steps, steps)

    d1 = np.arange(fr, to + steps, steps)
    d2 = np.arange(fr, to + steps, steps)
    d3 = np.arange(fr, to + steps, steps)
    d4 = np.arange(fr, to + steps, steps)
    d5 = np.arange(fr, to + steps, steps)











    ####################################
    templist=list()
    dd = [0.3, 0.0, 2.0, 0.0, 0.0, 0.3]
    demands = {(1, 2): dd[0], (1, 3): dd[1], (2, 1): dd[2], (2, 3): dd[3], (3, 1): dd[4], (3, 2): dd[5]}
    prob, flow_vars = basic_capacitated_node_link(g, demands)
    prob.solve()



    for v in prob.variables():
        # if v.varValue == 0.0: continue
        # outList.append(v.varValue)
        templist.append((v.varValue))
    print(templist)








    ###################################


    exit()























    outList = []
    outputFile = 'output-step' + str(steps) + '.csv'
    with open(outputFile, 'w') as t:

        for d0 in d:
            for d1 in d:
                for d2 in d:
                    for d3 in d:
                        for d4 in d:
                            for d5 in d:
                                demands = {(1, 2): d0, (1, 3): d1, (2, 1): d2, (2, 3): d3, (3, 1): d4, (3, 2): d5}
                                prob, flow_vars = basic_capacitated_node_link(g, demands)
                                prob.solve()
                                # print(LpStatus[prob.status])
                                if LpStatus[prob.status] == "Infeasible":
                                    # print("true")
                                    continue

                                '''outList.append(d0)
                                outList.append(d1)
                                outList.append(d2)
                                outList.append(d3)
                                outList.append(d4)
                                outList.append(d5)'''

                                t.write(str(d0))
                                t.write(", ")
                                t.write(str(d1))
                                t.write(", ")
                                t.write(str(d2))
                                t.write(", ")
                                t.write(str(d3))
                                t.write(", ")
                                t.write(str(d4))
                                t.write(", ")
                                t.write(str(d5))
                                t.write(", ")

                                for v in prob.variables():
                                    # if v.varValue == 0.0: continue
                                    # outList.append(v.varValue)
                                    t.write(str(v.varValue))
                                    t.write(", ")
                                # print(outList)
                                '''if len(df) == 0:
                                    df = pd.DataFrame(outList)
                                    #print(outList)
                                    outList = []

                                    continue'''

                                # print(outList)
                                # df.loc[len(df)] = outList
                                # df.append(outList)
                                outList = []
                                t.write('\n')
    # df.head()
    # df.to_csv("output.csv")
    t.close()
    # print(v.name, "=", v.varValue)

    # print(a, b, c, d, e, f)

    print("--- %s seconds ---" % (time.time() - start_time))

    # for v in prob.variables():
    #    print(v.name, "=", v.varValue)
    '''

    #print(d0, d1, d2, d3, d4, d5)
    #print("d0: ", d0)
    demands = {(1, 2): d0, (1, 3): d1, (2, 1): d2, (2, 3): d3, (3, 1): d4, (3, 2): d5}
    print(demands)
    #print(demands[(2, 1)])
    prob, flow_vars = basic_capacitated_node_link(g, demands)
    print("flow_vars: ", flow_vars)
    prob.writeLP("basicNodeLink2_1.lpt")
    prob.solve()
    print("Status:", LpStatus[prob.status])
    for v in prob.variables():
        #if v.varValue == 0.0: continue
        print(v.name, "=", v.varValue)'''