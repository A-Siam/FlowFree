from utils.formater import formatter
from model.case import case
from algorithm import smart
from utils.paths.modifiers import refresh_connected_terminals


def backtrack(
        initial_state,
        initial_assignments,
        inp,
        order_domain_values,
        assignment_complete,
        get_inferences,
        is_consistant,
        callback,
        get_var):
    connected_terminals = set()
    return _backtrack(initial_state, initial_assignments, inp, order_domain_values, assignment_complete, get_inferences, is_consistant, callback, get_var, connected_terminals)


def _backtrack(
        initial_state,
        assignments: dict,
        inp,
        order_domain_values,
        assignment_complete,
        get_inferences,
        is_consistant,
        callback,
        get_var,
        connected_terminals):
    if assignment_complete(assignments, inp):
        callback(assignments, None, None, None)
        return assignments
    v_tuple = get_var(initial_state, assignments, inp, connected_terminals)
    if v_tuple == case.failure:
        return case.failure
    var, variables_domain = v_tuple
    if var == None:
        return case.failure
    for value in order_domain_values(initial_state, assignments, inp, var, variables_domain):
        callback(assignments, variables_domain, var, value)
        assignments[var] = value
        if is_consistant(initial_state, {var: value},  assignments, inp, connected_terminals):
            connected_terminals = refresh_connected_terminals(
                {var: value}, assignments, connected_terminals, initial_state, inp)
            inferences = get_inferences()
            if inferences != case.failure:
                assignments = {**assignments, **inferences}
            res = _backtrack(
                initial_state,
                assignments,
                inp,
                order_domain_values,
                assignment_complete,
                get_inferences,
                is_consistant,
                callback,
                get_var,
                connected_terminals
            )
            if res != case.failure:
                return res
            if inferences != case.failure:
                for key in inferences:
                    del assignments[key]

        del assignments[var]
    return case.failure
