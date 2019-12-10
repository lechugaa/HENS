# Process Stream Class
# A process stream in the problems of interest is defined by:
# 1. An inlet temperature Tin
# 2. An outlet temperature Tout
from temperature_interval import Temperature_Interval

class Process_Stream:

    # Static Variable
    hot_stream_id = 0
    cold_stream_id = 0


    def __init__(self, Tin, Tout):
        self.Tin = Tin
        self.Tout = Tout
        self.is_hot = Tin > Tout
        self.interval = Temperature_Interval(Tin, Tout)
        self.__set_id()

    
    def __set_id(self):
        if self.is_hot:
            self.id = "H{}".format(Process_Stream.hot_stream_id)
            Process_Stream.hot_stream_id += 1
        else:
            self.id = "C{}".format(Process_Stream.cold_stream_id)
            Process_Stream.cold_stream_id += 1


    def __str__(self):
        return self.id

    
    def __repr__(self):
        return self.id
