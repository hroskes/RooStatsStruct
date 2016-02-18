#include "TFile.h"
#include "TH1.h"
#include "TString.h"
#include <iostream>
#include <map>
using namespace std;

bool justcopy = false;

void normalize(TH1* h, double newnormalization)
{
    h->Scale(newnormalization/h->Integral("width"));
}

TString olddir = "../ggH_fromMeng/";
TString newdir = ".";

const int nflavors = 3;
const int ntemplates = 3;
TString files[nflavors] = {
                           "2e2mu_fa3Adap_new.root",
                           "4e_fa3Adap_new.root",
                           "4mu_fa3Adap_new.root",
                          };
std::map<TString,TFile*> fold;
std::map<TString,TFile*> fnew;
TString templates[ntemplates] = {
                                 "template0PlusAdapSmoothMirror", "template0MinusAdapSmoothMirror", "templateIntAdapSmoothMirror",
                                };
//https://github.com/usarica/HiggsAnalysis-HZZ4l_Combination/blob/master/CreateDatacards/SM_inputs_8TeV/inputs_2e2mu.txt
const double luminosity = 19.712;
double rates[nflavors] = {
                          7.6807,
                          3.0898,
                          5.9471,
                         };

void normalizesig(int i)
{
    if (fold.find(files[i]) == fold.end())
        fold.emplace(files[i], TFile::Open(olddir + "/" + files[i]));
    if (fnew.find(files[i]) == fnew.end())
        fnew.emplace(files[i], TFile::Open(newdir + "/" + TString(files[i]).ReplaceAll("_fa3Adap_new", "_templates"), "RECREATE"));

    TH1 *hSM = (TH1*)fold[files[i]]->Get(templates[0]);
    double multiply = rates[i] / luminosity / hSM->Integral("width");
    cout << multiply << endl;

    for (int j = 0; j < ntemplates; j++)
    {
        TH1 *h = (TH1*)fold[files[i]]->Get(templates[j]);
        h->SetDirectory(fnew[files[i]]);
        cout << "    " << h->Integral("width") << endl;
        if (!justcopy)
            h->Scale(multiply);
        cout << "    " << h->Integral("width") << endl;

        h->SetXTitle("D_{0-}^{decay}");
        h->SetYTitle("D_{CP}^{decay}");
        h->SetZTitle("D_{bkg}");

        h->Write();
    }
}

void normalizesig()
{
    for (int i = 0; i < nflavors; i++)
        normalizesig(i);
}
