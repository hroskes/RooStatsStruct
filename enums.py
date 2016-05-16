class EnumItem(object):
    def __init__(self, name, code, *other):
        self.name = name
        self.code = code
        self.names = tuple([name, code] + list(other))

    def __str__(self):
        return self.name
    def __int__(self):
        return self.code
    def __format__(self, format_spec):
        return format(int(self), format_spec)
    def __hash__(self):
        return hash(self.names)

    def __eq__(self, other):
        if type(other) == int or type(other) == str:
            return other in self.names
        return str(self) == str(other) and int(self) == int(other)
    def __ne__(self, other):
        return not self == other

class MyEnum(object):
    def __init__(self, value):
        if isinstance(value, (MyEnum, EnumItem)):
            value = str(value)
        for item in self.enumitems:
            if value in item.names:
                self.item = item
                break
        else:
            raise ValueError("%s is not a member of enum "%value + type(self).__name__ + "!  Valid choices:\n"
                               + "\n".join(" aka ".join(str(name) for name in item.names) for item in self.enumitems))

    def __str__(self):
        return str(self.item)
    def __int__(self):
        return int(self.item)
    def __format__(self, format_spec):
        return format(self.item, format_spec)

    def __eq__(self, other):
        try:
            other = type(self)(other)
            return self.item == other.item
        except ValueError:
            if other is None or (type(other) == str and other == ""):
                return False
            raise
    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.item)

class OnOffShell(MyEnum):
    enumitems = (
                 EnumItem("onshell",  0, "on", "on-shell", "on_shell"),
                 EnumItem("offshell", 1, "off", "off-shell", "off_shell"),
                )

class Category(MyEnum):
    enumitems = (
                 EnumItem("ggH", 0, "HZZ"),
                 EnumItem("VH", 1),
                 EnumItem("VBF", 2),
                )

class Channel(MyEnum):
    enumitems = (
                 EnumItem("2e2mu", 0, "2mu2e"),
                 EnumItem("4mu", 1),
                 EnumItem("4e", 2),
                )

class TemplateType(MyEnum):
    enumitems = (
                 EnumItem("0+", 0, "SM", "scalar"),
                 EnumItem("0-", 1, "PS", "pseudoscalar"),
                 EnumItem("interference", 2, "interf"),
                 EnumItem("qqZZ", 3, "background", "bkg"),
                 EnumItem("g4power1", 4),
                 EnumItem("g4power2", 5),
                 EnumItem("g4power3", 6),
                )

class WhichTemplates(MyEnum):
    enumitems = (
                 EnumItem("ggH_2e2muonly", 0, "ggH_2e2mu"),
                 EnumItem("ggH_allflavors", 1),
                 EnumItem("ggH_4eonly", 2, "ggH_4e"),
                 EnumItem("VBF_nodecay", 3),
                 EnumItem("VBF_DCPVBF", 4),
                 EnumItem("VBF_g4power1", 5),
                 EnumItem("VBF_g4power2", 6),
                 EnumItem("VBF_g4power3", 7),
                 EnumItem("VBF_1D_D0minus_VBF", 8),
                 EnumItem("VBF_1D_D0minus_VBFdecay", 9),
                 EnumItem("VBF_1D_DCP_VBF", 10),
                 EnumItem("VBF_1D_g4power1", 11),
                 EnumItem("VBF_1D_g4power2", 12),
                 EnumItem("VBF_1D_g4power3", 13),
                 EnumItem("VBF_1D_g4power0", 14),
                 EnumItem("VBF_1D_DCP_VBFdecay", 15),
                 EnumItem("VBF_1D_g4power1_prime", 16),
                 EnumItem("VBF_1D_g4power2_prime", 17),
                 EnumItem("VBF_1D_g4power3_prime", 18),
                 EnumItem("VBF_g4power1_prime", 19),
                 EnumItem("VBF_g4power2_prime", 20),
                 EnumItem("VBF_g4power3_prime", 21),
                )

class PDFType(MyEnum):
    enumitems = (
                 EnumItem("decayonly_onshell", 0, "productiononly_onshell"),
                 EnumItem("production+decay_onshell", 1),
                )

class Hypothesis(MyEnum):
    enumitems = (
                 EnumItem("0+", 0, "SM", "scalar"),
                 EnumItem("0-", 1, "PS", "pseudoscalar"),
                 EnumItem("fa30.5", 2, "interf", "interf", "mix"),
                 EnumItem("fa30.25", 3),
                 EnumItem("fa3-0.5", 4),
                 EnumItem("fa3-0.9", 5),
                 EnumItem("a2", 6, "0h+"),
                 EnumItem("fa20.5", 7),
                 EnumItem("L1", 8, "Lambda1"),
                 EnumItem("fL10.5", 9, "flambda10.5"),
                 EnumItem("int_g1g4", 10, "int_a1a3"),
                 EnumItem("int_g1g2", 11, "int_a1a2"),
                 EnumItem("int_g1g1prime2", 12, "int_a1L1"),
                )

class ProductionMode(MyEnum):
    enumitems = (
                 EnumItem("ggH", 0),
                 EnumItem("VBF", 1),
                 EnumItem("H+jj", 2, "HJJ"),
                 EnumItem("ZH", 3),
                 EnumItem("WH", 4),
                 EnumItem("qqZZ", 5),
                 EnumItem("ggZZ", 6),
                 EnumItem("data", 7),
                )

categories = [Category(item) for item in Category.enumitems]
channels = [Channel(item) for item in Channel.enumitems]
hypotheses = [Hypothesis(item) for item in Hypothesis.enumitems]
onoffshell = [OnOffShell(item) for item in OnOffShell.enumitems]
productionmodes = [ProductionMode(item) for item in ProductionMode.enumitems]
templatetypes = [TemplateType(item) for item in TemplateType.enumitems]
