'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy
import numpy as np
import itertools

def ord_dh(csp):
    vars = csp.get_all_unasgn_vars()
    count = np.zeros(len(vars))

    for var in vars:
        for constraint in csp.get_cons_with_var(var):
            cons = constraint.get_scope()
            for varr in cons:
                if varr in vars:
                    count[vars.index(varr)] += 1

    res = vars[np.argmax(count)]

    return res

def ord_mrv(csp):
    min_len = 9999
    res = csp.vars[0]
    for var in csp.vars:
        if len(var.curdom)<min_len and var.assignedValue == None:
            res = var
            min_len = len(var.curdom)
    return res

def val_lcv(csp, var):

    res_dict = {}
    unassigned = csp.get_all_unasgn_vars()
    if var in unassigned:
        unassigned.remove(var)

    # for vvar in unassigned:
    #     count_prev += vvar.cur_domain_size()

    constraints = csp.get_cons_with_var(var)
    for val in var.cur_domain():
        count_val = 0
        var.assign(val)
        for constraint in constraints:
            for vvar in unassigned:
                for vval in vvar.cur_domain():
                    if constraint.has_support(vvar,vval):
                        count_val += 1
        var.unassign()
        res_dict[val] = count_val

    res = sorted(res_dict, key=res_dict.get, reverse=True)
    return res
