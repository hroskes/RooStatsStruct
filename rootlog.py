"""
to use:

- in other files (not this one!), replace:
    import ROOT
  with:
    import rootlog
    ROOT = rootlog.fakeroot()

- do not use:
    from ROOT import ...

- the if statement at the beginning of fakeroot.__getattr__
  may need some tweaking depending on what classes you use
"""

import ROOT

names = set([])
objects = []

class fakeroot(object):
    def __getattr__(self, name):
        if name.startswith("Roo") and "RooArg" not in name and name != "RooFit":
            return RooSomething(name)
        return getattr(ROOT, name)
    def __del__(self):
        print names
    def reset(self):
        names.clear()
        del objects[:]

class RooSomething(object):
    def __init__(self, classname):
        self.classname = classname
    def __call__(self, *args):
        if len(args) >= 0 and isinstance(args[0], basestring):
            if args[0] in names:
                raise ValueError(args[0] + " is already taken!")
            names.add(args[0])
        objects.append(getattr(ROOT, self.classname)(*args))
        return objects[-1]
    def __getattr__(self, name):
        return getattr(getattr(ROOT, self.classname), name)
