class EnumItem(object):
    def __init__(self, name, code, *other):
        self.name = name
        self.code = code
        self.names = [name, code] + list(other)

    def __str__(self):
        return self.name
    def __int__(self):
        return self.code
    def __format__(self, format_spec):
        return format(int(self), format_spec)

    def __eq__(self, other):
        if type(other) == int:
            return int(self) == other
        if type(other) == str:
            return str(self) == other
        return str(self) == str(other) and int(self) == int(other)
    def __ne__(self, other):
        return not self == other

class MyEnum(object):
    def __init__(self, value):
        if isinstance(value, type(self)):
            onoff = str(value)
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

class OnOffShell(MyEnum):
    enumitems = (
                 EnumItem("onshell",  0, "on"),
                 EnumItem("offshell", 1, "off"),
                )

class Category(MyEnum):
    enumitems = (
                 EnumItem("ggH", 0),
                 EnumItem("VH",  1),
                 EnumItem("VBF", 2),
                )

class Channel(MyEnum):
    enumitems = (
                 EnumItem("2e2mu", 0, "2mu2e"),
                 EnumItem("4mu",   1),
                 EnumItem("4e",    2),
                )

on_shell  = OnOffShell("onshell")
off_shell = OnOffShell("offshell")

ggH_category = Category("ggH")
VH_category  = Category("VH")
VBF_category = Category("VBF")

TwoETwoMu = Channel("2e2mu")
FourMu    = Channel("4mu")
FourE     = Channel("4e")
