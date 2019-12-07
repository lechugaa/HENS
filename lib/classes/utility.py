# Utility Class
# A utility in the problems of interest is defined by:
# 1. An inlet temperature Tin
# 2. An outlet temperature Tout
# 3. A unitary cost per unit of heat
from process_stream import Process_Stream

class Utility(Process_Stream):


    def __init__(self, Tin, Tout, cost):
        Process_Stream.__init__(self, Tin, Tout)
        self.cost = cost


    def __str__(self):
        return "Tin: {}, Tout: {}, Cost: {}".format(self.Tin, self.Tout, self.cost)
