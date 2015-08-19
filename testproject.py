import sys
sys.argv.insert(1, "-b")
import ROOT
del sys.argv[1]
import random
from extendedcounter import *
import style

########################################
#parameters
testmu = 100000
testfa3s = [-0.5, 0, 0.5, 1]
varnames = ["sMELA", "D0-_VBF", "Dcp_VBF"]
########################################

f = ROOT.TFile.Open("fa3_0_2_0_workspace_nobkg.root")
w = f.Get("workspace")

fa3 = w.var("fa3")
mu = w.var("mu")

pdf = w.pdf("Total_0_2_0_SumPDF")

for testfa3 in testfa3s:
    for varname in varnames:
        var = w.var(varname)

        othervarnames = varnames[:]
        othervarnames.remove(varname)
        othervars = [w.var(a) for a in othervarnames]

        ROOT.RooRandom.randomGenerator().SetSeed(random.randint(0,10000))

        c1 = ROOT.TCanvas.MakeDefCanvas()
        frame = var.frame()
        mu.setVal(testmu)
        fa3.setVal(testfa3)
        pdf.createProjection(ROOT.RooArgSet(*othervars)).plotOn(frame)

        frame.Draw()

        [c1.SaveAs("/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/%s_fa3=%s.%s" % (varname, testfa3, format)) for format in ["png", "eps", "root", "pdf"]]
