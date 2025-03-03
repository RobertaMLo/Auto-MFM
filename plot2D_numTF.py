import numpy as np
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def load_my_data_BSB(FOLDER, adap_bool):

    MEANfreq = np.load(FOLDER + '/numTF.npy', allow_pickle=True)
    sd_freq = np.load(FOLDER + '/FoutSD.npy', allow_pickle=True)
    Fi = np.load(FOLDER + '/fi.npy', allow_pickle=True)
    Fe = np.load(FOLDER + '/fe.npy', allow_pickle=True)
    delta_g = np.load(FOLDER + '/delta_e.npy', allow_pickle=True)
    delta_i = np.load(FOLDER + '/delta_i.npy', allow_pickle=True)
    params = np.load(FOLDER + '/params.npy', allow_pickle=True).item()
    sim_params = np.load(FOLDER + '/sim_len.npy', allow_pickle=True)

    if adap_bool:
        w = np.load(FOLDER + '/adaptation.npy', allow_pickle=True)
    else:
        w = np.zeros(len(Fi))

    return MEANfreq, sd_freq, w, Fi, Fe, delta_g, delta_i, params, sim_params

def plot_one_cmap(mossy_index):
    f_mossy = np.arange(0,81,4)
    x = np.arange(len(Fe[:,mossy_index])) #location
    y = np.arange(len(Fi[:,mossy_index]))
    mat = plt.imshow(MEANfreq[:, :, mossy_index])
    plt.title('mf  = '+str(f_mossy[mossy_index])+'Hz', fontsize = 16)
    plt.xticks(np.arange(len(Fe[:,mossy_index])), [round(f, 2) for f in Fe[:,mossy_index] ], fontsize=12, rotation = 90)
    plt.yticks(np.arange(len(Fi[:,mossy_index])), [round(f, 2) for f in Fi[:,mossy_index] ], fontsize=12)
    axcb = plt.colorbar(mat, shrink = 0.5)
    axcb.set_label("numTF [Hz]", labelpad=10, size=12) #labelpad to avoid overlaps of the title with ticks
    axcb.ax.tick_params(labelsize=12)
    plt.xlabel('GrC [Hz]', fontsize = 12 )
    plt.ylabel('GoC [Hz] (autoinhib)', fontsize = 12)
    plt.show()

def loop_plot_cmap(m_ind_to_plot):
    plt.ion()
    plt.figure(1)
    for i in range(len(m_ind_to_plot)):
        plt.subplot(1,4,i+1)
        plot_one_cmap(m_ind_to_plot[i])
    #plt.tight_layout()
    plt.subplots_adjust(left=0.04,
                    bottom=0.1,
                    right=0.99,
                    top=0.9,
                    wspace=0.2,
                    hspace=0.5)
    plt.ioff()
    plt.show()



def plot_cmap_2D_template(pop_name, y_inhib_label, x_excit_label, fold_name, font_size =15):

    cm_sel = plt.get_cmap("viridis")
    #mat = plt.matshow(MEANfreq+1e-3, cmap=cm_sel, norm = LogNorm() )

    plt.figure(1, figsize=(7,7))
    plt.imshow(MEANfreq, origin = 'lower')

    plt.title(pop_name + ' TF numerical template [Hz]', fontsize = font_size+2)
    plt.xticks(np.arange(0, len(Fe)), [round(f, 2) for f in Fe ], fontsize=font_size, rotation = 90)
    plt.yticks(np.arange(len(Fi)), [round(f, 2) for f in Fi], fontsize=font_size)

    ticks = np.linspace(MEANfreq.min(), MEANfreq.max(), 5, endpoint=True)

    color_map = plt.cm.ScalarMappable(cmap=cm_sel)
    color_map.set_array(MEANfreq.ravel())
    color_map.autoscale()

    axcb = plt.colorbar(color_map, ticks = ticks, shrink = 0.8, format='%.0f')
    axcb.set_label("Numerical TF [Hz]", labelpad=10, size=font_size+1) #labelpad to avoid overlaps of the title with ticks
    axcb.ax.tick_params(labelsize=15)
    plt.xlabel(x_excit_label, fontsize = font_size+1 )
    plt.ylabel(y_inhib_label, fontsize = font_size+1)
    plt.savefig(fold_name +'.png', dpi = 300, bbox_inches='tight')
    plt.show()



if __name__ == '__main__':
    import argparse
    import numpy as np

    parser = argparse.ArgumentParser(description=
                                     """ 
                                   'Load the results of the numerical simulation'
                                   """,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-FOLDER", help="folder name with the numTF - YOU MUST RUN numTF computation and the folder is automatically created.")
    parser.add_argument("-adap_bool", type=bool, default= False, help="Include Adaptation outcome or not")
    args = parser.parse_args()

    adap_bool = args.adap_bool
    FOLDER = args.FOLDER

    MEANfreq, sd_freq, w, Fi, Fe, delta_g, delta_i, params, sim_params = load_my_data_BSB(FOLDER, adap_bool)
    print('SIMULATION PARAMETERS: ')


    if 'GoC' in FOLDER:
        # routine to plot 4 cmap fixing mossy input
        print('Example of GoC numTF for fixed mossy inputs')

        m_ind_to_plot = [1, 10, 19]
        loop_plot_cmap(m_ind_to_plot)

    else:
        if 'GrC' in FOLDER:
            pop = 'GrC'
            xname = 'Mossy fibers ($\\nu_{drive}$ [Hz])'
            yname = 'GoC ($\\nu_i$ [Hz])'
        elif 'MLI' in FOLDER:
            pop = 'MLI'
            xname = 'GrC ($\\nu_{e}$ [Hz])'
            yname = 'MLI ($\\nu_i$ [Hz])'
        elif 'PC' in FOLDER:
            pop = 'PC'
            xname = 'GrC ($\\nu_{e}$ [Hz])'
            yname = 'MLI ($\\nu_i$ [Hz])'
        else:
            print ('FOLDER NAME NOT VALID FOR THIS OPERATION')


        plot_cmap_2D_template(pop_name=pop, y_inhib_label=yname, x_excit_label=xname, fold_name = args.FOLDER)
