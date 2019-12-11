# Greedy Minmax Delta
"""
Greedy proposed algorithm:

It selects matches between hot stream "h" and cold stream "c"
iteratively util it ends up with a feasible set of M matches
exchanging sum(hi) units of heat. 

In each iteration, the heuristic (given a feasible heat exchange qmax)
chooses a match that minimizes max(hi - qmax, ci - qmax).
"""

def greedy_minmax_delta(network):
    pass
    # TODO


def max_heat(network, h, c):
    T = network.T
    sigma = network.sigmas
    delta = network.deltas

    q = {}      # dictionary of (hot_stream, t_interval, cold_stream, t_interval): double 
    R = {}      # dictionary of t_interval: double
    
    for u in range(len(T) - 1): # first and last residual heat must be zero
        t_intervals = T[:u]
        R[T[u]] = sum(sigma[h, u] for u in t_intervals) - sum(delta[c, u] for u in t_intervals)
    
    for u in T:
        q[h, u, c, u] = min(sigma[h, u], delta[c, u])
        sigma[h, u] -= q[h, u, c, u]
        delta[c, u] -= q[h, u, c, u]
    
    for s in range(len(T) - 1):
        for t in range(s + 1, len(T)):
            iteration_intervals = T[s:t] # revisar
            q[h, T[s], c, T[t]] = min(sigma[h, T[s]], delta[c, T[t]], min(R[interval] for interval in iteration_intervals))
            sigma[h, T[s]] -= q[h, T[s], c, T[t]]
            delta[c,T[t]] -= q[h, T[s], c, T[t]]
            for u in range(s, len(T) - 1):
                R[T[u]] -= q[h, T[s], c, T[t]]

    return q
