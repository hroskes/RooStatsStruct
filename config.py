from enums import *
import getpass

if getpass.getuser() == "hroskes":
    plotdirs = {
                WhichTemplates("ggH_2e2mu"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/",
                WhichTemplates("ggH_allflavors"): "/afs/cern.ch/user/h/hroskes/www/VBF/Summer2015/scans/ggH_allflavors/",
               }
elif getpass.getuser() == "chmartin":
    plotdirs = {
                WhichTemplates("ggH_2e2mu"): "???",
                WhichTemplates("ggH_allflavors"): "???",
               }
else:
    raise ValueError("Who are you?  (see config.py)")



whichtemplates = WhichTemplates("ggH_2e2mu")
#whichtemplates = WhichTemplates("ggH_allflavors")



turnoffbkg = True







plotdir = plotdirs[whichtemplates] + ("/nobkg/" if turnoffbkg else "")
