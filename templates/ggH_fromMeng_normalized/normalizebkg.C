#include "TFile.h"
#include "TH1.h"
#include "TString.h"
#include <iostream>
#include <map>
using namespace std;

void normalize(TH1* h, double newnormalization)
{
    cout << newnormalization << endl;
    cout << h->Integral("width") << endl;
    h->Scale(newnormalization/h->Integral("width"));
    cout << h->Integral("width") << endl << endl;
}

TString olddir = "../ggH_fromMeng/";
TString newdir = "./";

const int n = 9;
TString files[n] =     {
                        "2e2mu_fa3Adap_new_bkg.root", "2e2mu_fa3Adap_new_bkg.root", "2e2mu_fa3Adap_new_bkg.root",
                        "4e_fa3Adap_new_bkg.root",    "4e_fa3Adap_new_bkg.root",    "4e_fa3Adap_new_bkg.root",
                        "4mu_fa3Adap_new_bkg.root",   "4mu_fa3Adap_new_bkg.root",   "4mu_fa3Adap_new_bkg.root",
                       };
std::map<TString,TFile*> fold;
std::map<TString,TFile*> fnew;
TString templates[n] = {
                        "template_qqZZ", "template_ggZZ", "template_ZX",
                        "template_qqZZ", "template_ggZZ", "template_ZX",
                        "template_qqZZ", "template_ggZZ", "template_ZX",
                       };
//https://github.com/meng-xiao/HiggsAnalysis-HZZ4l_Combination/blob/master/CreateDatacards/HZZ/cards_fa3/
const double luminosity = 19.712;
double rates[n] = {
                   13.6519/*8.8585*/,          0.5005,          4.2929,
                   5.9081/*2.9364*/,          0.2041,          2.7676,
                   9.2487/*7.6478*/,          0.4131,          1.1878,
                  };

void normalizebkg(int i)
{
    if (fold.find(files[i]) == fold.end())
        fold.emplace(files[i], TFile::Open(olddir + "/" + files[i]));
    if (fnew.find(files[i]) == fnew.end())
        fnew.emplace(files[i], TFile::Open(newdir + "/" + TString(files[i]).ReplaceAll("_fa3Adap_new", "_templates"), "RECREATE"));

    TH1 *h = (TH1*)fold[files[i]]->Get(templates[i]);
    h->SetDirectory(fnew[files[i]]);
    normalize(h, rates[i]/luminosity);

    h->SetXTitle("D_{0-}^{decay}");
    h->SetYTitle("D_{CP}^{decay}");
    h->SetZTitle("D_{bkg}");

    h->Write();
}

void normalizebkg()
{
    for (int i = 0; i < n; i++)
        normalizebkg(i);
}
