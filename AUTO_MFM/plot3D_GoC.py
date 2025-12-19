import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
#from pylab import *

# ------- LOADING FILES ------------------------------------------------------------------------------------------------
"""
abspath = '/home/bcc/bsb-ws/CRBL_MF_Model/20220211_165558_GoC_CRBL_CONFIG_20PARALLEL_wN_tsim5/'
filename = 'numTF.npy'
"""

abspath =  '/home/bcc/projects/Zebrine_plus/20241001_141542_GoC_CRBL_CONFIG_20PARALLEL_wN_tsim5/'
filename = 'numTF.npy'

GoC_num_TF = np.load(abspath+filename, allow_pickle=True)
Fgrc = np.load(abspath+'fe.npy', allow_pickle=True)
Fgoc = np.load(abspath+'fi.npy', allow_pickle=True)
Fmossy = np.arange(4, 81, 4)

# ------- GRAPHICAL STUFFS ---------------------------------------------------------------------------------------------

# create axis for my plot
x = np.arange(GoC_num_TF.shape[0])[:, None, None] #GoC
y = np.arange(GoC_num_TF.shape[1])[None, :, None] #GrC
z = np.arange(GoC_num_TF.shape[2])[None, None, :] #Mossy
x, y, z = np.broadcast_arrays(x, y, z)

# create colors for my plot
c = GoC_num_TF.ravel()[:, None] #array of values

# initialisation of figure tool
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# decide the colormap
cm_sel = plt.get_cmap("viridis")

# finally plot!!!!
cax = ax.scatter(x, y, GoC_num_TF, s=100, c=c, cmap=cm_sel)

# adding title and labels to plot axes
ax.set_title("GoC TF numerical template", fontsize = 11)
ax.set_xlabel('GoC ($\\nu_i$ [Hz])', fontsize = 10)
ax.set_ylabel('GrC ($\\nu_e$ [Hz])', fontsize = 10 )
ax.set_zlabel('Mossy fibres ($\\nu_{drive}$ [Hz])', fontsize = 10)

ax.set_xticks(np.arange(0, len(Fgoc), 10))  # 2 ticks for GoC
ax.set_xticklabels([round(Fgoc[0,0],2), round(Fgoc[8,4],2), round(Fgoc[24,16],2), round(Fgoc[-1,-1],2)], fontsize=9)

ax.set_yticks(np.arange(0, len(Fgrc), 5))  # 2 ticks for GoC
ax.set_yticklabels([round(Fgrc[0, 0], 2), round(Fgrc[4, 4] , 2), round(Fgrc[16, 12], 2), round(Fgrc[-1, -1], 2)], fontsize=9)

#ax.set_yticks(np.arange(0, len(Fgrc) + 1, 20))  # 3 ticks for GoC
#ax.set_yticklabels([round(Fgrc[0, 0], 2), round(Fgrc[-1, -1], 2)], fontsize=9)

ax.set_zticks(np.arange(0, len(Fmossy)+1, 5))  # 4 ticks for GoC
ax.set_zticklabels([round(Fmossy[0], 2), round(Fmossy[4], 2), round(Fmossy[12], 2),
                        round(Fmossy[16], 2), round(Fmossy[-1], 2)], fontsize=9)

"""
ax.set_xticks( np.arange(0, len(Fgoc)+1, 40) ) #2 ticks for GoC
ax.set_xticklabels([round(Fgoc[0,0],2), round(Fgoc[-1,-1],2)], fontsize = 9)

ax.set_yticks( np.arange(0, len(Fgrc)+1, 20) ) #3 ticks for GoC
ax.set_yticklabels([round(Fgrc[0,0],2), round(Fgrc[-1,-1],2)], fontsize = 9)

ax.set_zticks( np.arange(0, len(Fmossy)+1, 21) ) #4 ticks for GoC
ax.set_zticklabels([round(Fmossy[0],2), round(Fmossy[-1],2)], fontsize = 9)
"""

# doing stuff with colorbar
ticks = np.linspace(GoC_num_TF.min(), GoC_num_TF.max(), 5, endpoint=True)
cb = fig.colorbar(cax, ax = ax, ticks = ticks, shrink = 0.5)
cb.set_label('Numerical TF [Hz]', labelpad = 10, rotation= 270+180,)

cb.ax.tick_params(labelsize=9)

# displaying plot and BE HAPPY
plt.show()
