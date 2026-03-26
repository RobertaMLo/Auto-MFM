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
from scipy.stats import norm

import sys
sys.path.append('../')
import os
import pandas as pd


def plot_distribution(MF_avg, MF_sd, SNN_avg, SNN_sd, pop_name, color):
    """
    Function to plot the gaussian bell of SNN and MF distribution as in Zerlaut et al., 2018
    Input:
        Mean field avg and sd for a given pop
        SNN avg and sd for the same population

    My commment: Not used for the moment because for all pops but for PC, I got negative frequencies
    How can I comment this????
    """
    
    x_min = 0  #start from 0 for interpretation
    x_max = max(SNN_avg, MF_avg) + 5 * max(SNN_sd, MF_sd)
    
    # Points on X
    x = np.linspace(x_min, x_max, 1000)

    #x = np.linspace(min(MF_avg, SNN_avg) - 4 * max(MF_sd, SNN_sd), 
    #                max(MF_avg, SNN_avg) + 4 * max(MF_sd, SNN_sd), 1000)

    # Create the distributions
    SNN_dist = norm.pdf(x, loc=SNN_avg, scale=SNN_sd)
    MF_dist = norm.pdf(x, loc=MF_avg, scale=MF_sd)

    plt.figure(figsize=(5.8,4.1))
    plt.fill_between(x, SNN_dist/np.max(SNN_dist), alpha = 0.3, label='SNN', color='gray', linewidth=2)
    plt.fill_between(x, MF_dist/np.max(MF_dist), alpha = 0.3, label='MF', color=color, linewidth=2)

    # Aggiungi titolo e etichette
    plt.title(pop_name)
    plt.xlabel('Activty [Hz]')
    plt.ylabel('Density')
    plt.legend()

    plt.show()


def mf_snn_io_relation(MF_avg, MF_std, SNN_avg, SNN_std, fmossy, outdir, pop_name, color):
    
    """
    Function to plot the I/O relation of the MF and SNN
    Maybe a bit circular since I used this frequencies to build up the mean field!!!!
    Anyway.... I need to extract the vectors from the SNN simulations
    """
    
    plt.figure(figsize=(5.8,4.1))
    ymin = 0
    ymax = np.max(np.array([ MF_avg[-1]+MF_std[-1], SNN_avg[-1]+SNN_std[-1] ]))+1
    #plt.plot(fmossy, MF_avg, 'o', fmossy, SNN_avg, '')
    #plt.plot(fmossy, SNN_avg, 'ok')

    plt.errorbar(fmossy, MF_avg, yerr=MF_std, fmt='-o', color=color, alpha = 0.7, label = 'MF', capsize=8) 
    plt.errorbar(fmossy, SNN_avg, yerr=SNN_std, fmt='-o', color='gray', alpha = 0.5, label = 'SNN', capsize=8) 

    plt.title(pop_name + ' I/O relation', fontsize = 12)
    plt.ylim([ymin, ymax])
    plt.yticks(np.linspace(ymin, ymax, 5).round())
    plt.xlabel('Mossy fibres [Hz]', fontsize = 12)
    plt.ylabel('Activity [Hz]', fontsize = 12)
    plt.legend()

    plt.savefig(outdir+'/'+pop_name+'_IO_MF_SNN.png', dpi = 300,  bbox_inches='tight')
    #plt.show()


