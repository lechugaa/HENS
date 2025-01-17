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
        self.accepted_hu_sigmas = {}
        self.accepted_cu_deltas = {}
        self.DTmin = DTmin
        self.__init_streams(streams)
        self.__init_utilities(utilities)
        self.__init_temperatures(streams, utilities)
        self.__init_heats()
        self.__init_accepted_u_intervals()


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
            if not process_stream.is_hot:
                Tin += self.DTmin
            if Tin not in self.temperatures:
                self.temperatures.append(Tin)
            
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
                    self.sigmas[(hot_stream, interval)] = Temperature_Interval.common_interval(interval, hot_stream.interval).DT * hot_stream.FCp
                else:
                    self.sigmas[(hot_stream, interval)] = 0

            # initializing deltas. This one is tricky because intervals were constructed 
            # by adding DTmin to each CS interval, but CS intervals were nos modified    
            for cold_stream in self.CS:
                if cold_stream.interval.shifted(self.DTmin).passes_through_interval(interval):
                    self.deltas[(cold_stream, interval)] = Temperature_Interval.common_interval(interval, cold_stream.interval.shifted(self.DTmin)).DT * cold_stream.FCp
                else:
                    self.deltas[(cold_stream, interval)] = 0

    def __init_accepted_u_intervals(self):
        for interval in self.intervals:
            
            # accepted sigmas
            for hot_utility in self.HU:
                if hot_utility.interval.passes_through_interval(interval):
                    self.accepted_hu_sigmas[(hot_utility, interval)] = True
                else:
                    self.accepted_hu_sigmas[(hot_utility, interval)] = False

            # accepted deltas
            for cold_utility in self.CU:
                if cold_utility.interval.shifted(self.DTmin).passes_through_interval(interval):
                    self.accepted_cu_deltas[(cold_utility, interval)] = True
                else:
                    self.accepted_cu_deltas[(cold_utility, interval)] = False


    def __str__(self):
        return "HS: {} \nCS: {}\nHU: {}\nCU: {}\nDTmin: {}".format(
            len(self.HS), len(self.CS), 
            len(self.HU), len(self.CU), 
            self.DTmin)

    
    def __repr__(self):
        return self.__str__()


    @staticmethod
    def generate_from_data(data_id):
        
        path = 'data/original_problems/' + data_id + '.dat'
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        
        elements = [line.split() for line in lines]
        DTmin = float(elements[3][1])
        elements = elements[4:]
        streams = [Stream(Tin = float(e[1]), Tout = float(e[2]), FCp = float(e[3])) for e in elements if e[0][1]!='U']
        utilities = [Utility(Tin = float(e[1]),Tout = float(e[2]), cost = float(e[3])) for e in elements if e[0][1]=='U']

        return Min_Utility_Problem(streams, utilities, DTmin)