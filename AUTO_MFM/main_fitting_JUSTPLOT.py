import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from fitting_TF_withGoc_BSB import *
from main_fitting_TF_BSB import call_plot_fitting_goc, call_plot_fitting, plot_TF_numerical_vs_analytical_2D_modspace


def set_params_for_plotting(FOLDER, alpha, MEANfreq, sd_freq, w, fiSim, Fe_m_eff):
    
    max_index_fi = len(fiSim)
    max_ind_fe = len(Fe_m_eff)

    MEANfreq = MEANfreq[:max_index_fi, :max_ind_fe]
    SDfreq = sd_freq[:max_index_fi, :max_ind_fe]
    fiSim = fiSim[:max_index_fi, :max_ind_fe]
    Fe_eff_m = Fe_m_eff[:max_index_fi, :max_ind_fe]
    w = w[:max_index_fi, :max_ind_fe]
    P = np.load(FOLDER + '_alpha' + str(alpha) + '_fit.npy', allow_pickle=True)

    return MEANfreq, SDfreq, w, fiSim, Fe_eff_m, P

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     """ 
                                   'Procedure to check fitting of all pops'
                                   """,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-FOLDER', help="protocol folder of numerical TF data", \
                        default='data/example_data.npy')
    
    parser.add_argument('-zeb', help="zebrine configuration 0=YES - 1=NO", \
                        type = bool, default=1)

    parser.add_argument('-alpha', help="alpha value used to compute P", \
                        type = float, default=1.0)



    args = parser.parse_args()

    adap = False

    if '_GoC_' in args.FOLDER:
        MEANfreq_goc, sd_freq_goc, w_goc, fiSim_goc, Fe_m_eff_goc, Fe_g_eff_goc, params_goc, sim_params_goc = \
            load_my_data_bsb_goc(args.FOLDER, adap)

        print('=============== GOLGI ===========================')
        fix_index_mossy = 3 #last mf input -- most critical

        #P = np.load(FOLDER_goc_numTF+'_alpha1.0_fit.npy',allow_pickle=True)
        barname = '_GoC_'
        call_plot_fitting_goc(args.FOLDER, args.alpha, MEANfreq_goc, sd_freq_goc, w_goc, fiSim_goc,  Fe_g_eff_goc, Fe_m_eff_goc, params_goc, barname,
                          fix_index_mossy)
                          
                          
                          
    elif '_MLI_' in args.FOLDER or '_PC_' in args.FOLDER:

        MEANfreq, sd_freq, w, fiSim, Fe_m_eff, params, sim_params = \
            load_my_data_bsb(args.FOLDER, adap)

        #P = np.load(FOLDER_mli_numTF + '_alpha1.5_fit.npy', allow_pickle=True)
        #max_index_fi = len(fiSim)
        #max_ind_fe = len(Fe_m_eff)
        #call_plot_fitting(args.FOLDER, args.alpha, MEANfreq, sd_freq, w, fiSim, Fe_m_eff, params,
        #              xname='GrC', barname='MLI')
                      
        yout_max = 80
                      
        MEANfreq, SDfreq, w, fiSim, Fe_eff_m, P = set_params_for_plotting(args.FOLDER, args.alpha, MEANfreq, sd_freq, w, fiSim, Fe_m_eff)


        plot_TF_numerical_vs_analytical_2D_modspace(MEANfreq, SDfreq, fiSim, Fe_eff_m, yout_max, w,
                                                 P, args.alpha, params, xname='', barname='', FOLDER=args.FOLDER, facW=1)


  

    elif '_GrC_' in args.FOLDER:

        MEANfreq_grc, sd_freq_grc, w_grc, fiSim_grc, Fe_m_eff_grc, params_grc, sim_params_grc = \
            load_my_data_bsb(args.FOLDER, adap)

        print('=============== GRANULES ===========================')
        #P = np.load(FOLDER_grc_numTF + '_alpha1.7_fit.npy', allow_pickle=True)

        #max_index_fi = len(fiSim_grc)
        #max_ind_fe = len(Fe_m_eff_grc)
        #call_plot_fitting(args.FOLDER, args.alpha, MEANfreq_grc, sd_freq_grc, w_grc, fiSim_grc, Fe_m_eff_grc, params_grc,
        #              xname='mossy fibres', barname='GoC')
        
        yout_max = 280#125
                      
        MEANfreq, SDfreq, w, fiSim, Fe_eff_m, P = set_params_for_plotting(args.FOLDER, args.alpha, MEANfreq_grc, sd_freq_grc, w_grc, fiSim_grc, Fe_m_eff_grc)


        plot_TF_numerical_vs_analytical_2D_modspace(MEANfreq, SDfreq, fiSim, Fe_eff_m, yout_max, w,
                                                 P, args.alpha, params_grc, xname='', barname='', FOLDER=args.FOLDER, facW=1)
                      
                      
         
