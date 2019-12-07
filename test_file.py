# This file tests the implementation of the classes
from lib.classes.stream import Stream
from lib.classes.utility import Utility
from lib.classes.minimum_utility_problem import Min_Utility_Problem


# Auxiliary method to pretty print a two-dimensional list
def print_2d_list(table):
    print('\n'.join([''.join(['{:10}'.format(item) for item in row]) for row in table]))


if __name__ == '__main__':

    # Test example taken from "Chen, Grossmann, Miller. Computers and Chemical Engineering 82, p. 68-83, 2015".
    DTmin = 10.0
    # HS0 = Stream(400.0, 120.0, 1.0)
    # HS1 = Stream(340.0, 120.0, 2.0)
    # HS2 = Stream(380.0, 150.0, 1.5)
    # HS3 = Stream(300.0, 100.0, 2.5)
    # HS4 = Stream(420.0, 160.0, 1.7)
    # CS0 = Stream(160.0, 400.0, 1.5)
    # CS1 = Stream(100.0, 250.0, 1.3)
    # CS2 = Stream(50.0, 300.0, 2.5)
    # CS3 = Stream(200.0, 380.0, 2.8)
    # CS4 = Stream(150.0, 450.0, 1.9)
    # HU0 = Utility(500.0, 499.0, 80.0)
    # HU1 = Utility(350.0, 349.0, 50.0)
    # CU0 = Utility(20.0, 21.0, 20.0)
    # streams = [HS0, HS1, HS2, HS3, HS4, CS0, CS1, CS2, CS3, CS4]
    # utilities = [HU0, HU1, CU0]

    CS1 = Stream(120, 235, 2)
    CS2 = Stream(180, 240, 4)
    HS1 = Stream(260, 160, 3)
    HS2 = Stream(250, 130, 1.5)
    streams = [CS1, CS2, HS1, HS2]
    utilities = []

    chen_utility_problem = Min_Utility_Problem(streams, utilities, DTmin)
    print(chen_utility_problem)
    for interval in chen_utility_problem.intervals:
        print(interval)    
    print("--------------------------Deltas-------------------------------")
    print_2d_list(chen_utility_problem.deltas)
    print("--------------------------Sigmas-------------------------------")
    print_2d_list(chen_utility_problem.sigmas)
