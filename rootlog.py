"""
to use:

- in other files (not this one!), replace:
    import ROOT
  with:
    import rootlog
    ROOT = rootlog.thefakeroot

- do not use:
    from ROOT import ...

- the if statement at the beginning of fakeroot.__getattr__
  may need some tweaking depending on what classes you use
"""

import ROOT

names = set([])
reusednames = set([])
objects = []
files = {}

class fakeroot(object):
    def __getattr__(self, name):
        if name in ["RooArgSet", "RooArgList"]:
            return RooArgSetOrList(name)
        elif name.startswith("Roo") and name != "RooFit":
            return RooSomething(name)
        elif name == "TFile":
            return TFile()
        else:
            return getattr(ROOT, name)
    def reset(self):
        names.clear()
        del objects[:]
        [f.Close() for f in files.values()]
        files.clear()
    def __del__(self):
         if reusednames:
             print "Warning!  The following names were used to create Roo*'s multiple times:\n" + "\n".join(sorted(reusednames))

thefakeroot = fakeroot()

class RooArgSetOrList(object):
    def __init__(self, classname):
        self.classname = classname
    def __call__(self, *args):
        fancystuff = len(args) > 9
        for arg in args[:-1]:
            if not isinstance(arg, ROOT.RooAbsArg):
                fancystuff = False
                break
        if fancystuff:
            tlist = ROOT.TList()
            for arg in args[:-1]:
                tlist.Add(arg)
            if isinstance(args[-1], ROOT.RooAbsArg):
                tlist.Add(args[-1])
                return getattr(ROOT, self.classname)(tlist)
            else:
                return getattr(ROOT, self.classname)(tlist, args[-1])
        else:
            return getattr(ROOT, self.classname)(*args)

class RooSomething(object):
    def __init__(self, classname):
        self.classname = classname
    def __call__(self, *args):
        if len(args) >= 0 and isinstance(args[0], basestring):
            if args[0] in names:
                reusednames.add(args[0])
            names.add(args[0])
        objects.append(getattr(ROOT, self.classname)(*args))
        return objects[-1]
    def __getattr__(self, name):
        return getattr(getattr(ROOT, self.classname), name)

class TFile(object):
    def __call__(self, *args):
        if len(args) == 0:
            raise TypeError("Who uses the TFile default constructor?")
        if args[0] not in files:
            files.update({args[0]: ROOT.TFile.Open(*args)})
        return files[args[0]]
    def __getattr__(self, name):
        if name == "Open":
            return self
        return getattr(ROOT.TFile, name)
