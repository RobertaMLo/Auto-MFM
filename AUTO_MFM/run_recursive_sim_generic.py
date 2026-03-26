"""
PATHOLOGY MFM USE-CASE:
- load of pathological TF
- simulation background noise-like (f = 4 --- 40 Hz)
- computation of statistics and boxplots

To be runned to get the differences in trend in the input spaces.
"""


#import the libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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


def plot_MF_activity_withSD_m(t, X, finput, mytitle, col_vec, alpha, X_ticks, font_size=22, linew=1.5, lines = '-', axes=None):
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
    ax1.plot(t, X[:, 10], col_vec[0], linewidth=linew, alpha=alpha,  linestyle= lines)
    ax1.fill_between(t, X[:, 10] - np.sqrt(abs(X[:, 15])), X[:, 10] + np.sqrt(abs(X[:, 15])),
                     color=col_vec[0], alpha=0.05)
    ax1.set_yticks(X_ticks[0])
    #ax1.set_xticks([])
    ax1.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))

    # MLI
    ax2.plot(t, X[:, 9], col_vec[1], linewidth=linew, alpha=alpha,  linestyle= lines)
    ax2.fill_between(t, X[:, 9] - np.sqrt(abs(X[:, 11])), X[:, 9] + np.sqrt(abs(X[:, 11])),
                     color=col_vec[1], alpha=0.1)
    ax2.set_yticks(X_ticks[1])
    ax2.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))

    # GoC
    ax3.plot(t, X[:, 1], col_vec[2], linewidth=linew, alpha=alpha, linestyle= lines)
    ax3.fill_between(t, X[:, 1] - np.sqrt(abs(X[:, 6])), X[:, 1] + np.sqrt(abs(X[:, 6])),
                     color=col_vec[2], alpha=0.05)
    ax3.set_ylabel(r'$\nu$ [Hz]', fontsize=font_size, ha='center', va='center', labelpad=20)
    ax3.set_yticks(X_ticks[2])
    ax3.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))

    # GrC
    ax4.plot(t, X[:, 0], col_vec[3], linewidth=linew, alpha=alpha,  linestyle= lines)
    ax4.fill_between(t, X[:, 0] - np.sqrt(abs(X[:, 2])), X[:, 0] + np.sqrt(abs(X[:, 2])),
                     color=col_vec[3], alpha=0.1)
    ax4.set_yticks(X_ticks[3])
    ax4.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))

    # Input (solo una volta, ma se vuoi puoi plottarlo più volte)
    ax5.plot(t, finput, 'black', linewidth=linew, alpha = alpha, linestyle=lines)
    ax5.set_yticks(X_ticks[4])
    ax5.set_xticks(np.round(np.linspace(0, 0.5, 3, endpoint=True),2))
    ax5.set_xlabel('t [s]', fontsize=font_size, ha='center', va='center', labelpad=20)

    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    fig.subplots_adjust(hspace=0.5, top=0.92, bottom=0.1)

    return fig, axes


def plot_pato_vs_control(X_back, X_back_hyp, fn, finput, ttrans, avg_idx, sd_idx, pop, basepath, input_name, color, plt_input=False):
    
    plt.figure(figsize=(2, 1))

    print(len(t[ttrans:]))
    print(X_back[:, avg_idx].max)

    plt.plot(t[ttrans:]*1e3, X_back[:,avg_idx], color = color, linestyle = '-', linewidth = 0.8)
    plt.fill_between(t[ttrans:]*1e3, X_back[:, avg_idx] - np.sqrt(abs(X_back[:, sd_idx])), 
                 X_back[:, avg_idx] + np.sqrt(abs(X_back[:, sd_idx])), color=color, alpha=0.05)

    plt.plot(t[ttrans:]*1e3, X_back_hyp[:,avg_idx], color = color, linestyle = '--', linewidth = 0.8)
    plt.fill_between(t[ttrans:]*1e3, X_back_hyp[:, avg_idx] - np.sqrt(abs(X_back_hyp[:, sd_idx])), 
                 X_back_hyp[:, avg_idx] + np.sqrt(abs(X_back_hyp[:, sd_idx])), color=color, alpha=0.05)
    
    #plt.yticks(yticks, fontsize = 10)
    plt.xticks([0, 250, 500], fontsize = 8)
    plt.ylabel('$\\nu_{PC}$ [Hz]', fontsize = 12)
    plt.xlabel('time [ms]', fontsize=12)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)

    plt.tight_layout()
    #plt.show()
    plt.savefig(basepath+'/'+pop+'_'+input_name+'_'+str(fn)+'.pdf', dpi=300, bbox_inches = 'tight')


    if plt_input == True:
        plt.figure(figsize=(2, 1))
        plt.plot(t[ttrans:]*1e3, finput, color = 'black', linestyle = '-', linewidth = 0.8)
        plt.yticks([0, 80], fontsize = 8)
        plt.xticks([0, 500], fontsize = 8)
        plt.ylabel('$\\nu_{drive}$ [Hz]', fontsize = 10)
        plt.xlabel('time [ms]', fontsize=10)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(True)
        plt.gca().spines['bottom'].set_visible(True)

        plt.tight_layout()
        #plt.show()
        plt.savefig(basepath+'/'+input_name+'_'+str(fn)+'.pdf', dpi=300, bbox_inches = 'tight')
        #plt.savefig(basepath+'/activity_'+str(fn)+'.eps', dpi=300)
        #plt.show()


