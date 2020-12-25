from typing import List
from utils.paths.points import get_item_in_coord, is_empty, search_around, is_terminals_connect, get_same_color_neighbors, check_for_good_combinations, get_neighbors_coords
from model.case import case
from utils.paths.path_state import is_surrounding_square_filled,is_good_combination, terminal_with_two_same_color_exist
from random import random, shuffle

def assignment_complete(assignments, inp):
    """
    input:
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
    inp: 2d list of the input

    return weather or not the assignments are complete
    """
    # if len of assignments keys length of inp (rows * columns) - starting points
    # then assignment is complete

    return len(assignments) >= (len(inp) * len(inp[0]))


# changed
def select_unassigned_variable(initial_state, csp, assignments: dict, inp):
    """
    input:
    assignment: a dict contains only the colored points with key (coordinate) values (colors) including the terminals
    inp: 2d list of the input

    return a random coordinate
    """

    # TODO (DONE)
    # initially assignments will be terminals
    # select the last one
    # the first empty place should be returned

    _tmp = []
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if assignments.get((i, j)) == None:
                _tmp.append((i, j))
    rand_index = int(random()*len(_tmp) // 1)

    return _tmp[rand_index]

    # if len(_tmp) != 0:
    #     return _tmp[rand_index]
    # else:
    #     rand_index_1 = int(random() * len(inp) // 1)
    #     rand_index_2 = int(random() * len(inp) // 1)
    #     return (rand_index_1, rand_index_2)

# changed
# ROI TODO: you can use cached values BUT DON'T DO IT B4 YOU TELL THE WHOLE TEAM


def order_domain_values(initial_state,csp, assignments, inp, var):
    """
    return the available values, in the dummy case return all values
    """

    # # remove the totally connected

    terminals = initial_state[0]
    colors = [color.lower() for color in terminals.keys()]
    shuffle(colors)
    return colors


# TODO: study consistency to know the paramters you should pass here
def inference():
    """
    return inferences as list or state.faileur
    """

    return case.failure


def is_consistant(initial_state,current_assignment: dict, assignments: List[dict], inp, csp):
    """
    input:
    current_assignment: the coordinate = value dict 
    assignments: the current assignments w/o current assignmet
    csp: (you violate the constraint be returning true) in dump it is just an array of constrains in dumb it should be just an array with a square case checking 

    return: weather or not assignment is consistant with assignments according to the csp
    """

    # TODO
    # steps
    # - check each constraint in csp they all should result True
    #    if no -> return false, return true otherwise

    # TODO now every constraint is hardcoded this should improved in other backtrack logic
    # NOTE for other is consistant you might use a totally different csp and this
    # is ok

    # if the node already assigned
    # TODO delete
    # if assignments.get(list(current_assignment.keys())[0]) != None:
    #     return False

    current_assignment_color = list(current_assignment.values())[0]
    current_assignment_coord = list(current_assignment.keys())[0]

    # check if already marked point will be in the path

    # Combination check
    good_comb = is_good_combination(current_assignment_coord,assignments,inp)
    if not good_comb :
        return False

    # select
    # for terminals check wheather or not they have more than one similar neighbor
    terminal_with_two_neighbors = terminal_with_two_same_color_exist(initial_state,assignments,inp)
    if terminal_with_two_neighbors :
        return False

    terminal_connected = is_terminals_connect(
        initial_state,current_assignment_color, inp, {**assignments})

    if terminal_connected:
        return False

    # weather or not any point had the same color
    # surrounded_points = get_same_color_neighbors(current_assignment_coord,current_assignment_color,assignments,inp)
    # has_no_same_color_sur = (len(surrounded_points) == 0)
    # if has_no_same_color_sur :
    #     return False

    return True
