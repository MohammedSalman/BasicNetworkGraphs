# Copyright 2014 Dr. Greg M. Bernstein
""" This file shows how to generate the LP problem for the capacitated
    network design problem (multi-commodity routing) in the node-link
    formulation. The sample main program uses example 2.1 from Pioro and Medhi for
    network and demands.
"""
import time
import numpy as np
#import pandas as pd
import networkx as nx
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum
import random

# df = pd.DataFrame()
start_time = time.time()

def generate_random_demands(rows, columns):
    sample = np.random.uniform(low=0, high=0.09, size=(rows, columns))
    return sample

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
    g_temp.add_edge(1, 8, capacity=1, weight=1)
    g_temp.add_edge(2, 3, capacity=1, weight=1)
    g_temp.add_edge(2, 4, capacity=1, weight=1)
    g_temp.add_edge(3, 6, capacity=1, weight=1)
    g_temp.add_edge(4, 5, capacity=1, weight=1)
    g_temp.add_edge(4, 11, capacity=1, weight=1)
    g_temp.add_edge(5, 6, capacity=1, weight=1)
    g_temp.add_edge(5, 7, capacity=1, weight=1)
    g_temp.add_edge(6, 10, capacity=1, weight=1)
    g_temp.add_edge(6, 13, capacity=1, weight=1)
    g_temp.add_edge(7, 8, capacity=1, weight=1)
    g_temp.add_edge(8, 9, capacity=1, weight=1)
    g_temp.add_edge(9, 10, capacity=1, weight=1)
    g_temp.add_edge(9, 12, capacity=1, weight=1)
    g_temp.add_edge(9, 14, capacity=1, weight=1)
    g_temp.add_edge(11, 12, capacity=1, weight=1)
    g_temp.add_edge(11, 14, capacity=1, weight=1)
    g_temp.add_edge(12, 13, capacity=1, weight=1)
    g_temp.add_edge(13, 14, capacity=1, weight=1)

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
    dd = [0.18422266, 0.06233564, 0.52392307, 1.49384433, 0.79119154,
        1.35945998, 1.96925816, 0.97016577, 1.69170347, 0.55327078,
        0.33132771, 1.44724894, 1.99274553, 1.66270438, 1.50957802,
        0.73584806, 1.04123075, 0.04867879, 0.54059585, 0.27513416,
        0.64708431, 0.901252  , 1.58961308, 1.45797537, 0.93143786,
        1.41735661, 0.68237035, 1.26611655, 0.15199571, 1.70001858,
        0.60231951, 1.37338468, 0.52825669, 0.77183132, 1.13311607,
        1.41747603, 1.2892963 , 0.90109087, 0.83882952, 0.02951946,
        1.00046574, 1.14465838, 0.21580805, 1.27890129, 1.00419698,
        1.51041312, 1.87076334, 0.09407585, 1.58163448, 1.71275478,
        1.93593117, 1.04527553, 1.74863141, 1.8881635 , 0.79314005,
        0.27919258, 1.80655765, 1.51243016, 0.85606477, 0.40617054,
        0.2340743 , 0.78437337, 1.80990422, 1.26683235, 1.4970607 ,
        1.28009347, 1.08790337, 0.87930707, 1.10043118, 1.41689179,
        1.85430211, 1.35731063, 0.13367596, 0.23721368, 0.42279566,
        0.97875642, 1.17717279, 1.20913946, 1.81288718, 0.35276388,
        1.51963091, 1.96918035, 0.89295815, 1.14504074, 1.78881074,
        0.94325628, 1.38106198, 0.47283155, 0.62799906, 1.05799139,
        1.19852777, 0.7231912 , 1.76391078, 1.29395986, 1.25277001,
        1.95368561, 0.72692627, 1.85587141, 1.00409937, 1.9389634 ,
        1.58479078, 1.60710297, 1.67443214, 1.43022798, 1.06411202,
        0.11113216, 1.14101617, 1.73773352, 0.96102347, 0.33726481,
        1.4243191 , 0.37934957, 0.64918263, 0.02855302, 1.37450676,
        1.07345736, 1.71024793, 1.34468987, 0.03592246, 1.69698383,
        1.43719348, 0.21546515, 0.94807679, 0.81564831, 1.51933046,
        0.67101336, 1.2048994 , 0.05541071, 1.47195984, 0.56846495,
        0.56797218, 0.48010629, 0.1849746 , 1.28089673, 0.54511191,
        1.95457776, 1.35945721, 1.39088353, 0.41719796, 1.88827633,
        1.29606937, 0.90007286, 1.70543806, 1.53544129, 1.20343389,
        1.91480737, 1.63402088, 1.34935461, 0.31331627, 0.65549469,
        0.20206968, 0.69459116, 0.75969584, 1.8108884 , 0.37824005,
        0.23703678, 0.44670124, 1.73789099, 1.70506258, 0.93321436,
        0.53514231, 1.96302233, 0.06549123, 0.8375841 , 1.35158887,
        0.79195645, 1.66850919, 0.65090553, 1.5049539 , 1.82669471,
        1.33012711, 1.66993377, 1.3466623 , 0.66448641, 0.15377026,
        1.02117531, 0.8056676 , 1.16976452, 0.15983921, 0.2209544 ,
        1.16306075, 1.98567681]

    #generate tuples first
    list_of_tuples = []
    for i in range(1, 14+1):
        for j in range(1, 14+1):
            if i == j:
                continue
            tuple = (i, j)
            list_of_tuples.append(tuple)
    #print("len is: ", len(list_of_tuples))
    #print(list_of_tuples)
    dd = generate_random_demands(1, 182)
    #print(len(dd))
    #print(dd)
    #dd[0] = [0.07] * 182
    #print(dd[0])
    demands = dict(zip(list_of_tuples, dd[0]))
    #demands = {(1, 2): dd[0], (1, 3): dd[1], (2, 1): dd[2], (2, 3): dd[3], (3, 1): dd[4], (3, 2): dd[5]}
    prob, flow_vars = basic_capacitated_node_link(g, demands)
    tic=time.time()
    prob.solve()
    print("Taken time: ", time.time()-tic, " Seconds!")

    from termcolor import colored



    for v in prob.variables():
        # if v.varValue == 0.0: continue
        # outList.append(v.varValue)
        templist.append((v.varValue))
        if v.varValue > 2:
            #colored('hello', 'red')
            print(colored("unrealistic number exist: ", 'red'), colored(v.varValue,'blue'))

    print(templist)
    print(len(templist))








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