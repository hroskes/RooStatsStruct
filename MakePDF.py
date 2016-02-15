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
			Category("ggH"): 2.55052,  #+/- 0.00018
			Category("VBF"): 0.297979, #+/- 0.000013
			Category("VH"):  0.144057, #+/- 1.4e-5    this is for ZH
			#     for WH:    0.1236136  +/- 7.7e-6    might cause problems...
		}
		g4_for_fa3half = {
			category: ROOT.RooConstVar("g4_for_fa3_half_%s"%category, "g4_for_fa3_half_%s"%category, value)
				for category, value in g4_values_for_fa3half.iteritems()
		}
		fa3 = {}
		fa3[Category("ggH")] = ROOT.RooRealVar("fa3_ggH", "fa3_ggH", 0, -1, 1)
		for category in categories:
			if category == "ggH": continue
                        ggH = Category("ggH")
			fa3[category] = ROOT.RooFormulaVar("fa3_%s"%category, "fa3_%s"%category,
								"(@0>0 ? 1 : -1) / (1 + (1 - @0)*@1**2 / (@0*@2**2))",
								ROOT.RooArgList(fa3[ggH], g4_for_fa3half[category], g4_for_fa3half[ggH])
							  )

		#These variables are fixed as const. THIS IS ONLY TEMPORARY
		phi = ROOT.RooRealVar("phia3","phia3",0.,-math.pi,math.pi)
		phi.setConstant(True)
		luminosity = ROOT.RooRealVar("luminosity","luminosity",19.712)
		luminosity.setConstant(True)


		if not os.path.exists("workspaces"):
			os.mkdir("workspaces")
		FileName = "workspaces/{0}_fa3_{1}_{2}_workspace.root".format(str(config.whichtemplates), self.channel, self.on_off)
		if config.turnoffbkg:
			FileName = FileName.replace(".root", "_nobkg.root")
		w = ROOT.RooWorkspace("workspace","workspace")


		for category in categories:

			#if statements to make Discriminants
			Disc0_name = None
			Disc1_name = None
			Disc2_name = None
			if self.on_off == "onshell":
				if category == "ggH":
					Disc0_name = "sMELA_ggH"
					Disc1_name = "D0-_dec"
					Disc2_name = "Dcp_dec"
				elif category == "VH":
					Disc0_name = "sMELA_VH"
					Disc1_name = "D0-_VH"
					Disc2_name = "Dcp_VH"
				elif category == "VBF":
					Disc0_name = "sMELA_VBF"
					Disc1_name = "D0-_VBF"
					Disc2_name = "Dcp_VBF"
				else:
					print "INVALID ANALYSIS CATEGORY!"
					assert(0)
			elif self.on_off == "offshell":
				if category == "ggH":
					Disc0_name = "zz4l_mass_ggH"
					Disc1_name = "Dgg"
					Disc2_name = "D0-_dec_offshell"
				elif category == "VH":
					Disc0_name = "zz4l_mass_VH"
					Disc1_name = "D0-_VH_offshell"
					#Disc2_name = "Dcp_VH_offshell"
				elif category == "VBF":
					Disc0_name = "zz4l_mass_VBF"
					Disc1_name = "D0-_VBF_offshell"
					#Disc2_name = "Dcp_VBF_offshell"
				else:
					print "INVALID ANALYSIS CATEGORY!"
					assert(0)

			else:
				print "INVALID ON-OFF SHELL CATEGORY!"
				assert(0)


			#Build Signal PDF
			SMtemplate = templatefiles.template(category, self.channel, self.on_off, "SM")
			PStemplate = templatefiles.template(category, self.channel, self.on_off, "PS")
			MIXtemplate = templatefiles.template(category, self.channel, self.on_off, "interference")
			BKGtemplate = templatefiles.template(category, self.channel, self.on_off, "qqZZ")

			dBins0 = SMtemplate.GetXaxis().GetNbins()
			dLow0 = SMtemplate.GetXaxis().GetXmin()
			dHigh0 = SMtemplate.GetXaxis().GetXmax()

			dBins1 = SMtemplate.GetYaxis().GetNbins()
			dLow1 = SMtemplate.GetYaxis().GetXmin()
			dHigh1 = SMtemplate.GetYaxis().GetXmax()

			if Disc2_name is not None:
				dBins2 = SMtemplate.GetZaxis().GetNbins()
				dLow2 = SMtemplate.GetZaxis().GetXmin()
				dHigh2 = SMtemplate.GetZaxis().GetXmax()
			else:
				dBins2 = 1
				dLow2 = 0
				dHigh2 = 1


			Disc0 = ROOT.RooRealVar(Disc0_name,Disc0_name,dLow0,dHigh0)
			Disc0.setBins(dBins0)
			Disc1 = ROOT.RooRealVar(Disc1_name,Disc1_name,dLow1,dHigh1)
			Disc1.setBins(dBins1)
			if Disc2_name is not None:
				Disc2 = ROOT.RooRealVar(Disc2_name,Disc2_name,dLow2,dHigh2)
				Disc2.setBins(dBins2)
			else:
				Disc2 = None

			if Disc2 is not None:
				DiscArgList = ROOT.RooArgList(Disc0,Disc1,Disc2)
				DiscArgSet = ROOT.RooArgSet(Disc0,Disc1,Disc2)
			else:
				DiscArgList = ROOT.RooArgList(Disc0,Disc1)
				DiscArgSet = ROOT.RooArgSet(Disc0,Disc1)



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

			r1 = ROOT.RooRealVar("r1","r1",0.966)
			r1.setConstant(True)
			r2 = ROOT.RooRealVar("r2","r2",1.968)
			r2.setConstant(True)
			r3 = ROOT.RooRealVar("r3","r3",1.968)
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
				TotalPDF = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SignalPDF,BKGhistFunc),ROOT.RooArgList(SIGnorm,BKGnorm))
				ggHpdf = ROOT.RooRealSumPdf(TotalPDF,"ggH_{0}_{1}".format(self.channel,self.on_off))
				getattr(w, 'import')(ggHpdf, ROOT.RooFit.RecycleConflictNodes())
				print "Go There ggH"
			elif category == "VH":
				SIGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@6*@5*((1-abs(@0))+abs(@0)*@1 +(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1-abs(@0)))*(cos(@4)*(@2-1-@1) +sin(@4)*(@3-1-@1)))",ROOT.RooArgList(fa3[category], r1, r2, r3, phi, mu, luminosity))
				TemplateName = "Temp_{0}_{1}_{2}_SumPDF".format(self.channel,category,self.on_off)
				TotalPDF = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SignalPDF,BKGhistFunc),ROOT.RooArgList(SIGnorm,BKGnorm))
				VHpdf = ROOT.RooRealSumPdf(TotalPDF,"VH_{0}_{1}".format(self.channel,self.on_off))
				getattr(w, 'import')(VHpdf, ROOT.RooFit.RecycleConflictNodes())
				print "Go There VH"
			elif category == "VBF":
				SIGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@6*@5*((1-abs(@0))+abs(@0)*@1 +(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1-abs(@0)))*(cos(@4)*(@2-1-@1) +sin(@4)*(@3-1-@1)))",ROOT.RooArgList(fa3[category], r1, r2, r3, phi, mu, luminosity))
				TemplateName = "Temp_{0}_{1}_{2}_SumPDF".format(self.channel,category,self.on_off)
				TotalPDF = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SignalPDF,BKGhistFunc),ROOT.RooArgList(SIGnorm,BKGnorm))
				VBFpdf = ROOT.RooRealSumPdf(TotalPDF,"VBF_{0}_{1}".format(self.channel,self.on_off))
				getattr(w, 'import')(VBFpdf, ROOT.RooFit.RecycleConflictNodes())
				print "Go There VBF"

			else:
				print "INVALID ANALYSIS CATEGORY!"
				assert(0)

		ggHpdf.Print()
		VHpdf.Print()
		VBFpdf.Print()

		one = ROOT.RooConstVar("one", "one", 1.0)
		TemplateName = "Cat_{0}_{1}_SumPDF".format(self.channel,self.on_off)
		#one = ROOT.RooFormula
		CatSumPDF = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(ggHpdf,VHpdf,VBFpdf), ROOT.RooArgList(one, one, one))


		getattr(w, 'import')(CatSumPDF, ROOT.RooFit.RecycleConflictNodes())
		w.writeToFile(FileName)
