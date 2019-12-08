# This file tests the implementation of the classes
from lib.classes.stream import Stream
from lib.classes.utility import Utility
from lib.classes.minimum_utility_problem import Min_Utility_Problem
from pyomo.environ import ConcreteModel, Var, NonNegativeReals, RangeSet, Objective, Constraint, SolverFactory


if __name__ == '__main__':

    # Test example taken from "Chen, Grossmann, Miller. Computers and Chemical Engineering 82, p. 68-83, 2015".
    DTmin = 10.0
    HS0 = Stream(400.0, 120.0, 1.0)
    HS1 = Stream(340.0, 120.0, 2.0)
    HS2 = Stream(380.0, 150.0, 1.5)
    HS3 = Stream(300.0, 100.0, 2.5)
    HS4 = Stream(420.0, 160.0, 1.7)
    CS0 = Stream(160.0, 400.0, 1.5)
    CS1 = Stream(100.0, 250.0, 1.3)
    CS2 = Stream(50.0, 300.0, 2.5)
    CS3 = Stream(200.0, 380.0, 2.8)
    CS4 = Stream(150.0, 450.0, 1.9)
    HU0 = Utility(500.0, 499.0, 80.0)
    HU1 = Utility(350.0, 349.0, 50.0)
    CU0 = Utility(20.0, 21.0, 20.0)
    streams = [HS0, HS1, HS2, HS3, HS4, CS0, CS1, CS2, CS3, CS4]
    utilities = [HU0, HU1, CU0]

    minup = Min_Utility_Problem(streams, utilities, DTmin)
    for interval in minup.intervals:
        print(interval)

    #############################Pyomo Model################################

    # declaring model
    model = ConcreteModel(name = "MIN_UTILITY") # declaring concrete model

    # declaring model inputs
    HS = minup.HS
    CS = minup.CS
    HU = minup.HU
    CU = minup.CU
    TI = minup.intervals
    sigma_HS = minup.sigmas
    delta_CS = minup.deltas
    accepted_HU_sigmas = minup.accepted_hu_sigmas
    accepted_CU_deltas = minup.accepted_cu_deltas
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