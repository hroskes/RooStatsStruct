import config
import extendedcounter
import rootlog
ROOT = rootlog.thefakeroot
import ROOT as therealROOT
import style

def plotwithcombine(filenameroot, combinefilenameC, newsaveas):

    #extract the multigraph from the file
    f = ROOT.TFile.Open(filenameroot)
    c1 = f.GetListOfKeys().At(0).ReadObj()
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
        print ext
        print newsaveas + ext
        print c1.SaveAs(newsaveas + ext)

    f.Close()

if __name__ == '__main__':
    plotwithcombine(config.plotdir + "scan_fa3=0.0.root", "plotsfromcombine/fa3=0.0_2e2mu_qqZZ.C", "test.png")
