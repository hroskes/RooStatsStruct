import sys
sys.argv.insert(1, "-b")
import ROOT
import loadlib
del sys.argv[1]
import random
from extendedcounter import *
import style


def testfit(nNLLs = 100,
            nbins = 1000,
            low = -1,
            high = 1,
            testmu = 1,
            testfa3 = 0,
            zoomed = False,
            ntoys = 1000,  #default if None: BKGrate+SMrate
           ):

    f = ROOT.TFile.Open("fa3_0_0_workspace_nobkg.root")
    w = f.Get("workspace")

    fa3 = w.var("fa3")
    mu = w.var("mu")

    pdf = w.pdf("Cat_0_0_SumPDF")
    sMELA = w.var("sMELA_ggH")
    D0minus = w.var("D0-_dec")
    DCP = w.var("Dcp_dec")

    if ntoys is None:
        ntoys = (w.var("BKGrate").getVal() + w.var("SMrate").getVal())

    print "Number of toys:", ntoys

    ROOT.RooRandom.randomGenerator().SetSeed(random.randint(0,10000))

    fa3.setRange(-1, 1)

    bincenters = [1.0*i/nbins * high + (1-(1.0*i)/nbins) * low for i in range(nbins+1)]

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
    print bincenters[-1], averageNLL[bincenters[-1]]

    graph = averageNLL.TGraph()
    graph.SetLineWidth(3)
    multigraph.Add(graph)

    multigraph.Draw("AC")
    multigraph.GetYaxis().SetTitle("-2#Deltaln L")
    multigraph.GetXaxis().SetTitle("f_{a_{3}}")

    style.drawlines()

    [c1.SaveAs("plots/scan_fa3=%s%s.%s" % (testfa3, "",        format)) for format in ["png", "eps", "root", "pdf"]]

    multigraph.GetYaxis().SetRangeUser(0,1)

    [c1.SaveAs("plots/scan_fa3=%s%s.%s" % (testfa3, "_zoomed", format)) for format in ["png", "eps", "root", "pdf"]]

if __name__ == '__main__':
    [testfit(testfa3=testfa3) for testfa3 in [-0.5, 0.5, 0, 1]]
