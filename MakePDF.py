#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2015.05.29
# by Chris & Hshey for StandAlone fa3 Sum 2015
#-----------------------------------------------
import sys, os, pwd, commands
import optparse, shlex, re
import math
from ROOT import *
import ROOT
from array import array


class MakePDF:

	def makeWorkspace(self, channelCode, templateFile, on_off_Code):

		#Placeholder for Inputs
		self.channel = channelCode # 0 = 2e2mu, 1 = 4mu, 2 = 4e
		self.category = categoryCode # 0 = ggH, 1 = VH, 2 = VBF
		self.on_off = on_off_Code  # 0 = on-shell, 1 = off-shell
		self.tempalteFile = templateFile # Input Templates		


		#Variables
		mu = ROOT.RooRealVar("mu","mu",0.,15.)
		fa3 = ROOT.RooRealVar("fa3","fa3",0.,1.)	


		#if statements to make Discriminants
		Disc0_name = None
		Disc1_name = None
		Disc2_name = None
		if self.on_off == 0:
			Disc0_name = "sMELA"
			if self.category == 0:
				Disc1_name = "D0-_dec"
				Disc2_name = "Dcp_dec"
			elif self.category == 1:	
				Disc1_name = "D0-_VH"
				Disc2_name = "Dcp_VH"
			elif self.category == 2:
				Disc1_name = "D0-_VBF"
				Disc2_name = "Dcp_VBF"
			else:
				print "INVALID ANALYSIS CATEGORY!"
		elif self.on_off == 1:
                        Disc0_name = "zz4l_mass"
                        if self.category == 0:
                                Disc1_name = "Dgg"  
                                Disc2_name = "D0-_dec"
                        elif self.category == 1:        
                                Disc1_name = "D0-_VH"
                                #Disc2_name = "Dcp_VH"
                        elif self.category == 2:
                                Disc1_name = "D0-_VBF"
                                #Disc2_name = "Dcp_VBF"
                        else:
                                print "INVALID ANALYSIS CATEGORY!"

		else:
			print "INVALID ON-OFF SHELL CATEGORY!"

		
		#Build Signal PDF
		InputFileName = "{0}".format(self.templateFile)
		InputRootFile = ROOT.TFile(InputFileName)
		SMtemplate = InputRootFile.Get("")
		PStemplate = InputRootFile.Get("")
		MIXtemplate = InputRootFile.Get("")

		dBins0 = SMtemplate.GetXaxis().GetNbins()
		dLow0 = SMtemplate.GetXaxis().GetXmin()
		dHigh0 = SMtempalte.GetXaxis().GetXmax()
		
		dBins1 = SMtemplate.GetYaxis().GetNbins()
                dLow1 = SMtemplate.GetYaxis().GetXmin()
                dHigh1 = SMtempalte.GetYaxis().GetXmax()

		dBins2 = 1
		dLow2 = 0
		dHigh2 = 1
		if self.on_off != 1 and self.category > 0:
			dBins2 = SMtemplate.GetZaxis().GetNbins()
                	dLow2 = SMtemplate.GetZaxis().GetXmin()
                	dHigh2 = SMtempalte.GetZaxis().GetXmax()


		Disc0 = ROOT.RooRealVar(Disc0_name,Disc0_name,dLow0,dHigh0)
		Disc0.setBins(dBins0)
		Disc1 = ROOT.RooRealVar(Disc1_name,Disc1_name,dLow1,dHigh1)
                Disc1.setBins(dBins1)
		Disc2 = ROOT.RooRealVar(Disc2_name,Disc2_name,dLow2,dHigh2)
                Disc2.setBins(dBins2)

		DiscArgSet = ROOT.RooArgSet()
		if self.on_off == 0:
                       DiscArgSet = ROOT.RooArgSet(Disc0,Disc1,Disc2) 
                elif self.on_off == 1:
                        if self.category == 0:
                                DiscArgSet = ROOT.RooArgSet(Disc0,Disc1,Disc2)
                        elif self.category == 1:
                                DiscArgSet = ROOT.RooArgSet(Disc0,Disc1)
                        elif self.category == 2:
                                DiscArgSet = ROOT.RooArgSet(Disc0,Disc1)
                        else:
                                print "INVALID ANALYSIS CATEGORY!"

                else:
                        print "INVALID ON-OFF SHELL CATEGORY!"



		TemplateName = "SM_{0}_{1}_{2}_dataHist".format(self.channel,self.category,self.on_off)
		SMdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgSet, SMtemplate)
		TemplateName = "PS_{0}_{1}_{2}_dataHist".format(self.channel,self.category,self.on_off)
                PSdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgSet, PStemplate)
		TemplateName = "MIX_{0}_{1}_{2}_dataHist".format(self.channel,self.category,self.on_off)
                MIXdataHist = ROOT.RooDataHist(TemplateName, TemplateName, DiscArgSet, MIXtemplate)		

		TemplateName = "SM_{0}_{1}_{2}_HistPDF".format(self.channel,self.category,self.on_off)	
		SMhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, SMdataHist)
                TemplateName = "PS_{0}_{1}_{2}_HistPDF".format(self.channel,self.category,self.on_off)  
                PShistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, PSdataHist)
                TemplateName = "MIX_{0}_{1}_{2}_HistPDF".format(self.channel,self.category,self.on_off)  
                MIXhistFunc = ROOT.RooHistFunc(TemplateName, TemplateName, DiscArgSet, MIXdataHist)

		TemplateName = "SM_{0}_{1}_{2}_norm".format(self.channel,self.category,self.on_off)
		SMnorm = ROOT.RooFormulaVar(TemplateName, "(1-@0)",ROOT.RooArgList(fa3))
		TemplateName = "MIX_{0}_{1}_{2}_norm".format(self.channel,self.category,self.on_off)   
                MIXnorm = ROOT.RooFormulaVar(TemplateName, "sqrt(@0*(1-@0))",ROOT.RooArgList(fa3))
		TemplateName = "PS_{0}_{1}_{2}_norm".format(self.channel,self.category,self.on_off)   
                PSnorm = ROOT.RooFormulaVar(TemplateName, "@0",ROOT.RooArgList(fa3))
		

		TemplateName = "Signal_{0}_{1}_{2}_SumPDF".format(self.channel,self.category,self.on_off)
		SignalPDF = ROOT.RooRealSumPdf(TemplateName, TemplateName, ROOT.RooArgList(SMhistFunc, MIXhistFunc, PShistFunc), ROOT.RooArgSet(SMnorm,MIXnorm,PSnorm))

		TemplateName = "fa3_{0}_{1}_{2}_workspace.root".format(self.channel,self.category,self.on_off) 
		w = ROOT.RooWorkspace("workspace","workspace")
		getattr(w, 'import')(SignalPDF, ROOT.RooFit.RecycleConflictNodes())

		w.writeToFile(TemplateName)  
