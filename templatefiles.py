import config
import constants
from enums import *
import os
import rootlog
ROOT = rootlog.thefakeroot



def template(*args):
    return templategetters[config.whichtemplates](*args).template()

def pdftype(*args):
    return templategetters[config.whichtemplates](*args).pdftype()

def createg1g4(fa3, g4_for_fa3half, *args):
    return templategetters[config.whichtemplates](*args).createg1g4(fa3, g4_for_fa3half)

basedirVBF = "templates/VBF"
basedirggH_fromMeng = "templates/ggH_fromMeng_normalized/"
basedirggH = "templates/ggH"

class BaseTemplateGetter(object):

    emptytemplates = {}

    def __init__(self, *args):
        self.channel, self.on_off, self.category, self.templatetype, self.info = None, None, None, None, False
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

            if isinstance(arg, basestring) and arg == "info":
                self.templatetype = TemplateType(self.infotemplatetype)
                found += 1

            if found > 1:
                raise ValueError("Argument %s to TemplateFile is ambiguous" % arg)
            if found == 0:
                raise ValueError("Invalid argument %s to TemplateFile" % arg)

    def template(self):
        self.fileandname()
        self.setisempty()

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
                            "empty%i"%len(self.emptytemplates),
                            "empty",
                            template.GetNbinsX(), template.GetXaxis().GetXmin(), template.GetXaxis().GetXmax(),
                            template.GetNbinsY(), template.GetYaxis().GetXmin(), template.GetYaxis().GetXmax(),
                        )
                    except TypeError:    #TH1?
                        self.emptytemplates[(self.file, self.name)] = type(template)(  #create a new histogram to be the empty one
                            "empty%i"%len(self.emptytemplates),
                            "empty",
                            template.GetNbinsX(), template.GetXaxis().GetXmin(), template.GetXaxis().GetXmax(),
                        )
            template = self.emptytemplates[(self.file, self.name)]

        return template

class TemplateGetter_ggH(BaseTemplateGetter):
    infotemplatetype = "SM"
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

    def pdftype(self):
        return PDFType("decayonly_onshell")

    def createg1g4(self, fa3, g4_for_fa3half):
        ggH = Category("HZZ")
        #these are g1 and g4 normalized so that g1^2*xsec_SM + g1^2*xsec_PS = xsec_SM
        #   for decay
        g1 = ROOT.RooFormulaVar("g1", "g_{1}", "sqrt(1-abs(@0))", ROOT.RooArgList(fa3[ggH]))
        g4 = ROOT.RooFormulaVar("g4", "g_{4}", "(@0>0 ? 1 : -1) * sqrt(abs(@0))*@1",
                                ROOT.RooArgList(fa3[ggH], g4_for_fa3half[ggH])
                               )
        return g1, g4

class TemplateGetter_ggHonly_oneflavor(TemplateGetter_ggHonly):
    def setisempty(self):
        super(TemplateGetter_ggHonly_oneflavor, self).setisempty()
        if self.channel != self.theflavor:
            self.empty = True

class TemplateGetter_ggHonly_2e2mu(TemplateGetter_ggHonly_oneflavor):
    theflavor = "2e2mu"

class TemplateGetter_ggHonly_4e(TemplateGetter_ggHonly_oneflavor):
    theflavor = "4e"


class TemplateGetter_ggH_run2(BaseTemplateGetter):
    infotemplatetype = "SM"
    def fileandname_ggH(self):
        if self.templatetype == "SM":
            self.file = os.path.join(basedirggH, "ggH0+_%s.root" % self.channel)
        elif self.templatetype == "PS":
            self.file = os.path.join(basedirggH, "ggH0-_%s.root" % self.channel)
        elif self.templatetype == "interference":
            self.file = os.path.join(basedirggH, "ggHint_g1g4_%s.root" % self.channel)
        elif self.templatetype == "qqZZ":
            self.file = os.path.join(basedirggH, "qqZZ_%s.root" % self.channel)
        else:
            raise ValueError("Bad templatetype! %s" % self.templatetype)

        self.name = "template_fa3_decay_allevents"

