from enums import *
import rootlog
ROOT = rootlog.fakeroot()



def template(*args):
    return templategetters[config.whichtemplates](*args).template()




basedir = "/afs/cern.ch/work/h/hroskes/Summer2015_VBF/makeTemplates/templates/"
basedirmeng = "/afs/cern.ch/work/x/xiaomeng/public/forChris/"

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

    def template(self):
        tfile = ROOT.TFile.Open(self.file)
        if not tfile:
            raise IOError(self.file + " does not exist!")
        template = tfile.Get(self.name)
        print template
        if not template:
            raise IOError(self.file + " does not contain " + self.name + "!")

        if self.empty:

            todelete = []
            for a in self.emptytemplates:
                if not self.emptytemplates[a]:
                    todelete.append(a)
            for a in todelete:
                del self.emptytemplates[a]

            if (self.file, self.name) not in self.emptytemplates:  #empty template with the same bins as the given template from file and name
                try:    #TH3?
                    self.emptytemplates[(self.file, self.name)] = template.__class__(  #create a new histogram to be the empty one
                        "empty%i"%len(self.emptytemplates),
                        "empty",
                        template.GetNbinsX(), template.GetXaxis().GetXmin(), template.GetXaxis().GetXmax(),
                        template.GetNbinsY(), template.GetYaxis().GetXmin(), template.GetYaxis().GetXmax(),
                        template.GetNbinsZ(), template.GetZaxis().GetXmin(), template.GetZaxis().GetXmax(),
                    )
                except TypeError:
                    try:    #TH2?
                        self.emptytemplates[(self.file, self.name)] = template.__class__(  #create a new histogram to be the empty one
                            "empty"+len(self.emptytemplates),
                            "empty",
                            template.GetNbinsX(), template.GetXaxis().GetXmin(), template.GetXaxis().GetXmax(),
                            template.GetNbinsY(), template.GetYaxis().GetXmin(), template.GetYaxis().GetXmax(),
                        )
                    except TypeError:    #TH1?
                        self.emptytemplates[(self.file, self.name)] = template.__class__(  #create a new histogram to be the empty one
                            "empty"+len(self.emptytemplates),
                            "empty",
                            template.GetNbinsX(), template.GetXaxis().GetXmin(), template.GetXaxis().GetXmax(),
                        )
            template = self.emptytemplates[(self.file, self.name)]

        return template
        

class TemplateGetter_ggHonly_2e2mu(BaseTemplateGetter):
    def fileandname(self):
        if self.on_off == "onshell" and self.category == "ggH" and self.channel == "2e2mu":
            self.empty = False
        else:
            self.empty = True

        if self.templatetype == "SM":
            self.file = basedirmeng + "%s_fa3Adap_new.root" % self.channel
            self.name = "template0PlusAdapSmoothMirror"
        elif self.templatetype == "PS":
            self.file = basedirmeng + "%s_fa3Adap_new.root" % self.channel
            self.name = "template0MinusAdapSmoothMirror"
        elif self.templatetype == "interference":
            self.file = basedirmeng + "%s_fa3Adap_new.root" % self.channel
            self.name = "templateIntAdapSmoothMirror"
        elif self.templatetype == "qqZZ":
            self.file = basedirmeng + "%s_fa3Adap_new_bkg.root" % self.channel
            self.name = "template_qqZZ"
        else:
            raise ValueError("Bad templatetype! %s" % self.templatetype)

class TemplateGetter_ggHonly_allflavors(BaseTemplateGetter):
    def fileandname(self):
        if self.on_off == "onshell" and self.category == "ggH":
            self.empty = False
        else:
            self.empty = True

        if self.templatetype == "SM":
            self.file = basedirmeng + "%s_fa3Adap_new.root" % self.channel
            self.name = "template0PlusAdapSmoothMirror"
        elif self.templatetype == "PS":
            self.file = basedirmeng + "%s_fa3Adap_new.root" % self.channel
            self.name = "template0MinusAdapSmoothMirror"
        elif self.templatetype == "interference":
            self.file = basedirmeng + "%s_fa3Adap_new.root" % self.channel
            self.name = "templateIntAdapSmoothMirror"
        elif self.templatetype == "qqZZ":
            self.file = basedirmeng + "%s_fa3Adap_new_bkg.root" % self.channel
            self.name = "template_qqZZ"
        else:
            raise ValueError("Bad templatetype! %s" % self.templatetype)

class TemplateGetter_ggHVBF_2e2mu(BaseTemplateGetter):
    def fileandname(self):
        if self.channel == "2e2mu" and self.on_off == "on_shell" and self.category != "VH":
            self.empty = True
        else:
            self.empty = False

        if self.category == "VBF":
            if self.templatetype == "SM":
                self.file = basedir + "%s_templates.root" % self.channel
                self.name = "template_VBFscalar"
            elif self.templatetype == "PS":
                self.file = basedir + "%s_templates.root" % self.channel
                self.name = "template_VBFpseudoscalar"
            elif self.templatetype == "interference":
                self.file = basedir + "%s_templates.root" % self.channel
                self.name = "template_VBFinterference"
            elif self.templatetype == "qqZZ":
                self.file = basedir + "%s_templates_bkg.root" % self.channel
                self.name = "template_qqZZ"
            else:
                raise ValueError("Bad templatetype! %s" % self.templatetype)
        elif self.category in ("ggH", "VBF"):
            if self.templatetype == "SM":
                self.file = basedirmeng + "%s_fa3Adap_new.root" % "2e2mu"
                self.name = "template0PlusAdapSmoothMirror"
            elif self.templatetype == "PS":
                self.file = basedirmeng + "%s_fa3Adap_new.root" % "2e2mu"
                self.name = "template0MinusAdapSmoothMirror"
            elif self.templatetype == "interference":
                self.file = basedirmeng + "%s_fa3Adap_new.root" % "2e2mu"
                self.name = "templateIntAdapSmoothMirror"
            elif self.templatetype == "qqZZ":
                self.file = basedirmeng + "%s_fa3Adap_new_bkg.root" % "2e2mu"
                self.name = "template_qqZZ"
            else:
                raise ValueError("Bad templatetype! %s" % self.templatetype)
        else:
            raise ValueError("Bad category! %s" % self.category)

templategetters = {
    WhichTemplates("ggH_2e2mu"): TemplateGetter_ggHonly_2e2mu,
    WhichTemplates("ggH_allflavors"): TemplateGetter_ggHonly_allflavors,
}
