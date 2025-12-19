#import the libraries
import numpy as np
import matplotlib.pyplot as plt
from plot_utils import *
import sys
sys.path.append('../')
import os

from load_config_TF import *
from master_equation_CRBL_MF import *
from theoretical_tools import *


def get_three_ticks(data, variance):
        y_min = np.min(data - np.sqrt(abs(variance)))
        y_max = np.max(data + np.sqrt(abs(variance)))
        y_mid = (y_min + y_max) / 2

        if y_min < 0: y_min=0
        return [round(y_min), round(y_mid), round(y_max)]

def plot_MF_activity_withSD_m(t, X, finput, mytitle, col_vec, alpha, X_ticks, font_size=22, linew=1.5, axes=None):
    """
    Se axes è None, crea una nuova figura con 5 subplot.
    Se axes è passato, disegna sugli assi esistenti.
    """
    if axes is None:
        fig, axes = plt.subplots(5, 1, figsize=(2.4, 4.1))
        fig.suptitle(mytitle, fontsize=font_size + 2)
    else:
        fig = axes[0].figure  # recupera la figura dagli assi

    ax1, ax2, ax3, ax4, ax5 = axes

    # PC
    ax1.plot(t, X[:, 10], col_vec[0], linewidth=linew, alpha=alpha)
    ax1.fill_between(t, X[:, 10] - np.sqrt(abs(X[:, 15])), X[:, 10] + np.sqrt(abs(X[:, 15])),
                     color=col_vec[0], alpha=0.15)
    ax1.set_yticks(X_ticks[0])
    #ax1.set_xticks([])
    ax1.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))

    # MLI
    ax2.plot(t, X[:, 9], col_vec[1], linewidth=linew, alpha=alpha)
    ax2.fill_between(t, X[:, 9] - np.sqrt(abs(X[:, 11])), X[:, 9] + np.sqrt(abs(X[:, 11])),
                     color=col_vec[1], alpha=0.15)
    ax2.set_yticks(X_ticks[1])
    ax2.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))

    # GoC
    ax3.plot(t, X[:, 1], col_vec[2], linewidth=linew, alpha=alpha)
    ax3.fill_between(t, X[:, 1] - np.sqrt(abs(X[:, 6])), X[:, 1] + np.sqrt(abs(X[:, 6])),
                     color=col_vec[2], alpha=0.15)
    ax3.set_ylabel(r'$\nu$ [Hz]', fontsize=font_size, ha='center', va='center', labelpad=20)
    ax3.set_yticks(X_ticks[2])
    ax3.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))

    # GrC
    ax4.plot(t, X[:, 0], col_vec[3], linewidth=linew, alpha=alpha)
    ax4.fill_between(t, X[:, 0] - np.sqrt(abs(X[:, 2])), X[:, 0] + np.sqrt(abs(X[:, 2])),
                     color=col_vec[3], alpha=0.15)
    ax4.set_yticks(X_ticks[3])
    ax4.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))

    # Input (solo una volta, ma se vuoi puoi plottarlo più volte)
    ax5.plot(t, finput, 'black', linewidth=linew*0.5, alpha = alpha)
    ax5.set_yticks(X_ticks[4])
    ax5.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))
    ax5.set_xlabel('t [s]', fontsize=font_size, ha='center', va='center', labelpad=20)

    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    fig.subplots_adjust(hspace=0.5, top=0.92, bottom=0.1)

    return fig, axes


def save_my_files(filename, input_f, mfm_pred):
    #np.savez(filename+'.npz', input_f = input_f, mfm_pred = mfm_pred)
    combined = np.column_stack([input_f, mfm_pred])
    np.savetxt(filename+'.txt', combined)


