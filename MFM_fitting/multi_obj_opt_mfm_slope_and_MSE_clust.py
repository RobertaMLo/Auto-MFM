from abc import ABC, abstractmethod
from pymoo.core.problem import Problem
from pymoo.termination.default import DefaultMultiObjectiveTermination
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
import numpy as np
import pandas as pd
import os

from load_config_TF import *
from master_equation_CRBL_MF import find_fixed_point_mossy

def optimization(problem, algorithm, xtol=1e-8, cvtol=1e-8, ftol=25e-4, period=30,
                 n_gen=100, n_max_evals=10000):

    termination = DefaultMultiObjectiveTermination(
        xtol=xtol, cvtol=cvtol, ftol=ftol, period=period, n_max_gen=n_gen, n_max_evals=n_max_evals
    )

    results = minimize(problem, algorithm, ('n_gen', n_gen), seed=1, verbose=True)  # STANDARD FOR NSGA
    return results


def load_snn_ground_truth(folder_path):
    data = {}
    for cell in ['granule_cell', 'golgi_cell', 'MLI_cell', 'purkinje_cell']:
        df = pd.read_csv(os.path.join(folder_path, f'{cell}_fr_for_TF.csv')) #TRIAL ON ALL FREQ
        data[cell] = {
            'freqs': df.iloc[:, 0].values,
            'mean': df.iloc[:, 1].values,
            'std': df.iloc[:, 2].values,
        }
    return data

## Abstract class for MFM optimization problem:
## generic method that is neededin each optimization problem is the simulate_MF


class MFOptimizationBase(Problem, ABC):
    def __init__(self,
                 input_freqs,
                 ci_vec_base,
                 fixed_args,
                 n_var=4,
                 n_obj=2,
                 xl=None, #devo definirli qui perchè non li sto definendo più fuori
                 xu=None
    ):
        super().__init__(
            input_freqs=input_freqs,
            ci_vec_base=ci_vec_base,
            fixed_args=fixed_args,
            n_var=n_var,
            n_obj=n_obj,
            xl=xl,
            xu=xu
        )

        self.freqs = input_freqs
        self.ci_vec_base = ci_vec_base
        self.fixed_args = fixed_args
        self.FMOSSY_IDX = 8


    def simulate_MF(self, alphas, input_freq):
        load_transfer_functions, find_fixed_point_mossy, t, w, T, Ngrc, Ngoc, Nmossy, Nmli, Npc = self.fixed_args.values()

        NTWK = 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5'
        
        FILE_GrC = '20250904_101211_GrC_CRBL_CONFIG_AUTOMFM_AWAKE_KmfgrcPLV_tsim5_alpha2.6_fit.npy'
        FILE_GoC = '20250903_213910_GoC_CRBL_CONFIG_AUTOMFM_AWAKE_KgrcgocSUM_tsim5_alpha1.9_fit.npy'
        
        FILE_MLI = '20250903_184431_MLI_CRBL_CONFIG_AUTOMFM_AWAKE_MLIMLIxPLV_tsim5_alpha1.8_fit.npy'
        FILE_PC = '20250903_190157_PC_CRBL_CONFIG_AUTOMFM_AWAKE_Qmlipc1.22_KgrcpcSUM_tsim5_alpha1.8_fit.npy'

        TFgrc = load_transfer_functions('GrC', NTWK, FILE_GrC, alpha=alphas[0])
        TFgoc = load_transfer_functions_goc('GoC', NTWK, FILE_GoC, alpha=alphas[1])
        TFmli = load_transfer_functions('MLI', NTWK, FILE_MLI, alpha=alphas[2])
        TFpc = load_transfer_functions('PC', NTWK, FILE_PC, alpha=alphas[3])

        input_vec = self.ci_vec_base.copy()
        input_vec[self.FMOSSY_IDX] = input_freq
        f_backnoise = np.random.rand(len(t)) * input_freq

        X = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, input_vec, t, w, f_backnoise,
                                   Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)

        return np.average(X[:, [0, 1, 9, 10]], axis=0)

    @abstractmethod
    def _evaluate(self, X, out, *args, **kwargs):
        pass


