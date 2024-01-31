# =============================
# Student Names:
# Group ID:
# Date:
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
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

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
    '''
    Check constraints that have exactly one unassigned variable in their scope, 
    Remove variable domain values that are not legal in the constraint. 
    If newVar is None, search  all constraints. 
    If newVar is given, only search  constraints involving newVar

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
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    pass
