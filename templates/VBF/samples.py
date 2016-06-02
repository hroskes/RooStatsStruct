import constants
import itertools
from enums import Hypothesis, ProductionMode, Channel
from math import copysign, sqrt
import os
import re

class Sample(object):
    def __init__(self, *args):
        attrs = {"productionmode": ProductionMode, "hypothesis": Hypothesis, "flavor": Channel}
        for arg, (attr, attrtype) in itertools.product(args, attrs.iteritems()):
            try:
                setattr(self, attr, attrtype(arg))
            except ValueError:
                pass

        assert hasattr(self, "productionmode")

        if self.isbkg() or self.isdata():
            assert not hasattr(self, "hypothesis")
            self.hypothesis = ""
        else:
            assert hasattr(self, "hypothesis")

        if self.productionmode == "ggZZ":
            assert hasattr(self, "flavor")
        else:
            assert not hasattr(self, "flavor")
            self.flavor = ""

        if self.hypothesis not in ("int_g1g4", "int_g1g2", "int_g1g1prime2") and not self.isdata():
            self.calcg1g4()

    def __str__(self):
        return "%s %s %s" % (self.productionmode, self.hypothesis, self.flavor)
    def __repr__(self):
        return "Sample({!s}, {!s}, {!s})".format(self.productionmode, self.hypothesis, self.flavor)
    def __hash__(self):
        return hash((self.productionmode, self.hypothesis, self.flavor))

    def __eq__(self, other):
        return self.hypothesis == other.hypothesis and self.productionmode == other.productionmode and self.flavor == other.flavor
    def __ne__(self, other):
        return not self == other

    def templatesfile(self, flavor, index):
        if self.flavor != "" and self.flavor != flavor:
            raise ValueError
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
             return self.g1g1xs() + self.g1g4xs() + self.g4g4xs() + self.g1g2xs() + self.g2g2xs() + self.g1g1prime2xs() + self.g1prime2g1prime2xs()
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
            elif self.hypothesis == "0+" or self.hypothesis == "a2" or self.hypothesis == "L1" or self.hypothesis == "fa20.5" or self.hypothesis == "fL10.5":
                return 0.0
            elif self.hypothesis == "fa30.5":
                return 0.5
        assert False

    def calcg1g4(self):
        if self.isbkg(): return
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
            self.__g1 = self.__g4 = self.__g2 = self.__g1prime2 = 0
            if self.hypothesis == "0+" or self.hypothesis == "fa30.5" or self.hypothesis == "fa20.5" or self.hypothesis == "fL10.5":
                self.__g1 = 1
            if self.hypothesis == "a2" or self.hypothesis == "fa20.5":
                self.__g2 = constants.g2_mix_ggH
            if self.hypothesis == "0-" or self.hypothesis == "fa30.5":
                self.__g4 = constants.g4_mix_ggH
            if self.hypothesis == "L1" or self.hypothesis == "fL10.5":
                self.__g4 = constants.g1prime2_mix_ggH

            divideby = (self.JHUcrosssection() / constants.JHU_XS_a1_ggH)
            self.__g1 /= divideby**.5
            self.__g2 /= divideby**.5
            self.__g4 /= divideby**.5
            self.__g1prime2 /= divideby**.5

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

    def g1g1xs(self):
        if self.productionmode == "ggH":
            return self.__g1**2 * constants.JHU_XS_a1_ggH
        assert False
    def g1g4xs(self):
        if self.productionmode == "ggH":
            return constants.JHU_XS_g1g4_int_ggH
        assert False
    def g4g4xs(self):
        if self.productionmode == "ggH":
            return self.__g4**2 * constants.JHU_XS_a3_ggH
        assert False
    def g1g2xs(self):
        if self.productionmode == "ggH":
            return self.__g1*self.__g1prime2 * constants.JHU_XS_g1g2_int_ggH
        assert False
    def g2g2xs(self):
        if self.productionmode == "ggH":
            return self.__g2**2 * constants.JHU_XS_a2_ggH
        assert False
    def g1g1prime2xs(self):
        if self.productionmode == "ggH":
            return self.__g1*self.__g1prime2 * constants.JHU_XS_g1g1prime2_int_ggH
        assert False
    def g1prime2g1prime2xs(self):
        if self.productionmode == "ggH":
            return self.__g1prime2**2 * constants.JHU_XS_L1_ggH
        assert False

    def isbkg(self):
        return self.productionmode == "ggZZ" or self.productionmode == "qqZZ"
    def isdata(self):
        return self.productionmode == "data"
