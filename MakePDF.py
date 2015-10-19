#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2015.05.29
# by Chris & Heshy for StandAlone fa3 Sum 2015
#-----------------------------------------------
import sys, os, pwd, commands
import optparse, shlex, re
import math
from ROOT import *
import ROOT
from array import array

turnoffbkg = True

class MakePDF:

	def makeWorkspace(self, channelCode, templateFile, templateFile_bkg, on_off_Code, templatename_SM, templatename_PS, templatename_mix, templatename_bkg):

		#Placeholder for Inputs
		self.channel = channelCode # 0 = 2e2mu, 1 = 4mu, 2 = 4e
		self.category = 0 # 0 = ggH, 1 = VH, 2 = VBF
		self.on_off = on_off_Code  # 0 = on-shell, 1 = off-shell

		#new variables to make code more clear
		self.on_shell = 0
		self.off_shell = 1
		self.ggH_category = 0
		self.VH_category = 1
		self.VBF_category = 2
		self.TwoETwoMu = 0
		self.FourMu = 1
		self.FourE = 2

		#libraries for template names
                self.templateFile = templateFile # Input Templates
                self.templateFile_bkg = templateFile_bkg
                self.templatename_SM = templatename_SM
                self.templatename_PS = templatename_PS
                self.templatename_mix = templatename_mix
                self.templatename_bkg = templatename_bkg

                #Variables
                mu = ROOT.RooRealVar("mu","mu",0.,100.)
                fa3 = ROOT.RooRealVar("fa3","fa3",-1.,1.)

                #These variables are fixed as const. THIS IS ONLY TEMPORARY
                phi = ROOT.RooRealVar("phia3","phia3",0.,-math.pi,math.pi)
                phi.setConstant(True)
                r1 = ROOT.RooRealVar("r1","r1",0.966)
                r1.setConstant(True)
                r2 = ROOT.RooRealVar("r2","r2",1.968)
                r2.setConstant(True)
                r3 = ROOT.RooRealVar("r3","r3",1.968)
                r3.setConstant(True)
                BKGrate = ROOT.RooRealVar("BKGrate","BKGrate",0 if turnoffbkg else 13.6519)
                BKGrate.setConstant(True)
                SMrate = ROOT.RooRealVar("SMrate","SMrate",7.6807)
                SMrate.setConstant(True)

                FileName = "fa3_{0}_{1}_workspace.root".format(self.channel,self.on_off)
                if turnoffbkg:
                        FileName = FileName.replace(".root", "_nobkg.root")
                w = ROOT.RooWorkspace("workspace","workspace")
		ggHnorm = ROOT.RooFormulaVar()
		VHnorm = ROOT.RooFormulaVar()
		VBFnorm = ROOT.RooFormulaVar()
                ggHpdf = ROOT.RooRealSumPdf()
                VHpdf = ROOT.RooRealSumPdf()
                VBFpdf = ROOT.RooRealSumPdf()


		for self.category in range(0,3): # 0 = ggH, 1 = VH, 2 = VBF

			#if statements to make Discriminants
			Disc0_name = None
			Disc1_name = None
			Disc2_name = None
			if self.on_off == self.on_shell:
				Disc0_name = "sMELA"
				if self.category == self.ggH_category:
					Disc1_name = "D0-_dec"
					Disc2_name = "Dcp_dec"
				elif self.category == self.VH_category:
					Disc1_name = "D0-_VH"
					Disc2_name = "Dcp_VH"
				elif self.category == self.VBF_category:
					Disc1_name = "D0-_VBF"
					Disc2_name = "Dcp_VBF"
				else:
					print "INVALID ANALYSIS CATEGORY!"
					assert(0)
			elif self.on_off == self.off_shell:
				Disc0_name = "zz4l_mass"
				if self.category == self.ggH_category:
					Disc1_name = "Dgg"
					Disc2_name = "D0-_dec"
				elif self.category == self.VH_category:
					Disc1_name = "D0-_VH"
					#Disc2_name = "Dcp_VH"
				elif self.category == self.VBF_category:
					Disc1_name = "D0-_VBF"
					#Disc2_name = "Dcp_VBF"
				else:
					print "INVALID ANALYSIS CATEGORY!"
					assert(0)

			else:
				print "INVALID ON-OFF SHELL CATEGORY!"
				assert(0)


			#Build Signal PDF
			InputFileName = "{0}".format(self.templateFile)
			InputRootFile = ROOT.TFile(InputFileName)
			SMtemplate = InputRootFile.Get(self.templatename_SM)
			PStemplate = InputRootFile.Get(self.templatename_PS)
			MIXtemplate = InputRootFile.Get(self.templatename_mix)
			InputFileName_bkg = "{0}".format(self.templateFile_bkg)
			InputRootFile_bkg = ROOT.TFile(InputFileName_bkg)
			BKGtemplate = InputRootFile_bkg.Get(self.templatename_bkg)
			
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



			TemplateName = "SM_{0}_{1}_{2}_dataHist".format(self.channel,self.category,self.on_off)
			SMdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList, SMtemplate)
			TemplateName = "PS_{0}_{1}_{2}_dataHist".format(self.channel,self.category,self.on_off)
			PSdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList, PStemplate)
			TemplateName = "MIX_{0}_{1}_{2}_dataHist".format(self.channel,self.category,self.on_off)
			MIXdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList, MIXtemplate)
			TemplateName = "BKG_{0}_{1}_{2}_dataHist".format(self.channel,self.category,self.on_off)
			BKGdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgList, BKGtemplate)
			
			TemplateName = "SM_{0}_{1}_{2}_HistPDF".format(self.channel,self.category,self.on_off)
			SMhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, SMdataHist)
			TemplateName = "PS_{0}_{1}_{2}_HistPDF".format(self.channel,self.category,self.on_off)
			PShistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, PSdataHist)
			TemplateName = "MIX_{0}_{1}_{2}_HistPDF".format(self.channel,self.category,self.on_off)
			MIXhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, MIXdataHist)
			TemplateName = "BKG_{0}_{1}_{2}_HistPDF".format(self.channel,self.category,self.on_off)
			BKGhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, BKGdataHist)
			

			TemplateName = "SM_{0}_{1}_{2}_norm".format(self.channel,self.category,self.on_off)
			SMnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "(1-abs(@0))",ROOT.RooArgList(fa3))
			TemplateName = "MIX_{0}_{1}_{2}_norm".format(self.channel,self.category,self.on_off)
			MIXnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1-abs(@0)))",ROOT.RooArgList(fa3))
			TemplateName = "PS_{0}_{1}_{2}_norm".format(self.channel,self.category,self.on_off)
			PSnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "abs(@0)",ROOT.RooArgList(fa3))


			TemplateName = "Signal_{0}_{1}_{2}_SumPDF".format(self.channel,self.category,self.on_off)
			SignalPDF = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SMhistFunc, MIXhistFunc, PShistFunc), ROOT.RooArgList(SMnorm,MIXnorm,PSnorm))

			TemplateName = "Signal_{0}_{1}_{2}_norm".format(self.channel,self.category,self.on_off)
			#NOTE BELOW INCLUDES MU AND SMrate 
			#Below NOT COMBINE COMPATIBLE
			SIGnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "@6*@5*((1-abs(@0))+abs(@0)*@1 +(@0>0 ? 1.: -1.)*sqrt(abs(@0)*(1-abs(@0)))*(cos(@4)*(@2-1-@1) +sin(@4)*(@3-1-@1)))",RooArgList(fa3, r1, r2, r3, phi, mu, SMrate))
			TemplateName = "Total_{0}_{1}_{2}_SumPDF".format(self.channel,self.category,self.on_off)
			TotalPDF = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SignalPDF,BKGhistFunc),ROOT.RooArgList(SIGnorm,BKGrate))
                	getattr(w, 'import')(TotalPDF, ROOT.RooFit.RecycleConflictNodes())

			#combine categories
			TemplateName = "Category_{0}_{1}_{2}_Norm".format(self.channel,self.category,self.on_off)

			if self.category == self.ggH_category:
                        	ggHnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "(1.-abs(@0))",RooArgList(fa3))
				getattr(w, 'import')(ggHnorm, ROOT.RooFit.RecycleConflictNodes())
				ggHpdf = ROOT.RooRealSumPdf(TotalPDF)
				print "Go There ggH"
                        elif self.category == self.VH_category:
                                VHnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "(1.-abs(@0))",RooArgList(fa3))
                                getattr(w, 'import')(VHnorm, ROOT.RooFit.RecycleConflictNodes())
				VHpdf = ROOT.RooRealSumPdf(TotalPDF)
				print "Go There VH"
                        elif self.category == self.VBF_category:
                                VBFnorm = ROOT.RooFormulaVar(TemplateName, TemplateName, "(1.-abs(@0))",RooArgList(fa3))
                                getattr(w, 'import')(VBFnorm, ROOT.RooFit.RecycleConflictNodes())
				VBFpdf = ROOT.RooRealSumPdf(TotalPDF)
				print "Go There VBF"
			else:
                                print "INVALID ANALYSIS CATEGORY!"
                                assert(0)
		
		TemplateName = "Cat_{0}_{1}_SumPDF".format(self.channel,self.on_off)
		CatSumPDF = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(ggHpdf,VHpdf,VBFpdf),ROOT.RooArgList(ggHnorm,VHnorm,VBFnorm))
		getattr(w, 'import')(CatSumPDF, ROOT.RooFit.RecycleConflictNodes())
		w.writeToFile(FileName)
