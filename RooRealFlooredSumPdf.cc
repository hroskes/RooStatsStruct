#include "RooRealFlooredSumPdf.h"

ClassImp(RooRealFlooredSumPdf)



//_____________________________________________________________________________
RooRealFlooredSumPdf::RooRealFlooredSumPdf() :
RooRealSumPdf(),
_doFloor(true),
_floor(floor)
{}



//_____________________________________________________________________________
RooRealFlooredSumPdf::RooRealFlooredSumPdf(const char *name, const char *title) :
RooRealSumPdf(name, title),
_doFloor(true),
_floor(floor)
{}



//_____________________________________________________________________________
RooRealFlooredSumPdf::RooRealFlooredSumPdf(const char *name, const char *title, const RooArgList& inFuncList, const RooArgList& inCoefList, Bool_t extended) :
RooRealSumPdf(name, title, inFuncList, inCoefList, extended),
_doFloor(true),
_floor(floor)
{}




//_____________________________________________________________________________
RooRealFlooredSumPdf::RooRealFlooredSumPdf(const char *name, const char *title, RooAbsReal &func1, RooAbsReal &func2, RooAbsReal &coef1) :
RooRealSumPdf(name, title, func1, func2, coef1),
_doFloor(true),
_floor(floor)
{}




//_____________________________________________________________________________
RooRealFlooredSumPdf::RooRealFlooredSumPdf(const RooRealFlooredSumPdf& other, const char* name) :
RooRealSumPdf(other, name),
_doFloor(other._doFloor),
_floor(other._floor)
{}



//_____________________________________________________________________________
RooRealFlooredSumPdf::~RooRealFlooredSumPdf() {}





//_____________________________________________________________________________
Double_t RooRealFlooredSumPdf::evaluate() const
{
  Double_t value = RooRealSumPdf::evaluate();
  if (value < _floor && _doFloor) value = _floor; // Last IEEE double precision

  return value;
}




//_____________________________________________________________________________
Double_t RooRealFlooredSumPdf::analyticalIntegralWN(Int_t code, const RooArgSet* normSet2, const char* rangeName) const
{
  Double_t result = RooRealSumPdf::analyticalIntegralWN(code, normSet2, rangeName);
  if (result<_floor && _doFloor){
    coutW(Eval) << "RooRealFlooredSumPdf::integral(" << GetName()
      << " WARNING: Integral below threshold: " << result << endl;
    result = _floor; // A somewhat larger number
  }
  return result;
}
