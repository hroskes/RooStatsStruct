#use from the python shell, from getvars.py import *

import config
import loadlib
import rootlog
from enums import *
ROOT = rootlog.fakeroot()

fs, ws, pdfs = {}, {}, {}
fa3 = None

for channel in channels:
    fs[channel] = ROOT.TFile.Open("workspaces/{0}_fa3_{1}_{2}_workspace{3}.root".format(str(config.whichtemplates), channel, 0, "_nobkg" if config.turnoffbkg else ""))
    ws[channel] = fs[channel].Get("workspace")
    pdfs[channel] = ws[channel].pdf("Cat_{0}_{1}_SumPDF".format(channel, 0))
    if fa3 is None:  #this is the first one
        fa3 = ws[channel].var("fa3_ggH")
        mu = ws[channel].var("mu")
        sMELA_ggH = ws[channel].var("sMELA_ggH")
        D0minus_ggH = ws[channel].var("D0-_dec")
        DCP_ggH = ws[channel].var("Dcp_dec")
        sMELA_VBF = ws[channel].var("sMELA_VBF")
        D0minus_VBF = ws[channel].var("D0-_VBF")
        DCP_VBF = ws[channel].var("Dcp_VBF")
        sMELA_VH = ws[channel].var("sMELA_VH")
        D0minus_VH = ws[channel].var("D0-_VH")
        DCP_VH = ws[channel].var("Dcp_VH")

one = ROOT.RooConstVar("one", "one", 1.0)
TemplateName = "SumPDF"
pdf = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(*pdfs.values()), ROOT.RooArgList(*([one]*len(pdfs))))

discriminants = ROOT.RooArgSet(*[globals()["%s_%s" % (a,b)] for a in ("D0minus", "DCP", "sMELA") for b in ("ggH", "VBF", "VH")])
pdfnorm = pdf.createIntegral(discriminants)
