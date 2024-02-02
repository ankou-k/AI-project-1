# =============================
# Student Names: Panfilov Alex, Shum Amanda and Deschatrette Margaux
# Group ID: 26
# Date: 02/02/2024
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def create_vars(grid_size):
    """Creates a list of all CSP variables including their respective names and domains.

    Arg:
        grid_size (int): the size of the grid
    
    Returns:
        var_array (list): an array containing all the CSP variables. Index 0 represents 
        the top left grid cell, and index (grid_size^2)-1 the bottom left grid cell
    """

    # create domain
    domain = [0]*grid_size
    for i in range(grid_size):
        domain[i] = i+1
    print(domain)

    # create variables
    var_array = [0]*(grid_size*grid_size)

    for i in range(grid_size):
        for j in range(grid_size):
            var_name = f"{i+1},{j+1}"
            new_var = Variable(var_name, domain)
            var_array[i*grid_size+j] = new_var

    # return variables
    return var_array

def binary_ne_grid(cagey_grid):
    """Creates a model of a Cagey grid (without cage constraints) built using 
    only binary not-equal constraints for both the row and column constraints.

    Arg:
        cagey_grid : the size of the grid
    
    Returns:
        binary_csp: A CSP object built on the binary_not_equal constraint 
        var_array (array): an array containing all the CSP Variables objects representing
            the board
    """

    # get grid size
    grid_size = cagey_grid[0]

    # create the variables
    var_array = create_vars(grid_size)

    # create variable domains for satisfying tuples
    varDoms = [0]*2
    domain = [0]*grid_size
    for i in range(grid_size):
        domain[i] = i+1
    varDoms[0] = domain
    varDoms[1] = domain

    # create list of satisfying tuples
    sat_tuples = []
    for t in itertools.product(*varDoms):
        if t[0] != t[1]:
            sat_tuples.append(t)
    print(sat_tuples)

    # create constraints that no 2 items in a row are equal to each other
    # and no 2 items in a column are equal to each other
    cons = []
    for i in range(grid_size):
        for comb in itertools.combinations(range(grid_size), 2):

            # create name and scope of row constraint
            row_name = f"Row{i+1}-{comb[0]+1},{comb[1]+1}"
            row_scope = [var_array[i*grid_size + comb[0]], var_array[i*grid_size + comb[1]]]
            
            # create name and scope of column constraint
            col_name = f"Col{i+1}-{comb[0]+1},{comb[1]+1}"
            col_scope = [var_array[i + comb[0]*grid_size], var_array[i + comb[1]*grid_size]]

            # create row and column constraints and add them to list of contraints
            row_con = Constraint(row_name, row_scope)
            row_con.add_satisfying_tuples(sat_tuples)
            col_con = Constraint(col_name, col_scope)
            col_con.add_satisfying_tuples(sat_tuples)
            cons.append(row_con)
            cons.append(col_con)
    
    # create CSP
    binary_csp = CSP("binary_ne_grid", var_array)
    for c in cons:
        binary_csp.add_constraint(c)
    
    # return csp and variables
    return binary_csp, var_array


def nary_ad_grid(cagey_grid):
    """Creates a model of a Cagey grid (without cage constraints) built 
    using only n-ary all different constraints for both the row and column constraints.

    Arg:
        cagey_grid : the size of the grid
    
    Returns:
        binary_csp: A CSP object built on the n_all_different constraint 
        var_array (array): an array containing all the CSP Variables objects representing
            the board
    """

    # get grid size
    grid_size = cagey_grid[0]

    # create the variables
    var_array = create_vars(grid_size)

    # create variable domains for satisfying tuples
    #potential issue - relative assignment
    varDoms = [0]*grid_size
    domain = [0]*grid_size

    for i in range(grid_size):
        domain[i] = i+1
    
    for i in range(grid_size):
        varDoms[i] = domain

    # create list of satisfying tuples
    sat_tuples = []
    for t in itertools.product(*varDoms):
        valid = True
        for i in range (grid_size):
           if t[i] in t[i+1:grid_size]:
                valid = False
                break
        if valid == True:
            sat_tuples.append(t)
    
    # create constraints : items in a row and a column are different 
    print("sat tuples 2",sat_tuples)
    cons = []

    for i in range(grid_size):
             # create name and scope of row constraint 
            row_name = f"Row{i+1}"
            print("row_name:", row_name)
            col_name = f"Col{i+1}"
            print("col_name:", col_name)
            row_scope2 = []
            col_scope2 = []
            for j in range(grid_size):
                row_scope2.append(var_array[i*grid_size+j])
                col_scope2.append(var_array[i + j*grid_size]) 
            # create row and column constraints and add them to list of contraints
            row_con = Constraint(row_name, row_scope2)
            row_con.add_satisfying_tuples(sat_tuples)
            col_con = Constraint(col_name, col_scope2)
            col_con.add_satisfying_tuples(sat_tuples)
            cons.append(row_con)
            cons.append(col_con)
    
    # create CSP
    nary_csp = CSP("nary_ne_grid", var_array)
    for c in cons:
        nary_csp.add_constraint(c)
    
    # return csp and variables
    return nary_csp, var_array

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT

    pass

create_vars(6)
binary_ne_grid((3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")]))