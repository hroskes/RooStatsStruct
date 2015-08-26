import sys
import ROOT
import random
from extendedcounter import *
import style
import os

########################################
#parameters
testfa3s = {0: 1, 1: 2, 0.5: 4, -0.5: 418}
varnames = ["sMELA", "D0-_VBF", "Dcp_VBF"]
########################################

ROOT.gStyle.SetCanvasDefW(1000)

f = ROOT.TFile.Open("fa3_0_2_0_workspace_nobkg.root")
w = f.Get("workspace")

fa3 = w.var("fa3")

pdf = w.pdf("Signal_0_2_0_SumPDF")

c1 = ROOT.TCanvas.MakeDefCanvas()
c1.SetRightMargin(0.2)
#c1.SetLeftMargin(0.5)

for varname in varnames:
    var = w.var(varname)

    othervarnames = varnames[:]
    othervarnames.remove(varname)
    othervars = [w.var(a) for a in othervarnames]

    for testfa3 in testfa3s:

        fa3.setVal(testfa3)

        bins = var.getBins()
        minval = var.getMin()
        maxval = var.getMax()
        for i in range(bins):
            value = (minval*(bins-i) + maxval*i)/bins
            var.setVal(value)

            print ",".join(othervarnames)
            pdf.createHistogram(",".join(othervarnames)).Draw("colz")

            try:
                os.mkdir("/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/test/%sslices_fa3=%s/" % (varname, testfa3))
            except OSError:
                pass
            [c1.SaveAs("/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/test/%sslices_fa3=%s/slice_%s.%s" % (varname, testfa3, value, format)) for format in ["png", "eps", "root", "pdf"]]
