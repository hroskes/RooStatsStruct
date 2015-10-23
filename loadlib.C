#include "TSystem.h"
#include "TROOT.h"
//https://github.com/usarica/CMSJHU_AnalysisMacros/blob/9651a7b6c75ece8429041a920eaef058a76f01fd/HiggsLifetime/loadLib.C
int loadlib()
{
    gSystem->AddIncludePath("-I$CMSSW_BASE/src/");
    gSystem->AddIncludePath("-I$ROOFITSYS/include/");
    gROOT->LoadMacro("RooRealFlooredSumPdf.cc+");
    return 0;
}

const int dummy = loadlib();
