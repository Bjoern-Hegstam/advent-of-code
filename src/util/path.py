from heapq import heappop, heappush


def path(previous, s):
    """Return a list of states that lead to state s, according to the previous dict."""
    return [] if (s is None) else path(previous, previous[s]) + [s]


def a_star_search(initial_state, h_fun, move_fun):
    # A* by Peter Norvig from https://nbviewer.jupyter.org/url/norvig.com/ipython/Advent%20of%20Code.ipynb
    frontier = [(h_fun(initial_state), initial_state)]  # Priority queue of (f = g + h, State)
    previous = {initial_state: None}  # From which state did we get to the state
    path_cost = {initial_state: 0}  # Cost of best path to a state

    while frontier:
        (f, current_state) = heappop(frontier)

        if h_fun(current_state) == 0:
            return path(previous, current_state)

        for neighbor in move_fun(current_state):
            new_cost = path_cost[current_state] + 1
            if neighbor not in path_cost or new_cost < path_cost[neighbor]:
                heappush(frontier, (new_cost + h_fun(neighbor), neighbor))
                path_cost[neighbor] = new_cost
                previous[neighbor] = current_state

    return dict(fail=True, front=len(frontier), prev=len(previous))
