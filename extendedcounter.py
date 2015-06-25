import collections
import array
import ROOT

class ExtendedCounter(collections.Counter):
    def __init__(self, *args, **kwargs):
        super(ExtendedCounter, self).__init__(*args, **kwargs)

    def __add__(self, other):
        return ExtendedCounter(super(ExtendedCounter, self).__add__(other))
    def __sub__(self, other):
        return ExtendedCounter(super(ExtendedCounter, self).__sub__(other))

    def __mul__(self, other):
        """multiply by a scalar"""
        result = ExtendedCounter(self)
        for item in result:
            result[item] *= other
        return result

    def _rmul__(self, other):
        """multiply by a scalar"""
        return self * other

    def __div__(self, other):
        """divide by a scalar"""
        result = ExtendedCounter(self)
        for item in result:
            result[item] /= other
        return result

    def TGraph(self):
        """make a TGraph with the data in self.  Keys and values have to be numbers."""
        x = array.array("d", self.keys())
        y = array.array("d", self.values())
        print "=====TGraph====="
        print self
        print x
        print y
        return ROOT.TGraph(len(self), x, y)
