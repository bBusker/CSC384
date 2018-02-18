'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

from cspbase import *

def binary_ne_grid(kenken_grid):
    size = kenken_grid[0][0]

    dom = []
    for i in range(size):
        dom += [i+1]

    vars = []
    for i in range(size*size):
        vars += [Variable('K{}{}'.format(int(i/size)+1, i%size+1), dom)]

    cons = []
    for i in range(len(vars)):
        for j in range(len(vars)):
            if ((int(i/size) == int(j/size)) or (i%size == j%size)) and (i != j) and (j>i):
                con = Constraint("C(K{}{},K{}{})".format(int(i/size)+1, i%size+1, int(j/size)+1, j%size+1), [vars[i], vars[j]])
                sat_tuples = []
                for k in dom:
                    for l in dom:
                        if k != l:
                            sat_tuples += [(k,l)]
                con.add_satisfying_tuples(sat_tuples)
                cons += [con]

    res = CSP("{}-size_binary_ne_grid".format(size), vars)
    for c in cons:
        res.add_constraint(c)
    return res, vars


def nary_ad_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    pass

def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!
    pass

