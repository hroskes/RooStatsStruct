import ROOT


templates = """
template_decay_allevents
template_notVBF
template_VBF_alone
template_VBF_DCP_VBF
template_VBF_g4power1
template_VBF_g4power2
template_VBF_g4power3
template_decay_allevents_2D
template_notVBF_2D
template_VBF_alone_2D
template_VBF_DCP_VBF_2D
template_VBF_g4power1_2D
template_VBF_g4power2_2D
template_VBF_g4power3_2D
D_bkg_0plus
D_0minus_decay
D_CP_decay
D_bkg_0plus_notVBF
D_0minus_decay_notVBF
D_CP_decay_notVBF
D_0minus_VBF
D_CP_VBF
D_0minus_VBFdecay
D_g4power1_VBFdecay
D_g4power2_VBFdecay
D_g4power3_VBFdecay
""".split()

f = ROOT.TFile("VBF0+_2e2mu.root")
for t in templates:
    h = f.Get(t)
    print "{:30}{:30}{:30}".format(t, h.GetBinContent(0), h.GetBinContent(h.GetNbinsX()+1))
