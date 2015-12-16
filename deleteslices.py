import os
import config

for a in os.listdir(config.plotdir):
    if "slices" in a and os.path.isdir(config.plotdir + "/" + a):
        for b in os.listdir(config.plotdir + "/" + a):
            if any(c in b for c in (".png", ".eps", ".root", ".pdf")):
                os.remove(config.plotdir + "/" + a + "/" + b)
