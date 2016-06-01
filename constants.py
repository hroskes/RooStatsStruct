from enums import Category
from math import copysign

SMXS_ggH = 44140  #fb
SMXS_VBF = 3748   #fb
SMBR = 2.76E-04

JHU_XS_a1_ggH = 0.10105985E-01 #+/- 0.36487440E-06
JHU_XS_a2_ggH = 0.36551352E-02 #+/- 0.11450634E-06
JHU_XS_a3_ggH = 0.15447785E-02 #+/- 0.59623472E-07
JHU_XS_L1_ggH = 0.68974668E-10 #+/- 0.23967546E-14
g4_mix_ggH = 2.55052
g2_mix_ggH = 1.65684
g1prime2_mix_ggH = 12100.42

#TEMPORARY DUMMY values for now
#/work-zfs/lhc/heshy/JHUGen/xsecs/JHUGen_interference/JHUGenerator
JHU_XS_g1g2_ggH = 2*JHU_XS_a1_ggH
JHU_XS_g1g4_ggH = 2*JHU_XS_a1_ggH
JHU_XS_g1g1prime2_ggH = 2*JHU_XS_a1_ggH

JHU_XS_g1g2_int_ggH = JHU_XS_g1g2_ggH - JHU_XS_a1_ggH - JHU_XS_a2_ggH*g2_mix_ggH**2
JHU_XS_g1g4_int_ggH = JHU_XS_g1g4_ggH - JHU_XS_a1_ggH - JHU_XS_a3_ggH*g4_mix_ggH**2
JHU_XS_g1g1prime2_int_ggH = JHU_XS_g1g1prime2_ggH - JHU_XS_a1_ggH - JHU_XS_L1_ggH*g1prime2_mix_ggH**2



JHU_XS_a1_VBF = 968.674284006 #+/- 0.075115702763
JHU_XS_a2_VBF = 13102.7106117 #+/- 0.522399748272
JHU_XS_a3_VBF = 10909.5390002 #+/- 0.50975030067
JHU_XS_L1_VBF = 0.000208309799883 #+/- 1.24640942579e-08
g4_mix_VBF = (JHU_XS_a1_VBF / JHU_XS_a3_VBF) ** .5

JHU_XS_a1_ZH = 9022.36 #+/- 1.17
JHU_XS_a3_ZH = 434763.7 #+/- 62.2
g4_mix_ZH = (JHU_XS_a1_ZH / JHU_XS_a3_ZH) ** .5

JHU_XS_a1_WH = 30998.54 #+/- 2.50
JHU_XS_a3_WH = 2028656 #+/- 191
g4_mix_WH = (JHU_XS_a1_WH / JHU_XS_a3_WH) ** .5

luminosity = 30    #fb^-1
r1 = 0.966
r2 = 1.968
r3 = 1.968

g4_mix = {
    Category("ggH"): g4_mix_ggH,
    Category("VBF"): g4_mix_VBF,
    Category("VH"): g4_mix_ZH,
}

def convertfa3(fa3in, categoryin, categoryout):
    categoryin = Category(categoryin)
    categoryout = Category(categoryout)
    return copysign(
                    (abs(fa3in) * g4_mix[categoryin]**2)/(abs(fa3in) * g4_mix[categoryin]**2 + (1-abs(fa3in)) * g4_mix[categoryout]**2),
                    fa3in
                   )
