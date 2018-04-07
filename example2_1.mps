*SENSE:Minimize
NAME          P&M Example 2.1
ROWS
 N  OBJ
 E  Demand1_2
 E  Demand1_3
 E  Demand2_3
 L  Link1_2
 L  Link1_3
 L  Link2_3
COLUMNS
    x12       Demand1_2   1.000000000000e+00
    x12       Link1_2    1.000000000000e+00
    x12       OBJ        2.000000000000e+00
    x123      Demand1_3   1.000000000000e+00
    x123      Link1_2    1.000000000000e+00
    x123      Link2_3    1.000000000000e+00
    x123      OBJ        1.000000000000e+00
    x13       Demand1_3   1.000000000000e+00
    x13       Link1_3    1.000000000000e+00
    x13       OBJ        2.000000000000e+00
    x132      Demand1_2   1.000000000000e+00
    x132      Link1_3    1.000000000000e+00
    x132      Link2_3    1.000000000000e+00
    x132      OBJ        1.000000000000e+00
    x213      Demand2_3   1.000000000000e+00
    x213      Link1_2    1.000000000000e+00
    x213      Link1_3    1.000000000000e+00
    x213      OBJ        1.000000000000e+00
    x23       Demand2_3   1.000000000000e+00
    x23       Link2_3    1.000000000000e+00
    x23       OBJ        2.000000000000e+00
RHS
    RHS       Demand1_2   5.000000000000e+00
    RHS       Demand1_3   7.000000000000e+00
    RHS       Demand2_3   8.000000000000e+00
    RHS       Link1_2    1.000000000000e+01
    RHS       Link1_3    1.000000000000e+01
    RHS       Link2_3    1.500000000000e+01
BOUNDS
ENDATA
