# This file tests the implementation of the classes
from lib.classes.stream import Stream
from lib.classes.utility import Utility
from lib.classes.minimum_utility_problem import Min_Utility_Problem
from lib.solvers.min_utility_solver import solve_min_uility_instace
from lib.classes.network import Network
from pyomo.environ import ConcreteModel, Var, NonNegativeReals, RangeSet, Objective, Constraint, SolverFactory, Binary


if __name__ == '__main__':

    # problems = ["balanced5", "balanced8", "balanced10", "balanced12", "balanced15"]
    # problems += ["unbalanced5", "unbalanced10", "unbalanced15", "unbalanced17", "unbalanced20"]
    
    minup = Min_Utility_Problem.generate_from_data("balanced5")
    (sigma_HU, delta_HU) = solve_min_uility_instace(minup)
    network = Network(minup, sigma_HU, delta_HU)
    
    # declaring model
    model = ConcreteModel(name = "MIN_MATCHES_TRANSSHIPMENT")

    # declaring model inputs
    H = network.H               # hot streams including utilities
    C = network.C               # cold streams including utilities
    T = network.T               # temperature intervals
    sigma = network.sigmas      # heat supply per hot stream per interval
    delta = network.deltas      # heat demand per cold stream per interval
    U = network.U               # Big-M parameter

    # declaring model variables
    model.q = Var(H, C, T, within = NonNegativeReals)
    model.y = Var(H, C, within = Binary)
    model.rset = RangeSet(0, len(T))
    model.R = Var(H, model.rset, within = NonNegativeReals)
    last_R = len(T)

    # model objective
    def matches_min_rule(model):
        return sum(model.y[h, c] for h in H for c in C)
    model.obj = Objective(rule = matches_min_rule)

    # heat conservation
    def heat_conservation_rule(model, h, t):
        interval_index = T.index(t) + 1
        exiting_heat = sum(model.q[h, c, t] for c in C) + model.R[h, interval_index]
        entering_heat = sigma[h, t] + model.R[h, interval_index - 1]
        return exiting_heat == entering_heat
    model.heat_conservation_constraint = Constraint(H, T, rule = heat_conservation_rule)

    # zero residual constraint
    def zero_residual_rule(model, h, r):
        if (r == 0) or (r == last_R):
            return model.R[h, r] == 0
        else:
            return Constraint.Skip
    model.zero_residual_constraint = Constraint(H, model.rset, rule = zero_residual_rule)

    # heat demand satisfaction
    def heat_demand_rule(model, c, t):
        return sum(model.q[h, c, t] for h in H) == delta[c, t]
    model.demand_satisfaction_constraint = Constraint(C, T, rule = heat_demand_rule)

    # big-M restriction
    def big_M_rule(model, h, c):
        return sum(model.q[h, c, t] for t in T) <= U[h, c] * model.y[h, c]
    model.big_m_constraint = Constraint(H, C, rule = big_M_rule)

    # solving model
    solver = SolverFactory("glpk")
    solver.solve(model)
    model.y.pprint()
