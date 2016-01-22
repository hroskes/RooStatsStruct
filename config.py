from enums import *
import getpass

if getpass.getuser() == "hroskes":
    plotdirs = {
                WhichTemplates("ggH_2e2mu"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/2e2mu",
                WhichTemplates("ggH_allflavors"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/SEED/allflavors/",
               }
elif getpass.getuser() == "chmartin":
    plotdirs = {
                WhichTemplates("ggH_2e2mu"): "/afs/cern.ch/user/c/chmartin/www/Pheno/2e2mu/",
                WhichTemplates("ggH_allflavors"): "/afs/cern.ch/user/c/chmartin/www/Pheno/All/",
               }
else:
    raise ValueError("Who are you?  (see config.py)")



whichtemplates = WhichTemplates("ggH_2e2mu")
#whichtemplates = WhichTemplates("ggH_allflavors")



turnoffbkg = True


seed = 123456






plotdir = (plotdirs[whichtemplates] + ("/nobkg/" if turnoffbkg else "")).replace("SEED", str(seed))





#I want to get this from the templates, but I don't have time now
sigrates = {
            WhichTemplates("ggH_2e2mu"): 7.6807,
            WhichTemplates("ggH_allflavors"): 7.6807 + 3.0898 + 5.9471,
           }
bkgrates = {
            WhichTemplates("ggH_2e2mu"): 13.6519,   #8.8585 = qqZZ only
            WhichTemplates("ggH_allflavors"): 13.6519 + 5.9081 + 9.2487,   #8.8585 + 2.9364 + 7.6478 = qqZZ only
           }


sigrate = sigrates[whichtemplates]
bkgrate = 0 if turnoffbkg else bkgrates[whichtemplates]
