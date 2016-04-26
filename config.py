from enums import *
import getpass
import os
import sys

if getpass.getuser() == "hroskes":
    plotdirs = {
                WhichTemplates(whichtemplates): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/%s"%whichtemplates
                    for whichtemplates in WhichTemplates.enumitems
               }
elif getpass.getuser() == "jroskes1@jhu.edu":
    plotdirs = {
                WhichTemplates(whichtemplates): "/scratch/users/jroskes1@jhu.edu/RooStatsStruct/plots/SEED/%s"%whichtemplates
                    for whichtemplates in WhichTemplates.enumitems
               }
elif getpass.getuser() == "chmartin":
    plotdirs = {
                WhichTemplates("ggH_2e2mu"): "/afs/cern.ch/user/c/chmartin/www/Pheno/2e2mu/",
                WhichTemplates("ggH_4e"): "/afs/cern.ch/user/c/chmartin/www/Pheno/4e/",
                WhichTemplates("ggH_allflavors"): "/afs/cern.ch/user/c/chmartin/www/Pheno/All/",
               }
elif getpass.getuser() == "ubuntu": #circle
    plotdirs = {
                WhichTemplates(whichtemplates): "%s/%s"%(os.environ["CIRCLE_ARTIFACTS"], whichtemplates)
                    for whichtemplates in WhichTemplates.enumitems
               }
else:
    raise ValueError("Who are you?  (see config.py)")



#whichtemplates = WhichTemplates("ggH_2e2mu")
#whichtemplates = WhichTemplates("ggH_4e")
#whichtemplates = WhichTemplates("ggH_allflavors")
#whichtemplates = WhichTemplates("VBF_nodecay")
#whichtemplates = WhichTemplates("VBF_DCPVBF")
#whichtemplates = WhichTemplates("VBF_g4power1")
#whichtemplates = WhichTemplates("VBF_g4power2")
#whichtemplates = WhichTemplates("VBF_g4power3")
#whichtemplates = WhichTemplates("VBF_1D_D0minus_VBF")
#whichtemplates = WhichTemplates("VBF_1D_D0minus_VBFdecay")
#whichtemplates = WhichTemplates("VBF_1D_DCP_VBF")
#whichtemplates = WhichTemplates("VBF_1D_DCP_VBFdecay")
#whichtemplates = WhichTemplates("VBF_1D_g4power0")
#whichtemplates = WhichTemplates("VBF_1D_g4power1")
#whichtemplates = WhichTemplates("VBF_1D_g4power2")
#whichtemplates = WhichTemplates("VBF_1D_g4power3")
#whichtemplates = WhichTemplates("VBF_1D_g4power1_prime")
#whichtemplates = WhichTemplates("VBF_1D_g4power2_prime")
#whichtemplates = WhichTemplates("VBF_1D_g4power3_prime")
#whichtemplates = WhichTemplates("VBF_g4power1_prime")
#whichtemplates = WhichTemplates("VBF_g4power2_prime")
#whichtemplates = WhichTemplates("VBF_g4power3_prime")

try:
    if sys.argv[1]: whichtemplates = WhichTemplates(sys.argv[1])
except IndexError:
    pass


turnoffbkg = True


seed = 987654





try:
    plotdir = (plotdirs[whichtemplates] + ("/nobkg/" if turnoffbkg else "")).replace("SEED", str(seed))
    if not os.path.isdir(plotdir):
        os.makedirs(plotdir)
except KeyError:
    raise KeyError("need to add folder for %s in config.py" % whichtemplates)
