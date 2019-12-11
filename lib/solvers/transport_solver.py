# Minimization of Matches Solver via Transport Model
from pyomo.environ import ConcreteModel, Var, NonNegativeReals, RangeSet, Objective, Constraint, SolverFactory, Binary

def solve_transport_model(network):

    # declaring model
    model = ConcreteModel(name = "MIN_MATCHES_TRANSPORT")

    # declaring model inputs
    H = network.H               # hot streams including utilities
    C = network.C               # cold streams including utilities
    T = network.T               # temperature intervals
    sigma = network.sigmas      # heat supply per hot stream per interval
    delta = network.deltas      # heat demand per cold stream per interval
    U = network.U               # Big-M parameter

    # declaring model variables
    model.y = Var(H, C, within = Binary)
    model.q = Var(H, T, C, T, within = NonNegativeReals)

    # declaring model objective
    def matches_min_rule(model):
        return sum(model.y[h, c] for h in H for c in C)
    model.obj = Objective(rule = matches_min_rule)

    # heat balance for supplies
    def supply_balance_constraint(model, h, s):
        return sum(model.q[h, s, c, t] for c in C for t in T) == sigma[h, s]
    model.supply_balance_constraint = Constraint(H, T, rule = supply_balance_constraint)

    # heat balance for demands
    def demand_balance_constraint(model, c, t):
        return sum(model.q[h, s, c, t] for h in H for s in T) == delta[c, t]
    model.demand_balance_constraint = Constraint(C, T, rule = demand_balance_constraint)

    # big-M constraint
    def big_M_rule(model, h, c):
        return sum(model.q[h, s, c, t] for s in T for t in T) <= U[h, c] * model.y[h, c]
    model.big_M_constraint = Constraint(H, C, rule = big_M_rule)

    # zero heat transmition constraint
    def zero_heat_rule(model, h, c, s, t):
        s_index = T.index(s)
        t_index = T.index(t)
        if s_index > t_index:
            return model.q[h, s, c, t] == 0
        else:
            return Constraint.Skip
    model.zero_heat_constraint = Constraint(H, C, T, T, rule = zero_heat_rule)

    # solving model
    solver = SolverFactory("glpk")
    results = solver.solve(model)
    y = [model.y[h, c].value for h in H for c in C]
    print("HS: {}, CS: {}, TI: {}".format(len(H), len(C), len(T)))
    print("Objective: y = {}".format(sum(y)))
    print(results)
    model.y.pprint()


def solve_transport_model_greedy(network):

    # declaring model
    model = ConcreteModel(name = "MIN_MATCHES_TRANSPORT")

    # declaring model inputs
    H = network.H               # hot streams including utilities
    C = network.C               # cold streams including utilities
    T = network.T               # temperature intervals
    sigma = network.sigmas      # heat supply per hot stream per interval
    delta = network.deltas      # heat demand per cold stream per interval
    U = network.U_greedy        # Big-M parameter

    # declaring model variables
    model.y = Var(H, C, within = Binary)
    model.q = Var(H, T, C, T, within = NonNegativeReals)

    # declaring model objective
    def matches_min_rule(model):
        return sum(model.y[h, c] for h in H for c in C)
    model.obj = Objective(rule = matches_min_rule)

    # heat balance for supplies
    def supply_balance_constraint(model, h, s):
        return sum(model.q[h, s, c, t] for c in C for t in T) == sigma[h, s]
    model.supply_balance_constraint = Constraint(H, T, rule = supply_balance_constraint)

    # heat balance for demands
    def demand_balance_constraint(model, c, t):
        return sum(model.q[h, s, c, t] for h in H for s in T) == delta[c, t]
    model.demand_balance_constraint = Constraint(C, T, rule = demand_balance_constraint)

    # big-M constraint
    def big_M_rule(model, h, c):
        return sum(model.q[h, s, c, t] for s in T for t in T) <= U[h, c] * model.y[h, c]
    model.big_M_constraint = Constraint(H, C, rule = big_M_rule)

    # zero heat transmition constraint
    def zero_heat_rule(model, h, c, s, t):
        s_index = T.index(s)
        t_index = T.index(t)
        if s_index > t_index:
            return model.q[h, s, c, t] == 0
        else:
            return Constraint.Skip
    model.zero_heat_constraint = Constraint(H, C, T, T, rule = zero_heat_rule)

    # solving model
    solver = SolverFactory("glpk")
    results = solver.solve(model)
    y = [model.y[h, c].value for h in H for c in C]
    print("HS: {}, CS: {}, TI: {}".format(len(H), len(C), len(T)))
    print("Objective: y = {}".format(sum(y)))
    print(results)
    model.y.pprint()
