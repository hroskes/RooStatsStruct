import sys
sys.argv.insert(1, "-b")
import ROOT
del sys.argv[1]
import random
import style
import itertools

########################################
#parameters
testfa3 = -.5
varnames = ["Dcp_VBF", "D0-_VBF", "sMELA",]
########################################

f = ROOT.TFile.Open("fa3_0_2_0_workspace_nobkg.root")
w = f.Get("workspace")

fa3 = w.var("fa3")
fa3.setVal(testfa3)
pdf = w.pdf("Signal_0_2_0_SumPDF")

vars = {}
bins = {}
mins = {}
maxes = {}
for v in varnames:
    vars[v] = w.var(v)
    bins[v] = vars[v].getBins()
    mins[v] = vars[v].getMin()
    maxes[v] = vars[v].getMax()

header = "(%s)" % ", ".join(varnames)
print "=" * len(header)
print header
print "=" * len(header)

for bin in itertools.product(*(range(bins[v]) for v in varnames)):
    bin = {varnames[i]: bin[i] for i in range(len(varnames))}
    for v in varnames:
        vars[v].setVal((mins[v]*(bins[v]-bin[v]) + maxes[v]*bin[v]) / bins[v])

    print "(%s): %f" % (", ".join(str(vars[v].getVal()) for v in varnames), pdf.getVal())
