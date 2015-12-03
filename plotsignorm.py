import sys
sys.argv.insert(1, "-b")
import ROOT
del sys.argv[1]
import random
from extendedcounter import *
import style
import config

f = ROOT.TFile.Open("fa3_0_2_0_workspace_nobkg.root")
w = f.Get("workspace")

fa3 = w.var("fa3")
mu = w.var("mu")
mu.setVal(1)
w.Print()

pdf = w.pdf("Total_0_2_0_SumPDF")

c1 = ROOT.TCanvas.MakeDefCanvas()

frame = fa3.frame()
SIGnorm = w.function("Signal_0_2_0_norm")

SIGnorm.plotOn(frame)
frame.GetYaxis().SetRangeUser(7.4, 7.7)

frame.Draw()
[c1.SaveAs("%s/signorm.%s" % (config.plotdir, format)) for format in ["png", "eps", "root", "pdf"]]
