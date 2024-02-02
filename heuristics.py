# =============================
# Student Names: Panfilov Alex, Shum Amanda and Deschatrette Margaux
# Group ID: 26
# Date: 01/02/2024
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' Choose the next variable to be assigned for the propagator according to the 
        Degree Heuristic (DH), i.e. the variable involved in the largest number of 
        constraints and which have other unassigned variables

    Args:
        csp: A CSP object

    Returns:
        chosen_var: the next unassigned variable to be assigned with the largest 
        number of constraints
    '''
    # IMPLEMENT
    # find variable with highest number of contraints, which have other unassigned variables
    
    # get all unassigned variables
    unasgn_vars = csp.get_all_unasgn_vars()

    # get all constraint counts for each unassigned variable
    num_constraints = []
    for var in unasgn_vars:
        cons_list = csp.get_cons_with_var(var)
        # make sure constrain has other unassigned variables
        count = 0
        for con in cons_list:
            if con.get_n_unasgn() > 1:
                count += 1

        # add amount of valid constraints to list
        num_constraints.append(count)

    # find the unassigned variable with the largest number of constraints
    # which have other unassigned variables
    max_degree = max(num_constraints)
    index = num_constraints.index(max_degree)
    chosen_var = unasgn_vars[index]
    return chosen_var

def ord_mrv(csp):
    ''' Choose the next variable to be assigned for the propagator according to the 
        Minimum Remaining Values heuristic (MRV), i.e. the variable with the most 
        constrained current domain

    Args:
        csp: A CSP object

    Returns:
        chosen_var: The next unassigned variable from class Variable to be assigned with the 
        fewest legal values remaining
    '''
    # IMPLEMENT
    # get all unassigned variables
    unasgn_vars = csp.get_all_unasgn_vars()

    # get all domain sizes, find the one with smallest domain
    domain_sizes = []
    for var in unasgn_vars:
        domain_sizes.append(var.cur_domain_size())

    # find the unassigned variable with the fewest legal values remaining
    min_size = min(domain_sizes)
    index = domain_sizes.index(min_size)
    chosen_var = unasgn_vars[index]
    return chosen_var
