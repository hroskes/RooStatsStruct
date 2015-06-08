import sys
import random

sys.argv.insert(1, "-b")
import ROOT
del sys.argv[1]

f = ROOT.TFile.Open("fa3_0_2_0_workspace.root")
w = f.Get("workspace")

fa3 = w.var("fa3")
mu = w.var("mu")

pdf = w.pdf("Total_0_2_0_SumPDF")
sMELA = w.var("sMELA")
D0minus = w.var("D0-_VBF")
DCP = w.var("Dcp_VBF")

testmu = 1
testfa3 = 0
ntoys = 1000000

mu.setVal(testmu)
fa3.setVal(testfa3)
data = pdf.generate(ROOT.RooArgSet(sMELA, D0minus, DCP), ntoys)

#mu.setVal(random.random())
#fa3.setVal(random.random())
#pdf.fitTo(data)

#https://twiki.cern.ch/twiki/bin/view/Main/LearningRoostats
nll = pdf.createNLL(data)
fa3.setRange(-0.9999, 0.9999)
frame = fa3.frame()
nll.plotOn(frame, ROOT.RooFit.ShiftToZero())

c1 = ROOT.TCanvas.MakeDefCanvas()
frame.Draw()
#frame.GetYaxis().SetRangeUser(0, frame.GetYaxis().GetXmax())
frame.GetYaxis().SetRangeUser(0, 10**5)
c1.SaveAs("/afs/cern.ch/user/h/hroskes/www/TEST/test.png")
