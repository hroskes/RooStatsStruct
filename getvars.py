#use from the python shell, from getvars.py import *

import loadlib
import rootlog
ROOT = rootlog.fakeroot()

f = ROOT.TFile.Open("workspaces/ggH_2e2muonly_fa3_0_0_workspace.root")
w = f.Get("workspace")

dcp = w.var("D0-_dec")
d0m = w.var("sMELA_ggH")
dbkg = w.var("Dcp_dec")
