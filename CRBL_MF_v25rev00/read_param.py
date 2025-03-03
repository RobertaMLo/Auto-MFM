import numpy as np

FOLDER = '20250131_161943_GrC_CRBL_CONFIG_20PARALLEL_wN_tsim5'
FOLDER = '20250203_165809_GoC_CRBL_CONFIG_20PARALLEL_wN_tsim5'

params_numTF = np.load(FOLDER+'/params.npy', allow_pickle = True)

print(FOLDER)
print(params_numTF)
