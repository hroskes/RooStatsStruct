from enums import *
import rootlog
ROOT = rootlog.fakeroot()



def template(*args):
    #choose one
    #TemplateGetter = TemplateGetter_ggHonly_2e2mu
    #TemplateGetter = TemplateGetter_ggHonly_allflavors
    TemplateGetter = TemplateGetter_ggHVBF_2e2mu
    return TemplateGetter(*args).template()




basedir = "/afs/cern.ch/work/h/hroskes/Summer2015_VBF/makeTemplates/templates/"
basedirmeng = "/afs/cern.ch/work/x/xiaomeng/public/forChris/"

class BaseTemplateGetter(object):
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
        if not template:
            raise IOError(self.file + " does not contain " + self.name + "!")
        return template

class TemplateGetter_ggHonly_2e2mu(BaseTemplateGetter):
    def fileandname(self):
        if self.on_off == "onshell" and self.category == "ggH" and self.channel == "2e2mu":
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
        else:
            self.file = basedir + "emptytemplate.root"
            self.name = "empty"

class TemplateGetter_ggHonly_allflavors(BaseTemplateGetter):
    def fileandname(self):
        if self.on_off == "onshell" and self.category == "ggH":
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
        else:
            self.file = basedir + "emptytemplate.root"
            self.name = "empty"

class TemplateGetter_ggHVBF_2e2mu(BaseTemplateGetter):
    def fileandname(self):
        if self.on_off == "onshell" and self.category == "ggH" and self.channel == "2e2mu":
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
        elif self.on_off == "onshell" and self.category == "VBF" and self.channel == "2e2mu":
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
        else:
            self.file = basedir + "emptytemplate.root"
            self.name = "empty"
