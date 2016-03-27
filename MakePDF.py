#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2015.05.29
# by Chris & Heshy for StandAlone fa3 Sum 2015
#-----------------------------------------------
import sys, os, pwd, commands
import optparse, shlex, re
import math
import rootlog
import templatefiles
import config
import constants
from enums import *

#import ROOT
ROOT = rootlog.thefakeroot
import ROOT as therealROOT

ROOT.gSystem.Load('libRooFit')
import loadlib
from array import array

class MakePDF(object):

    def __init__(self):
        for on_off_code in ["on"]:
            for flavor in "2e2mu", "4e", "4mu":
                self.makeWorkspace(flavor, on_off_code)

    def makeWorkspace(self, channelCode, on_off_Code):

        ggH = Category("ggH")
        VH = Category("VH")
        VBF = Category("VBF")

        #Placeholder for Inputs
        self.channel = Channel(channelCode) # 0 = 2e2mu, 1 = 4mu, 2 = 4e
        self.on_off = OnOffShell(on_off_Code) # 0 = on-shell, 1 = off-shell

        #Variables
        mu = ROOT.RooRealVar("mu","mu",1.,0.,100.)
        g4_values_for_fa3half = {
            ggH: constants.g4_mix_ggH,
            VBF: constants.g4_mix_VBF,
            VH:  constants.g4_mix_ZH, #WH is a bit different, not sure what to do about this
        }

        g4_for_fa3half = {
            category: ROOT.RooConstVar("g4_for_fa3half_%s"%category, "g4_for_fa3half_%s"%category, value)
                for category, value in g4_values_for_fa3half.iteritems()
        }

        fa3 = {}
        fa3[ggH] = ROOT.RooRealVar("fa3_HZZ", "(f_{a3})_{HZZ}", 0, -1, 1)
        for category in categories:
            if category == "ggH": continue
            fa3[category] = ROOT.RooFormulaVar("fa3_%s"%category, "(f_{a3})_{%s}"%category,
                                               "(@0>0 ? 1 : -1) * abs(@0)*@2**2 / (abs(@0)*@2**2 + (1-abs(@0)) * @1**2)",
                                               ROOT.RooArgList(fa3[ggH], g4_for_fa3half[category], g4_for_fa3half[ggH])
                                              )

        #these are g1 and g4 normalized so that g1^2*xsec_SM + g1^2*xsec_PS = xsec_SM
        g1, g4 = templatefiles.createg1g4(fa3, g4_for_fa3half)

        #These variables are fixed as const. THIS IS ONLY TEMPORARY
        phi = ROOT.RooRealVar("phia3","phia3",0.,-math.pi,math.pi)
        phi.setConstant(True)
        luminosity = ROOT.RooRealVar("luminosity","luminosity",constants.luminosity)
        luminosity.setConstant(True)

        TotalPDFs = {}

        one = ROOT.RooConstVar("one", "one", 1.0)

        if not os.path.exists("workspaces"):
            os.mkdir("workspaces")
        FileName = "workspaces/{0}_fa3_{1}_{2}_workspace.root".format(str(config.whichtemplates), self.channel, self.on_off)
        if config.turnoffbkg:
            FileName = FileName.replace(".root", "_nobkg.root")
        w = ROOT.RooWorkspace("workspace","workspace")

        #get discriminants
        DiscArgList = {}
        DiscArgSet = {}
        BigDiscList = []
        for category in categories:

            if self.on_off == "onshell":
                Disc_name = ["Disc%i_%s" % (i, category) for i in range(3)]
            elif self.on_off == "offshell":
                Disc_name = ["Disc%i_%s_offshell" % (i, category) for i in range(3)]
            else:
                assert(0)

            infotemplate = templatefiles.template(category, self.channel, self.on_off, "info")

            if isinstance(infotemplate, ROOT.TH3):
                dimensions = 3
            elif isinstance(infotemplate, ROOT.TH2):
                dimensions = 2
            elif isinstance(infotemplate, ROOT.TH1):
                dimensions = 1
            else:
                assert False

            dBins = []
            dTitle = []
            dLow = []
            dHigh = []
            Disc = []

            for i in range(dimensions):
                axis = GetAxis(infotemplate, i)
                dTitle.append(axis.GetTitle())
                dBins.append(axis.GetNbins())
                dLow.append(axis.GetXmin())
                dHigh.append(axis.GetXmax())

                Disc.append(ROOT.RooRealVar(Disc_name[i], dTitle[i], dLow[i], dHigh[i]))

            DiscArgList[category] = ROOT.RooArgList(*Disc)
            DiscArgSet[category] = ROOT.RooArgSet(*Disc)
            BigDiscList += Disc

        BigDiscArgSet = ROOT.RooArgSet(*BigDiscList)
        BigDiscArgList = ROOT.RooArgList(*BigDiscList)

        #Build Signal PDF
        for category in categories:
            if templatefiles.pdftype(category) == "decayonly_onshell":
                SMtemplate = templatefiles.template(category, self.channel, self.on_off, "SM")
                PStemplate = templatefiles.template(category, self.channel, self.on_off, "PS")
                MIXtemplate = templatefiles.template(category, self.channel, self.on_off, "interference")
                BKGtemplate = templatefiles.template(category, self.channel, self.on_off, "qqZZ")

                TemplateName = "SM_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
                SMdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList[category], SMtemplate)
                TemplateName = "PS_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
                PSdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList[category], PStemplate)
                TemplateName = "MIX_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
                MIXdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList[category], MIXtemplate)
                TemplateName = "BKG_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
                BKGdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList[category], BKGtemplate)

                TemplateName = "SM_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
                SMhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, BigDiscArgSet, SMdataHist)
                TemplateName = "PS_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
                PShistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, BigDiscArgSet, PSdataHist)
                TemplateName = "MIX_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
                MIXhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, BigDiscArgSet, MIXdataHist)
                TemplateName = "BKG_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
                BKGhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, BigDiscArgSet, BKGdataHist)

                r1 = ROOT.RooRealVar("r1","r1",constants.r1)
                r1.setConstant(True)
                r2 = ROOT.RooRealVar("r2","r2",constants.r2)
                r2.setConstant(True)
                r3 = ROOT.RooRealVar("r3","r3",constants.r3)
                r3.setConstant(True)

                TemplateName = "SM_{0}_{1}_{2}_norm".format(self.channel,category,self.on_off)
                SMnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "(1.-abs(@0))",ROOT.RooArgList(fa3[category]))
                TemplateName = "MIX_{0}_{1}_{2}_norm".format(self.channel,category,self.on_off)
                MIXnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1.-abs(@0)))",ROOT.RooArgList(fa3[category]))
                TemplateName = "PS_{0}_{1}_{2}_norm".format(self.channel,category,self.on_off)
                PSnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "abs(@0)",ROOT.RooArgList(fa3[category]))


                TemplateName = "Signal_{0}_{1}_{2}_SumPDF".format(self.channel,category,self.on_off)
                SignalPDF = ROOT.RooRealFlooredSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SMhistFunc, MIXhistFunc, PShistFunc), ROOT.RooArgList(SMnorm,MIXnorm,PSnorm))

                TemplateName = "qqZZ_{0}_{1}_{2}_norm".format(self.channel,category,self.on_off)
                BKGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@0", ROOT.RooArgList(luminosity))

                TemplateName = "Signal_{0}_{1}_{2}_norm".format(self.channel,category,self.on_off)
                #NOTE BELOW INCLUDES MU AND SMrate
                #Below NOT COMBINE COMPATIBLE
                SIGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@6*@5*((1-abs(@0))+abs(@0)*@1 +(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1-abs(@0)))*(cos(@4)*(@2-1-@1) +sin(@4)*(@3-1-@1)))",ROOT.RooArgList(fa3[category], r1, r2, r3, phi, mu, luminosity))

            elif templatefiles.pdftype(category) == "production+decay_onshell":
                g4powertemplate = [None]*5
                for i in range(5):
                    g4powertemplate[i] = templatefiles.template(category, self.channel, self.on_off, ["SM", "g4power1", "g4power2", "g4power3", "PS"][i])
                BKGtemplate = templatefiles.template(category, self.channel, self.on_off, "qqZZ")

                datahists = [None]*5
                histfuncs = [None]*5
                norms = [None]*5

                for i in range(5):
                    TemplateName = "g4power{0}_{1}_{2}_{3}_dataHist".format(i, self.channel,category,self.on_off)
                    datahists[i] = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList[category], g4powertemplate[i])
                    TemplateName = "g4power{0}_{1}_{2}_{3}_HistPDF".format(i, self.channel,category,self.on_off)
                    histfuncs[i] = ROOT.RooHistFunc(TemplateName, TemplateName, BigDiscArgSet, datahists[i])
                    TemplateName = "g4power{0}_{1}_{2}_{3}_norm".format(i, self.channel,category,self.on_off)
                    norms[i] = ROOT.RooFormulaVar(TemplateName, TemplateName, "@0**%i * @1**%i"%(i, 4-i), ROOT.RooArgList(g4, g1))

                TemplateName = "BKG_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
                BKGdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList[category], BKGtemplate)
                TemplateName = "BKG_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
                BKGhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, BigDiscArgSet, BKGdataHist)
                TemplateName = "qqZZ_{0}_{1}_{2}_norm".format(self.channel,category,self.on_off)
                BKGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@0", ROOT.RooArgList(luminosity))

                TemplateName = "Signal_{0}_{1}_{2}_SumPDF".format(self.channel,category,self.on_off)
                SignalPDF = ROOT.RooRealFlooredSumPdf(TemplateName, TemplateName, ROOT.RooArgList(*histfuncs), ROOT.RooArgList(*norms))
                TemplateName = "Signal_{0}_{1}_{2}_norm".format(self.channel,category,self.on_off)
                SIGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@0*@1", ROOT.RooArgList(luminosity, mu))
            else:
                assert False

            TemplateName = "{0}_{1}_{2}_SumPDF".format(str(category),self.channel,self.on_off) #different format, category as string goes first
            TotalPDFs[category] = ROOT.RooRealFlooredSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SignalPDF,BKGhistFunc),ROOT.RooArgList(SIGnorm,BKGnorm))
            #getattr(w, 'import')(TotalPDFs[category], ROOT.RooFit.RecycleConflictNodes())
            print "Go There", category

            #delete these variables, to make sure they are actually assigned next time
            #the actual objects are not deleted, they still have a reference in rootlog
            del SignalPDF, BKGhistFunc, SIGnorm, BKGnorm



        TemplateName = "Cat_{0}_{1}_SumPDF".format(self.channel,self.on_off)
        CatSumPDF = ROOT.RooRealFlooredSumPdf(TemplateName, TemplateName, ROOT.RooArgList(TotalPDFs[ggH], TotalPDFs[VH], TotalPDFs[VBF]), ROOT.RooArgList(one, one, one))


        getattr(w, 'import')(CatSumPDF, ROOT.RooFit.RecycleConflictNodes())
        w.writeToFile(FileName)

def GetAxis(h, axis):
    """
    axis: 0=x, 1=y, 2=z
    """
    if axis == 0 or axis in ['x', 'X']:
        return h.GetXaxis()
    elif axis == 1 or axis in ['y', 'Y']:
        return h.GetYaxis()
    elif axis == 2 or axis in ['z', 'Z']:
        return h.GetZaxis()
    else:
        raise ValueError("Bad axis %s"%axis)

if __name__ == "__main__":
    MakePDF()
