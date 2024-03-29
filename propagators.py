# =============================
# Student Names:  Panfilov Alex, Shum Amanda and Deschatrette Margaux
# Group ID: 26
# Date: 02/02/2024
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation : check fully instantiated constraints with 
    a variable V if NewVar is not None, do nothing otherwise.  

    Args:
        csp: A CSP object which contains the variables and constraints of the problem
        newVar (optional) : A newly instantiated variable of class Variable. Default to None.

    Returns:
        bool: False if a constraint is not satisfied; True otherwise or if newVar is None 
        list : an empty list [], as nothing has been pruned by the propagator 
    '''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Check constraints that have exactly one remaining unassigned variable 
    in their scope and remove variable domain values that are not legal in the constraint. 
    Search all unary constraints if newVar is None or search only the constraints involving
    newVar if newVar is given.

    Args:
        csp : A CSP object which contains the variables and constraints of the problem
        newVar (optional): A newly instantiated variable of class Variable. Default to None. 
            If not None, newVar is the most recently assigned variable of the search. 

    Returns:
        bool : False if a dead-end is found, True if we can continue
        pruned_list (list): a list of variable, values tuples that have been pruned by the
            FC propagator 
    '''

    # A list of (Variable, value) tuples pruned by FC  
    pruned_list = []
    
  
    # If newVar is given, only get constraints involving this newVar
    # If None as in default, get all constraints
    t_cons_list = csp.get_cons_with_var(newVar) if newVar else csp.get_all_cons()

    # update, only choose the constrainsts with 1 unassigned var
    cons_list = [c for c in t_cons_list if c.get_n_unasgn() == 1]

 
    for c in cons_list:
        
        # --if only 1 var in constraint c's scope is unassigned
        var_list = c.get_unasgn_vars()

        # only select the constraints with ONLY one unassigned var
        last_var = var_list[0]
    
        # check constraints with the domain values of 'this' variable
        for d_val in last_var.cur_domain():  
            
            # temporarily assign value to this variable (will unassign ....)
            last_var.assign(d_val)
            
            # get the assigned values from constraint after newly assigning a variable
            vals = [v.get_assigned_value() for v in c.get_scope()]

            # check the constraint with its scope values.
            # if not consistent/legal, remove it from its current domain.
            # Also, add to the pruned list as a tuple to be returned 
            if not c.check(vals):
                pair = (last_var, d_val)
                if (pair not in pruned_list):
                    last_var.prune_value(d_val) # remove from variable's domain
                    pruned_list.append(pair)    # add to the to be returned list

            # unassign after testing
            last_var.unassign()
                
            # if this variable has no more domain values, return false to be backtracked
            if last_var.cur_domain_size() == 0:  
                return False, pruned_list

    return True, pruned_list



def prop_GAC(csp, newVar=None):
    '''Do a Generalized Arc Consistency (GAC) propagation. If newVar is None, initialize
    the GAC queue with all constraints of the csp. 
    If newVar is True, initialize the GAC queue with all constraints containing V.

    Args:
        csp: A CSP object which contains the variables and constraints of the problem
        newVar (optional): A newly instantiated variable of class Variable. 
            If not None, newVar is the most recently assigned variable of the search. 

    Returns:
        bool: False if a dead-end is found, True if we can continue
        pruned_list (list): a list of variable, values tuples that have been pruned by the
            GAC propagator 
    '''
    
    pruned_list = []    # function returned list with pruned tuple(s), (var, val)
    arc_queue = []      # stores the hyper-arcs (constraints) to be processed, until empty
    
    # If newVar is given, only get constraints (hyper-arcs) involving this newVar
    # If None as in default, get all constraints (hyper-arcs)
    arc_queue = csp.get_cons_with_var(newVar) if newVar else csp.get_all_cons()
    
    # checking contraints continues if queue is NOT empty
    while len(arc_queue) != 0:
        
        arc = arc_queue.pop(0)  # constraint is hyper-arc

        arc_scope = arc.get_scope() # constraint variables

        # check every variable is consistent with  other variables in the constraint (hyper-arc)
        for v in arc_scope:

            for d in v.cur_domain():

                # prune if (v,d) pair does not satisfy the constraint
                if not arc.has_support(v, d):

                    pair = (v, d)       # prepare the (v,d ) tuple for returned prune list

                    # do not duplicate the prune list
                    # remove the unsatifying value from the varible domain
                    if(pair not in pruned_list):
                        pruned_list.append(pair)
                        v.prune_value(d)        # remove value from variable

                     # deadend reached, returns False to signal backtrack
                    if v.cur_domain_size() == 0:   
                        return False, pruned_list
                    
                    # repeatedly check the constraints associated with the updated variable 
                    for c in csp.get_cons_with_var(v):
                        if (c not in arc_queue):
                            arc_queue.append(c)
    return True, pruned_list    
 