def compute_stats_per_sim_box(X_1, X_2, mean_idx, sd_idx, fn, labels, pop, save_path, input_name):

    stats = {}

    # distribuzioni
    dist_1 = X_1[:, mean_idx]
    dist_2  = X_2[:, mean_idx]

    # statistiche
    means = [dist_1.mean(), dist_2.mean()]
    sdevs = [np.sqrt(np.abs(X_1[:, sd_idx])).max(),np.sqrt(np.abs(X_2[:, sd_idx])).max()]

    stats[pop] = (means, sdevs)

    # ---- BOXPLOT ----
    plt.figure(figsize=(1.4, 1.4))
    plt.boxplot(
        [dist_1, dist_2],
        labels=labels,
        showfliers=False
    )
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(nbins=8))

    plt.title(f"{pop}")
    plt.ylabel(r'$\nu$ [Hz]', fontsize = 8)
    plt.grid(alpha=0.3)
    
    plt.savefig(save_path + f"/{pop}_{input_name}_boxplot_"+str(fn)+".pdf", dpi = 300, bbox_inches="tight")
    #plt.savefig(save_path + f"/{pop}_boxplot_"+str(fn)+".tif", dpi = 300, bbox_inches="tight")
    #plt.show()

    return stats


def rect_input(time, t_start, t_end, minval, freq, noise_freq):

    """
    time = time vector of simulation
    t_start = start of the step INDEX
    t_end = end of the step INDEX
    minval = baseline value (deviation from 0)
    freq = peak value
    noise_freq = random noise frequencies
    """

    y = np.ones(len(time)) * freq + np.random.rand(len(time)) * noise_freq
    y[:t_start] = y[:t_start]*0+np.random.rand(t_start)*noise_freq
    y[t_end:] = y[t_end:]*0+np.random.rand(len(time) - t_end)*noise_freq
    y = y + minval

    return y


