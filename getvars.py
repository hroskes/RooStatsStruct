#use from the python shell, from getvars.py import *

import config
from enums import *
from itertools import product
import loadlib
import os
import ROOT as therealROOT
import rootlog
import sys

ROOT = rootlog.fakeroot()

fs, ws, pdfs = {}, {}, {}
fa3 = None

for channel in channels:
    fs[channel] = ROOT.TFile.Open("workspaces/{0}_fa3_{1}_{2}_workspace{3}.root".format(str(config.whichtemplates), channel, 0, "_nobkg" if config.turnoffbkg else ""))
    ws[channel] = fs[channel].Get("workspace")
    pdfs[channel] = ws[channel].pdf("Cat_{0}_{1}_SumPDF".format(channel, 0))
    if fa3 is None:  #this is the first one
        fa3 = ws[channel].var("fa3_HZZ")
        fa3_VBF = ws[channel].obj("fa3_VBF")
        mu = ws[channel].var("mu")
        Disc = {category: {} for category in categories}
        for category, i in product(categories, range(3)):
            discriminant = ws[channel].var("Disc%i_%s" % (i, category))
            if discriminant:
                Disc[category][i] = ws[channel].var("Disc%i_%s" % (i, category))
            del discriminant
del channel

one = ROOT.RooConstVar("one", "one", 1.0)
TemplateName = "SumPDF"
pdf = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(*pdfs.values()), ROOT.RooArgList(*([one]*len(pdfs))))

discriminants = sum((Disc[category].values() for category in categories),[])
discriminantsargset = ROOT.RooArgSet(*discriminants)

if os.isatty(sys.stdout.fileno()):
    #to make it easier to get things from the workspace
    #  but only if in interactive mode, so as not to complicate things
    #  in scripts
    w = ws[Channel("2e2mu")]
    def __getattr__(self, attr):
        result = self.obj(attr)
        if result:
            return result
        raise AttributeError("No object named '%s' in the workspace!" % attr)
    type(w).__getattr__ = __getattr__
    del __getattr__
    #can now get things from w using w.name

    #integral
    def int(self, whichdiscriminants = "ggH VH VBF"):
        discs = []
        for category in whichdiscriminants.split():
            assert category in ("ggH", "VH", "VBF")
            discs += [disc for disc in discriminants if category in disc.GetName()]
        return self.createIntegral(ROOT.RooArgSet(*discs)).getVal()
    therealROOT.RooAbsReal.int = int
    del int
