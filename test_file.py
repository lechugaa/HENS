# This file tests the implementation of the classes
from lib.classes.stream import Stream
from lib.classes.utility import Utility
from lib.classes.minimum_utility_problem import Min_Utility_Problem
from lib.solvers.min_utility_solver import solve_min_utility_instace
from lib.solvers.transshipment_solver import solve_transshipment_model
from lib.solvers.transport_solver import solve_transport_model
from lib.classes.network import Network


if __name__ == '__main__':

    problems = ["balanced5", "balanced8", "balanced10", "balanced12", "balanced15"]
    problems += ["unbalanced5", "unbalanced10", "unbalanced15", "unbalanced17", "unbalanced20"]

    problem = "balanced5"
    
    minup = Min_Utility_Problem.generate_from_data(problem)
    (sigma_HU, delta_HU) = solve_min_utility_instace(minup)
    network = Network(minup, sigma_HU, delta_HU)
    solve_transport_model(network)
    