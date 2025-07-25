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

xl = np.array([1.8, 1.8, 1.6, 2.1])
xu = np.array([2.2, 2.2, 2.0, 10.0])

class AlphaOptimizationMF(Problem):
    def __init__(self, snn_data_path, input_freqs, ci_vec_base, fixed_args):
        super().__init__(n_var=4, n_obj=2, xl=xl, xu=xu)

        self.FMOSSY_IDX = 8

        self.freqs = input_freqs
        self.snn_data = self.load_snn_ground_truth(snn_data_path)
        self.ci_vec_base = ci_vec_base
        self.fixed_args = fixed_args  # dict with TF loading & sim setup args

    def load_snn_ground_truth(self, folder_path):
        data = {}
        for cell in ['granule_cell', 'golgi_cell', 'MLI_cell', 'purkinje_cell']:
            df = pd.read_csv(os.path.join(folder_path, f'{cell}_fr_for_TF_3.csv'))
            data[cell] = {
                'freqs': df.iloc[:, 0].values,
                'mean': df.iloc[:, 1].values,
                'std': df.iloc[:, 2].values,
            }
        return data

    def simulate_MF(self, alphas, input_freq):
        load_transfer_functions, find_fixed_point_mossy, t, w, T, Ngrc, Ngoc, Nmossy, Nmli, Npc = self.fixed_args.values()

        NTWK = 'CRBL_CONFIG_PLV_ONLYK_GoCautoinib_asorev00_debugQmliPC'

        FILE_GrC = '20250605_163824_GrC_CRBL_CONFIG_PLV_ONLYK_tsim5_alpha2.0_fit.npy'
        FILE_GoC = '20250624_200053_GoC_CRBL_CONFIG_PLV_ONLYK_new_tsim5_alpha2.0_fit.npy'
        FILE_MLI = '20250625_151658_MLI_CRBL_CONFIG_PLV_ONLYK_GoCasorev00_tsim5_alpha1.8_fit.npy'
        FILE_PC = '20250702_235209_PC_CRBL_CONFIG_PLV_ONLYK_GoCautoinib_asorev00_debugQmliPC_tsim5_alpha2.3_fit.npy'

        NRN1, NRN2, NRN3, NRN4 = 'GrC', 'GoC', 'MLI', 'PC'

        TFgrc = load_transfer_functions(NRN1, NTWK, FILE_GrC, alpha=alphas[0])
        TFgoc = load_transfer_functions_goc(NRN2, NTWK, FILE_GoC, alpha=alphas[1])
        TFmli = load_transfer_functions(NRN3, NTWK, FILE_MLI, alpha=alphas[2])
        TFpc  = load_transfer_functions(NRN4, NTWK, FILE_PC,  alpha=alphas[3])

        input_vec = self.ci_vec_base.copy()
        input_vec[self.FMOSSY_IDX] = input_freq
        f_backnoise = np.random.rand(len(t)) * input_freq

        X = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, input_vec, t, w, f_backnoise,
                                   Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)

        return np.average(X[:, [0, 1, 9, 10]], axis=0)


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

                    err = abs((mf_rates[i_cell] - snn_mean)/safe_std)
                    err_f += err

                    print(f, cell, 'mf_rates', mf_rates[i_cell], 'snn_mean', snn_mean, 'err', err)

                local_freqs.append(f)
                local_mse.append((f, err_f)) # errore per quella frequenza -- somma tutte pops
                pc_rates.append(mf_rates[3])  # -- solo PC
                print('err sum over all pops: ', local_mse)

            # # ------ ERROR ----------------------------------------------------------------------------------
            merged_mse = dict(local_mse)
            total_mse = sum(merged_mse.values()) / len(merged_mse) # mi normalizzo errore per numero di frequenze

            mse_errors.append(total_mse)

            # # ------ SLOPE ----------------------------------------------------------------------------------
            if len(local_freqs) < 2 or np.all(np.array(local_freqs) == local_freqs[0]):
                slope_error = 1e6 # in realtà passo sempre più di due freq
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
        np.savez("./pareto_solutions_temp.npz", **results_dict)
        print(" ===============================================================\n")

# # Here problem is defined as a class
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

# === OPTIM PARTY IS STARTING=== #
tol = 1e-5
pops = 8
n_gen = 10

algorithm = NSGA2(pop_size=pops)

results = optimization(problem, algorithm, xtol=tol, n_gen=n_gen)

np.savez("final_pareto_front.npz", alphas=results.X, mse=results.F[:, 0], slope=results.F[:, 1])
print("Final fronte saved", results.X.shape)