class TemplateGetter_ggHonly_run2(TemplateGetter_ggH_run2, TemplateGetter_ggHonly): pass


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

    def pdftype(self):
        return PDFType("production+decay_onshell")

    def createg1g4(self, fa3, g4_for_fa3half):
        ggH = Category("HZZ")
        VBF = Category("VBF")
        #these are g1 and g4 normalized so that (g1^2*xsec_SM + g1^2*xsec_PS) * (g1^2*xsec_SM + g1^2*xsec_PS) = xsec_SM
        #   for VBF*decay
        #multiply scales g1 and g4 together, so that the cross section remains correct
        multiply = ROOT.RooFormulaVar("scaleg1g4", "1/(1-abs(@0) + (abs(@0) * (@1/@2)**2)) ** .25",
                                      ROOT.RooArgList(fa3[ggH], g4_for_fa3half[ggH], g4_for_fa3half[VBF])
                                     )
        g1 = ROOT.RooFormulaVar("g1", "g_{1}", "@1*sqrt(1-abs(@0))", ROOT.RooArgList(fa3[ggH], multiply))
        g4 = ROOT.RooFormulaVar("g4", "g_{4}", "@2*(@0>0 ? 1 : -1) * sqrt(abs(@0))*@1",
                                ROOT.RooArgList(fa3[ggH], g4_for_fa3half[ggH], multiply)
                               )
        return g1, g4

def TemplateGetterFactory_VBF(classname, templatename):
    class TemplateGetter_VBF(BaseTemplateGetter):
        infotemplatetype = "SM"
        def fileandname_VBF(self):
            if self.templatetype == "SM":
                g1power = 4
                g4power = 0
            elif self.templatetype == "g4power1":
                g1power = 3
                g4power = 1
            elif self.templatetype == "g4power2":
                g1power = 2
                g4power = 2
            elif self.templatetype == "g4power3":
                g1power = 1
                g4power = 3
            elif self.templatetype == "PS":
                g1power = 0
                g4power = 4
            elif self.templatetype == "qqZZ":
                #temporary
                g1power = 4
                g4power = 0
                assert config.turnoffbkg
            else:
                raise ValueError("Invalid TemplateType for VBF templategetter: %s" % self.templatetype)

            self.file = os.path.join(basedirVBF, "VBFfinal_%s.root" % self.channel)
            self.name = "%s_g1%ig4%i" % (templatename, g1power, g4power)

    TemplateGetter_VBF.__name__ = classname
    return TemplateGetter_VBF

#Dbkg from decay, but D0- and DCP from VBF alone with no decay info
TemplateGetter_VBFdiscriminants = TemplateGetterFactory_VBF("TemplateGetter_VBFdiscriminants", "template_VBF_alone_2D")
#D0-_VBFdecay, DCP_VBF
TemplateGetter_VBFdecay = TemplateGetterFactory_VBF("TemplateGetter_VBFdecay", "template_VBF_DCP_VBF_2D")
TemplateGetter_VBF_g4power = {
                              i:
                                 TemplateGetterFactory_VBF(
                                                           "TemplateGetter_VBF_g4power%i"%i,
                                                           "template_VBF_g4power%i_2D"%i
                                                          ) for i in (1, 2, 3)
                             }

TemplateGetter_VBF_1D_D0minus_VBF = TemplateGetterFactory_VBF("TemplateGetter_VBF_1D_D0minus", "D_0minus_VBF")
TemplateGetter_VBF_1D_D0minus_VBFdecay = TemplateGetterFactory_VBF("TemplateGetter_VBF_1D_D0minus_VBFdecay", "D_0minus_VBFdecay")
TemplateGetter_VBF_1D_DCP_VBF = TemplateGetterFactory_VBF("TemplateGetter_VBF_1D_DCP", "D_CP_VBF")
TemplateGetter_VBF_1D_DCP_VBFdecay = TemplateGetterFactory_VBF("TemplateGetter_VBF_1D_DCP_VBFdecay", "D_CP_VBFdecay")
TemplateGetter_VBF_1D_g4power = {
                                 i:
                                    TemplateGetterFactory_VBF(
                                                              "TemplateGetter_VBF_1D_g4power%i"%i,
                                                              "D_g4power%i_VBFdecay"%i
                                                             ) for i in (0, 1, 2, 3)
                                }
TemplateGetter_VBF_1D_g4power_prime = {
                                       i:
                                          TemplateGetterFactory_VBF(
                                                                    "TemplateGetter_VBF_1D_g4power%i_prime"%i,
                                                                    "D_g4power%i_VBFdecay_prime"%i
                                                                   ) for i in (1, 2, 3)
                                      }
TemplateGetter_VBF_g4power_prime = {
                                    i:
                                       TemplateGetterFactory_VBF(
                                                                 "TemplateGetter_VBF_g4power%i_prime"%i,
                                                                 "template_VBF_g4power%i_prime_2D"%i
                                                                ) for i in (1, 2, 3)
                                   }

