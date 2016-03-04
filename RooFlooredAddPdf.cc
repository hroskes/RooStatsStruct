#include "RooFlooredAddPdf.h"

ClassImp(RooFlooredAddPdf)



//_____________________________________________________________________________
RooFlooredAddPdf::RooFlooredAddPdf() :
RooAddPdf(),
_doFloor(true),
_floor(floor)
{}



//_____________________________________________________________________________
RooFlooredAddPdf::RooFlooredAddPdf(const char *name, const char *title) :
RooAddPdf(name, title),
_doFloor(true),
_floor(floor)
{}



//_____________________________________________________________________________
RooFlooredAddPdf::RooFlooredAddPdf(const char *name, const char *title, RooAbsPdf &pdf1, RooAbsPdf &pdf2, RooAbsReal &coef1) :
RooAddPdf(name, title, pdf1, pdf2, coef1),
_doFloor(true),
_floor(floor)
{}




//_____________________________________________________________________________
RooFlooredAddPdf::RooFlooredAddPdf(const char *name, const char *title, const RooArgList &pdfList) :
RooAddPdf(name, title, pdfList),
_doFloor(true),
_floor(floor)
{}




//_____________________________________________________________________________
RooFlooredAddPdf::RooFlooredAddPdf(const char *name, const char *title, const RooArgList &pdfList, const RooArgList &coefList, Bool_t recursiveFraction) :
RooAddPdf(name, title, pdfList, coefList, recursiveFraction),
_doFloor(true),
_floor(floor)
{}




//_____________________________________________________________________________
RooFlooredAddPdf::RooFlooredAddPdf(const RooFlooredAddPdf& other, const char* name) :
RooAddPdf(other, name),
_doFloor(other._doFloor),
_floor(other._floor)
{}



//_____________________________________________________________________________
RooFlooredAddPdf::~RooFlooredAddPdf() {}





//_____________________________________________________________________________
Double_t RooFlooredAddPdf::evaluate() const
{
  Double_t value = RooAddPdf::evaluate();
  if (value < _floor && _doFloor) value = _floor; // Last IEEE double precision

  return value;
}




//_____________________________________________________________________________
Double_t RooFlooredAddPdf::analyticalIntegralWN(Int_t code, const RooArgSet* normSet2, const char* rangeName) const
{
  Double_t result = RooAddPdf::analyticalIntegralWN(code, normSet2, rangeName);
  if (result<_floor && _doFloor){
    coutW(Eval) << "RooFlooredAddPdf::integral(" << GetName()
      << " WARNING: Integral below threshold: " << result << endl;
    result = _floor; // A somewhat larger number
  }
  return result;
}
