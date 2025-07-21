from pymoo.core.problem import Problem
from pymoo.termination.default import DefaultMultiObjectiveTermination
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
import numpy as np
import pandas as pd
import os
import argparse

from load_config_TF import *
from master_equation_CRBL_MF import find_fixed_point_mossy


def optimization(problem, algorithm, xtol=1e-8, cvtol=1e-8, ftol=25e-4, period=30,
                 n_gen=100, n_max_evals=10000):

    termination = DefaultMultiObjectiveTermination(
        xtol=xtol, cvtol=cvtol, ftol=ftol, period=period, n_max_gen=n_gen, n_max_evals=n_max_evals
    )
    results = minimize(problem, algorithm, termination, seed=1, verbose=True)
    # results = minimize(problem, algorithm, ('n_gen', 40), seed=1, verbose=True)
    return results



parser = argparse.ArgumentParser()
parser.add_argument('--freqs', nargs='+', type=float, required=True,
                    help="Lista delle frequenze mossy da usare (es. --freqs 4 40 80)")
args = parser.parse_args()

input_freqs = args.freqs
print(f"User-defined input frequencies: {input_freqs}")



class AlphaOptimizationMF(Problem):
    def __init__(self, snn_data_path, input_freqs, ci_vec_base, fixed_args):
        super().__init__(n_var=4, n_obj=1, xl=np.array([0.1, 0.1, 0.1, 0.1]), xu=np.array([10.0, 10.0, 10.0, 10.0]))

        self.FMOSSY_IDX = 8

        self.freqs = input_freqs
        self.snn_data = self.load_snn_ground_truth(snn_data_path)
        self.ci_vec_base = ci_vec_base
        self.fixed_args = fixed_args  # dict with TF loading & sim setup args

    def load_snn_ground_truth(self, folder_path):
        # Load SNN stats: assumes 4 CSV files: GrC.csv, GoC.csv, MLI.csv, PC.csv
        data = {}
        for cell in ['granule_cell', 'golgi_cell', 'MLI_cell', 'purkinje_cell']:
            df = pd.read_csv(os.path.join(folder_path, f'{cell}_fr_for_TF.csv'))
            data[cell] = {
                'freqs': df.iloc[:, 0].values,
                'mean': df.iloc[:, 1].values,
                'std': df.iloc[:, 2].values,
            }
        return data

    def simulate_MF(self, alphas, input_freq):
        # Unpack fixed args
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
        input_vec[self.FMOSSY_IDX] = input_freq  # Set mossy fiber freq
        f_backnoise = np.ones(len(t)) * input_freq

        X = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, input_vec, t, w, f_backnoise,
                                   Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)
        return np.mean(X[-100:, [0, 1, 9, 10]], axis=0)  # Avg last portion of sim: GrC, GoC, MLI, PC

    def _evaluate_NONSAFE(self, X, out, *args, **kwargs):
        errors = []
        for alpha_set in X:
            total_err = 0
            for f in self.freqs:

                mf_rates = self.simulate_MF(alpha_set, f)

                for i, cell in enumerate(['granule_cell', 'golgi_cell', 'MLI_cell', 'purkinje_cell']):
                    snn_mean = np.interp(f, self.snn_data[cell]['freqs'], self.snn_data[cell]['mean'])
                    snn_std  = np.interp(f, self.snn_data[cell]['freqs'], self.snn_data[cell]['std'])

                    ## This is my objective function for one cell for one freq
                    err = ((mf_rates[i] - snn_mean) / snn_std) ** 2  # normalized squared error
                    ## I sum over the cekk
                    total_err += err

            print(f"Alphas: {alpha_set} -> Error: {total_err:.4f}")
            errors.append(total_err)

        out["F"] = np.array(errors).reshape(-1, 1)

    def _evaluate(self, X, out, *args, **kwargs):
        errors = []
        for alpha_set in X:
            total_err = 0
            invalid = False #flag

            for f in self.freqs:
                print('I AM SIMULATING FOR FREQ: ', f)
                mf_rates = self.simulate_MF(alpha_set, f)

                # Check nan o inf
                if np.any(np.isnan(mf_rates)) or np.any(np.isinf(mf_rates)):
                    print(f"Invalid MF rates for alpha_set = {alpha_set}, freq = {f} → {mf_rates}")
                    total_err = 1e6  # Penalizzazione pesantissima baby - ti sistemo se sei nan!!!
                    invalid = True
                    break

                for i, cell in enumerate(['granule_cell', 'golgi_cell', 'MLI_cell', 'purkinje_cell']):

                    print('I AM COMPUTING ERR FOR CELL: ', cell)

                    snn_mean = np.interp(f, self.snn_data[cell]['freqs'], self.snn_data[cell]['mean'])
                    snn_std = np.interp(f, self.snn_data[cell]['freqs'], self.snn_data[cell]['std'])

                    # check std = 0 that brings err to NAN val
                    safe_std = snn_std if snn_std > 1e-6 else 1e-6

                    ## This is my objective function for one cell for one freq
                    err = ((mf_rates[i] - snn_mean) / safe_std) ** 2

                    #I sum over the cell
                    total_err += err

            if not invalid:
                print(f"Alphas: {alpha_set} → Error: {total_err:.4f}")
            errors.append(total_err)

        out["F"] = np.array(errors).reshape(-1, 1)


problem = AlphaOptimizationMF(
    snn_data_path='./',
    input_freqs=np.arange(4, 84, 4),

    ci_vec_base= [0.5, 5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 4, 15, 38, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # dal tuo codice
    fixed_args={
        'load_transfer_functions': load_transfer_functions,
        'find_fixed_point_mossy': find_fixed_point_mossy,
        't': np.arange(0, 0.5, 1e-4), 'w': 0., 'T': 3.5e-3,
        'Ngrc': 29916, 'Ngoc': 71, 'Nmossy': 2340, 'Nmli': 302+150, 'Npc': 69
    }
)

algorithm = NSGA2(pop_size=24)

#results = minimize(problem, algorithm, ('n_gen', 40), seed=1, verbose=True)

#Default option : cvtol=1e-8, ftol=25e-4, period=30, n_gen=100, n_max_evals=10000
results = optimization(problem, algorithm, xtol=1e-3)

best_idx = np.argmin(results.F)
best_alphas = results.X[best_idx]
print("Best alpha values:", best_alphas)
