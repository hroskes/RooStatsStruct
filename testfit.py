import sys
sys.argv.insert(1, "-b")
import ROOT
del sys.argv[1]
import random
from extendedcounter import *
import style


########################################
#parameters
nNLLs = 100
nbins = 1000
low = -1
high = 1
testmu = 1
testfa3 = 0
zoomed = False
ntoys = None  #default if None: BKGrate+SMrate
########################################

f = ROOT.TFile.Open("fa3_0_2_0_workspace.root")
w = f.Get("workspace")

fa3 = w.var("fa3")
mu = w.var("mu")

pdf = w.pdf("Total_0_2_0_SumPDF")
sMELA = w.var("sMELA")
D0minus = w.var("D0-_VBF")
DCP = w.var("Dcp_VBF")

if ntoys is None:
    ntoys = (w.var("BKGrate").getVal() + w.var("SMrate").getVal())

print "Number of toys:", ntoys

ROOT.RooRandom.randomGenerator().SetSeed(random.randint(0,10000))

fa3.setRange(-1, 1)

bincenters = [(i+.5)/nbins * high + (1-(i+.5)/nbins) * low for i in range(nbins)]

c1 = ROOT.TCanvas.MakeDefCanvas()
multigraph = ROOT.TMultiGraph()

averageNLL = ExtendedCounter()
for j in range(nNLLs):
    mu.setVal(testmu)
    fa3.setVal(testfa3)
    data = pdf.generate(ROOT.RooArgSet(sMELA, D0minus, DCP), ntoys)
    nll = pdf.createNLL(data)
    result = ExtendedCounter()
    for bincenter in bincenters:
        fa3.setVal(bincenter)
        result[bincenter] = nll.getVal()
    result *= 2
    averageNLL += result
    graph = result.TGraph()
    graph.SetLineColor(17)
    multigraph.Add(graph)
    if (j+1) % 25 == 0 or (j+1) == nNLLs:
        print str(j+1) + " / " + str(nNLLs)

averageNLL /= nNLLs

graph = averageNLL.TGraph()
graph.SetLineWidth(3)
multigraph.Add(graph)

multigraph.Draw("AC")
multigraph.GetYaxis().SetTitle("-2#Deltaln L")
multigraph.GetXaxis().SetTitle("f_{a_{3}}")
if zoomed:
    multigraph.GetYaxis().SetRangeUser(0,.003)

style.drawlines()

[c1.SaveAs("/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/fa3=%s%s.%s" % (testfa3, "_zoomed" if zoomed else "", format)) for format in ["png", "eps", "root", "pdf"]]
