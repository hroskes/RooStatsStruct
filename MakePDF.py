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

class MakePDF:

	def makeWorkspace(self, channelCode, on_off_Code):

		#Placeholder for Inputs
		self.channel = Channel(channelCode) # 0 = 2e2mu, 1 = 4mu, 2 = 4e
		self.on_off = OnOffShell(on_off_Code) # 0 = on-shell, 1 = off-shell

		#Variables
		mu = ROOT.RooRealVar("mu","mu",1.,0.,100.)
		g4_values_for_fa3half = {
			Category("ggH"): constants.g4_mix_ggH,
			Category("VBF"): constants.g4_mix_VBF,
			Category("VH"):  constants.g4_mix_ZH, #WH is a bit different, not sure what to do about this
		}
		g4_for_fa3half = {
			category: ROOT.RooConstVar("g4_for_fa3_half_%s"%category, "g4_for_fa3_half_%s"%category, value)
				for category, value in g4_values_for_fa3half.iteritems()
		}
		fa3 = {}
		fa3[Category("ggH")] = ROOT.RooRealVar("fa3_HZZ", "(f_{a3})_{HZZ}", 0, -1, 1)
		for category in categories:
			if category == "ggH": continue
			ggH = Category("ggH")
			fa3[category] = ROOT.RooFormulaVar("fa3_%s"%category, "(f_{a3})_{%s}"%category,
								"(@0>0 ? 1 : -1) * abs(@0)*@2**2 / (abs(@0)*@2**2 + (1-abs(@0)) * @1**2)",
								ROOT.RooArgList(fa3[ggH], g4_for_fa3half[category], g4_for_fa3half[ggH])
							  )

		#These variables are fixed as const. THIS IS ONLY TEMPORARY
		phi = ROOT.RooRealVar("phia3","phia3",0.,-math.pi,math.pi)
		phi.setConstant(True)
		luminosity = ROOT.RooRealVar("luminosity","luminosity",constants.luminosity)
		luminosity.setConstant(True)

		one = ROOT.RooConstVar("one", "one", 1.0)
		volumes = {}

		if not os.path.exists("workspaces"):
			os.mkdir("workspaces")
		FileName = "workspaces/{0}_fa3_{1}_{2}_workspace.root".format(str(config.whichtemplates), self.channel, self.on_off)
		if config.turnoffbkg:
			FileName = FileName.replace(".root", "_nobkg.root")
		w = ROOT.RooWorkspace("workspace","workspace")

		for category in categories:

			#if statements to make Discriminants
			if self.on_off == "onshell":
				Disc_name = ["Disc%i_%s" % (i, category) for i in range(3)]
			elif self.on_off == "offshell":
				Disc_name = ["Disc%i_%s_offshell" % (i, category) for i in range(3)]
			else:
				assert(0)


			#Build Signal PDF
			SMtemplate = templatefiles.template(category, self.channel, self.on_off, "SM")
			PStemplate = templatefiles.template(category, self.channel, self.on_off, "PS")
			MIXtemplate = templatefiles.template(category, self.channel, self.on_off, "interference")
			BKGtemplate = templatefiles.template(category, self.channel, self.on_off, "qqZZ")

			if isinstance(SMtemplate, ROOT.TH3):
				dimensions = 3
			elif isinstance(SMtemplate, ROOT.TH2):
				dimensions = 2
			elif isinstance(SMtemplate, ROOT.TH1):
				dimensions = 1
			else:
				assert False

			dBins = []
			dTitle = []
			dLow = []
			dHigh = []
			Disc = []

			for i in range(dimensions):
				axis = GetAxis(SMtemplate, i)
				dTitle.append(axis.GetTitle())
				dBins.append(axis.GetNbins())
				dLow.append(axis.GetXmin())
				dHigh.append(axis.GetXmax())

				Disc.append(ROOT.RooRealVar(Disc_name[i], dTitle[i], dLow[i], dHigh[i]))

			DiscArgList = ROOT.RooArgList(*Disc)
			DiscArgSet = ROOT.RooArgSet(*Disc)
			volumes[category] = one.createIntegral(ROOT.RooArgSet(*Disc)).getVal()

			TemplateName = "SM_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
			SMdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList, SMtemplate)
			TemplateName = "PS_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
			PSdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList, PStemplate)
			TemplateName = "MIX_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
			MIXdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList, MIXtemplate)
			TemplateName = "BKG_{0}_{1}_{2}_dataHist".format(self.channel,category,self.on_off)
			BKGdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList, BKGtemplate)

			TemplateName = "SM_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
			SMhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, SMdataHist)
			TemplateName = "PS_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
			PShistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, PSdataHist)
			TemplateName = "MIX_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
			MIXhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, MIXdataHist)
			TemplateName = "BKG_{0}_{1}_{2}_HistPDF".format(self.channel,category,self.on_off)
			BKGhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, BKGdataHist)

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

			if category == "ggH":
				SIGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@6*@5*((1-abs(@0))+abs(@0)*@1 +(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1-abs(@0)))*(cos(@4)*(@2-1-@1) +sin(@4)*(@3-1-@1)))",ROOT.RooArgList(fa3[category], r1, r2, r3, phi, mu, luminosity))
				TemplateName = "Temp_{0}_{1}_{2}_SumPDF".format(self.channel,category,self.on_off)
				TotalPDF = ROOT.RooRealFlooredSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SignalPDF,BKGhistFunc),ROOT.RooArgList(SIGnorm,BKGnorm))
				ggHpdf = ROOT.RooRealFlooredSumPdf(TotalPDF,"ggH_{0}_{1}".format(self.channel,self.on_off))
				getattr(w, 'import')(ggHpdf, ROOT.RooFit.RecycleConflictNodes())
				print "Go There ggH"
			elif category == "VH":
				SIGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@6*@5*((1-abs(@0))+abs(@0)*@1 +(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1-abs(@0)))*(cos(@4)*(@2-1-@1) +sin(@4)*(@3-1-@1)))",ROOT.RooArgList(fa3[category], r1, r2, r3, phi, mu, luminosity))
				TemplateName = "Temp_{0}_{1}_{2}_SumPDF".format(self.channel,category,self.on_off)
				TotalPDF = ROOT.RooRealFlooredSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SignalPDF,BKGhistFunc),ROOT.RooArgList(SIGnorm,BKGnorm))
				VHpdf = ROOT.RooRealFlooredSumPdf(TotalPDF,"VH_{0}_{1}".format(self.channel,self.on_off))
				getattr(w, 'import')(VHpdf, ROOT.RooFit.RecycleConflictNodes())
				print "Go There VH"
			elif category == "VBF":
				SIGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@6*@5*((1-abs(@0))+abs(@0)*@1 +(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1-abs(@0)))*(cos(@4)*(@2-1-@1) +sin(@4)*(@3-1-@1)))",ROOT.RooArgList(fa3[category], r1, r2, r3, phi, mu, luminosity))
				TemplateName = "Temp_{0}_{1}_{2}_SumPDF".format(self.channel,category,self.on_off)
				TotalPDF = ROOT.RooRealFlooredSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SignalPDF,BKGhistFunc),ROOT.RooArgList(SIGnorm,BKGnorm))
				VBFpdf = ROOT.RooRealFlooredSumPdf(TotalPDF,"VBF_{0}_{1}".format(self.channel,self.on_off))
				getattr(w, 'import')(VBFpdf, ROOT.RooFit.RecycleConflictNodes())
				print "Go There VBF"

			else:
				print "INVALID ANALYSIS CATEGORY!"
				assert(0)


                #each category PDF is multiplied 1/(volume of other categories' phase space)
                #this way the integral over all 9 discriminants gives the number of events
		catnorm = {}
		for category in categories:
			othervolume = 1
			for othercategory in categories:
				if othercategory == category: continue
				othervolume *= volumes[othercategory]
			TemplateName = "{0}_{1}_{2}_norm".format(self.channel, category, self.on_off)
			catnorm[str(category)] = ROOT.RooConstVar(TemplateName, TemplateName, 1/othervolume)

		TemplateName = "Cat_{0}_{1}_SumPDF".format(self.channel,self.on_off)
		CatSumPDF = ROOT.RooRealFlooredSumPdf(TemplateName, TemplateName, ROOT.RooArgList(ggHpdf,VHpdf,VBFpdf), ROOT.RooArgList(catnorm["ggH"], catnorm["VH"], catnorm["VBF"]))


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
