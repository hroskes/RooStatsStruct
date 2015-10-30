import MakePDF

templatedir = "/afs/cern.ch/work/h/hroskes/Summer2015_VBF/makeTemplates/templates/"
channelnames = {
    0: "2e2mu",
    #1: "4mu",
    #2: "4e",
}

class MakePDF_Heshy(MakePDF.MakePDF):

    def __init__(self):
        for channel in channelnames:
            self.makeWorkspace(channel)

    def makeWorkspace(self, channelCode):
        #categoryCode = 2
        templateFile = templatedir + channelnames[channelCode] + "_templates.root"
        templateFile_bkg = templatedir + channelnames[channelCode] + "_templates_bkg.root"
        on_off_Code = 0
        templateName_SM = "template_VBFscalar"
        templateName_PS = "template_VBFpseudoscalar"
        templateName_mix = "template_VBFinterference"
        templateName_bkg = "template_qqZZ"
        MakePDF.MakePDF.makeWorkspace(self, channelCode, templateFile, templateFile_bkg, on_off_Code, templateName_SM, templateName_PS, templateName_mix, templateName_bkg)

if __name__ == '__main__':
    MakePDF.turnoffbkg = True
    MakePDF_Heshy()
    MakePDF.ROOT.reset()
    MakePDF.turnoffbkg = False
    MakePDF_Heshy()
