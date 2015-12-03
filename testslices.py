import sys
import ROOT
import loadlib
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
floorminus999 = False
########################################

ROOT.gStyle.SetCanvasDefW(1000)
ROOT.gErrorIgnoreLevel = 1001

f = ROOT.TFile.Open("fa3_0_0_workspace_nobkg.root")
w = f.Get("workspace")

fa3 = w.var("fa3")

TotalPDF = w.pdf("ggH_0_0")

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
                    if floorminus999:
                        h.SetBinContent(i+1, j+1, -999)
                    print "%sslices_fa3=%s/slice_%s.%s" % (varname, testfa3, value, format), i, j, pdf.getVal()

            h.Draw("colz")

            dir = "%s/%s" % (config.plotdir, "no-999" if floorminus999 else "")
            try:
                os.mkdir("%s/%sslices_fa3=%s/" % (dir, varname, testfa3))
            except OSError:
                pass
            try:
                os.symlink("/afs/cern.ch/user/h/hroskes/www/index.php", "%s/%sslices_fa3=%s/index.php" % (dir, varname, testfa3))
            except OSError:
                pass
            [c1.SaveAs("%s/%sslices_fa3=%s/slice_%s.%s" % (dir, varname, testfa3, value, format)) for format in ["png", "eps", "root", "pdf"]]
            del h
