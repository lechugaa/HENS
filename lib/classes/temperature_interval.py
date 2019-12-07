# Temperature Interval Class
# Abstracts the idea of a temperature interval 
# going from T1 to T2

class Temperature_Interval:

    
    def __init__(self, T1, T2):
        self.Tmax = max(T1, T2)
        self.Tmin = min(T1, T2)
        self.DT = self.Tmax - self.Tmin

    
    def __str__(self):
        return "[{}, {}]".format(self.Tmax, self.Tmin)


    def passes_through_interval(self, other):
        """
        This method checks if self temperature 
        interval passes through other temperature
        interval. 
        Returns True if it does.
        """
        # self interval is to the left of other interval
        if self.Tmin >= other.Tmax:
            return False
        
        # self interval is to the right of other interval
        if self.Tmax <= other.Tmin:
            return False

        # otherwise it is contained
        return True


    def shifted(self, shift):
        return Temperature_Interval(self.Tmax + shift, self.Tmin + shift)


    @staticmethod
    def common_interval(interval_1, interval_2):

        assert interval_1.passes_through_interval(interval_2), "Intervals do not have common ground."

        Tmax = min(interval_1.Tmax, interval_2.Tmax)
        Tmin = max(interval_1.Tmin, interval_2.Tmin)

        return Temperature_Interval(Tmax, Tmin)
