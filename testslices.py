import sys
import ROOT
import loadlib
import random
from extendedcounter import *
import style
import itertools
import os

########################################
#parameters
testfa3s = [-1 + a/4.0 for a in range(8,0,-1)]
varnames = ["sMELA", "D0-_VBF", "Dcp_VBF"]
floorminus999 = False
########################################

ROOT.gStyle.SetCanvasDefW(1000)
ROOT.gErrorIgnoreLevel = 1001

f = ROOT.TFile.Open("fa3_0_2_0_workspace_nobkg.root")
w = f.Get("workspace")

fa3 = w.var("fa3")

SMhistFunc = w.function("SM_0_2_0_HistPDF")
PShistFunc = w.function("PS_0_2_0_HistPDF")
MIXhistFunc = w.function("MIX_0_2_0_HistPDF")
SMnorm = w.function("SM_0_2_0_norm")
PSnorm = w.function("PS_0_2_0_norm")
MIXnorm = w.function("MIX_0_2_0_norm")

pdf = ROOT.RooFormulaVar("SignalPdfAsFunction", "SignalPdfAsFunction", "(@0*@1 + @2*@3 + @4*@5)", ROOT.RooArgList(SMhistFunc, SMnorm, MIXhistFunc, MIXnorm, PShistFunc, PSnorm))
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

            dir = "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/test/%s" % ("no-999" if floorminus999 else "")
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