if __name__ == '__main__':
    import argparse
    import time
    parser = argparse.ArgumentParser(description=
                                    """ 
                                    'Main routine for constrcutive validity with basal awake configuration'
                                    """,
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-path_mf",
                        help="Folder where MF global stats are saved (average and SD)")
    
    parser.add_argument("-path_snn", 
                        help="Folder where SNN avg FR for each cell type is stored")

    parser.add_argument("-outdir",
                        help="where to saved the images")
    
    parser.add_argument("-NTWK", 
                        help="Network name - used to build up folder name where to take the data from", default = '_CRBL_CONFIG_PLV_KandQ_v3')

    parser.add_argument('-save_constr', type=bool, default=False,
                        help ="save constructive validity output")

    args = parser.parse_args()

    
    path_mf = args.path_mf
    path_snn =args.path_snn
    #date_time = time.strftime("%Y%m%d_%H%M%S")
    #outdir = path_mf+date_time+'_'+args.NTWK+'_output_constr_validity'
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    print('I choose this as output dir to save my outputfile: ', outdir)
  
    PC=[]
    GrC=[]
    GoC=[]
    MLI=[]

    pc_snn = []
    mli_snn = []
    goc_snn = []
    grc_snn = []

    
    fmossy = np.arange(4, 81, 4)

    for i in fmossy:
        
        print('fmossy: ', i)

        PC_mf = np.load(os.path.join(path_mf,str(i)+'.0_'+ args.NTWK,'PC_TOT_AVG_SD.npy'), allow_pickle = True)
        MLI_mf = np.load(os.path.join(path_mf,str(i)+'.0_'+ args.NTWK,'MLI_TOT_AVG_SD.npy'),allow_pickle = True)
        GoC_mf = np.load(os.path.join(path_mf,str(i)+'.0_'+args.NTWK,'GoC_TOT_AVG_SD.npy'), allow_pickle = True)
        GrC_mf= np.load(os.path.join(path_mf,str(i)+'.0_'+ args.NTWK,'GrC_TOT_AVG_SD.npy'), allow_pickle = True)

        PC.append(PC_mf)
        MLI.append(MLI_mf)
        GoC.append(GoC_mf)
        GrC.append(GrC_mf)

    PC_arr = np.array(PC)
    GoC_arr = np.array(GoC)
    GrC_arr = np.array(GrC)
    MLI_arr = np.array(MLI)


    csv_file_pc = os.path.join(path_snn, 'purkinje_cell_fr_for_TF.csv')
    csv_file_mli = os.path.join(path_snn, 'MLI_cell_fr_for_TF.csv')
    csv_file_goc = os.path.join(path_snn, 'golgi_cell_fr_for_TF.csv')
    csv_file_grc = os.path.join(path_snn, 'granule_cell_fr_for_TF.csv')


    df_pc = pd.read_csv(csv_file_pc, header = None)
    df_mli = pd.read_csv(csv_file_mli, header = None)
    df_goc = pd.read_csv(csv_file_goc, header = None)
    df_grc = pd.read_csv(csv_file_grc, header = None)
        
    pc_snn.append([df_pc.iloc[:, 1], df_pc.iloc[:, 2] ])
    mli_snn.append([ df_mli.iloc[:, 1], df_mli.iloc[:, 2] ])
    goc_snn.append([ df_goc.iloc[:, 1], df_goc.iloc[:, 2] ])
    grc_snn.append([ df_grc.iloc[:, 1], df_grc.iloc[:, 2] ])

    pc_snn_arr = np.array(pc_snn).squeeze()
    mli_snn_arr = np.array(mli_snn).squeeze()
    goc_snn_arr = np.array(goc_snn).squeeze()
    grc_snn_arr = np.array(grc_snn).squeeze()

    #print(np.shape(MLI_arr))
    #print(np.shape(mli_snn_arr)) #Transposed with respect to the mean-field prediction....
    #print(mli_snn_arr)

    mf_snn_io_relation(PC_arr[:,0], PC_arr[:,1], pc_snn_arr[0,:].T, pc_snn_arr[1,:].T, fmossy, outdir = outdir, pop_name='PC', color='green')
    mf_snn_io_relation(MLI_arr[:,0], MLI_arr[:,1], mli_snn_arr[0,:], mli_snn_arr[1,:], fmossy, outdir = outdir, pop_name= 'MLI', color='orange')
    mf_snn_io_relation(GoC_arr[:,0], GoC_arr[:,1], goc_snn_arr[0,:], goc_snn_arr[1,:], fmossy, outdir = outdir, pop_name='GoC', color='blue')
    mf_snn_io_relation(GrC_arr[:,0], GrC_arr[:,1], grc_snn_arr[0,:], grc_snn_arr[1,:], fmossy, outdir = outdir, pop_name='GrC', color='red')


    """
    pcs = np.load(os.path.join(path_snn,'80_purkinje_cell_SNNsim.npy'), allow_pickle = True)
    basks = np.load(os.path.join(path_snn,'80_basket_cell_SNNsim.npy'),allow_pickle = True)
    stells = np.load(os.path.join(path_snn,'80_stellate_cell_SNNsim.npy'),allow_pickle = True)
    gocs = np.load(os.path.join(path_snn,'80_golgi_cell_SNNsim.npy'), allow_pickle = True)
    grcs = np.load(os.path.join(path_snn,'80_granule_cell_SNNsim.npy'), allow_pickle = True)

    pcs_avg = np.average(pcs)
    pcs_sd = np.std(pcs)

    gocs_avg = np.average(gocs)
    gocs_sd = np.std(gocs)

    grcs_avg = np.average(grcs)
    grcs_sd = np.std(grcs)

    bask_avg = np.average(basks)
    bask_sd = np.std(basks)

    stell_avg = np.average(stells)
    stell_sd = np.std(stells)


    plot_distribution(PC_avg, PC_sd, pcs_avg, pcs_sd, 'PC', 'green')
    plot_distribution(MLI_avg, MLI_sd, bask_avg, bask_sd, 'MLI-BASK', 'orange')
    plot_distribution(MLI_avg, MLI_sd, stell_avg, stell_sd, 'MLI-STELL', 'orange')
    plot_distribution(GoC_avg, GoC_sd, gocs_avg, gocs_sd, 'GoC', 'blue')
    plot_distribution(GrC_avg, GrC_sd, grcs_avg, grcs_sd, 'GrC', 'red')
    """
