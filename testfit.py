import sys
import random
from extendedcounter import *


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
testfa3 = 0.5
ntoys = w.var("BKGrate").getVal() + w.var("SMrate").getVal()
print ntoys

mu.setVal(testmu)
fa3.setVal(testfa3)

ROOT.RooRandom.randomGenerator().SetSeed(random.randint(0,10000))

fa3.setRange(-0.9999, 0.9999)
frame = fa3.frame()

def getNLLs(nNLLs):
    for j in range(nNLLs):
        if j % 25 == 0:
            print str(j) + " / " + str(nNLLs)
        data = pdf.generate(ROOT.RooArgSet(sMELA, D0minus, DCP), ntoys)
        nll = pdf.createNLL(data)
        plot = nll.plotOn(frame, ROOT.RooFit.ShiftToZero())
        bins = plot.GetNbinsX()
        xaxis = plot.GetXaxis()
        print bins
        result =  ExtendedCounter({
                                   (xaxis.GetBinLowEdge(i+1) + xaxis.GetBinLowEdge(i+2)) / 2 :
                                       plot.GetBinContent(i+1)
                                   for i in range(plot.GetNbinsX())
                                  })
        print result
        yield result
nNLLs = 10
averageNLL = sum(getNLLs(nNLLs), ExtendedCounter()) / nNLLs
print averageNLL

graph = averageNLL.TGraph()

c1 = ROOT.TCanvas.MakeDefCanvas()
graph.Draw("AC")
#frame.GetYaxis().SetRangeUser(0, frame.GetYaxis().GetXmax())
c1.SaveAs("/afs/cern.ch/user/h/hroskes/www/TEST/test.png")
