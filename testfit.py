import sys
sys.argv.insert(1, "-b")
import ROOT
import loadlib
del sys.argv[1]
import random
from extendedcounter import *
from enums import *
import style
import config
import os


def testfit(nNLLs = 1000,
            nbins = 1000,
            low = -1,
            high = 1,
            testmu = 1,
            testfa3 = 0,
            zoomed = False,
            ntoys = None,  #default if None: BKGrate+SMrate
           ):

    fs, ws, pdfs = {}, {}, {}
    fa3 = None

    for channel in channels:
        fs[channel] = ROOT.TFile.Open("workspaces/{0}_fa3_{1}_{2}_workspace{3}.root".format(str(config.whichtemplates), channel, 0, "_nobkg" if config.turnoffbkg else ""))
        ws[channel] = fs[channel].Get("workspace")
        pdfs[channel] = ws[channel].pdf("Cat_{0}_{1}_SumPDF".format(channel, 0))
        if fa3 is None:  #this is the first one
            fa3 = ws[channel].var("fa3")
            mu = ws[channel].var("mu")
            sMELA_ggH = ws[channel].var("sMELA_ggH")
            D0minus_ggH = ws[channel].var("D0-_dec")
            DCP_ggH = ws[channel].var("Dcp_dec")
            sMELA_VBF = ws[channel].var("sMELA_VBF")
            D0minus_VBF = ws[channel].var("D0-_VBF")
            DCP_VBF = ws[channel].var("Dcp_VBF")
            sMELA_VH = ws[channel].var("sMELA_VH")
            D0minus_VH = ws[channel].var("D0-_VH")
            DCP_VH = ws[channel].var("Dcp_VH")

    one = ROOT.RooConstVar("one", "one", 1.0)
    TemplateName = "SumPDF"
    pdf = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(*pdfs.values()), ROOT.RooArgList(*([one]*len(pdfs))))

    if ntoys is None:
        ntoys = pdf.getNorm(ROOT.RooArgSet(sMELA_ggH, D0minus_ggH, DCP_ggH, sMELA_VBF, D0minus_VBF, DCP_VBF, sMELA_VH, D0minus_VH, DCP_VH))
        print ntoys
        assert False

    print "Number of toys:", ntoys

    ROOT.RooRandom.randomGenerator().SetSeed(config.seed)

    fa3.setRange(-1, 1)

    bincenters = [1.0*i/nbins * high + (1-(1.0*i)/nbins) * low for i in range(nbins+1)]

    c1 = ROOT.TCanvas.MakeDefCanvas()
    multigraph = ROOT.TMultiGraph()

    averageNLL = ExtendedCounter()
    for j in range(nNLLs):
        mu.setVal(testmu)
        fa3.setVal(testfa3)

        data = pdf.generate(ROOT.RooArgSet(sMELA_ggH, D0minus_ggH, DCP_ggH), ntoys)
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

    try:
        os.makedirs(config.plotdir)
    except OSError:
        pass

    [c1.SaveAs("%s/scan_fa3=%s%s.%s" % (config.plotdir, testfa3, "",        format)) for format in ["png", "eps", "root", "pdf"]]

    multigraph.GetYaxis().SetRangeUser(0,1)

    [c1.SaveAs("%s/scan_fa3=%s%s.%s" % (config.plotdir, testfa3, "_zoomed", format)) for format in ["png", "eps", "root", "pdf"]]

if __name__ == '__main__':
    fa3s = sys.argv[1:]
    if not fa3s:
        fa3s = [0, 1, .5, -.5]
    [testfit(
             testfa3=float(testfa3),
             ntoys = config.sigrate + config.bkgrate
            ) for testfa3 in fa3s]
