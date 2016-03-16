import constants
from contextlib import closing
import ROOT
import style

def TFile(*args):
    f = ROOT.TFile(*args)
    f.close = f.Close
    return closing(f)

def gethorig(fa3):
    if fa3 == 0:
        a = "0+"
    elif fa3 == 1:
        a = "0-"
    elif fa3 in [.5, -.5, .25]:
        a = "fa3%s"%fa3

    with TFile("VBF%s_2e2mu.root"%a) as f:
        h = f.Get("D_g4power1_VBFdecay")
        h.SetDirectory(0)

    return h


def geth(g1, g4):

    with TFile("VBFfinal_2e2mu.root") as f:
        T = [f.Get("D_g4power1_VBFdecay_g1%ig4%i" % (4-i, i)) for i in range(5)]

        h = T[0].Clone()
        h.Reset()
        h.SetDirectory(0)

        for i in range(5):
            print "   ", g1**(4-i) * g4**i
            h.Add(T[i], g1**(4-i) * g4**i)

        return h

def compare(fa3):

    print fa3

    if fa3 == 0: g1, g4 = 1, 0
    if fa3 == 1: g1, g4 = 0, (constants.JHU_XS_a1_VBF * constants.JHU_XS_a1_ggH / (constants.JHU_XS_a3_VBF * constants.JHU_XS_a3_ggH))**.25
    if fa3 == .5: g1, g4 = 1/2**.25, (constants.JHU_XS_a1_VBF * constants.JHU_XS_a1_ggH / (constants.JHU_XS_a3_VBF * constants.JHU_XS_a3_ggH))**.25 / 2**.25
    if fa3 == -.5: g1, g4 = 1, -(constants.JHU_XS_a1_VBF * constants.JHU_XS_a1_ggH / (constants.JHU_XS_a3_VBF * constants.JHU_XS_a3_ggH))**.25
    if fa3 == .25: g1, g4 = 1, (constants.JHU_XS_a1_VBF * constants.JHU_XS_a1_ggH / (3 * constants.JHU_XS_a3_VBF * constants.JHU_XS_a3_ggH))**.25

    h = geth(g1, g4)
    horig = gethorig(fa3)

    h.SetLineColor(1)
    horig.SetLineColor(2)

    hs = ROOT.THStack("hs", horig.GetTitle())
    hs.Add(h)
    hs.Add(horig)
    c1 = ROOT.TCanvas()
    hs.Draw("histnostack")
    c1.SaveAs("~/www/TEST/test_%f.png"%fa3)

if __name__ == "__main__":
    for a in 0, 1, .5, -.5, .25:
        compare(a)
