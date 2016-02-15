import sys
sys.argv.insert(1, "-b")
import ROOT
import loadlib
del sys.argv[1]
import random
from extendedcounter import *
import style
import itertools
import os
import config

########################################
#parameters
testfa3s = [-1 + a/4.0 for a in range(8,0,-1)]
varnames = ["sMELA_ggH", "D0-_dec", "Dcp_dec"]
########################################

ROOT.gStyle.SetCanvasDefW(1000)
ROOT.gErrorIgnoreLevel = 1001

if config.turnoffbkg:
    f = ROOT.TFile.Open("workspaces/ggH_2e2muonly_fa3_0_0_workspace_nobkg.root")
else:
    f = ROOT.TFile.Open("workspaces/ggH_2e2muonly_fa3_0_0_workspace.root")

w = f.Get("workspace")

fa3 = w.var("fa3_ggH")

TotalPDF = w.pdf("Cat_0_0_SumPDF")

pdf = ROOT.RooFormulaVar("SignalPdfAsFunction", "SignalPdfAsFunction", "(@0)", ROOT.RooArgList(TotalPDF))
c1 = ROOT.TCanvas.MakeDefCanvas()
c1.SetRightMargin(0.2)
#c1.SetLeftMargin(0.5)

for varname in varnames:
    var = w.var(varname)

    othervarnames = varnames[:]
    othervarnames.remove(varname)
    othervars = [w.var(a) for a in othervarnames]

    for testfa3 in testfa3s:
        toprint = "%s %s" % (varname, testfa3)
        print "=" * len(toprint)
        print toprint
        print "=" * len(toprint)

        fa3.setVal(testfa3)

        slicebins = var.getBins()
        slicemin = var.getMin()
        slicemax = var.getMax()
        for i in range(slicebins):
            value = (slicemin*(slicebins-i) + slicemax*i)/slicebins
            var.setVal(value)

            xbins = othervars[0].getBins()
            xmin = othervars[0].getMin()
            xmax = othervars[0].getMax()
            ybins = othervars[1].getBins()
            ymin = othervars[1].getMin()
            ymax = othervars[1].getMax()
            h = ROOT.TH2F("h", "h", xbins, xmin, xmax, ybins, ymin, ymax)

            for i, j in itertools.product(range(xbins), range(ybins)):
                xvalue = (xmin*(xbins-i) + xmax*i)/xbins
                othervars[0].setVal(xvalue)
                yvalue = (ymin*(ybins-j) + ymax*j)/ybins
                othervars[1].setVal(yvalue)
                if pdf.getVal() >= 0:
                    h.SetBinContent(i+1, j+1, pdf.getVal())
                else:
                    print "%sslices_fa3=%s/slice_%s.%s" % (varname, testfa3, value, format), i, j, pdf.getVal()

            h.Draw("colz")

            try:
                os.makedirs("%s/%sslices_fa3=%s/" % (config.plotdir, varname, testfa3))
            except OSError:
                pass
            try:
                os.symlink("/afs/cern.ch/user/h/hroskes/www/index.php", "%s/%sslices_fa3=%s/index.php" % (config.plotdir, varname, testfa3))
            except OSError:
                pass
            [c1.SaveAs("%s/%sslices_fa3=%s/slice_%s.%s" % (config.plotdir, varname, testfa3, value, format)) for format in ["png", "eps", "root", "pdf"]]
            del h
