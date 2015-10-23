import ROOT
#https://github.com/usarica/CMSJHU_AnalysisMacros/blob/9651a7b6c75ece8429041a920eaef058a76f01fd/HiggsLifetime/loadLib.C
ROOT.gSystem.AddIncludePath("-I$CMSSW_BASE/src/");
ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include/");
ROOT.gROOT.LoadMacro("RooRealFlooredSumPdf.cc+");

