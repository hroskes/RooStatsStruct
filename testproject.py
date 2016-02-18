import config
import constants
from enums import *
from extendedcounter import *
from getvars import discriminants, fa3, mu, pdf
import loadlib
import random
import ROOT
import style
import sys

##############################################
#parameters
testmu = 1
testfa3s = {0: 1, 1: 2, .5: 418, -.5: 4}
if "VBF" in str(config.whichtemplates):
    fa3interpretation = "VBF"
else:
    fa3interpretation = "HZZ"
##############################################

testfa3s = {constants.convertfa3(fa3, fa3interpretation, "HZZ"): color for fa3, color in testfa3s.iteritems()}

for var in discriminants:
    if not var.GetTitle(): continue
    c1 = ROOT.TCanvas.MakeDefCanvas()
    frame = var.frame()
    frame.SetXTitle(var.GetTitle())

    othervars = [othervar for othervar in discriminants if othervar is not var]

    for testfa3 in testfa3s:
        mu.setVal(testmu)
        fa3.setVal(testfa3)
        pdf.createProjection(ROOT.RooArgSet(*othervars)).plotOn(frame, ROOT.RooFit.LineColor(testfa3s[testfa3]))

    frame.Draw()
    [c1.SaveAs("%s/projection_%s.%s" % (config.plotdir, var.GetName(), format)) for format in ["png", "eps", "root", "pdf"]]
