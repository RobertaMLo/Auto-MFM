import numpy as np
import argparse
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from fitting_TF_withGoc_BSB import *


def call_plot_fitting_goc(FOLDER, alpha, MEANfreq, sd_freq, w, fiSim, Fe_g_eff, Fe_m_eff, params, barname, fix_index_mossy):
    max_ind_fi = len(fiSim)
    max_ind_fe = len(Fe_g_eff)

    MEANfreq = MEANfreq[:max_ind_fi, :max_ind_fe, fix_index_mossy]
    SDfreq = sd_freq[:max_ind_fi, :max_ind_fe, fix_index_mossy]
    fiSim = fiSim[:max_ind_fi, :max_ind_fe, fix_index_mossy]
    Fe_eff_grc = Fe_g_eff[:max_ind_fi, :max_ind_fe, fix_index_mossy]
    w = w[:max_ind_fi, :max_ind_fe, fix_index_mossy]
    P = np.load(FOLDER + '_alpha' + str(alpha) + '_fit.npy', allow_pickle=True)
    plot_TF_numerical_vs_analytical_goc_fixMossy(MEANfreq, SDfreq, fiSim, Fe_eff_grc, Fe_m_eff, w, fix_index_mossy,
                                                 P, alpha, params, barname, facW=1)


def call_plot_fitting(FOLDER, alpha, MEANfreq, sd_freq, w, fiSim, Fe_m_eff, params, xname, barname):
    max_index_fi = len(fiSim)
    max_ind_fe = len(Fe_m_eff)

    MEANfreq = MEANfreq[:max_index_fi, :max_ind_fe]
    SDfreq = sd_freq[:max_index_fi, :max_ind_fe]
    fiSim = fiSim[:max_index_fi, :max_ind_fe]
    Fe_eff_m = Fe_m_eff[:max_index_fi, :max_ind_fe]
    w = w[:max_index_fi, :max_ind_fe]
    P = np.load(FOLDER + '_alpha' + str(alpha) + '_fit.npy', allow_pickle=True)

    plot_TF_numerical_vs_analytical_2D(MEANfreq, SDfreq, fiSim, Fe_eff_m, w,
                                                 P, alpha, params, xname, barname, FOLDER, facW=1)



if __name__ == '__main__':
    # First a nice documentation
    parser = argparse.ArgumentParser(description=
                                     """ 
                                   'TF Fitting Procedure to get P coefficient'
                                   """,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-FOLDER', help="file name of numerical TF data", \
                        default='data/example_data.npy')

    parser.add_argument("-alpha", help="params to fit high frequencies",
                        type=float, default=1.)

    parser.add_argument("-adap_bool", type=bool, default=False, help="Include Adaptation outcome or not")

    args = parser.parse_args()
    alpha = args.alpha
    FOLDER = args.FOLDER
    xname = 'mossy fibers' #'GrC'#'mossy fibres'
    barname = 'GoC' #'MLI'#'GoC'

    if '_GoC_' in args.FOLDER:
        print('3 Pops fitting')

        MEANfreq, sd_freq, w, fiSim, Fe_m_eff, Fe_g_eff, params, sim_params = load_my_data_bsb_goc(args.FOLDER,
                                                                                               args.adap_bool)

        # some checks
        #print('Adap bool: ', args.adap_bool)
        print('Alpha: ', args.alpha)

        P_goc = make_fit_from_data_eglif_goc_bsb(args.FOLDER, args.alpha, args.adap_bool)

        fix_index_mossy =  15
        

        print('======================================== Plot with Fixed Fmossy at: ', Fe_m_eff[fix_index_mossy])

        call_plot_fitting_goc(FOLDER, alpha, MEANfreq, sd_freq, w, fiSim, Fe_g_eff, Fe_m_eff, params, barname, fix_index_mossy)

    else:
        print ('2 Pops routine')

        MEANfreq, sd_freq, w, fiSim, Fe_m_eff, params, sim_params = load_my_data_bsb(args.FOLDER, args.adap_bool)

        # some checks
        #print('Adap bool: ', args.adap_bool)
        print('Alpha: ', args.alpha)

        max_index_fi = len(fiSim)
        max_ind_fe = len(Fe_m_eff)

        P = make_fit_from_data_eglif_bsb(args.FOLDER, args.alpha, args.adap_bool)

        call_plot_fitting(FOLDER, alpha, MEANfreq, sd_freq, w, fiSim, Fe_m_eff, params, xname=xname, barname=barname)


