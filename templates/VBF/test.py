import constants
from contextlib import closing
import ROOT
import style

histname = "D_g4power1_VBFdecay"

def TFile(*args):
    f = ROOT.TFile(*args)
    f.close = f.Close
    return closing(f)

def gethorig(fa3):
    if fa3 == 0:
        a = "0+"
    elif fa3 == 1:
        a = "0-"
    else:
        a = "fa3%s"%fa3

    with TFile("VBF%s_2e2mu.root"%a) as f:
        h = f.Get(histname)
        if h: h.SetDirectory(0)

    return h


def geth(g1, g4):

    with TFile("VBFfinal_2e2mu.root") as f:
        T = [f.Get("%s_g1%ig4%i" % (histname, 4-i, i)) for i in range(5)]

        h = T[0].Clone()
        h.Reset()
        h.SetDirectory(0)

        for i in range(5):
            print "   ", g1**(4-i) * g4**i
            h.Add(T[i], g1**(4-i) * g4**i)

        return h

def compare(fa3):

    print fa3

    if abs(fa3) == 0: g1, g4 = 1, 0
    if abs(fa3) == 1: g1, g4 = 0, (constants.JHU_XS_a1_VBF * constants.JHU_XS_a1_ggH / (constants.JHU_XS_a3_VBF * constants.JHU_XS_a3_ggH))**.25
    if abs(fa3) == .5: g1, g4 = 0.83806711453, 0.249726416396
    if abs(fa3) == .25: g1, g4 = 0.92955527457, 0.159919078204
    if abs(fa3) == .9: g1, g4 = 0.54637026335, 0.488420624767

    if fa3 < 0: g4 *= -1

    h = geth(g1, g4)
    horig = gethorig(fa3)

    h.SetLineColor(1)
    if horig: horig.SetLineColor(2)

    print " ", h.Integral("width"), horig.Integral("width")
    print " ", h.GetMinimum(), horig.GetMinimum()

    hs = ROOT.THStack("", "")
    hs.Add(h)
    if horig: hs.Add(horig)
    c1 = ROOT.TCanvas()
    hs.Draw("histnostack")
    for ext in "png", "eps", "root", "pdf":
        c1.SaveAs("~/www/TEST/test_%f.%s"%(fa3, ext))

if __name__ == "__main__":
    for a in 0, 1, .5, -.5, .25, -.9:
        compare(a)
