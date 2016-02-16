import config
from enums import *
from extendedcounter import *
import loadlib
import random
import ROOT
import style
import sys

##############################################
#parameters
testmu = 1
testfa3s = {0: 1, 1: 2, 0.5: 4, -0.5: 418}
varnames = ["Dcp_dec", "sMELA_ggH", "D0-_dec",
            "Dcp_VBF", "sMELA_VBF", "D0-_VBF"]
##############################################

fs, ws, pdfs = {}, {}, {}
fa3 = None
vars = {}

for channel in channels:
    fs[channel] = ROOT.TFile.Open("workspaces/{0}_fa3_{1}_{2}_workspace{3}.root".format(str(config.whichtemplates), channel, 0, "_nobkg" if config.turnoffbkg else ""))
    ws[channel] = fs[channel].Get("workspace")
    pdfs[channel] = ws[channel].pdf("Cat_{0}_{1}_SumPDF".format(channel, 0))
    if fa3 is None:  #this is the first one
        fa3 = ws[channel].var("fa3_ggH")
        mu = ws[channel].var("mu")
        for varname in varnames:
            vars[varname] = ws[channel].var(varname)
            if not vars[varname]:
                del vars[varname]

one = ROOT.RooConstVar("one", "one", 1.0)
TemplateName = "SumPDF"
pdf = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(*pdfs.values()), ROOT.RooArgList(*([one]*len(pdfs))))

for varname, var in vars.iteritems():
    frame = var.frame()

    othervars = [othervar for othervar in vars.values() if othervar is not var]

    for testfa3 in testfa3s:
        c1 = ROOT.TCanvas.MakeDefCanvas()
        mu.setVal(testmu)
        fa3.setVal(testfa3)
        pdf.createProjection(ROOT.RooArgSet(*othervars)).plotOn(frame, ROOT.RooFit.LineColor(testfa3s[testfa3]))

    frame.Draw()
    [c1.SaveAs("%s/projection_%s.%s" % (config.plotdir, varname, format)) for format in ["png", "eps", "root", "pdf"]]
