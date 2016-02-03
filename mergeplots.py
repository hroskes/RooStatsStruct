import config
import extendedcounter
import rootlog
ROOT = rootlog.thefakeroot
import ROOT as therealROOT
import style
import os

def mergeplots(newsaveas, *rootfiles):
    if not rootfiles:
        raise ValueError("No rootfiles to merge!")
    isdir = [os.path.isdir(a) for a in rootfiles]
    if any(isdir) != all(isdir):
        raise ValueError("mergeplots needs all input files to be either ROOT files or directories!")
    if all(isdir):
        try:
            os.makedirs(newsaveas)
        except OSError:
            if not os.path.isdir(newsaveas):
                raise ValueError(newsaveas + " is not a directory!")

        filenames = []
        for dir in rootfiles:
            filenames.append(set([f for f in os.listdir(dir) if f.endswith(".root")]))
        filenames = set.intersection(*filenames)

        for filename in filenames:
            mergeplots(newsaveas + "/" + filename, *[dir + "/" + filename for dir in rootfiles])

        return

    f1 = None
    c1 = None
    mergedmultigraph = None
    averageNLL = extendedcounter.ExtendedCounter()
    ngraphs = 0
    addedcombine = False
    for rootfile in rootfiles:
        f = ROOT.TFile(rootfile)
        if not f:
            raise IOError("no file " + rootfile + "!")
        c = f.GetListOfKeys().At(0).ReadObj()
        if not c or type(c) != ROOT.TCanvas:
            raise IOError("no canvas in file " + rootfile + "!")
        multigraph = c.GetListOfPrimitives().At(1)

        if c1 is None and mergedmultigraph is None:
            f1 = f
            c1 = c
            mergedmultigraph = multigraph
            for g in multigraph.GetListOfGraphs():
                if g.GetLineColor() == 1:
                    multigraph.RecursiveRemove(g)
                elif g.GetLineColor() == 2:
                    addedcombine = True
                elif g.GetLineColor() == 17:
                    averageNLL += extendedcounter.makefromTGraph(g)
                    ngraphs += 1
                else:
                    raise ValueError("File " + rootfile + " has a graph with color %i.  Don't know what to do with it." % g.GetLineColor())

        else:
            for g in multigraph.GetListOfGraphs():
                if g.GetLineColor() == 1:
                    pass
                elif g.GetLineColor() == 2:
                    if not addedcombine:
                        mergedmultigraph.Add(g)
                        addedcombine = True
                elif g.GetLineColor() == 17:
                    averageNLL += extendedcounter.makefromTGraph(g)
                    ngraphs += 1
                    mergedmultigraph.Add(g)
                else:
                    raise ValueError("File " + rootfile + " has a graph with color %i.  Don't know what to do with it." % g.GetLineColor())

    averageNLL /= ngraphs
    graph = averageNLL.TGraph()
    graph.SetLineWidth(3)
    mergedmultigraph.Add(graph)
    c1 = ROOT.TCanvas()
    mergedmultigraph.Draw("AC")

    mergedmultigraph.GetYaxis().SetTitle("-2#Deltaln L")
    mergedmultigraph.GetXaxis().SetTitle("f_{a_{3}}")
    if "zoomed" in newsaveas:
        mergedmultigraph.GetYaxis().SetRangeUser(0,1)
    style.drawlines()

    exts = (".eps", ".png", ".root", ".pdf")
    for ext in exts:
        newsaveas = newsaveas.replace(ext, "")
    for ext in exts:
        c1.SaveAs(newsaveas + ext)

if __name__ == '__main__':
    mergeplots("/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/123456+234567/2e2mu/", "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/234567/2e2mu/", "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/123456/2e2mu/withcombine/")
    mergeplots("/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/123456+234567/2e2mu/nobkg/", "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/234567/2e2mu/nobkg/", "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/123456/2e2mu/nobkg/withcombine/")
    mergeplots("/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/123456+234567/allflavors/", "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/234567/allflavors/", "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/123456/allflavors/withcombine/")
    mergeplots("/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/123456+234567/allflavors/nobkg/", "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/234567/allflavors/nobkg/", "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/123456/allflavors/nobkg/withcombine/")