if __name__ == '__main__':

    type_sim = 'hyper'

    protocol_name = 'gaussian_input_hyper_65' #where to save the output of this protocol of stimulation
    protocol_dir = protocol_name+'_output'
    do_plot = True #true to get the figures

    NRN1, NRN2, NRN3, NRN4 = 'GrC', 'GoC', 'MLI', 'PC'

    root_path = os.getcwd()+'/' #folder where P coefficients were stored
    aa = [3.00, 2.51, 4.31, 9.24] #thr=0.0015 & 0.0020

    NTWK = 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5'
    NTWK_hyp = 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_5_bis' #autism-like; Soda et al.,2019,J.ofNeurosci.
    NTWK_red = 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m6' #schizofrenia-like; Vergani et al.,2025,Poster
    
    print(type_sim)

    if type_sim == 'std':
        FILE_GrC = root_path  + '20250904_101211_GrC_CRBL_CONFIG_AUTOMFM_AWAKE_KmfgrcPLV_tsim5_alpha2.6_fit.npy'
        TFgrc = load_transfer_functions(NRN1, NTWK, FILE_GrC, alpha=aa[0])

    elif type_sim == 'hyper':
        aa_hyp = 4.2
        FILE_GrC_hyp = root_path  + '20251009_214051_GrC_CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_5_bis_tsim5_alpha4.2_fit.npy'
        TFgrc = load_transfer_functions(NRN1, NTWK_hyp, FILE_GrC_hyp, alpha=aa_hyp)

    elif type_sim == 'hypo':
        aa_red = 1.0
        FILE_GrC_red = root_path  + '20251103_194645_GrC_CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m6_tsim5_alpha1.0_fit.npy'
        TFgrc = load_transfer_functions(NRN1, NTWK_red, FILE_GrC_red, alpha=aa_red)

    else:
        print('Error in type sim')

    FILE_GoC = root_path + '20250903_213910_GoC_CRBL_CONFIG_AUTOMFM_AWAKE_KgrcgocSUM_tsim5_alpha1.9_fit.npy'
    TFgoc = load_transfer_functions_goc(NRN2, NTWK, FILE_GoC, alpha=aa[1])

    FILE_MLI = root_path + '20250903_184431_MLI_CRBL_CONFIG_AUTOMFM_AWAKE_MLIMLIxPLV_tsim5_alpha1.8_fit.npy'
    TFmli = load_transfer_functions(NRN3, NTWK, FILE_MLI, alpha=aa[2])

    FILE_PC = root_path + '20250903_190157_PC_CRBL_CONFIG_AUTOMFM_AWAKE_Qmlipc1.22_KgrcpcSUM_tsim5_alpha1.8_fit.npy'
    TFpc = load_transfer_functions(NRN4, NTWK, FILE_PC, alpha=aa[3])


    os.makedirs(protocol_dir, exist_ok=True)

    
    ## Standard parameters
    Ngrc = 29916
    Ngoc = 71
    Nmossy = 2340
    Nmli = 302+150
    Npc = 69

    dt = 1e-4
    sim_len = 0.5
    t = np.arange(0, sim_len, dt)

    T = 3.5e-3
    w = 0. #adaptation not included at the moment

    ## Backnoise 
    f_backnoise = np.random.rand(len(t))*4 #background noise set around 4 Hz

   #Gaussian parameters 
    sigmas = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    amps = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]


    for sigma in sigmas:
        for amp in amps:

            # Gaussian definition
            mu = t[len(t)//2]
            gauss = amp * np.exp(-0.5 * ((t - mu) / sigma)**2)
            f_gauss_back = gauss + f_backnoise

            # Simulation for gaussian input
            CI_vec = [0.5, 5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, f_backnoise[0], 15, 38, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
            X_gauss = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, CI_vec, t, w, f_gauss_back, Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)
            save_my_files(protocol_dir+'/'+protocol_name+str(sigma)+'_'+str(amp), input_f=f_gauss_back, mfm_pred=X_gauss)

            #plotting part
            if do_plot:
                X_ticks_PC    = get_three_ticks(X_gauss[:, 10], X_gauss[:, 15])
                X_ticks_MLI   = get_three_ticks(X_gauss[:, 9],  X_gauss[:, 11])
                X_ticks_GoC   = get_three_ticks(X_gauss[:, 1],  X_gauss[:, 6])
                X_ticks_GrC   = get_three_ticks(X_gauss[:, 0],  X_gauss[:, 2])
                X_ticks_input = get_three_ticks(f_gauss_back, np.zeros_like(f_gauss_back))
                X_ticks = [X_ticks_PC, X_ticks_MLI, X_ticks_GoC, X_ticks_GrC, X_ticks_input]

                fig_stim, axes_stim = plot_MF_activity_withSD_m(
                    t, X_gauss, f_gauss_back, "", 
                    col_vec=['green','orange','blue','red'], 
                    alpha=0.99, X_ticks=X_ticks, font_size=14, linew=0.8
                )

                fig_stim.savefig(protocol_dir+'/'+protocol_name+str(sigma)+str(amp)+'.png', dpi=300, bbox_inches="tight")



