from enums import channels
from samples import Sample
import numpy
import os
import ROOT

def maketemplates():

    SM = Sample("VBF", "0+")
    PS = Sample("VBF", "0-")
    half = Sample("VBF", "fa30.5")
    minushalf = Sample("VBF", "fa3-0.5")
    quarter = Sample("VBF", "fa30.25")

    samples = (SM, PS, half, minushalf, quarter)
    for sample in samples: print sample, sample.g1(), sample.g4(), sample.fa3VBF(), sample.JHUcrosssection()

    multipliers = {}
    for sample in samples:
        multipliers[sample] = 1

    matrix = numpy.matrix([[(sample.g1()**(4-i) * sample.g4()**i) * multipliers[sample] for i in range(5)] for sample in samples])
    """
    matrix looks something like this:
    1,    0,      0,        0,      0
    0,    0,      0,        0,      g4^4
    g1^4, g1^3g4, g1^2g4^2, g1g4^3, g4^4
    g1^4, g1^3g4, g1^2g4^2, g1g4^3, g4^4
    g1^4, g1^3g4, g1^2g4^2, g1g4^3, g4^4

    invert the matrix, then multiply by the vector of templates.  This should give back
       templates for each respective term (g1^4g4^0, g1^3g4^1, ...)
    In the PDF, the templates need to be multiplied by (g1^i)(g4^(4-i))
    """
    invertedmatrix = matrix.I
    print matrix
    print invertedmatrix

    for channel in channels:
        f = {}
        for sample in samples:
            f[sample] = ROOT.TFile.Open(sample.templatesfile(channel, None))

        newf = ROOT.TFile.Open(SM.templatesfile(channel, None).replace("0+", "final"), "recreate")
        assert newf
        hstore = {}
        for key in f[SM].GetListOfKeys():
            hold = {}
            hold[SM] = key.ReadObj()
            holdname = hold[SM].GetName()
            for sample in samples:
                if sample is SM: continue
                hold[sample] = f[sample].Get(holdname)

            for i in range(5):
                h = hold[SM].Clone(holdname + "_g1%ig4%i" % (4-i, i))
                hstore[key,i] = h  #so they don't get deleted by python
                h.Reset()
                h.SetTitle(hold[SM].GetTitle() + "_g1%ig4%i" % (4-i, i))
                h.SetDirectory(newf)
                for j, sample in enumerate(samples):
                    h.Add(hold[sample], invertedmatrix[i,j])

        newf.Write()
        newf.Close()

if __name__ == '__main__':
    maketemplates()
