# Minimization of Utility Solver
from pyomo.environ import ConcreteModel, Var, NonNegativeReals, RangeSet, Objective, Constraint, SolverFactory

def solve_min_uility_instace(problem_instance):

    # declaring model
    model = ConcreteModel(name = "MIN_UTILITY") # declaring concrete model

    # declaring model inputs
    HS = problem_instance.HS
    CS = problem_instance.CS
    HU = problem_instance.HU
    CU = problem_instance.CU
    TI = problem_instance.intervals
    sigma_HS = problem_instance.sigmas
    delta_CS = problem_instance.deltas
    accepted_HU_sigmas = problem_instance.accepted_hu_sigmas
    accepted_CU_deltas = problem_instance.accepted_cu_deltas
    k_HU = {}
    for hot_utility in HU:
        k_HU[hot_utility] = hot_utility.cost
    k_CU = {}
    for cold_utility in CU:
        k_CU[cold_utility] = cold_utility.cost   

    # declaring model variables
    model.cost = Var(within = NonNegativeReals)
    model.sigma_HU = Var(HU, TI, within = NonNegativeReals)
    model.delta_CU = Var(CU, TI, within = NonNegativeReals)
    model.Rset = RangeSet(0, len(TI))
    model.R = Var(model.Rset, within = NonNegativeReals)
    last_R = len(TI)

    # defining model cost computation
    def utility_cost_rule(model):
        HU_cost = sum(k_HU[hu] * model.sigma_HU[hu, ti] for hu in HU for ti in TI)
        CU_cost = sum(k_CU[cu] * model.delta_CU[cu, ti] for cu in CU for ti in TI)
        return  model.cost == HU_cost + CU_cost
    model.utility_cost_constraint = Constraint(rule = utility_cost_rule)

    # defining model objective
    def cost_min_rule(model):
        return  model.cost
    model.obj = Objective(rule = cost_min_rule)

    # heat balance restriction
    def heat_balance_rule(model, t_interval):
        interval_index = TI.index(t_interval) + 1
        entering_energy = sum(sigma_HS[hs, t_interval] for hs in HS) + sum(model.sigma_HU[hu, t_interval] for hu in HU) + model.R[interval_index - 1]
        exiting_energy = sum(delta_CS[cs, t_interval] for cs in CS) + sum(model.delta_CU[cu, t_interval] for cu in CU) + model.R[interval_index]
        return entering_energy == exiting_energy
    model.heat_balance_contraint = Constraint(TI, rule = heat_balance_rule) 

    # residual heat entering the first temperature interval and the one exiting the last temperature interval must be zero
    def r_zero_rule(model, r):
        if (r == 0) or (r == last_R):
            return model.R[r] == 0
        else:
            return Constraint.Skip
    model.r_zero_constraint = Constraint(model.Rset, rule = r_zero_rule)

    # forbidden heat exchanges for hot utilities
    def forbidden_hu_intervals(model, hu, ti):
        if accepted_HU_sigmas[hu, ti]:
            return Constraint.Skip
        else:
            return model.sigma_HU[hu, ti] == 0
    model.forbidden_hu_intervals_constraint = Constraint(HU, TI, rule = forbidden_hu_intervals)

    # forbidden heat exchanges for cold utilities
    def forbidden_cu_intervals(model, cu, ti):
        if accepted_CU_deltas[cu, ti]:
            return Constraint.Skip
        else:
            return model.delta_CU[cu, ti] == 0
    model.forbidden_cu_intervals_constraint = Constraint(CU, TI, rule = forbidden_cu_intervals)

    # solving model
    solver = SolverFactory("glpk")
    solver.solve(model)
    model.cost.pprint()
    model.R.pprint()
