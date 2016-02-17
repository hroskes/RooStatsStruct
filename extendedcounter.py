import collections
import array
import ROOT

class ExtendedCounter(collections.Counter):
    """For one reason or another I can't get Counter.__add__ and __sub__
       to work here"""

    def __add__(self, other):
        result = ExtendedCounter(self)
        for item in other:
            if item not in result:
                result[item] = 0
            result[item] += other[item]
        return result

    def __sub__(self, other):
        result = ExtendedCounter(self)
        for item in other:
            if item not in result:
                result[item] = 0
            result[item] -= other[item]
        return result

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

    def zero(self):
        minvalue = min(self.values())
        for key in self:
            self[key] -= minvalue

    def TGraph(self, transformx=lambda x: x, transformy=lambda x: x):
        """
        make a TGraph with the data in self.  Keys and values have to be numbers.
        transformx and transformy: functions applied to x and y before creating the
                                   graph
        """
        self.zero()
        items = self.items()
        items = [(transformx(x), transformy(y)) for x, y in items]
        items.sort(key = lambda x: x[0])
        keysvalues = zip(*items)
        keys = keysvalues[0]
        values = keysvalues[1]
        x = array.array("d", keys)
        y = array.array("d", values)
        return ROOT.TGraph(len(self), x, y)

def makefromcombineC(combinefilename):
    result = ExtendedCounter()
    with open(combinefilename) as f:
        for line in f:
            try:
                line = line.split("graph->SetPoint(")[1].split(")")[0]
                line = line.split(",")
                result[float(line[1])] = float(line[2])
            except (IndexError, ValueError):
                pass
    return result

def makefromTGraph(g):
    return ExtendedCounter({x: y for x, y, dummy in zip(g.GetX(), g.GetY(), range(g.GetN()))})
