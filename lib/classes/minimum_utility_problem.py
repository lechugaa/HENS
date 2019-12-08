# Minimum Utility Problem Class
# It encapsulates all the necessary elements of a minimum utility cost problem
# This class is defined by:
# 1. A set of strems
# 3. A set of utilities
# 5. A minimum aproach heat
from process_stream import Process_Stream
from temperature_interval import Temperature_Interval
from stream import Stream
from utility import Utility

class Min_Utility_Problem:


    def __init__(self, streams, utilities, DTmin):
        self.HS = []
        self.CS = []
        self.HU = []
        self.CU = []
        self.temperatures = []
        self.intervals = []
        self.sigmas = {}
        self.deltas = {}
        self.DTmin = DTmin
        self.__init_streams(streams)
        self.__init_utilities(utilities)
        self.__init_temperatures(streams, utilities)
        self.__init_heats()


    def __init_streams(self, streams):
        """
        This method helps in the initialization of the streams.
        It receives a set of streams and initializes the hot 
        and cold streams lists.
        """
        for stream in streams:
            if stream.is_hot:
                self.HS.append(stream)
            else:
                self.CS.append(stream)


    def __init_utilities(self, utilities):
        """
        This method helps in the initialization of the utilities.
        It receives a set of streams and initializes the hot and 
        cold streams lists.
        """
        for utility in utilities:
            if utility.is_hot:
                self.HU.append(utility)
            else:
                self.CU.append(utility)

    
    def __init_temperatures(self, streams, utilities):
        """
        This method intialized a list of unique temperature
        values affected by DTmin.
        """
        process_streams = streams + utilities
        for process_stream in process_streams:
            Tin = process_stream.Tin
            Tout = process_stream.Tout
            if not process_stream.is_hot:
                Tin += self.DTmin
                Tout += self.DTmin
            
            if Tin not in self.temperatures:
                self.temperatures.append(Tin)
            if Tout not in self.temperatures:
                self.temperatures.append(Tout)
        self.temperatures.sort(reverse = True)

        # creating intervals
        for i in range(len(self.temperatures) - 1):
            new_interval = Temperature_Interval(self.temperatures[i], self.temperatures[i + 1])
            self.intervals.append(new_interval)


    def __init_heats(self):
        for interval in self.intervals:

            # initializing sigmas
            for hot_stream in self.HS:
                if hot_stream.interval.passes_through_interval(interval):
                    self.sigmas[(hot_stream, interval)] = interval.DT * hot_stream.FCp
                else:
                    self.sigmas[(hot_stream, interval)] = 0

            # initializing deltas. This one is tricky because intervals were constructed 
            # by adding DTmin to each CS interval, but CS intervals were nos modified    
            for cold_stream in self.CS:
                if cold_stream.interval.shifted(self.DTmin).passes_through_interval(interval):
                    self.deltas[(cold_stream, interval)] = interval.DT * cold_stream.FCp
                else:
                    self.deltas[(cold_stream, interval)] = 0
                
  
    def __str__(self):
        return "HS: {} \nCS: {}\nHU: {}\nCU: {}\nDTmin: {}".format(
            len(self.HS), len(self.CS), 
            len(self.HU), len(self.CU), 
            self.DTmin)

    
    def __repr__(self):
        return self.__str__()
