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
    dd = np.random.rand(1, 182)
    dd = dd[0]
    dd = [4] + [0] * 181
    print(dd)
    print(len(dd))
    dd = [0.08220968500069636, 0.5219585638345694, 0.24749372367650269, 0.013344960326749502, 0.1177980351456013,
          0.0008810286726378871, 0.002738039417152542, 0.008439602217455114, 0.0031690724371252503,
          0.0011287951925710714, 0.0004091215248593205, 7.660601214422049e-05, 8.735182612971353e-05,
          0.8050485698399746, 0.0925277404782925, 0.09681092057969054, 0.0024387761993910928, 0.0006362523366081213,
          0.002397285319415503, 3.708806316742549e-05, 3.241182261730541e-05, 7.02603728415964e-05,
          3.055217999290323e-07, 1.4971745545174467e-07, 1.0462799921811907e-07, 3.7301920467768355e-09,
          0.0006132503603490068, 0.38291753315708943, 0.16595846246817963, 0.05839456600766549, 0.0015170857725900684,
          0.04705702900225938, 0.19240121380060538, 0.05380224595524471, 0.0947200608734918, 0.0014455854677298797,
          1.6025467250444404e-05, 0.001150093353917792, 3.79871181249706e-06, 0.12684042487788988, 0.4386960616863889,
          0.37384289643661556, 0.03559112059483131, 0.01687392665619217, 0.005446926024127138, 0.0004981100600705884,
          0.0006885476216615217, 0.00024472588735186245, 0.00034385536900687086, 0.00017427854113027063,
          0.0002609783046546454, 0.00020145891767547544, 0.007009149784637145, 0.06583714347977757,
          0.009347114629783843, 0.2784371278853948, 0.3753465359885337, 0.003278629101996568, 0.1880297669950602,
          0.026850195545502803, 0.024558402605357472, 0.020456964669345146, 8.601122908581747e-05,
          0.00031977305969936484, 0.00016486583745310042, 0.0006330694176182558, 0.023149218068769618,
          0.0008723725848541108, 0.16989955483211927, 0.4693222676595177, 0.3165697218268577, 0.014788286124997215,
          0.004600665919206655, 0.0001415747001062931, 1.824358628069148e-05, 3.539428424708772e-07,
          4.043628188552783e-06, 1.0290882196016634e-07, 0.05287516727475996, 0.003950089722558507,
          0.000439973807840766, 0.023281713691294833, 0.26440723546709455, 0.11541700737108367, 0.42857959086696956,
          0.04506024829044282, 0.01988452008353957, 0.030790548755606995, 0.005215229838052692, 0.006382044972481915,
          0.0023156945626379814, 0.0056663134571664645, 0.0011041024453005543, 0.00027869368956478184,
          0.002947564773533964, 0.06519071500717367, 0.22701813157522308, 0.32811252384370193, 0.1222635374634502,
          0.22037408505754813, 0.02505323307599481, 0.0011878771031843495, 3.850665838818203e-06, 0.0003321735803711943,
          0.0010074089713668632, 0.0013234549298153655, 0.0005307036538215381, 0.005052091346321681,
          0.058394394144453896, 0.06308389570586548, 0.1967012550571399, 0.02920391123464529, 0.5890833275249996,
          0.02536059123584516, 3.198214189219509e-05, 0.027278723597666373, 0.00122658558949471, 0.00028143574038989107,
          0.0002451840742194157, 0.00014688848796744558, 0.0052889619528649345, 0.006951765986451964,
          0.04529668358875677, 0.027346348663939143, 0.07023923853685475, 0.6348849538003881, 0.024818382912859746,
          0.08741514517279117, 0.05917826773674369, 0.010671730803642726, 1.226075411357677e-05, 0.0001947812556323772,
          7.062544071943166e-06, 0.004310833392134904, 0.02459835194806199, 0.01523269144625445, 0.0066796472715984845,
          0.036917986088197983, 0.05373345157562759, 0.007182930298662564, 0.413507036775115, 0.1911842484711268,
          0.214915944852732, 1.2687422679639245e-05, 0.00031615927697333196, 4.66327709336984e-05,
          0.00020285752814749896, 0.0007917095659668113, 0.009091282595273859, 0.0160087948498544, 0.036130683441358974,
          0.01755584287289416, 0.04045508017040653, 0.034510588545362174, 0.6354701856252499, 0.11472942044652616,
          2.0404408030059534e-07, 3.863796778880026e-05, 6.222446051313489e-08, 4.721342714241102e-05,
          0.0001290720374837413, 0.0066611261963895755, 0.03197700194240687, 5.482055093099462e-05, 0.02927456392036446,
          7.446031033568724e-05, 0.019358500860924235, 0.32180546028592844, 0.22016226669985398, 4.430488489989916e-08,
          4.028760717395752e-07, 1.1141184376536838e-06, 0.0002555568714914853, 0.000410319885093294,
          0.005810370872699786, 0.016169880425560394, 0.00010223113688615232, 0.001368114444039984,
          2.0155274949096825e-05, 0.3061939204883475, 0.0067802053535521165, 0.07397915577097482]

    #print(len(dd))
    #print(dd)
    #dd[0] = [0.07] * 182
    #print(dd[0])
    demands = dict(zip(list_of_tuples, dd))
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
    print("set of list: ", set(templist))
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