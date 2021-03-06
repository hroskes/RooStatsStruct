import config
import constants
from enums import *
from extendedcounter import *
import functools
from getvars import discriminants, mu, fa3, pdf
import loadlib
import os
import random
import ROOT
import style
import sys


def testfit(nNLLs = 100,
            nbins = 1000,
            low = -1,
            high = 1,
            testmu = 1,
            testfa3 = 0,
            zoomed = False,
            ntoys = None,  #default if None: BKGrate+SMrate
           ):

    vars = []
    for var in discriminants:
        if var.GetTitle():
            vars.append(var)

    fa3.setVal(testfa3)

    if ntoys is None:
        ntoys = pdf.getNorm(ROOT.RooArgSet(*vars))

    print "Number of toys:", ntoys

    ROOT.RooRandom.randomGenerator().SetSeed(config.seed)

    bincenters = [1.0*i/nbins * high + (1-(1.0*i)/nbins) * low for i in range(nbins+1)]

    graphcategories = (Category("HZZ"), Category("VBF"))
    multigraphs = {category: ROOT.TMultiGraph() for category in graphcategories}
    transformx = {category: functools.partial(constants.convertfa3, categoryin=Category("HZZ"), categoryout=category) for category in graphcategories}

    c1 = ROOT.TCanvas.MakeDefCanvas()
    averageNLL = ExtendedCounter()
    for j in range(nNLLs):
        mu.setVal(testmu)
        fa3.setVal(testfa3)

        data = pdf.generate(ROOT.RooArgSet(*vars), ntoys)
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
    fa3s = sys.argv[2:]
    if not fa3s:
        fa3s = [0, 1, .5, -.5, constants.convertfa3(.5, "VBF", "HZZ"), constants.convertfa3(-.5, "VBF", "HZZ")]
    [testfit(
             testfa3=float(testfa3),
             ntoys = None
            ) for testfa3 in fa3s]
