import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#path = '/home/bcc/bsb-ws/CRBL_MF_Model/20211014_222536_GoC_CRBL_CONFIG_tsim5/'
#path = '/home/bcc/bsb-ws/CRBL_MF_Model/20220211_165558_GoC_CRBL_CONFIG_20PARALLEL_wN_tsim5'
#path = '/home/bcc/bsb-ws/CRBL_MF_Model/20220301_220421_GoC_CRBL_CONFIG_20PARALLEL_wN_tsim5'
#path = '/home/bcc/bsb-ws/CRBL_MF_Model/20220519_155731_GoC_CRBL_CONFIG_20PARALLEL_wN_tsim5'
#path='/home/bcc/bsb-ws/CRBL_MF_Model/20220531_040209_GoC_CRBL_CONFIG_20PARALLEL_wN_GoCKiNsyn_tsim5'

path = '/home/bcc/projects/BSB4_demo/cerebellum_zmin_Ie1.2/20250212_124057_GoC_CRBL_CONFIG_20PARALLEL_wN_PLOS23_Kgocgrc_red_tsim5'


fe = np.load(path + '/fe.npy', allow_pickle=True)
fi = np.load(path + '/fi.npy', allow_pickle=True)
tf = np.load(path + '/numTF.npy', allow_pickle=True)
n_stim_on_mossy = 20
n = 0.8
plt.figure(figsize = (n*10,n*20))
x, y, z = list(), list(), list()
for k in range(n_stim_on_mossy):
    for j in range(40):
        for i in range(20):
            x.append(fe[i,k])
            y.append(fi[j,k])
            z.append(tf[j,i,k])

    """plt.scatter(x, y, c = z, alpha = 0.7, marker = "s")
    plt.xlabel('GrC ($\\nu_e$ [Hz])', fontsize = 10 )
    plt.ylabel('GoC ($\\nu_i$ [Hz])', fontsize = 10)
    plt.show()
    """

sc = plt.scatter(x, y, c = z, marker = "s")


ticks = np.linspace(tf.min(), tf.max(), 5, endpoint=True)
cb = plt.colorbar(sc, ticks = ticks, shrink = 0.7)
cb.set_label('Numerical TF [Hz]', labelpad = 10, rotation= 270+180,)

#plt.yscale('log')
#plt.xscale('log')
plt.xlabel('GrC ($\\nu_e$ [Hz])', fontsize = 10 )
plt.ylabel('GoC ($\\nu_i$ [Hz])', fontsize = 10)
plt.show()
