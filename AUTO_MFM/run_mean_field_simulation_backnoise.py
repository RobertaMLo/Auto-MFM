"""
CRBL MF v25
v.1 -  February 2025 - SNN reference = basal awake v0.5

authors: Roberta Maria Lorenzi </b>
contacts: robertamaria.lorenzi01@universitadipavia.it

Update version of Cerebellar mean-field (CRBL-MF v25) based on a mouse-awake configurations
See 'CRBL_CONFIG_20PARALLEL_wN_PLOS23_Kredmf_grc' for details on K and Q tuning.
SNN is the canonical awake. Prameters tuning to scale up from micro to mesoscale performed for numerical TF computation.

Method reference to be cited: 
Lorenzi et al. 2023 (https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011434)
"""

import numpy as np
import matplotlib.pyplot as plt

#import sys
#sys.path.append('../')
import os

from load_config_TF import *
from master_equation_CRBL_MF import *
from theoretical_tools import *



def plot_MF_activity_withSD(t, X, finput, mytitle, outdir, font_size = 22, linew=1.5):
    """
    Function to plot and save the mean field predction.
    
    Input:
        t = (ndarray) simulation time (ntimepoint)
        X = (ndarray) simulated activity (ntimepoint x nequations)
            X= [Vgrc, Vgoc, Cgrcgrc, Cgrcgoc, Cgrcm, Cmgoc, Cgocgoc, Cmm, Vm, Vmli, Vpc, 
                    Cmlimli, Cmlipc, Cgrcpc, Cgrcmli, Cpcpc, Cmligoc, Cmlimossy, Cpcgoc, Cpcmossy]
        finput = (ndarray) input frequency (ntimepoint)
        outdir = output directory for saving the plot (.png, dpi = 300)
        fontsize  = (int) font size for the figures
        linew = (float) thickness for the lines plotted

    !!!!!!! N.B.: With python 3.10 ax.fill_between might throw an error. Here, runned with python 3.8
    """

    fig, (ax1, ax2, ax3, ax4, ax5 ) = plt.subplots(5, 1, figsize =(5.8,4.1)) # for half of 1/4 of A4
    fig.suptitle(mytitle, fontsize = font_size+2)

    def get_three_ticks(data, variance):
        """
        To get equispaced ticks based on avg and std
        """
        y_min = np.min(data - np.sqrt(variance))
        y_max = np.max(data + np.sqrt(variance))
        y_mid = (y_min + y_max) / 2
        return [round(y_min), round(y_mid), round(y_max)]

    # Limit at 0, because I don't want negative freqiencies
    mask = (X< 0) | np.isnan(X) | np.isinf(X)
    X[mask] = 0

    # PC --------------------------------------------------------------------------------------------------------------
    
    pc_line, = ax1.plot(t, X[:, 10], 'green', linewidth = linew, label = 'PC')
    ax1.fill_between(t, X[:,10] - np.sqrt(X[:, 15]), X[:,10] + np.sqrt(X[:,15]), color = 'green', alpha = 0.4)
    
    #Three ticks for each subplot (max min and middle point between max and min)
    ax1.set_yticks(get_three_ticks(X[:,10], X[:,15]))

    ax1.set_xticks([])

    # MLI --------------------------------------------------------------------------------------------------------------
    mli_line, = ax2.plot(t, X[:,9], 'orange', linewidth = linew, label  = 'MLI')
    ax2.fill_between(t, X[:, 9] + np.sqrt(abs(X[:, 11])), X[:, 9] - np.sqrt(abs(X[:, 11])), facecolor='orange', alpha=0.4)

    ax2.set_yticks(get_three_ticks(X[:,9], X[:,11]))

    ax2.set_xticks([])

    # GoC --------------------------------------------------------------------------------------------------------------
    goc_line, = ax3.plot(t, X[:,1], 'blue', linewidth = linew, label = 'GoC')
    ax3.fill_between(t, X[:, 1] + np.sqrt(abs(X[:, 6])), X[:, 1] - np.sqrt(abs(X[:, 6])), facecolor='blue', alpha=0.4)
    
    #to get the generic y labels at middle of suplots 
    ax3.set_ylabel('Activity [Hz]', fontsize=font_size, ha='center', va = 'center', labelpad = 20)
    
    ax3.set_yticks(get_three_ticks(X[:,1], X[:,6]))

    ax3.set_xticks([])

    # GrC --------------------------------------------------------------------------------------------------------------
    grc_line, = ax4.plot(t, X[:,0], 'red', linewidth = linew, label = 'GrC')
    ax4.fill_between(t, X[:, 0] + np.sqrt(abs(X[:, 2])), X[:, 0] - np.sqrt(abs(X[:, 2])), facecolor='red', alpha=0.4)

    ax4.set_yticks(get_three_ticks(X[:,0], X[:,2]))

    ax4.set_xticks([])

    # Input ------------------------------------------------------------------------------------------------------------
    input_line, = ax5.plot(t, finput, 'black', linewidth = linew, label = 'mfs')

    ax5.set_yticks(get_three_ticks(finput, np.zeros_like(finput)))

    ax5.set_xlabel('time [s]', fontsize = font_size, ha='center', va = 'center', labelpad = 20)

    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    #fig.tight_layout()
    fig.subplots_adjust(hspace = 0.5, top=0.92, bottom = 0.1)

    legend_lines = [pc_line, mli_line, goc_line, grc_line, input_line]

    fig.legend(handles = legend_lines, loc="center left", fontsize=font_size - 2, ncol=1, frameon=True, bbox_to_anchor=(0.95, 0.5))

    plt.savefig(outdir+'/'+'mf_activity.pdf', dpi = 300, bbox_inches='tight') #bbox added to save the figure correctly
    #plt.show()
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=
                                    """ 
                                    'Main routine for constrcutive validity with basal awake configuration'
                                    """,
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-FOLDER",
                        help="Folder where my Pfile are stored")
    
    parser.add_argument("-NTWK", help="synaptic and connectivity properties",
                        default = 'CRBL_CONFIG_PLV_KandQ_v3')

    parser.add_argument('-f_backnoise', type=float, 
                        default=4., help="Backgound noise rate [Hz], default at 4 Hz")
    
    parser.add_argument('-alfa', type=float, nargs=4, default=[1.8, 2.9, 1.9, 2.7], #fist trial [2., 1.7, 3., 10.]
                        help="alpha for prediction [GrC GoC MLI PC]")
    
    parser.add_argument('-sim_len', type=float, default=0.5,
                        help="length of the simulation [s]")
    
    parser.add_argument('-dt', type=float, default=1e-4,
                        help=" time step [s]")
    
    parser.add_argument('-t_trans', type=int, default=1000,
                        help ="points to be discared for transients")

    parser.add_argument('-save_sim', type=bool, default=False,
                        help ="save npy file ofr each pop [avg, sd]")

    args = parser.parse_args()

    
    root_path = args.FOLDER
    NTWK = args.NTWK
    f_backnoise = args.f_backnoise
    sim_len = args.sim_len
    dt = args.dt
    t_trans = args.t_trans

    outdir_name= str(f_backnoise)+'_'+NTWK 
    outdir = os.path.join(root_path, outdir_name)
    os.makedirs(outdir, exist_ok=True)
    
    
    print('\n\n========================================================================')
    print('Running in: ', root_path)
    print('Output will be saved in: ', outdir, '\nsave flag: ',args.save_sim)
    print('Configurations: ', NTWK)
    print('alpha  [Grc, GoC, MLI, PC]: ', args.alfa)
    print('Background noise frequency: ', f_backnoise)
    print('===========================================================================\n\n')

    # Number of cells are fixed according to SNN
    Ngrc = 29916
    Ngoc = 71
    Nmossy = 2340
    Nmli = 302+150
    Npc = 69

    # Mean Field time constat fixed to the optimized value (Lorenzi et al., 20203, PLOS Comp Bio)
    T = 3.5e-3
    w = 0. #adaptation not included at the moment

    # Populations
    NRN1, NRN2, NRN3, NRN4 = 'GrC', 'GoC', 'MLI', 'PC'
    
    print(root_path)

    # Loading the Transfer Functions - definitiva
    FILE_GrC = root_path + '20250904_101211_GrC_CRBL_CONFIG_AUTOMFM_AWAKE_KmfgrcPLV_tsim5_alpha2.6_fit.npy'
    print(FILE_GrC)
    FILE_GoC = root_path + '20250903_213910_GoC_CRBL_CONFIG_AUTOMFM_AWAKE_KgrcgocSUM_tsim5_alpha1.9_fit.npy'


    #FIT 5
    FILE_MLI = root_path + '20250903_184431_MLI_CRBL_CONFIG_AUTOMFM_AWAKE_MLIMLIxPLV_tsim5_alpha1.8_fit.npy'
    
    #FILE_PC = root_path + '20250903_190157_PC_CRBL_CONFIG_AUTOMFM_AWAKE_Qmlipc1.22_KgrcpcSUM_tsim5_alpha1.8_fit.npy' #zmin
    
    FILE_PC = root_path + '20251107_181916_PC_CRBL_CONFIG_AUTOMFM_AWAKE_tsim5_580_alpha1.5_fit.npy' #plus



    TFgrc = load_transfer_functions(NRN1, NTWK, FILE_GrC, alpha = args.alfa[0]) 
    TFgoc = load_transfer_functions_goc(NRN2, NTWK, FILE_GoC, alpha = args.alfa[1])
    TFmli = load_transfer_functions(NRN3, NTWK, FILE_MLI, alpha = args.alfa[2])
    TFpc = load_transfer_functions(NRN4, NTWK, FILE_PC, alpha = args.alfa[3]) 

    t = np.arange(0, sim_len, dt)
    
    # Simulations!

    # X = vector of activity with Vp = population p mean activity, Csp = covariance between population s and p
    # X = [Vgrc, Vgoc, Cgrcgrc, Cgrcgoc, Cgrcm, Cmgoc, Cgocgoc, Cmm, Vm, Vmli, Vpc, Cmlimli, Cmlipc, Cgrcpc, Cgrcmli,
    #     Cpcpc, Cmligoc, Cmlimossy, Cpcgoc, Cpcmossy]
    f_mossy = np.random.rand(len(t))*f_backnoise

    #f_mossy = np.ones(len(t))*f_backnoise #background noise set around 4 Hz

    CI_vec = [0.5, 5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, f_mossy[0], 15, 38, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

    X_sim = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, CI_vec, t, w, f_mossy,
                           Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)

    ## metto a mano il check su sdev!!!!
    mask = (X_sim < 0) | np.isnan(X_sim) | np.isinf(X_sim)
    X_sim[mask] = 0

    if args.save_sim:
    
        # Simulated activity and SD for each population (5000, ) --> timeseries
        np.save(outdir+'/PC_act_sd.npy', [X_sim[:, 10], np.sqrt(X_sim[:, 15])])
        np.save(outdir+'/MLI_act_sd.npy', [X_sim[:, 9], np.sqrt(X_sim[:, 11])])
        np.save(outdir+'/GoC_act_sd.npy', [X_sim[:, 1], np.sqrt(X_sim[:, 6])])
        np.save(outdir+'/GrC_act_sd.npy', [X_sim[:, 0], np.sqrt(X_sim[:, 2])])
        np.save(outdir+'/Input.npy', f_mossy)
        np.savetxt(outdir+'/alphas.txt', args.alfa)
        #np.savetxt(outdir+'/TFnames.txt',TFgrc, TFgoc, TFmli, TFpc)
        print('Full-time simulations saved in: ', outdir)

        #Average activity and SD for each population (1, ) --> value for boxplot
        np.save(outdir+'/PC_TOT_AVG_SD.npy', [np.average(X_sim[:, 10]), np.average(np.sqrt(X_sim[:, 15]))])
        np.save(outdir+'/MLI_TOT_AVG_SD.npy', [np.average(X_sim[:, 9]), np.average(np.sqrt(X_sim[:, 11]))])
        np.save(outdir+'/GoC_TOT_AVG_SD.npy', [np.average(X_sim[:, 1]), np.average(np.sqrt(X_sim[:, 6]))])
        np.save(outdir+'/GrC_TOT_AVG_SD.npy', [np.average(X_sim[:, 0]), np.average(np.sqrt(X_sim[:, 2]))])
   

    plot_MF_activity_withSD(t[t_trans:], X_sim[t_trans:], f_mossy[t_trans:], 
                            mytitle = 'MF_activity', outdir = outdir, font_size = 12, linew=1)



