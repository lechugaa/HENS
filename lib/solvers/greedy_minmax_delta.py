# Greedy Min Delta
"""
Greedy proposed algorithm:

It selects matches between hot stream "h" and cold stream "c"
iteratively util it ends up with a feasible set of M matches
exchanging sum(hi) units of heat. 

In each iteration, the heuristic (given a feasible heat exchange qmax)
chooses a match that minimizes max(hi - qmax, ci - qmax).
"""
import sys
from time import time

def greedy_min_delta(network):
    
    H = network.H
    C = network.C
    T = network.T
    sigma = network.sigmas
    delta = network.deltas
    heats = network.heats
    demands = network.demands

    M = []
    q = {}
    total_heat = sum(heats[hot_stream] for hot_stream in H)
    total_demand = sum(demands[cold_stream] for cold_stream in C)

    # termination criterion
    remaining_heat = total_heat + total_demand

    # Tolerance
    tolerance = 10**(-7)

    # Starting time
    starting_time = time()

    while remaining_heat > tolerance:

        matched_hs = None
        matched_cs = None
        matched_q = {}
        matched_heat = 0

        minimum_delta = float(sys.maxint)

        for h in H:
            for c in C:
                if (h, c) not in M:
                    (iteration_heat, iteration_q) = max_heat(network, h, c)
                    iteration_delta = max(heats[h] - iteration_heat, demands[c] - iteration_heat)

                    if minimum_delta - iteration_delta > tolerance:
                        matched_hs = h
                        matched_cs = c
                        matched_q = iteration_q
                        matched_heat = 0

        M.append((matched_hs, matched_cs))

        for s in T:
            for t in T:
                q[matched_hs, s, matched_cs, t] = matched_q[matched_hs, s, matched_cs, t]
                heats[matched_hs] -= matched_q[matched_hs, s, matched_cs, t]
                demands[matched_cs] -= matched_q[matched_hs, s, matched_cs, t]

        total_heat = sum(heats[hot_stream] for hot_stream in H)
        total_demand = sum(demands[cold_stream] for cold_stream in C)
        remaining_heat = total_heat + total_demand

        # ending time
        ending_time = time()
        elapsed_time = round(ending_time - starting_time, 3)
        print(len(M))
        print(elapsed_time)



def max_heat(network, h, c):
    T = network.T
    sigma = network.sigmas
    delta = network.deltas

    q = {}      # dictionary of (hot_stream, t_interval, cold_stream, t_interval): double 
    R = {}      # dictionary of t_interval: double
    total_heat = 0
    
    for u in range(len(T) - 1): # first and last residual heat must be zero
        t_intervals = T[:u]
        R[T[u]] = sum(sigma[h, u] for u in t_intervals) - sum(delta[c, u] for u in t_intervals)
    
    for u in T:
        q[h, u, c, u] = min(sigma[h, u], delta[c, u])
        sigma[h, u] -= q[h, u, c, u]
        delta[c, u] -= q[h, u, c, u]
        total_heat += q[h, u, c, u]
    
    for s in range(len(T) - 1):
        for t in range(s + 1, len(T)):
            iteration_intervals = T[s:t] # revisar
            q[h, T[s], c, T[t]] = min(sigma[h, T[s]], delta[c, T[t]], min(R[interval] for interval in iteration_intervals))
            sigma[h, T[s]] -= q[h, T[s], c, T[t]]
            delta[c,T[t]] -= q[h, T[s], c, T[t]]
            for u in range(s, len(T) - 1):
                R[T[u]] -= q[h, T[s], c, T[t]]
            total_heat += q[h, T[s], c, T[t]]

    return (total_heat, q)