class TemplateGetter_VBFonly_VBFdiscriminants(TemplateGetter_VBFonly, TemplateGetter_VBFdiscriminants): pass
class TemplateGetter_VBFonly_VBFdecay(TemplateGetter_VBFonly, TemplateGetter_VBFdecay): pass
class TemplateGetter_VBFonly_g4power1(TemplateGetter_VBFonly, TemplateGetter_VBF_g4power[1]): pass
class TemplateGetter_VBFonly_g4power2(TemplateGetter_VBFonly, TemplateGetter_VBF_g4power[2]): pass
class TemplateGetter_VBFonly_g4power3(TemplateGetter_VBFonly, TemplateGetter_VBF_g4power[3]): pass
class TemplateGetter_VBFonly_g4power1_prime(TemplateGetter_VBFonly, TemplateGetter_VBF_g4power_prime[1]): pass
class TemplateGetter_VBFonly_g4power2_prime(TemplateGetter_VBFonly, TemplateGetter_VBF_g4power_prime[2]): pass
class TemplateGetter_VBFonly_g4power3_prime(TemplateGetter_VBFonly, TemplateGetter_VBF_g4power_prime[3]): pass

class TemplateGetter_VBFonly_1D_D0minus_VBF(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_D0minus_VBF): pass
class TemplateGetter_VBFonly_1D_D0minus_VBFdecay(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_D0minus_VBFdecay): pass
class TemplateGetter_VBFonly_1D_DCP_VBF(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_DCP_VBF): pass
class TemplateGetter_VBFonly_1D_DCP_VBFdecay(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_DCP_VBFdecay): pass
class TemplateGetter_VBFonly_1D_g4power0(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_g4power[0]): pass
class TemplateGetter_VBFonly_1D_g4power1(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_g4power[1]): pass
class TemplateGetter_VBFonly_1D_g4power2(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_g4power[2]): pass
class TemplateGetter_VBFonly_1D_g4power3(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_g4power[3]): pass
class TemplateGetter_VBFonly_1D_g4power1_prime(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_g4power_prime[1]): pass
class TemplateGetter_VBFonly_1D_g4power2_prime(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_g4power_prime[2]): pass
class TemplateGetter_VBFonly_1D_g4power3_prime(TemplateGetter_VBFonly, TemplateGetter_VBF_1D_g4power_prime[3]): pass

templategetters = {
    WhichTemplates("ggH_2e2mu"): TemplateGetter_ggHonly_2e2mu,
    WhichTemplates("ggH_4e"): TemplateGetter_ggHonly_4e,
    WhichTemplates("ggH_allflavors"): TemplateGetter_ggHonly,
    WhichTemplates("VBF_nodecay"): TemplateGetter_VBFonly_VBFdiscriminants,
    WhichTemplates("VBF_DCPVBF"): TemplateGetter_VBFonly_VBFdecay,
    WhichTemplates("VBF_g4power1"): TemplateGetter_VBFonly_g4power1,
    WhichTemplates("VBF_g4power2"): TemplateGetter_VBFonly_g4power2,
    WhichTemplates("VBF_g4power3"): TemplateGetter_VBFonly_g4power3,
    WhichTemplates("VBF_1D_D0minus_VBF"): TemplateGetter_VBFonly_1D_D0minus_VBF,
    WhichTemplates("VBF_1D_D0minus_VBFdecay"): TemplateGetter_VBFonly_1D_D0minus_VBFdecay,
    WhichTemplates("VBF_1D_DCP_VBF"): TemplateGetter_VBFonly_1D_DCP_VBF,
    WhichTemplates("VBF_1D_g4power1"): TemplateGetter_VBFonly_1D_g4power1,
    WhichTemplates("VBF_1D_g4power2"): TemplateGetter_VBFonly_1D_g4power2,
    WhichTemplates("VBF_1D_g4power3"): TemplateGetter_VBFonly_1D_g4power3,
    WhichTemplates("VBF_1D_g4power0"): TemplateGetter_VBFonly_1D_g4power0,
    WhichTemplates("VBF_1D_DCP_VBFdecay"): TemplateGetter_VBFonly_1D_DCP_VBFdecay,
    WhichTemplates("VBF_1D_g4power1_prime"): TemplateGetter_VBFonly_1D_g4power1_prime,
    WhichTemplates("VBF_1D_g4power2_prime"): TemplateGetter_VBFonly_1D_g4power2_prime,
    WhichTemplates("VBF_1D_g4power3_prime"): TemplateGetter_VBFonly_1D_g4power3_prime,
    WhichTemplates("VBF_g4power1_prime"): TemplateGetter_VBFonly_g4power1_prime,
    WhichTemplates("VBF_g4power2_prime"): TemplateGetter_VBFonly_g4power2_prime,
    WhichTemplates("VBF_g4power3_prime"): TemplateGetter_VBFonly_g4power3_prime,
    WhichTemplates("ggH_run2"): TemplateGetter_ggHonly_run2,
}
