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
import itertools

def binary_ne_grid(kenken_grid):
    size = kenken_grid[0][0]

    dom = []
    for i in range(size):
        dom += [i+1]

    vars = []
    for i in range(size):
        t_vars = []
        for j in range(size):
            t_vars += [Variable('K{}{}'.format(i+1, j+1), dom)]
        vars += [t_vars]

    cons = []
    for x1,y1 in itertools.product(range(len(vars)), repeat = 2):
        for x2,y2 in itertools.product(range(len(vars)), repeat = 2):
            if (x1 == x2 or y1 == y2) and (x1,y1) != (x2,y2) and (x1+y1)<(x2+y2):
                con = Constraint("C(K{}{},K{}{})".format(x1+1, y1+1, x2+1, y2+1), [vars[x1][y1], vars[x2][y2]])
                sat_tuples = []
                for k in dom:
                    for l in dom:
                        if k != l:
                            sat_tuples += [(k,l)]
                con.add_satisfying_tuples(sat_tuples)
                cons += [con]


    # for i in range(len(vars)):
    #     for j in range(len(vars)):
    #         if ((int(i/size) == int(j/size)) or (i%size == j%size)) and (i != j) and (j>i):
    #             con = Constraint("C(K{}{},K{}{})".format(int(i/size)+1, i%size+1, int(j/size)+1, j%size+1), [vars[i], vars[j]])
    #             sat_tuples = []
    #             for k in dom:
    #                 for l in dom:
    #                     if k != l:
    #                         sat_tuples += [(k,l)]
    #             con.add_satisfying_tuples(sat_tuples)
    #             cons += [con]

    res = CSP("{}-size_binary_ne_grid".format(size))

    for var_l in vars:
        for var in var_l:
            res.add_var(var)

    for c in cons:
        res.add_constraint(c)

    return res, vars  #TODO: check vars ordering


def nary_ad_grid(kenken_grid):
    size = kenken_grid[0][0]

    dom = []
    for i in range(size):
        dom += [i + 1]

    vars = []
    for i in range(size):
        t_vars = []
        for j in range(size):
            t_vars += [Variable('K{}{}'.format(i+1, j+1), dom)]
        vars += [t_vars]

    cons = []
    for i in range(size):
        con_c = Constraint("C_col{}".format(i),  [row[i] for row in vars])
        sat_tuples = [x for x in itertools.permutations(range(1, size+1), size)]
        con_c.add_satisfying_tuples(sat_tuples)
        cons += [con_c]

        con_r = Constraint("C_row{}".format(i), vars[i])
        sat_tuples = [x for x in itertools.permutations(range(1, size+1), size)]
        con_r.add_satisfying_tuples(sat_tuples)
        cons += [con_r]

    res = CSP("{}-size_nary_ad_grid".format(size))

    for var_l in vars:
        for var in var_l:
            res.add_var(var)

    for c in cons:
        res.add_constraint(c)
    return res, vars



def kenken_csp_model(kenken_grid):
    res, vars = nary_ad_grid(kenken_grid)
    size = kenken_grid[0][0]

    for cage in kenken_grid[1:]:
        cage_vars = []
        if len(cage) == 2:
            v = cage[0]
            cage_vars += [vars[(int(str(v)[0]) - 1)][int(str(v)[1]) - 1]]
            con = Constraint("C_cage{}".format(kenken_grid.index(cage)), cage_vars)
            con.add_satisfying_tuples([[cage[1]]])
            res.add_constraint(con)
            continue

        for v in cage[:-2]:
            cage_vars += [vars[(int(str(v)[0])-1)][int(str(v)[1])-1]]
        con = Constraint("C_cage{}".format(kenken_grid.index(cage)), cage_vars)
        sat_tuples = []
        target = cage[-2]
        num_vars = len(cage[:-2])
        if cage[-1] == 0: # Addition
            for i in itertools.product(range(1, size+1), repeat = num_vars):
                if sum(i) == target:
                    sat_tuples += [i]

        elif cage[-1] == 1: # Subtraction
            for i in itertools.product(range(1, size+1), repeat = num_vars):
                if functools.reduce(lambda x, y: x-y, i) == target:
                    for j in itertools.permutations(i):
                        if j not in sat_tuples:
                            sat_tuples += [j]
                
        elif cage[-1] == 2: # Division
            for i in itertools.product(range(1, size+1), repeat = num_vars):
                if functools.reduce(lambda x, y: int(x/y), i) == target:
                    for j in itertools.permutations(i):
                        if j not in sat_tuples:
                            sat_tuples += [j]

        elif cage[-1] == 3: # Multiplication
            for i in itertools.product(range(1, size+1), repeat = num_vars):
                if functools.reduce(lambda x, y: x*y, i) == target:
                    sat_tuples += [i]

        con.add_satisfying_tuples(sat_tuples)
        res.add_constraint(con)

    return res, vars