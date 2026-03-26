
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon, linregress


cells_info = {
    'GrC': {'name': "granule", 'color': "red", 'idx_avg':0, 'idx_sd':2, 'ytick40':[0, 35, 70]},
    'GoC': {'name': "golgi",   'acronym': "GoC", 'color': "blue",'idx_avg':1, 'idx_sd':6, 'ytick40':[0, 35, 70]},
    'MLI': {'name': "MLI", 'acronym': "MLI", 'color': "orange", 'idx_avg':9, 'idx_sd':11, 'ytick40':[10, 60, 110]},
    'PC':  {'name': "purkinje", 'acronym': "PC", 'color': "green", 'idx_avg':10, 'idx_sd':15, 'ytick40':[80, 145, 210]}
}
    
pato_name = 'Ataxia'#Autism' #'Ataxia'
basepath = 'TF_exploration_ATAXIA_NEW' #'TF_exploration_AUTISM_NEW'
pop = 'PC'#'PC'
name_control = pop+ '_superharp_' #'_superharp_' #'_back_' #'_gauss_superharp_' #'step' #'back'
name_pato_suff = '_pat'

marker = '*'

idx_avg = cells_info[pop]['idx_avg']
idx_sd = cells_info[pop]['idx_sd']
color = cells_info[pop]['color']
laby = rf'$\nu_{{{pop}}}$ [Hz]'
idx_f = 9

#ataxia
ytic = cells_info[pop]['ytick40']
#autism
#ytic = [80, 145, 210]  #[0, 25, 50] #[0, 35, 70] #[10, 60, 110]   
xtic = [0, 500]


fn_arr = np.arange(4, 80, 4)

print('FREQ FOR PLOT: ', fn_arr[idx_f])

control = []
pato = []
for f in fn_arr:
    c = np.load(basepath+'/'+name_control+str(f)+'.npy', allow_pickle=True)
    p = np.load(basepath+'/'+name_control+str(f)+name_pato_suff+'.npy', allow_pickle=True)
    control.append(c)
    pato.append(p)

control_arr = np.array(control)
pato_arr = np.array(pato)
print('control shape: ', control_arr.shape, 'pato shape: ', pato_arr.shape)

C_ctr_m = control_arr[:,:,idx_avg]  # activity
C_ctr_s = control_arr[:,:,idx_sd]  # standard dev
C_pato_m = pato_arr[:,:,idx_avg]
C_pato_s = pato_arr[:,:,idx_sd]


t = np.arange(0,0.5,1e-4)
ttrans = 100
t=t[ttrans:]


plt.figure(figsize=(2, 1))
plt.plot(t*1e3, C_ctr_m[idx_f, :], color = color, linestyle = '-', linewidth = 0.8)
plt.fill_between(t*1e3, C_ctr_m[idx_f, :] - np.sqrt(abs(C_ctr_s[idx_f, :])), 
                 C_ctr_m[idx_f, :] + np.sqrt(abs(C_ctr_s[idx_f, :])), color=color, alpha=0.05)

plt.plot(t*1e3, C_pato_m[idx_f, :], color = color, linestyle = ':', linewidth = 0.8)
plt.fill_between(t*1e3, C_pato_m[idx_f, :] - np.sqrt(abs(C_pato_s[idx_f, :])), 
                 C_pato_m[idx_f, :]+ np.sqrt(abs(C_pato_s[idx_f, :])), color=color, alpha=0.05)
    
plt.yticks(ytic, fontsize =8)
plt.xticks(xtic, fontsize = 8)
plt.ylabel(laby, fontsize = 10)
plt.xlabel('time [ms]', fontsize=10)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(True)
plt.gca().spines['bottom'].set_visible(True)

plt.tight_layout()
#plt.show()
plt.savefig(basepath+'/'+pop+'_activity_'+str(fn_arr[idx_f])+'.pdf', dpi=300, bbox_inches = 'tight')


# ============================================================================
# WILCOXON SIGNED-RANK TEST
# ============================================================================

