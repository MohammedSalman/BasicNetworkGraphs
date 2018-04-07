# Copyright 2014 Dr. Greg M. Bernstein
""" This file shows how to create and solve a LP problem by "hand" with
    Python and the PuLP library. It uses example 2.1 from Pioro and Medhi
    as an example problem.
"""
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus

if __name__ == '__main__':
    prob = LpProblem("P&M Example 2.1", LpMinimize)
    # Define the path flow variables
    x12 = LpVariable("x12", 0)
    x123 = LpVariable("x123", 0)
    x13 = LpVariable("x13", 0)
    x132 = LpVariable("x132", 0)
    x23 = LpVariable("x23", 0)
    x213 = LpVariable("x213", 0)
    # Add objective function to the problem
    #prob += x12 + 2.0*x123 + x13 + 2.0*x132 + x23 + 2.0*x213
    prob += 2.0*x12 + x123 + 2.0*x13 + x132 + 2.0*x23 + x213
    # Add demand constraints
    prob += x12 + x132 == 5.0, "Demand1_2"
    prob += x13 + x123 == 7.0, "Demand1_3"
    prob += x23 + x213 == 8.0, "Demand2_3"
    # Add link capacity constraints
    prob += x12 + x123 + x213 <= 10.0, "Link1_2"
    prob += x13 + x132 + x213 <= 10.0, "Link1_3"
    prob += x23 + x132 + x123 <= 15.0, "Link2_3"
    prob.writeMPS("example2_1.mps")
    prob.writeLP("example2_1.lpt")
    prob.solve()
    print "Status:", LpStatus[prob.status]
    for v in prob.variables():
        print v.name, "=", v.varValue
