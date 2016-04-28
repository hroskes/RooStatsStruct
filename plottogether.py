from collections import namedtuple
import ROOT
import style

LineOnGraph = namedtuple("LineOnGraph", "filename title color")

def plottogether(*lines):
    mg = ROOT.TMultiGraph("mg", "mg")
    graphs = []
    legend = ROOT.TLegend(.6, .7, .9, .9)
    for line in lines:
        f = ROOT.TFile(line.filename)
        if not f:
            raise IOError("no file " + line.filename + "!")
        c1 = f.GetListOfKeys().At(0).ReadObj()
        if not c1 or type(c1) != ROOT.TCanvas:
            raise IOError("no canvas in file " + line.filename + "!")
        multigraph = c1.GetListOfPrimitives().At(1)
        graph = multigraph.GetListOfGraphs()[-1].Clone("")
        graphs.append(graph)
        graph.SetLineColor(line.color)
        legend.AddEntry(graph, line.title,"l")
        mg.Add(graph)

    c = ROOT.TCanvas()
    mg.Draw("AC")
    legend.Draw()
    c.SaveAs("test.png")

if __name__ == "__main__":
    plottogether(
                 LineOnGraph("~/www/VBF/Summer2015/scans/987654/VBF_g4power1/nobkg/scan_fa3_VBF=0.0.root", "D_g4power1", 1),
                 LineOnGraph("~/www/VBF/Summer2015/scans/987654/VBF_g4power1_prime/nobkg/scan_fa3_VBF=0.0.root", "D_g4power1_prime", 2),
                 LineOnGraph("~/www/VBF/Summer2015/scans/987654/VBF_DCPVBF/nobkg/scan_fa3_VBF=0.0.root", "D_CP_VBF", 3),
                )