# Average across simulations for each frequency -- for super sharp input - better the maximu,
ctr_mean_per_freq = np.max(C_ctr_m, axis=1) #np.mean(C_ctr_m, axis=1)
pato_mean_per_freq = np.max(C_pato_m, axis=1) #np.mean(C_pato_m, axis=1)

print('Shape of my array: ', np.shape(ctr_mean_per_freq))

# Wilcoxon test
stat, p_value = wilcoxon(ctr_mean_per_freq, pato_mean_per_freq, alternative='two-sided')

print("\n" + "="*60)
print("WILCOXON SIGNED-RANK TEST")
print("="*60)
print(f"Statistic: {stat:.4f}")
print(f"p-value: {p_value:.6f}")
print(f"Result: {'SIGNIFICANT' if p_value < 0.05 else 'NOT significant'} (α=0.05)")
print("="*60 + "\n")

"""
plt.figure(figsize=(4, 3))

plt.errorbar(fn_arr, ctr_mean_per_freq, yerr=np.sqrt(C_ctr_s.shape[0]), 
             marker='o', markersize=3, linewidth=0.8, label='Control', capsize=5, color=color)

plt.errorbar(fn_arr, pato_mean_per_freq, yerr=np.sqrt(C_pato_s.shape[0]), 
             marker='s', markersize=3, linewidth=0.8, label='Autism', capsize=5, color=color)
"""


plt.figure(figsize=(3.1, 2.2))
plt.plot(fn_arr, ctr_mean_per_freq, color = color, linestyle = '-', linewidth = 0.8, marker = 'o', markersize=3, label= 'Control')
plt.fill_between(fn_arr, ctr_mean_per_freq - np.sqrt(abs(ctr_mean_per_freq)), 
                 ctr_mean_per_freq + np.sqrt(abs(ctr_mean_per_freq)), color=color, alpha=0.05)

plt.plot(fn_arr, pato_mean_per_freq, color = color, linestyle = '-', linewidth = 0.8, marker = marker, markersize=4, label = pato_name)
plt.fill_between(fn_arr, pato_mean_per_freq - np.sqrt(abs(pato_mean_per_freq)), 
                pato_mean_per_freq + np.sqrt(abs(pato_mean_per_freq)), color=color, alpha=0.05)

plt.yticks(ytic, fontsize =10)
plt.ylabel(laby, fontsize = 12)
plt.xlabel('$\\nu_{drive}$ [Hz]', fontsize=12)
plt.xticks([4, 42, 80], fontsize =10)
#plt.title(f'Wilcoxon test: p={p_value:.4f}')
plt.legend(fontsize = 8)
plt.grid(True, alpha=0.3)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(True)
plt.gca().spines['bottom'].set_visible(True)
plt.tight_layout()
plt.savefig(basepath+'/wilcoxon_test'+name_control+'.pdf', dpi=300)
plt.show()


# Summary plot
means = [ctr_mean_per_freq.mean(), pato_mean_per_freq.mean()]
stds  = [ctr_mean_per_freq.std(),  pato_mean_per_freq.std()]

fig, ax = plt.subplots(figsize=(2, 2.2))

labels = ['Control', pato_name]
x = [0, 1]

bars = ax.bar(x, means, yerr=stds, width=0.5, color=color, alpha=0.7, capsize=6, error_kw=dict(linewidth=1.5, ecolor='black'))

# Significance plot
y_top = max(m + s for m, s in zip(means, stds)) * 1.1

ax.plot([0, 0, 1, 1], [y_top, y_top*1.02, y_top*1.02, y_top], color='black', linewidth=1)

sig = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'

ax.text(0.5, y_top * 1.03, f'{sig}', ha='center', va='bottom', fontsize=8)

ax.set_xticks(x)
ax.set_yticks([0, cells_info[pop]['ytick40'][-1]])
ax.set_xticklabels(labels, fontsize=12)
ax.set_ylabel('Mean Peak Response', fontsize=12)
#ax.set_title('Overall Response', fontsize=13)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(basepath+'/overall_score'+name_control+'.pdf', dpi=300)



