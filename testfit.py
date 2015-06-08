import sys
import random

sys.argv.insert(1, "-b")
import ROOT
del sys.argv[1]

f = ROOT.TFile.Open("RooStatsStruct/fa3_0_2_0_workspace.root")
w = f.Get("workspace")

fa3 = w.var("fa3")

pdf = w.pdf("Signal_0_2_0_SumPDF")
sMELA = w.var("sMELA")
D0minus = w.var("D0-_VBF")
DCP = w.var("Dcp_VBF")

testfa3 = .55
ntoys = 1000000

fa3.setVal(0)
data = pdf.generate(ROOT.RooArgSet(sMELA, D0minus, DCP), ntoys*(1-testfa3))
fa3.setVal(1)
data.append(pdf.generate(ROOT.RooArgSet(sMELA, D0minus, DCP), ntoys*testfa3))

#fa3.setVal(random.random())
#pdf.fitTo(data)

#https://twiki.cern.ch/twiki/bin/view/Main/LearningRoostats
nll = pdf.createNLL(data)
frame = fa3.frame()
nll.plotOn(frame)

c1 = ROOT.TCanvas.MakeDefCanvas()
frame.Draw()
c1.SaveAs("/afs/cern.ch/user/h/hroskes/www/TEST/test.png")