class AlphaOptimizationMF(MFOptimizationBase):
    def __init__(self,
                 snn_data_path,
                 input_freqs,
                 ci_vec_base,
                 fixed_args ## tutti questi argomenti li passo quando istanzio classe
    ):
        super().__init__(
            input_freqs=input_freqs,
            ci_vec_base=ci_vec_base,
            fixed_args=fixed_args,
            n_var=4,
            n_obj=2,
            xl=np.array([1.8, 1.8, 1.6, 2.1]),
            xu=np.array([3.0, 3.0, 8.0, 10.0]) ## li eredito da super class
        )

        self.FMOSSY_IDX = 8
        self.freqs = input_freqs
        self.snn_data = load_snn_ground_truth(snn_data_path) #se richiamo una funz definita dentro classe devo mettere self. Altrimenti np
        self.ci_vec_base = ci_vec_base
        self.fixed_args = fixed_args  # dict with TF loading & sim setup args

    #* mi prende altri argomenti che potrei passare a funz evaluate -- per evitare "gor unexpected argument"
    #**kwargs prende gli argomenti tipo x=10 e li salva in un dict{'x':10}
    #nel mio caso rimangono vuoti
    def _evaluate(self, X, out, *args, **kwargs):
        mse_errors = []       # Obiettivo 1: MSE
        slope_errors = []     # Obiettivo 2: slope solo PC
        print("\n================== EVALUATE ==============================")

        for alpha_set in X:
            local_mse = []
            pc_rates = []
            local_freqs = []

            for f in self.freqs:
                print(f"Simulating for freq: {f} Hz | ALPHA = {alpha_set}")
                mf_rates = self.simulate_MF(alpha_set, f)

                if np.any(np.isnan(mf_rates)) or np.any(np.isinf(mf_rates)):
                    print(f"INVALID MF RATES: alphas: {alpha_set}, freq: {f}, rates: {mf_rates}")
                    local_mse.append((f, 1e6 * 4))
                    continue

                err_f = 0
                for i_cell, cell in enumerate(['granule_cell', 'golgi_cell', 'MLI_cell', 'purkinje_cell']):
                    snn_mean = np.interp(f, self.snn_data[cell]['freqs'], self.snn_data[cell]['mean'])
                    snn_std = np.interp(f, self.snn_data[cell]['freqs'], self.snn_data[cell]['std'])

                    safe_std = snn_std if snn_std > 1e-6 else 1e-6  # just to be sure

                    err = abs((mf_rates[i_cell] - snn_mean)/safe_std) #--MAE norm for sd 
                    #err = abs((mf_rates[i_cell] - snn_mean)) #--MAE
                    #err = (mf_rates[i_cell] - snn_mean)**2 #squared error -- and then root for the RMSE
                    err_f += err

                    print(f, cell, 'mf_rates', mf_rates[i_cell], 'snn_mean', snn_mean, 'err', err)

                local_freqs.append(f)
                local_mse.append((f, err_f)) # errore per quella frequenza -- somma tutte pops
                pc_rates.append(mf_rates[3])  # -- solo PC
                print('err sum over all pops: ', local_mse)

            # # ------ ERROR ----------------------------------------------------------------------------------
            merged_mse = dict(local_mse)
            total_mse = sum(merged_mse.values()) / len(merged_mse) # normalization for N of observation - standard procedure for all erro
            #total_mse =  np.sqrt(sum(merged_mse.values()) / len(merged_mse))
            mse_errors.append(total_mse)

            # # ------ SLOPE ----------------------------------------------------------------------------------
            if len(local_freqs) < 2 or np.all(np.array(local_freqs) == local_freqs[0]):
                slope_error = 1e6 # in realtà passo sempre più di due freq
                print('NO SLOPE LESS THAN 2 FREQS')
                
            else:
                slope_mf = np.polyfit(local_freqs, pc_rates, deg=1)[0]
                slope_snn = np.polyfit(self.snn_data['purkinje_cell']['freqs'],
                                       self.snn_data['purkinje_cell']['mean'], deg=1)[0]

                slope_error = (slope_mf - slope_snn) ** 2
                print('Slope SNN: ', slope_snn, 'Slope MFM:', slope_mf)

            slope_errors.append(slope_error)

        out["F"] = np.column_stack([mse_errors, slope_errors])
        print(">>>>> F: mse_errore and slope_errors: ", out["F"])

        results_dict = {
            "alphas": X,
            "mse": np.array(mse_errors),
            "slope": np.array(slope_errors)
        }
        #np.savez("./pareto_solutions_temp_bello.npz", **results_dict)
        print(" ===============================================================\n")


# === OPTIM PARTY IS STARTING=== #

# choose who is che problem.
# Here it is alpha optim
problem = AlphaOptimizationMF(
    snn_data_path='./',
    input_freqs=np.array([4, 40, 80]),
    ci_vec_base=[0.5, 5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 4, 15, 38, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    fixed_args={
        'load_transfer_functions': load_transfer_functions,
        'find_fixed_point_mossy': find_fixed_point_mossy,
        't': np.arange(0, 0.5, 1e-4), 'w': 0., 'T': 3.5e-3,
        'Ngrc': 29916, 'Ngoc': 71, 'Nmossy': 2340, 'Nmli': 302+150, 'Npc': 69
    }
)

# set parameters of optimization
tol = 1e-8
pops = 24
n_gen = 50

#tol = 1e-5
#pops = 8
#n_gen = 10

algorithm = NSGA2(pop_size=pops)
#run the real optimization
results = optimization(problem, algorithm, xtol=tol, n_gen=n_gen)
#save Pareto Front
np.savez("PSTHbased_final_pareto_front_bello_NEW_CONFIG_5"+str(pops)+str(n_gen)+".npz", alphas=results.X, mse=results.F[:, 0], slope=results.F[:, 1])
print("Final fronte saved", results.X.shape)