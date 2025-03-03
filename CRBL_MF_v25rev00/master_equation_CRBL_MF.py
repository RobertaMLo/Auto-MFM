import numpy as np
import sys
sys.path.append('../')
from load_config_TF import *
import numpy as np

#matplotlib.use('TkAgg')


def build_up_differential_operator_mossy(TFgrc, TFgoc, TFmli, TFpc, w,
                                         Ngrc, Ngoc, Nmossy, Nmli, Npc, T):
    """
    Implements Equation (3.16) in El BOustani & Destexhe 2009
    in the case of a network of two populations:
    one excitatory and one inhibitory

    Each neuronal population has the same transfer function
    this 2 order formalism computes the impact of finite size effects
    T : is the bin for the Markovian formalism to apply

    the time dependent vector is
     V=[Vgrc, Vgoc, Cgrcgrc, Cgrcgoc, Cgrcm, Cmgoc, Cgocgoc, Cmm, Vm, Vmli, Vpc, Cmlimli, Cmlipc, Cgrcpc, Cgrcmli,
     Cpcpc, Cmligoc, Cmlimossy, Cpcgoc, Cpcmossy]
    the function returns Diff_OP
    and d(V)/dt = Diff_OP(V)
    """

    # dVgrc/dt : grc activity
    def A0(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                .5 * V[7] * diff2_fe_fe(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                .5 * V[5] * diff2_fe_fi(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                .5 * V[5] * diff2_fi_fe(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                .5 * V[6] * diff2_fi_fi(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                TFgrc(V[8] + pure_exc_aff, V[1] + inh_aff, w) - V[0])

    # dVgoc/dt : goc activity
    def A1(V, inh_aff=0, pure_exc_aff=0):
        #print('==========================', diff2_fgoc_fgoc_goc(TF2, V[8] + pure_exc_aff, V[0], V[1] + inh_aff))
        return 1. / T * (
                .5 * V[2] * diff2_fgrc_fgrc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                .5 * V[7] * diff2_fm_fm_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                .5 * V[4] * diff2_fgrc_fm_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                .5 * V[3] * diff2_fgrc_fgoc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                .5 * V[3] * diff2_fgoc_fgrc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                .5 * V[5] * diff2_fgoc_fm_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                .4 * V[4] * diff2_fm_fgrc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                .5 * V[5] * diff2_fm_fgoc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                .5 * V[6] * diff2_fgoc_fgoc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                TFgoc(V[8] + pure_exc_aff, V[0], V[1] + inh_aff, w) - V[1])

    # dCgrcgrc/dt : grc variance
    def A2(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                1. / Ngrc * TFgrc(V[8] + pure_exc_aff, V[1] + inh_aff, w) * (
                1. / T - TFgrc(V[8] + pure_exc_aff, V[1] + inh_aff, w)) +
                (TFgrc(V[8] + pure_exc_aff, V[1] + inh_aff, w) - V[0]) ** 2 +
                2. * V[4] * diff_fe(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                2. * V[3] * diff_fi(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                -2. * V[2])

    # dCgrcgoc/dt : grc and goc covariance
    # N.B.: dCgocgrc/dt = dCgrcgoc/dt
    def A3(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                (TFgrc(V[8] + pure_exc_aff, V[1] + inh_aff, w) - V[0]) * (
                TFgoc(V[8] + pure_exc_aff, V[0], V[1] + inh_aff, w) - V[1]) +
                V[2] * diff_fgrc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[3] * diff_fe(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                V[3] * diff_fgoc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[6] * diff_fi(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                V[5] * diff_fe(TFgrc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[4] * diff_fm_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff)+
                - 2. * V[3])

    # dCgrcm/dt : grc and mossy covariance
    def A4(V, inh_aff=0, pure_exc_aff=0):
        #print(V[8])
        return 1 / T *(
                V[5] * diff_fi(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                V[7] * diff_fe(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff)
                - 2. * V[4])

    # dCgocm/dt : goc and mossy covariance
    def A5(V, inh_aff=0, pure_exc_aff=0):
        return 1/ T *(
                V[4] * diff_fgrc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[5] * diff_fgoc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[7] * diff_fm_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff)
                - 2. * V[5])

    # dCgocgoc/dt : goc variance
    def A6(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                1. / Ngoc * TFgoc(V[8] + pure_exc_aff, V[0], V[1] + inh_aff, w) * (
                1. / T - TFgoc(V[8] + pure_exc_aff, V[0], V[1] + inh_aff, w)) +
                (TFgoc(V[8] + pure_exc_aff, V[0], V[1] + inh_aff, w) - V[1]) ** 2 +
                2. * V[3] * diff_fgrc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                2. * V[6] * diff_fgoc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                2. * V[5] * diff_fm_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff)
                - 2. * V[6])

    # dCmm/dt : mossy variance
    def A7(V, inh_aff=0, pure_exc_aff=0):
        #print(V[8])
        return 1. / T * (
                    1. / Nmossy * (V[8] * (
                        1. / T - V[8]))
                    -2. * V[7])

    # v mossy
    def A8(V, inh_aff=0, pure_exc_aff=0):
        #print(V[8])
        #return 1. /T * ((V[8]+1 - V[8])/1)
        return V[8]

    # dvmli/dt
    def A9(V, inh_aff=0, pure_exc_aff=0):
        return (1. / T) * (
                .5 * V[2] * diff2_fe_fe(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                .5 * V[14] * diff2_fe_fi(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                .5 * V[14] * diff2_fi_fe(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                .5 * V[11] * diff2_fi_fi(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                TFmli(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[9])

    # dvpc/dt
    def A10(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                .5 * V[2] * diff2_fe_fe(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                .5 * V[14] * diff2_fe_fi(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                .5 * V[14] * diff2_fi_fe(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                .5 * V[11] * diff2_fi_fi(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                TFpc(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[10])

    # dCmlimli/dt
    def A11(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                1. / Nmli * TFmli(V[0] + pure_exc_aff, V[9] + inh_aff, w) * (
                1. / T - TFmli(V[0] + pure_exc_aff, V[9] + inh_aff, w)) +
                (TFmli(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[9]) ** 2 +
                2. * V[11] * diff_fi(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                2. * V[14] * diff_fe(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff)
                -2. * V[11])

    # dCmlipc/ dt
    def A12(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                (TFmli(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[9]) * (
                TFpc(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[10]) +
                V[12] * diff_fi(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[11] * diff_fi(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[13] * diff_fe(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[14] * diff_fe(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff)
                - 2. * V[12])

    # dCgrcpc/ dt
    def A13(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                (TFgrc(V[8] + pure_exc_aff, V[1] + inh_aff, w) - V[0]) * (
                TFpc(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[10]) +
                V[13] * diff_fi(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[2] * diff_fe(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[18] * diff_fi(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                V[19] * diff_fe(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff)
                - 2. * V[13])

    # dCgrcmli/ dt
    def A14(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                (TFgrc(V[8] + pure_exc_aff, V[1] + inh_aff, w) - V[0]) * (
                TFmli(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[9]) +
                V[14] * diff_fi(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[2] * diff_fe(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[16] * diff_fi(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff) +
                V[17] * diff_fe(TFgrc, V[8] + pure_exc_aff, V[1] + inh_aff)
                - 2. * V[14])

    # dCpcpc/dt
    def A15(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                1. / Npc * TFpc(V[0] + pure_exc_aff, V[9] + inh_aff, w) * (
                1. / T - TFpc(V[0] + pure_exc_aff, V[9] + inh_aff, w)) +
                (TFpc(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[10]) ** 2 +
                2. * V[12] * diff_fi(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                2. * V[13] * diff_fe(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff)
                - 2. * V[15])

    # dCmligoc/dt
    def A16(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                (TFmli(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[9]) * (
                TFgoc(V[8] + pure_exc_aff, V[0], V[1] + inh_aff, w) - V[1]) +
                V[14] * diff_fgrc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[3] * diff_fe(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[16] * diff_fgoc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[16] * diff_fi(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[17] * diff_fm_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff)
                - 2. * V[16])

    # dCmlimossy/ dt
    def A17(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                V[17] * diff_fi(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[4] * diff_fe(TFmli, V[0] + pure_exc_aff, V[9] + inh_aff)
                - 2. * V[17])


    # dCpcgoc/ dt
    def A18(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                (TFpc(V[0] + pure_exc_aff, V[9] + inh_aff, w) - V[10]) * (
                TFgoc(V[8] + pure_exc_aff, V[0], V[1] + inh_aff, w) - V[1]) +
                V[13] * diff_fgrc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[3] * diff_fe(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[18] * diff_fgoc_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff) +
                V[16] * diff_fi(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[19] * diff_fm_goc(TFgoc, V[8] + pure_exc_aff, V[0], V[1] + inh_aff)
                - 2. * V[18])

    # dCpcmossy/dt
    def A19(V, inh_aff=0, pure_exc_aff=0):
        return 1. / T * (
                V[17] * diff_fi(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff) +
                V[4] * diff_fe(TFpc, V[0] + pure_exc_aff, V[9] + inh_aff)
                - 2. * V[19])


    def Diff_OP(V, inh_aff=0, pure_exc_aff=0):
        return np.array([A0(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A1(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A2(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A3(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A4(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A5(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A6(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A7(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A8(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A9(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A10(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A11(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A12(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A13(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A14(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A15(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A16(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A17(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A18(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff),
                         A19(V, inh_aff=inh_aff, pure_exc_aff=pure_exc_aff)
                         ], dtype=object)

    return Diff_OP

# TF differentials for GrC and all pops with two input connections -----------------------------------------------------
def diff_fe(TF, fe, fi, w=0, df=1e-4):
    #print('TF +DF', TF(fe+df_mf/2., fi, w))
    #print('TF-DF', TF(fe-df_mf/2.,fi, w))
    return (TF(fe+df/2., fi, w)-TF(fe-df/2.,fi, w))/df

def diff_fi(TF, fe, fi, w=0, df=1e-4):
    return (TF(fe, fi+df/2., w)-TF(fe, fi-df/2., w))/df

def diff2_fe_fe(TF, fe, fi, w=0, df=1e-4):
    return (diff_fe(TF, fe+df/2., fi, w)-diff_fe(TF, fe-df/2., fi, w))/df

def diff2_fi_fe(TF, fe, fi, w=0, df=1e-4):
    return (diff_fi(TF, fe+df/2., fi, w)-diff_fi(TF,fe-df/2.,fi, w))/df

def diff2_fe_fi(TF, fe, fi, w=0, df=1e-4):
    return (diff_fe(TF, fe, fi+df/2., w)-diff_fe(TF,fe, fi-df/2., w))/df

def diff2_fi_fi(TF, fe, fi, w=0, df=1e-4):
    return (diff_fi(TF, fe, fi+df/2., w)-diff_fi(TF,fe, fi-df/2., w))/df


# TF differentials for Golgi cells -------------------------------------------------------------------------------------
def diff_fm_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (TF_goc(fm+df/2., fgrc, fgoc, w)-TF_goc(fm-df/2., fgrc, fgoc, w))/df

def diff_fgrc_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (TF_goc(fm, fgrc+df/2., fgoc, w)-TF_goc(fm, fgrc-df/2., fgoc, w))/df

def diff_fgoc_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (TF_goc(fm, fgrc, fgoc+df/2., w)-TF_goc(fm, fgrc, fgoc-df/2., w))/df

def diff2_fm_fm_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (diff_fm_goc(TF_goc, fm+df/2., fgrc, fgoc, w)-diff_fm_goc(TF_goc, fm-df/2., fgrc, fgoc, w))/df

def diff2_fgrc_fgrc_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (diff_fgrc_goc(TF_goc, fm, fgrc+df/2., fgoc, w)-diff_fgrc_goc(TF_goc,fm, fgrc-df/2., fgoc, w))/df

def diff2_fgoc_fgoc_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (diff_fgoc_goc(TF_goc, fm, fgrc, fgoc+df/2., w)-diff_fgoc_goc(TF_goc,fm, fgrc, fgoc-df/2., w))/df

def diff2_fm_fgrc_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (diff_fm_goc(TF_goc, fm, fgrc+df/2., fgoc, w)-diff_fm_goc(TF_goc, fm, fgrc-df/2., fgoc, w))/df

def diff2_fgrc_fm_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
   return (diff_fgrc_goc(TF_goc, fm+df/2., fgrc, fgoc, w)-diff_fgrc_goc(TF_goc, fm-df/2., fgrc, fgoc, w))/df

def diff2_fm_fgoc_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (diff_fm_goc(TF_goc, fm, fgrc, fgoc+df/2., w)-diff_fm_goc(TF_goc, fm, fgrc, fgoc-df/2., w))/df

def diff2_fgoc_fm_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (diff_fgoc_goc(TF_goc, fm+df/2., fgrc, fgoc, w)-diff_fgoc_goc(TF_goc, fm-df/2., fgrc, fgoc, w))/df

def diff2_fgrc_fgoc_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (diff_fgrc_goc(TF_goc, fm, fgrc, fgoc+df/2., w)-diff_fgrc_goc(TF_goc, fm, fgrc, fgoc-df/2., w))/df

def diff2_fgoc_fgrc_goc(TF_goc, fm, fgrc, fgoc, w=0, df=1e-4):
    return (diff_fgoc_goc(TF_goc, fm, fgrc+df/2., fgoc, w)-diff_fgoc_goc(TF_goc, fm, fgrc-df/2., fgoc, w))/df



def find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, CI_vec2, t, w, fmossy, Ngrc, Ngoc, Nmossy, Nmli, Npc, T,
                           verbose=False):

    # V = [Vgrc, Vgoc, Cgrcgrc, Cgrcgoc, Cgrcm, Cmgoc, Cgocgoc, Cmm, Vm, Vmli, Vpc, Cmlimli, Cmlipc, Cgrcpc, Cgrcmli,
    #     Cpcpc, Cmligoc, Cmlimossy, Cpcgoc, Cpcmossy]

    ### SECOND ORDER ###

    # simple euler

    X = CI_vec2
    X_vett = np.zeros((len(t), 20))
    for i in range(len(t)):
        last_X = X
        X = X + (t[1] - t[0]) * build_up_differential_operator_mossy(TFgrc, TFgoc, TFmli, TFpc, w,
                                                                Ngrc=Ngrc, Ngoc=Ngoc, Nmossy=Nmossy, Nmli=Nmli, Npc=Npc,
                                                                T=T)(X)
        #X[8] = fmossy[i]/T
        X[8] = fmossy[i]
        #X[4], X[5], X[7] = 0, 0, 0
        X_vett[i, :] = X

    if verbose:
        print(X)
    if verbose:
        print('first order prediction: ', X[-1])

    # return X[-1][0], X[-1][1], np.sqrt(X[-1][2]), np.sqrt(X[-1][3]), np.sqrt(X[-1][4])
    # return X, X[0], X[1], np.sqrt(X[2]), np.sqrt(X[3]), np.sqrt(X[4])
    #return X_vett, X, X[0], X[1], np.sqrt(X[2]), np.sqrt(X[3]), np.sqrt(X[4])
    return X_vett
