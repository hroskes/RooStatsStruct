/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            *
 *****************************************************************************/

#ifndef ROOREALFLOOREDSUMPDF
#define ROOREALFLOOREDSUMPDF


#include "RooRealSumPdf.h"

using namespace RooFit;

class RooRealFlooredSumPdf : public RooRealSumPdf {
public:

        RooRealFlooredSumPdf();
        RooRealFlooredSumPdf(const char *name, const char *title);
        RooRealFlooredSumPdf(const char *name, const char *title, const RooArgList& funcList, const RooArgList& coefList, Bool_t extended = kFALSE);
        RooRealFlooredSumPdf(const char *name, const char *title, RooAbsReal &func1, RooAbsReal &func2, RooAbsReal &coef1);
        RooRealFlooredSumPdf(const RooRealFlooredSumPdf& other, const char* name = 0);
        virtual TObject* clone(const char* newname) const { return new RooRealFlooredSumPdf(*this, newname); }
        virtual ~RooRealFlooredSumPdf();

        Double_t evaluate() const;
        Double_t analyticalIntegralWN(Int_t code, const RooArgSet* normSet, const char* rangeName = 0) const;

        constexpr static const double floor = 1e-18;

protected:

        Bool_t _doFloor;
        Double_t _floor;

private:

        ClassDef(RooRealFlooredSumPdf, 4) // PDF constructed from a sum of (non-pdf) functions
};


#endif
