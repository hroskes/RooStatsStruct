import config
import constants
from enums import *
from extendedcounter import *
import functools
import loadlib
import os
import random
import ROOT
import style
import sys


def testfit(nNLLs = 10,
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
    #varnames = ["sMELA_ggH", "D0-_dec", "Dcp_dec", "sMELA_VBF", "D0-_VBF", "Dcp_VBF", "sMELA_VH", "D0-_VH", "Dcp_VH"]
    if config.whichtemplates == "VBF_VBFdiscriminants":
        varnames = ["D0-_VBF", "Dcp_VBF"]
    else:
        varnames = ["sMELA_ggH", "D0-_dec", "Dcp_dec"]
    vars = {}

    for channel in channels:
        fs[channel] = ROOT.TFile.Open("workspaces/{0}_fa3_{1}_{2}_workspace{3}.root".format(str(config.whichtemplates), channel, 0, "_nobkg" if config.turnoffbkg else ""))
        ws[channel] = fs[channel].Get("workspace")
        pdfs[channel] = ws[channel].pdf("Cat_{0}_{1}_SumPDF".format(channel, 0))
        if fa3 is None:  #this is the first one
            fa3 = ws[channel].var("fa3_ggH")
            mu = ws[channel].var("mu")
            for varname in varnames:
                vars[varname] = ws[channel].var(varname)
                if not vars[varname]:
                    del vars[varname]

    one = ROOT.RooConstVar("one", "one", 1.0)
    TemplateName = "SumPDF"
    pdf = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(*pdfs.values()), ROOT.RooArgList(*([one]*len(pdfs))))

    if ntoys is None:
        ntoys = pdf.getNorm(ROOT.RooArgSet(*vars.values()))

    print "Number of toys:", ntoys

    ROOT.RooRandom.randomGenerator().SetSeed(config.seed)

    fa3.setRange(-1, 1)

    bincenters = [1.0*i/nbins * high + (1-(1.0*i)/nbins) * low for i in range(nbins+1)]

    graphcategories = (Category("ggH"), Category("VBF"))
    multigraphs = {category: ROOT.TMultiGraph() for category in graphcategories}
    transformx = {category: functools.partial(constants.convertfa3, categoryin=Category("ggH"), categoryout=category) for category in graphcategories}

    c1 = ROOT.TCanvas.MakeDefCanvas()
    averageNLL = ExtendedCounter()
    for j in range(nNLLs):
        mu.setVal(testmu)
        fa3.setVal(testfa3)

        data = pdf.generate(ROOT.RooArgSet(*vars.values()), ntoys)
        nll = pdf.createNLL(data)
        result = ExtendedCounter()
        for bincenter in bincenters:
            fa3.setVal(bincenter)
            result[bincenter] = nll.getVal()
        result *= 2
        averageNLL += result
        for category, multigraph in multigraphs.iteritems():
            graph = result.TGraph(transformx=transformx[category])
            graph.SetLineColor(17)
            multigraph.Add(graph)
        if (j+1) % 25 == 0 or (j+1) == nNLLs:
            print str(j+1) + " / " + str(nNLLs)

    averageNLL /= nNLLs
    print bincenters[-1], averageNLL[bincenters[-1]]

    try:
        os.makedirs(config.plotdir)
    except OSError:
        pass

    for category, multigraph in multigraphs.iteritems():
        graph = averageNLL.TGraph(transformx=transformx[category])
        graph.SetLineWidth(3)
        multigraph.Add(graph)

        multigraph.Draw("AC")
        multigraph.GetYaxis().SetTitle("-2#Deltaln L")
        multigraph.GetXaxis().SetTitle("(f_{a_{3}})_{%s}"%category)

        style.drawlines()

        [c1.SaveAs("%s/scan_fa3_%s=%s%s.%s" % (config.plotdir, category, transformx[category](testfa3), "",        format)) for format in ["png", "eps", "root", "pdf"]]

        multigraph.GetYaxis().SetRangeUser(0,1)

        [c1.SaveAs("%s/scan_fa3_%s=%s%s.%s" % (config.plotdir, category, transformx[category](testfa3), "_zoomed", format)) for format in ["png", "eps", "root", "pdf"]]

if __name__ == '__main__':
    fa3s = sys.argv[1:]
    if not fa3s:
        fa3s = [0, 1, .5, -.5]
    [testfit(
             testfa3=float(testfa3),
             ntoys = None
            ) for testfa3 in fa3s]
