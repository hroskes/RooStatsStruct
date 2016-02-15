import config
from enums import *
import os
import rootlog
ROOT = rootlog.thefakeroot



def template(*args):
    return templategetters[config.whichtemplates](*args).template()




basedirVBF = "/afs/cern.ch/work/h/hroskes/Summer2015_VBF/maketemplates/step6_templates"
basedirggH_fromMeng = "templates/ggH_fromMeng_normalized/"

class BaseTemplateGetter(object):

    emptytemplates = {}

    def __init__(self, *args):
        self.channel, self.on_off, self.category = None, None, None
        for arg in args:
            found = 0
            try:
                self.category = Category(arg)
                found += 1
            except ValueError:
                pass
            try:
                self.channel = Channel(arg)
                found += 1
            except ValueError:
                pass
            try:
                self.on_off = OnOffShell(arg)
                found += 1
            except ValueError:
                pass
            try:
                self.templatetype = TemplateType(arg)
                found += 1
            except ValueError:
                pass

            if found > 1:
                raise ValueError("Argument %s to TemplateFile is ambiguous" % arg)

        self.fileandname()
        self.setisempty()

    def template(self):
        tfile = ROOT.TFile.Open(self.file)
        if not tfile:
            raise IOError(self.file + " does not exist!")
        template = tfile.Get(self.name)
        if not template:
            raise IOError(self.file + " does not contain " + self.name + "!")

        if self.empty or (config.turnoffbkg and self.templatetype == "qqZZ"):

            todelete = []
            for a in self.emptytemplates:
                if not self.emptytemplates[a]:
                    todelete.append(a)
            for a in todelete:
                del self.emptytemplates[a]

            if (self.file, self.name) not in self.emptytemplates:  #empty template with the same bins as the given template from file and name
                try:    #TH3?
                    self.emptytemplates[(self.file, self.name)] = type(template)(  #create a new histogram to be the empty one
                        "empty%i"%len(self.emptytemplates),
                        "empty",
                        template.GetNbinsX(), template.GetXaxis().GetXmin(), template.GetXaxis().GetXmax(),
                        template.GetNbinsY(), template.GetYaxis().GetXmin(), template.GetYaxis().GetXmax(),
                        template.GetNbinsZ(), template.GetZaxis().GetXmin(), template.GetZaxis().GetXmax(),
                    )
                except TypeError:
                    try:    #TH2?
                        self.emptytemplates[(self.file, self.name)] = type(template)(  #create a new histogram to be the empty one
                            "empty"+len(self.emptytemplates),
                            "empty",
                            template.GetNbinsX(), template.GetXaxis().GetXmin(), template.GetXaxis().GetXmax(),
                            template.GetNbinsY(), template.GetYaxis().GetXmin(), template.GetYaxis().GetXmax(),
                        )
                    except TypeError:    #TH1?
                        self.emptytemplates[(self.file, self.name)] = type(template)(  #create a new histogram to be the empty one
                            "empty"+len(self.emptytemplates),
                            "empty",
                            template.GetNbinsX(), template.GetXaxis().GetXmin(), template.GetXaxis().GetXmax(),
                        )
            template = self.emptytemplates[(self.file, self.name)]

        return template

class TemplateGetter_ggH(BaseTemplateGetter):
    def fileandname_ggH(self):
        if self.templatetype == "SM":
            self.file = os.path.join(basedirggH_fromMeng, "%s_templates.root" % self.channel)
            self.name = "template0PlusAdapSmoothMirror"
        elif self.templatetype == "PS":
            self.file = os.path.join(basedirggH_fromMeng, "%s_templates.root" % self.channel)
            self.name = "template0MinusAdapSmoothMirror"
        elif self.templatetype == "interference":
            self.file = os.path.join(basedirggH_fromMeng, "%s_templates.root" % self.channel)
            self.name = "templateIntAdapSmoothMirror"
        elif self.templatetype == "qqZZ":
            self.file = os.path.join(basedirggH_fromMeng, "%s_templates_bkg.root" % self.channel)
            self.name = "template_qqZZ"
        else:
            raise ValueError("Bad templatetype! %s" % self.templatetype)

class TemplateGetter_ggHonly(TemplateGetter_ggH):
    def setisempty(self):
        if self.on_off == "onshell" and self.category == "ggH":
            self.empty = False
        else:
            self.empty = True

    def fileandname(self):
        return self.fileandname_ggH()

class TemplateGetter_ggHonly_oneflavor(TemplateGetter_ggHonly):
    def setisempty(self):
        super(TemplateGetter_ggHonly_oneflavor, self).setisempty()
        if self.channel != self.theflavor:
            self.empty = True

class TemplateGetter_ggHonly_2e2mu(TemplateGetter_ggHonly_oneflavor):
    theflavor = "2e2mu"

class TemplateGetter_ggHonly_4e(TemplateGetter_ggHonly_oneflavor):
    theflavor = "4e"




class TemplateGetter_VBFonly(BaseTemplateGetter):
    """
    subclass this together with a class that provides the template files and names
    """
    def setisempty(self):
        if self.on_off == "onshell" and self.category == "VBF":
            self.empty = False
        else:
            self.empty = True

    def fileandname(self):
        return self.fileandname_VBF()

class TemplateGetter_VBFdiscriminants(BaseTemplateGetter):
    """
    Dbkg from decay, but D0- and DCP from VBF alone with no decay info
    """
    def fileandname_VBF(self):
        self.name = "template_VBF_alone"

        if self.templatetype == "SM":
            self.file = os.path.join(basedirVBF, "VBF0+_%s.root" % self.channel)
        elif self.templatetype == "PS":
            self.file = os.path.join(basedirVBF, "VBF0-_%s.root" % self.channel)
        elif self.templatetype == "fa30.5":
            self.file = os.path.join(basedirVBF, "VBFfa30.5_%s.root" % self.channel)
        elif self.templatetype == "qqZZ":
            self.file = os.path.join(basedirVBF, "VBF0+_%s.root" % self.channel)
            assert config.turnoffbkg

class TemplateGetter_VBFonly_VBFdiscriminants(TemplateGetter_VBFonly, TemplateGetter_VBFdiscriminants):
    pass

templategetters = {
    WhichTemplates("ggH_2e2mu"): TemplateGetter_ggHonly_2e2mu,
    WhichTemplates("ggH_4e"): TemplateGetter_ggHonly_4e,
    WhichTemplates("ggH_allflavors"): TemplateGetter_ggHonly,
    WhichTemplates("VBF_VBFdiscriminants"): TemplateGetter_VBFonly_VBFdiscriminants,
}
