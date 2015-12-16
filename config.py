from enums import *

plotdirs = {
            WhichTemplates("ggH_2e2mu"): "plots_ggH_2e2mu/",
            WhichTemplates("ggH_allflavors"): "plots_ggH_allflavors/",
           }

whichtemplates = WhichTemplates("ggH_2e2mu")
#whichtemplates = WhichTemplates("ggH_allflavors")





plotdir = plotdirs[whichtemplates]



turnoffbkg = False
