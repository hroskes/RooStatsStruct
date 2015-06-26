import ROOT

def style():
    ROOT.gStyle.SetCanvasColor(0);
    ROOT.gStyle.SetCanvasBorderMode(0);
    ROOT.gStyle.SetCanvasBorderSize(2);
    ROOT.gStyle.SetPadTickX(1);
    ROOT.gStyle.SetPadTickY(1);
    ROOT.gStyle.SetFrameFillStyle(0);
    ROOT.gStyle.SetFrameBorderMode(0);

def drawlines():
    line68 = ROOT.TLine()
    line68.SetLineStyle(9)
    line68.DrawLine(-1,1,1,1)
    line95 = ROOT.TLine()
    line95.SetLineStyle(9)
    line95.SetLineColor(4)
    line95.DrawLine(-1,3.84,1,3.84)
    print line95

    oneSig = ROOT.TPaveText(0.18,0.16,0.28,0.19,"NDC");
    oneSig.SetFillColor(0);
    oneSig.SetFillStyle(0);
    oneSig.SetTextFont(42);
    oneSig.SetBorderSize(0);
    oneSig.AddText("68\% CL");
    oneSig.Draw();

    twoSig = ROOT.TPaveText(0.18,0.24,0.28,0.27,"NDC");
    twoSig.SetFillColor(0);
    twoSig.SetFillStyle(0);
    twoSig.SetTextFont(42);
    twoSig.SetBorderSize(0);
    twoSig.AddText("95\% CL");
    twoSig.Draw();