# ============================================================================
# SLOPE ANALYSIS (Linear Regression)
# ============================================================================

# Linear regression for control
slope_ctr, intercept_ctr, r_ctr, p_ctr, se_ctr = linregress(fn_arr, ctr_mean_per_freq)

# Linear regression for pathological
slope_pato, intercept_pato, r_pato, p_pato, se_pato = linregress(fn_arr, pato_mean_per_freq)

print("="*60)
print("SLOPE ANALYSIS")
print("="*60)
print(f"\nControl:")
print(f"  Slope: {slope_ctr:.2f}")
print(f"  R²: {r_ctr**2:.4f}")
print(f"  p-value: {p_ctr:.2f}")

print(f"\nPathological:")
print(f"  Slope: {slope_pato:.6f}")
print(f"  R²: {r_pato**2:.4f}")
print(f"  p-value: {p_pato:.6f}")

print(f"\nSlope difference:")
slope_diff = slope_pato - slope_ctr
slope_ratio = slope_pato / slope_ctr if slope_ctr != 0 else np.inf
print(f"  Δ slope: {slope_diff:.6f}")
print(f"  Ratio (Pato/Control): {slope_ratio:.4f}")

if abs(slope_pato) > abs(slope_ctr):
    print(f"  → Pathological cells grow {'FASTER' if slope_pato > 0 else 'DECLINE FASTER'}")
else:
    print(f"  → Control cells grow {'FASTER' if slope_ctr > 0 else 'DECLINE FASTER'}")
    
print("="*60 + "\n")

"""
plt.figure(figsize=(4, 3))

plt.errorbar(fn_arr, ctr_mean_per_freq, yerr=np.sqrt(C_ctr_s.shape[0]), 
             marker='o', markersize=4, linewidth=0, label='', capsize=5, color=color, alpha=0.7)

plt.errorbar(fn_arr, pato_mean_per_freq, yerr=np.sqrt(C_pato_s.shape[0]), 
             marker='s', markersize=4, linewidth=0, label='', capsize=5, color=color, alpha=0.7)
"""

plt.figure(figsize=(3.1, 2.2))
plt.plot(fn_arr, ctr_mean_per_freq, color = color, linestyle = '-', linewidth = 0.8, marker = 'o', markersize=3, alpha = 0.6, label=f'Control Δ={slope_ctr:.1f})')
plt.fill_between(fn_arr, ctr_mean_per_freq - np.sqrt(abs(ctr_mean_per_freq)), 
                 ctr_mean_per_freq + np.sqrt(abs(ctr_mean_per_freq)), color=color, alpha=0.05)

plt.plot(fn_arr, pato_mean_per_freq, color = color, linestyle = '-', linewidth = 0.8, marker = marker, markersize=4, alpha = 0.6, label=f'{pato_name} Δ={slope_pato:.1f})')
plt.fill_between(fn_arr, pato_mean_per_freq - np.sqrt(abs(pato_mean_per_freq)), 
                pato_mean_per_freq + np.sqrt(abs(pato_mean_per_freq)), color=color, alpha=0.05)

# Plot regression lines
plt.plot(fn_arr, slope_ctr * fn_arr + intercept_ctr, '--', color='black', linewidth=0.5)
plt.plot(fn_arr, slope_pato * fn_arr + intercept_pato, '--', color='black', linewidth=0.5)

plt.ylabel(laby, fontsize = 12)
plt.xlabel('$\\nu_{drive}$ [Hz]', fontsize=12)
plt.yticks(ytic, fontsize = 10)
plt.xticks([4, 42, 80], fontsize  =10)
#plt.title('Slope Analysis')
plt.legend(fontsize = 8)
plt.grid(True, alpha=0.3)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(True)
plt.gca().spines['bottom'].set_visible(True)
plt.tight_layout()
plt.savefig(basepath+'/slope_analysis_'+name_control+'.pdf', dpi=300)
plt.show()

C_pato_m = np.max(pato_arr[:,:,10], axis=1)
C_pato_s = np.average(pato_arr[:,:,15], axis=1)