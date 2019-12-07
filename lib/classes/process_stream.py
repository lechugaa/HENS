# Process Stream Class
# A process stream in the problems of interest is defined by:
# 1. An inlet temperature Tin
# 2. An outlet temperature Tout
from temperature_interval import Temperature_Interval

class Process_Stream:


    def __init__(self, Tin, Tout):
        self.Tin = Tin
        self.Tout = Tout
        self.is_hot = Tin > Tout
        self.interval = Temperature_Interval(Tin, Tout)


    def __str__(self):
        return "Tin: {}, Tout: {}".format(self.Tin, self.Tout)
