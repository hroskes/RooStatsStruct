from enums import *
import getpass
import os

if getpass.getuser() == "hroskes":
    plotdirs = {
                WhichTemplates("ggH_2e2mu"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/2e2mu",
                WhichTemplates("ggH_4e"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/4e",
                WhichTemplates("ggH_allflavors"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/allflavors/",
                WhichTemplates("VBF_VBFdiscriminants"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/VBF_VBFdiscriminants",
                WhichTemplates("VBF_VBFdecay"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/VBF_VBFdecay",
                WhichTemplates("VBF_g4power1"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/VBF_g4power1",
                WhichTemplates("VBF_g4power2"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/VBF_g4power2",
                WhichTemplates("VBF_g4power3"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/VBF_g4power3",
               }
elif getpass.getuser() == "chmartin":
    plotdirs = {
                WhichTemplates("ggH_2e2mu"): "/afs/cern.ch/user/c/chmartin/www/Pheno/2e2mu/",
                WhichTemplates("ggH_4e"): "/afs/cern.ch/user/c/chmartin/www/Pheno/4e/",
                WhichTemplates("ggH_allflavors"): "/afs/cern.ch/user/c/chmartin/www/Pheno/All/",
               }
else:
    raise ValueError("Who are you?  (see config.py)")



#whichtemplates = WhichTemplates("ggH_2e2mu")
#whichtemplates = WhichTemplates("ggH_4e")
#whichtemplates = WhichTemplates("ggH_allflavors")
#whichtemplates = WhichTemplates("VBF_VBFdiscriminants")
#whichtemplates = WhichTemplates("VBF_VBFdecay")
whichtemplates = WhichTemplates("VBF_g4power1")
#whichtemplates = WhichTemplates("VBF_g4power2")
#whichtemplates = WhichTemplates("VBF_g4power3")



turnoffbkg = True


seed = 987653





try:
    plotdir = (plotdirs[whichtemplates] + ("/nobkg/" if turnoffbkg else "")).replace("SEED", str(seed))
    if not os.path.isdir(plotdir):
        os.makedirs(plotdir)
except KeyError:
    raise KeyError("need to add folder for %s in config.py" % whichtemplates)
