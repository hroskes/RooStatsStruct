import config
import extendedcounter
import rootlog
ROOT = rootlog.thefakeroot
import ROOT as therealROOT
import style
import os

def plotwithcombine(filenameroot, combinefilenameC, newsaveas):

    #extract the multigraph from the file
    f = ROOT.TFile.Open(filenameroot)
    if not f:
        raise IOError("no file " + filenameroot + "!")
    c1 = f.GetListOfKeys().At(0).ReadObj()
    if not c1 or type(c1) != ROOT.TCanvas:
        raise IOError("no canvas in file " + filenameroot + "!")
    multigraph = c1.GetListOfPrimitives().At(1)

    #get the combine TGraph from the .C file
    combinecounter = extendedcounter.makefromcombineC(combinefilenameC)
    combinegraph = combinecounter.TGraph()
    combinegraph.SetLineColor(2)
    combinegraph.SetLineWidth(3)
    multigraph.Add(combinegraph)

    exts = (".eps", ".png", ".root", ".pdf")
    for ext in exts:
        newsaveas = newsaveas.replace(ext, "")
    for ext in exts:
        c1.SaveAs(newsaveas + ext)

    f.Close()

if __name__ == '__main__':
    newsaveasdir = config.plotdir + "/withcombine/"
    try:
        os.makedirs(newsaveasdir)
    except OSError:
        pass

    for fa3 in [0., 1., 0.5, -0.5]:
        filenameroot = config.plotdir + "/scan_fa3=%s.root" % fa3

        combinefilenameC = "plotsfromcombine/fa3=%s_" % fa3
        if config.whichtemplates == "ggH_2e2mu":
            combinefilenameC += "2e2mu_"
        elif config.whichtemplates == "ggH_allflavors":
            pass
        else:
            raise ValueError("No combine plots for %s" % config.whichtemplates)

        if config.turnoffbkg:
            combinefilenameC += "nobkg"
        else:
            combinefilenameC += "qqZZ"

        combinefilenameC += ".C"

        newsaveas = newsaveasdir + "/scan_fa3=%s" % fa3

        plotwithcombine(filenameroot, combinefilenameC, newsaveas)
