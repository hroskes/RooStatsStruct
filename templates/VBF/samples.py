import constants
import itertools
from enums import Hypothesis, ProductionMode
from math import copysign, sqrt
import os
import re

class Sample(object):
    def __init__(self, *args):
        attrs = {"productionmode": ProductionMode, "hypothesis": Hypothesis}
        for arg, (attr, attrtype) in itertools.product(args, attrs.iteritems()):
            try:
                setattr(self, attr, attrtype(arg))
            except ValueError:
                pass
        self.calcg1g4()

    def __str__(self):
        return "%s %s" % (self.productionmode, self.hypothesis)

    def __eq__(self, other):
        return self.hypothesis == other.hypothesis and self.productionmode == other.productionmode
    def __ne__(self, other):
        return not self == other

    def templatesfile(self, flavor, index):
        result = "%s%s_%s.root" % (self.productionmode, self.hypothesis, flavor)

        if index is not None:
            result = result.replace(".root", "_%i.root"%index)

        return result

    def crosssection(self):
        if self.productionmode == "ggH":
            SMXS = constants.SMXS_ggH
            SMBR = constants.SMBR
            return SMXS * SMBR * (self.JHUcrosssection() / constants.JHU_XS_a1_ggH)
        elif self.productionmode == "VBF":
            SMXS = constants.SMXS_VBF
            SMBR = constants.SMBR
            return SMXS * SMBR * (self.JHUcrosssection() / (constants.JHU_XS_a1_VBF*constants.JHU_XS_a1_ggH))
        raise NotImplementedError("Information for %s not put into samples.Sample.crosssection!"%self)

    def JHUcrosssection(self):
        if self.productionmode == "ggH":
             return self.g12g40xs() + self.g11g41xs() + self.g10g42xs()
        elif self.productionmode == "VBF":
            return self.g14g40xs() + self.g13g41xs() + self.g12g42xs() + self.g11g43xs() + self.g10g44xs()
        assert False

    def fa3VBF(self):
        if self.productionmode == "VBF":
            if self.hypothesis == "0-":
                return 1.0
            elif self.hypothesis == "0+":
                return 0.0
            elif self.hypothesis == "fa30.5":
                 return .5
                 #test - print what happens for the case of fa3_VBFdecay = 0.5
                 #g1 = 1
                 #g4 = sqrt(constants.JHU_XS_a1_VBF * constants.JHU_XS_a1_ggH / (constants.JHU_XS_a3_VBF * constants.JHU_XS_a3_ggH))
                 #return (g4**2 * constants.JHU_XS_a3_VBF) / (g1**2 * constants.JHU_XS_a1_VBF + g4**2 * constants.JHU_XS_a3_VBF)
            elif self.hypothesis == "fa3-0.5":
                return -.5
            elif self.hypothesis == "fa30.25":
                return .25
            elif self.hypothesis == "fa3-0.9":
                return -0.9
        assert False

    def fa3HZZ(self):
        if self.productionmode == "ggH":
            if self.hypothesis == "0-":
                return 1.0
            elif self.hypothesis == "0+":
                return 0.0
            elif self.hypothesis == "fa30.5":
                return 0.5
        assert False

    def calcg1g4(self):
        if self.productionmode == "VBF":
            if self.hypothesis == "0-":
                self.__g1 = 0
                self.__g4 = (constants.JHU_XS_a1_VBF * constants.JHU_XS_a1_ggH / (constants.JHU_XS_a3_VBF * constants.JHU_XS_a3_ggH))**.25
            else:
                self.__g1 = 1
                self.__g4 = copysign(sqrt(abs(self.fa3VBF())*constants.JHU_XS_a1_VBF / ((1-abs(self.fa3VBF()))*constants.JHU_XS_a3_VBF)), self.fa3VBF())

            divideby = (self.JHUcrosssection() / (constants.JHU_XS_a1_VBF*constants.JHU_XS_a1_ggH))
            self.__g1 /= divideby**.25
            self.__g4 /= divideby**.25

        elif self.productionmode == "ggH":
            if self.hypothesis == "0-":
                self.__g1 = 0
                self.__g4 = (constants.JHU_XS_a1_ggH / constants.JHU_XS_a3_ggH)**.5
            else:
                self.__g1 = 1
                self.__g4 = copysign(sqrt(abs(self.fa3HZZ())*constants.JHU_XS_a1_ggH / ((1-abs(self.fa3HZZ()))*constants.JHU_XS_a3_ggH)), self.fa3HZZ())

            divideby = (self.JHUcrosssection() / constants.JHU_XS_a1_ggH)
            self.__g1 /= divideby**.5
            self.__g4 /= divideby**.5

        try:
            self.__g1, self.__g4
        except AttributeError:
            assert False

    def g1(self):
        return self.__g1
    def g4(self):
        return self.__g4

    def g14g40xs(self):
        if self.productionmode == "VBF":
            return self.__g1**4 * constants.JHU_XS_a1_VBF*constants.JHU_XS_a1_ggH
        assert False
    def g13g41xs(self):
        if self.productionmode == "VBF":
            return 0
        assert False
    def g12g42xs(self):
        if self.productionmode == "VBF":
            return self.__g1**2*self.__g4**2 * (constants.JHU_XS_a1_VBF*constants.JHU_XS_a3_ggH + constants.JHU_XS_a3_VBF*constants.JHU_XS_a1_ggH)
        assert False
    def g11g43xs(self):
        if self.productionmode == "VBF":
            return 0
        assert False
    def g10g44xs(self):
        if self.productionmode == "VBF":
            return self.__g4**4 * constants.JHU_XS_a3_VBF*constants.JHU_XS_a3_ggH
        assert False

    def g12g40xs(self):
        if self.productionmode == "ggH":
            return self.__g1**2 * constants.constants.JHU_XS_a1_ggH
        assert False
    def g11g41xs(self):
        if self.productionmode == "ggH":
            0
        assert False
    def g10g42xs(self):
        if self.productionmode == "ggH":
            return self.__g4**2 * constants.constants.JHU_XS_a3_ggH
        assert False
