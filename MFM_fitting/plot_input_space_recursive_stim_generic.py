
import numpy as np
import os
import matplotlib.pyplot as plt


cells_info = {
    'GrC': {'name': "granule", 'color': "red", 'idx_avg':0, 'idx_sd':2},
    'GoC': {'name': "golgi",   'acronym': "GoC", 'color': "blue",'idx_avg':1, 'idx_sd':6},
    'MLI': {'name': "MLI", 'acronym': "MLI", 'color': "orange", 'idx_avg':9, 'idx_sd':11},
    'PC':  {'name': "purkinje", 'acronym': "PC", 'color': "green", 'idx_avg':10, 'idx_sd':15}
}

basepath = 'TF_exploration_AUTISM_case'
pop = 'GrC'
name_control = pop+'_back_100' #'step' #'back'
name_pato_suff = '_aut'


fn_arr = np.arange(4, 62, 4)
control  = []
pato = []

for f in fn_arr:
    c = np.load(basepath+'/'+name_control+str(f)+'.npy', allow_pickle=True)
    p = np.load(basepath+'/'+name_control+str(f)+name_pato_suff+'.npy', allow_pickle=True)

    control.append(c)
    pato.append(p)

control_arr =np.array(control)
pato_arr = np.array(pato)
print('control shape: ', control_arr.shape, 'pato shape: ', pato_arr.shape)

idx_avg = cells_info[pop]['idx_avg']
idx_sd = cells_info[pop]['idx_sd']
color = cells_info[pop]['color']

C_ctr_m = np.max(control_arr[:,:,idx_avg], axis =1)
C_ctr_s =  np.average(control_arr[:,:,idx_sd], axis =1)

C_pato_m = np.max(pato_arr[:,:,idx_avg], axis = 1)
C_pato_s = np.average(pato_arr[:,:,idx_sd], axis =1)


plt.figure(figsize=(3, 2.4))
plt.plot(fn_arr, C_ctr_m, color = color, linestyle = '-', linewidth = 0.8, marker = 'o', markersize=2)
plt.fill_between(fn_arr, C_ctr_m - np.sqrt(abs(C_ctr_s)), 
                 C_ctr_m + np.sqrt(abs(C_ctr_s)), color=color, alpha=0.05)

plt.plot(fn_arr, C_pato_m, color = color, linestyle = '-', linewidth = 0.8, marker = 's', markersize=2)
plt.fill_between(fn_arr, C_pato_m - np.sqrt(abs(C_pato_s)), 
                C_pato_m + np.sqrt(abs(C_pato_s)), color=color, alpha=0.05)


plt.savefig(basepath+'/input_space_max_'+name_control+'.pdf', dpi=300)
plt.show()