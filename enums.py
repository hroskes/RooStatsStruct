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
            raise ValueError("%s is not a member of enum " + type(self).__name__ + "!  Valid choices:\n"
                               + "\n".join(" aka ".join(str(name) for name in item.names) for item in self.enumitems))

    def __str__(self):
        return str(self.item)
    def __int__(self):
        return int(self.item)
    def __format__(self, format_spec):
        return format(self.item, format_spec)

    def __eq__(self, other):
        try:
            return self.item == other.item
        except AttributeError:
            return self.item == other
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
                 EnumItem("interference", 2, "interf", "fa30.5"),
                 EnumItem("qqZZ", 3, "background", "bkg"),
                )

class WhichTemplates(MyEnum):
    enumitems = (
                 EnumItem("ggH_2e2muonly", 0, "ggH_2e2mu"),
                 EnumItem("ggH_allflavors", 1),
                 EnumItem("ggH_4eonly", 2, "ggH_4e"),
                 EnumItem("VBF_VBFdiscriminants", 3),
                 EnumItem("VBF_VBFdecay", 4),
                 EnumItem("VBF_g4power1", 4),
                 EnumItem("VBF_g4power2", 4),
                 EnumItem("VBF_g4power3", 4),
                )

onoffshell = OnOffShell.enumitems
categories = Category.enumitems
channels = Channel.enumitems
templatetypes = TemplateType.enumitems
