#include "TFile.h"
#include "TH1.h"
#include "TString.h"
#include <iostream>
#include <map>
using namespace std;

void normalize(TH1* h, double newnormalization)
{
    cout << newnormalization << endl;
    cout << h->Integral() << endl;
    h->Scale(newnormalization/h->Integral());
    cout << h->Integral() << endl << endl;
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
//https://github.com/usarica/HiggsAnalysis-HZZ4l_Combination/blob/master/CreateDatacards/SM_inputs_8TeV/inputs_2e2mu.txt
const double luminosity = 19.712;
double rates[n] = {
                   8.8585,          0.5005,          4.2929,
                   2.9364,          0.2041,          2.7676,
                   7.6478,          0.4131,          1.1878,
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
    h->Write();
}

void normalizebkg()
{
    for (int i = 0; i < n; i++)
        normalizebkg(i);
}
