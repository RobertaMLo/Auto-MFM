import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from mpl_toolkits.mplot3d.axes3d import get_test_data
import matplotlib
#from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt
from my_graph import build_bar_legend, set_plot
from fitting_TF_withGoc_BSB import get_fluct_regime_varsup_eglif_goc, pseq_params_eglif_goc,erfc_func,\
    threshold_func, load_my_data_bsb_goc


path_abs = '/home/bcc/projects/Zebrine_plus'
FOLDER = path_abs +'/20241001_141542_GoC_CRBL_CONFIG_20PARALLEL_wN_tsim5'
P_file = path_abs + '/20241001_141542_GoC_CRBL_CONFIG_20PARALLEL_wN_tsim5_alpha2.5_fit.npy'

alpha = 2.5
P = np.load(P_file, allow_pickle=True)

MEANfreq, sd_freq, w, fiSim, Fe_m_eff, Fe_g_eff, params, sim_params = load_my_data_bsb_goc(FOLDER, adap_bool = False)

Fgrc = np.load(FOLDER+'/fe.npy', allow_pickle=True)
Fgoc = np.load(FOLDER+'/fi.npy', allow_pickle=True)
Fmossy = np.arange(4, 80, 4)


#compute 3D fluc properties
_, _, _, _, muV, sV, muGn, TvN, Tv = get_fluct_regime_varsup_eglif_goc(Fe_m_eff, Fe_g_eff, fiSim, w,
                                                                       *pseq_params_eglif_goc(params), P[0])
# semianalyitical expression of TF
Fout_th = erfc_func(muV, sV, TvN, threshold_func(muV, sV, TvN, muGn, *P), params['Gl'], params['Cm'], alpha)

diff  = MEANfreq - Fout_th


def plot_3D_cube(Fout_th, GoC_num_TF):
    x = np.arange(Fout_th.shape[0])[:, None, None] #GoC
    y = np.arange(Fout_th.shape[1])[None, :, None] #GrC
    z = np.arange(Fout_th.shape[2])[None, None, :] #Mossy
    x, y, z = np.broadcast_arrays(x, y, z)

    # create colors for my plot
    c = Fout_th.ravel()[:, None] #array of values

    # initialisation of figure tool
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # decide the colormap
    cm_sel = plt.get_cmap("viridis")

    # finally plot!!!!
    cax = ax.scatter(x, y, z, s=100, c=c, cmap=cm_sel)

    # adding title and labels to plot axes
    ax.set_title("GoC TF numerical template", fontsize = 11)
    ax.set_xlabel('GoC ($\\nu_i$ [Hz])', fontsize = 10)
    ax.set_ylabel('GrC ($\\nu_e$ [Hz])', fontsize = 10 )
    ax.set_zlabel('Mossy fibres ($\\nu_{drive}$ [Hz])', fontsize = 10)

    x = np.arange(GoC_num_TF.shape[0])[:, None, None] #GoC
    y = np.arange(GoC_num_TF.shape[1])[None, :, None] #GrC
    z = np.arange(GoC_num_TF.shape[2])[None, None, :] #Mossy
    x, y, z = np.broadcast_arrays(x, y, z)

    cax2 = ax.scatter(x, y, z, s=10, c=c, cmap=plt.get_cmap("magma"))


    # displaying plot and BE HAPPY
    plt.show()

def plot_surf(Fout_th, colorscale, Fgoc, Fgrc, Fmossy):

    import matplotlib.pyplot as plt
    # This import registers the 3D projection, but is otherwise unused.
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
    import numpy as np
    npti = 50
    x = np.linspace(0, Fout_th.shape[0], npti)
    y = np.linspace(0, Fout_th.shape[1], npti)
    z = np.linspace(0, Fout_th.shape[2], npti)
    X, Y = np.meshgrid(x, y)
    Z = np.ones((npti,npti)) * z

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    C = np.linspace(Fout_th.min(), Fout_th.max(), Z.size).reshape(Z.shape)
    scamap = plt.cm.ScalarMappable(cmap=colorscale)
    fcolors = scamap.to_rgba(C)

    ax.plot_surface(X, Y, Z, facecolors=fcolors, cmap=colorscale)

    ticks = np.linspace(Fout_th.min(), Fout_th.max(), 5, endpoint=True)
    cb = fig.colorbar(scamap, ticks = ticks, shrink = 0.5)
    cb.set_label('Analytical TF [Hz]', labelpad=10, rotation=270 + 180, )

    ax.set_xlabel('GoC ($\\nu_i$ [Hz])')
    ax.set_ylabel('GrC ($\\nu_e$ [Hz])')
    ax.set_zlabel('Mossy fibers ($\\nu_{drive}$ [Hz])')


    ax.set_xticks(np.arange(0, len(Fgoc), 10))  # 2 ticks for GoC
    ax.set_xticklabels([round(Fgoc[0,0],2), round(Fgoc[8,4],2), round(Fgoc[24,16],2), round(Fgoc[-1,-1],2)], fontsize=9)

    ax.set_yticks(np.arange(0, len(Fgrc), 5))  # 2 ticks for GoC
    ax.set_yticklabels([round(Fgrc[0, 0], 2), round(Fgrc[4, 4] , 2), round(Fgrc[16, 12], 2), round(Fgrc[-1, -1], 2)], fontsize=9)

    #ax.set_yticks(np.arange(0, len(Fgrc) + 1, 20))  # 3 ticks for GoC
    #ax.set_yticklabels([round(Fgrc[0, 0], 2), round(Fgrc[-1, -1], 2)], fontsize=9)

    ax.set_zticks(np.arange(0, len(Fmossy)+1, 4))  # 4 ticks for GoC
    ax.set_zticklabels([round(Fmossy[0], 2), round(Fmossy[4], 2), round(Fmossy[12], 2),
                        round(Fmossy[16], 2), round(Fmossy[-1], 2)], fontsize=9)

    plt.show()


plot_surf(Fout_th, "viridis", Fgoc, Fgrc, Fmossy)