def gauss_input(t, sigma, amp):
    
    mu = t[len(t)//2]       # center
    sigma = sigma   # width (standard deviation)
    amp =amp 

    # gauss function
    gauss = amp * np.exp(-0.5 * ((t - mu) / sigma)**2)
    
    return gauss


## Pathological configuration  --------------------------------------------------------------------------------------------
pato_name = 'Ataxia' #Autism
basepath = 'TF_exploration_ATAXIA_NEW'#'TF_exploration_AUTISM_NEW'
os.makedirs(basepath, exist_ok=True)

root_path = os.getcwd()+'/' #folder where P coefficients were stored

NRN_pat = 'PC' #'GrC'
NTWK_pat = 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_ATAXIC' #'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_5_bis' #autism-like; Soda et al.,2019,J.ofNeurosci.
FILE_pat = root_path + '20260123_173440_PC_CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_ATAXIC_tsim5_alpha1.7_fit.npy'#'20260108_201050_GrC_CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_5_bis_tsim5_alpha3.5_fit.npy'
aa_pat = 3.5#ataxia tuned on literature
TF_pat = load_transfer_functions(NRN_pat, NTWK_pat, FILE_pat, alpha=aa_pat)


## Standard configuration --------------------------------------------------------------------------------------------
NRN1, NRN2, NRN3, NRN4 = 'GrC', 'GoC', 'MLI', 'PC'
NTWK = 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5'
FILE_GrC = root_path  + '20250904_101211_GrC_CRBL_CONFIG_AUTOMFM_AWAKE_KmfgrcPLV_tsim5_alpha2.6_fit.npy'
FILE_GoC = root_path + '20250903_213910_GoC_CRBL_CONFIG_AUTOMFM_AWAKE_KgrcgocSUM_tsim5_alpha1.9_fit.npy'
FILE_MLI = root_path + '20250903_184431_MLI_CRBL_CONFIG_AUTOMFM_AWAKE_MLIMLIxPLV_tsim5_alpha1.8_fit.npy'
FILE_PC = root_path + '20250903_190157_PC_CRBL_CONFIG_AUTOMFM_AWAKE_Qmlipc1.22_KgrcpcSUM_tsim5_alpha1.8_fit.npy'

aa = [2.1, 2.4, 1.63, 5.4] #thr=0.0015 & 0.0020

TFgrc = load_transfer_functions(NRN1, NTWK, FILE_GrC, alpha=aa[0])
TFgoc = load_transfer_functions_goc(NRN2, NTWK, FILE_GoC, alpha=aa[1])
TFmli = load_transfer_functions(NRN3, NTWK, FILE_MLI, alpha=aa[2])
TFpc = load_transfer_functions(NRN4, NTWK, FILE_PC, alpha=aa[3])


## TF array for computing data -------------------------------------------------------------------------------------
##mfm solver expects grc goc mli pc! in this way it is possible to assign pat leaving the function call generic.
TF_arr_pato = [TFgrc, TFgoc, TFmli, TF_pat] 


## Standard parameters ---------------------------------------------------------------------------------------------
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

#fn = 8
fn_arr = np.arange(40, 41, 4)
input_name = 'superharp'

for fn in fn_arr:
    print("***************** SIM FOR: ", fn)
    
    #f_backnoise = np.random.rand(len(t))*fn #background noise set around 4 Hz
    #f_tone = rect_input(time=t, t_start=500, t_end=4500, minval=0, freq=fn, noise_freq=0)
    f_tone = gauss_input(t, sigma = 0.01, amp = fn)
    f_backnoise = f_tone #+ f_backnoise

    ttrans =100

    CI_vec = [0.5, 5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, f_backnoise[0], 15, 38, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

    X_back = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, CI_vec, t, w, f_backnoise,
                           Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False) 


    X_back_pat = find_fixed_point_mossy(TF_arr_pato[0], TF_arr_pato[1], TF_arr_pato[2], TF_arr_pato[3], CI_vec, t, w, f_backnoise,
                           Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)

    X_back = X_back[ttrans:]
    X_back_pat = X_back_pat[ttrans:]
    f_backnoise = f_backnoise[ttrans:]

    np.save(basepath+'/mfs_'+input_name+'_'+str(fn), f_backnoise)

    labels= ['Control', pato_name]
    mean_idx_pop = 10
    sd_idx_pop = 15
    plot_pato_vs_control(X_back, X_back_pat, fn, f_backnoise, ttrans, mean_idx_pop, sd_idx_pop, 'PC', basepath, input_name, 'green', plt_input=True)
    stats = compute_stats_per_sim_box(X_back, X_back_pat, mean_idx_pop, sd_idx_pop, fn, labels, 'PC',  basepath, input_name)
    sim_name = 'PC_'+input_name+'_'+str(fn)
    np.save(basepath+'/'+sim_name, X_back)
    np.save(basepath+'/'+sim_name+'_pat', X_back_pat)

    """
    mean_idx_pop = 9
    sd_idx_pop = 11
    plot_pato_vs_control(X_back, X_back_pat, fn, f_backnoise, ttrans, mean_idx_pop, sd_idx_pop, 'MLI', basepath, input_name, 'orange')
    stats = compute_stats_per_sim_box(X_back, X_back_pat, mean_idx_pop, sd_idx_pop, fn, labels, 'MLI', basepath, input_name)
    sim_name = 'MLI_'+input_name+'_'+str(fn)
    np.save(basepath+'/'+sim_name, X_back)
    np.save(basepath+'/'+sim_name+'_aut', X_back_pat)

    mean_idx_pop = 1
    sd_idx_pop = 6
    plot_pato_vs_control(X_back, X_back_pat, fn, f_backnoise, ttrans, mean_idx_pop, sd_idx_pop, 'GoC', basepath, input_name, 'blue')
    stats = compute_stats_per_sim_box(X_back, X_back_pat, mean_idx_pop, sd_idx_pop, fn, labels, 'GoC', basepath, input_name)
    sim_name = 'GoC_'+input_name+'_'+str(fn)
    np.save(basepath+'/'+sim_name, X_back)
    np.save(basepath+'/'+sim_name+'_aut', X_back_pat)

    mean_idx_pop = 0
    sd_idx_pop = 2
    plot_pato_vs_control(X_back, X_back_pat, fn, f_backnoise, ttrans, mean_idx_pop, sd_idx_pop, 'GrC', basepath, input_name, 'red')
    stats = compute_stats_per_sim_box(X_back, X_back_pat, mean_idx_pop, sd_idx_pop, fn, labels, 'GrC', basepath, input_name)
    sim_name = 'GrC_'+input_name+'_'+str(fn)
    np.save(basepath+'/'+sim_name, X_back)
    np.save(basepath+'/'+sim_name+'_aut', X_back_pat)
    """
   