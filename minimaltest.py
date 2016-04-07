import ROOT
import sys

h = ROOT.TH1F("h", "h", 6, -1, 1)
h.Fill(-1, .25)
h.Fill(0, .75)

one = ROOT.RooConstVar("one", "one", 1)



var1 = ROOT.RooRealVar("var1", "var1", 0, -1, 1)
arglist1 = ROOT.RooArgList(var1)
argset1 = ROOT.RooArgSet(var1)

datahist1 = ROOT.RooDataHist("datahist1", "datahist1", arglist1, h)
histfunc1 = ROOT.RooHistFunc("histfunc1", "histfunc1", argset1, datahist1)
sumpdf1 = ROOT.RooRealSumPdf("sumpdf1", "sumpdf1", ROOT.RooArgList(histfunc1), ROOT.RooArgList(one))


var2 = ROOT.RooRealVar("var2", "var2", 0, -1, 1)
arglist2 = ROOT.RooArgList(var2)
argset2 = ROOT.RooArgSet(var2)

datahist2 = ROOT.RooDataHist("datahist2", "datahist2", arglist2, h)
histfunc2 = ROOT.RooHistFunc("histfunc2", "histfunc2", argset2, datahist2)
sumpdf2 = ROOT.RooRealSumPdf("sumpdf2", "sumpdf2", ROOT.RooArgList(histfunc2), ROOT.RooArgList(one))





sumsumpdf = ROOT.RooRealSumPdf("sumsumpdf", "sumsumpdf", ROOT.RooArgList(sumpdf1, sumpdf2), ROOT.RooArgList(one, one))



names = [a.GetName() for a in histfunc1, sumpdf1, histfunc2, sumpdf2, sumsumpdf]
values = [
          histfunc1.createIntegral(argset1).getVal(),
          sumpdf1.createIntegral(argset1).getVal(),
          histfunc2.createIntegral(argset2).getVal(),
          sumpdf2.createIntegral(argset2).getVal(),
          sumsumpdf.createIntegral(ROOT.RooArgSet(var1, var2)).getVal(),
         ]



w = ROOT.RooWorkspace("workspace","workspace")
getattr(w, 'import')(sumsumpdf, ROOT.RooFit.RecycleConflictNodes())
w.writeToFile("tmp.root")

print ("{:>12}"*len(names)).format(*names)
print ("{:12.5f}"*len(values)).format(*values)
#print h.Integral("width"), datahist.sum(True), histfunc.createIntegral(argset).getVal(), sumpdf.expectedEvents(argset), sumsumpdf.expectedEvents(argset) if sumsum else ""

del h, one, var1, arglist1, argset1, datahist1, histfunc1, sumpdf1, var2, arglist2, argset2, datahist2, histfunc2, sumpdf2, sumsumpdf, w

f = ROOT.TFile("tmp.root")
w = f.Get("workspace")
objects = {name: w.obj(name) for name in names}
var1 = w.obj("var1")
var2 = w.obj("var2")
arglist1 = ROOT.RooArgList(var1)
argset1 = ROOT.RooArgSet(var1)
arglist2 = ROOT.RooArgList(var2)
argset2 = ROOT.RooArgSet(var2)

values = [
          objects["histfunc1"].createIntegral(argset1).getVal(),
          objects["sumpdf1"].createIntegral(argset1).getVal(),
          objects["histfunc2"].createIntegral(argset2).getVal(),
          objects["sumpdf2"].createIntegral(argset2).getVal(),
          objects["sumsumpdf"].createIntegral(ROOT.RooArgSet(var1, var2)).getVal(),
         ]

print ("{:12.5f}"*len(values)).format(*values)
