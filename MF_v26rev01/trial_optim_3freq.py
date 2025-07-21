import argparse
import numpy as np
import pandas as pd
import os
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.cmaes import CMAES

from load_config_TF import *
from master_equation_CRBL_MF import find_fixed_point_mossy

# ===================== ARGPARSE =====================
parser = argparse.ArgumentParser()
parser.add_argument('--freqs', nargs='+', type=float, required=True,
                    help="Lista delle frequenze mossy da usare (es. --freqs 4 40 80)")
args = parser.parse_args()

input_freqs = args.freqs
print(f"User-defined input frequencies: {input_freqs}")

# ===================== CONFIG ======================
root_path = os.getcwd() + '/'
NRN = {'GrC': 'GrC', 'GoC': 'GoC', 'MLI': 'MLI', 'PC': 'PC'}
NTWK = 'CRBL_CONFIG_PLV_ONLYK_GoCautoinib_asorev00_debugQmliPC'

FILE = {
    'GrC': root_path  + '20250605_163824_GrC_CRBL_CONFIG_PLV_ONLYK_tsim5_alpha2.0_fit.npy',
    'GoC': root_path + '20250624_200053_GoC_CRBL_CONFIG_PLV_ONLYK_new_tsim5_alpha2.0_fit.npy',
    'MLI': root_path + '20250625_151658_MLI_CRBL_CONFIG_PLV_ONLYK_GoCasorev00_tsim5_alpha1.8_fit.npy',
    'PC':  root_path + '20250702_235209_PC_CRBL_CONFIG_PLV_ONLYK_GoCautoinib_asorev00_debugQmliPC_tsim5_alpha2.3_fit.npy'
}


COLS = {'GrC': 0, 'GoC': 1, 'MLI': 9, 'PC': 10}
NAMES = ['GrC', 'GoC', 'MLI', 'PC']
Ngrc, Ngoc, Nmossy, Nmli, Npc = 29916, 71, 2340, 452, 69
dt, sim_len = 1e-4, 0.5
T, w = 3.5e-3, 0.0
time = np.arange(0, sim_len, dt)

def load_snn_csv(path):
    df = pd.read_csv(path)
    return df.iloc[:,0].values, df.iloc[:,1].values, df.iloc[:,2].values

def run_simulation(alphas, mossy_input):
    alpha_grc, alpha_goc, alpha_mli, alpha_pc = alphas

    TFgrc = load_transfer_functions(NRN['GrC'], NTWK, FILE['GrC'], alpha=alpha_grc)
    TFgoc = load_transfer_functions_goc(NRN['GoC'], NTWK, FILE['GoC'], alpha=alpha_goc)
    TFmli = load_transfer_functions(NRN['MLI'], NTWK, FILE['MLI'], alpha=alpha_mli)
    TFpc  = load_transfer_functions(NRN['PC'],  NTWK, FILE['PC'],  alpha=alpha_pc)

    CI_vec = [0.5]*8 + [mossy_input] + [15, 38] + [0.5]*9
    f_backnoise = np.ones(len(time)) * mossy_input

    X = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, CI_vec, time, w, f_backnoise,
                               Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)
    return X

# ================ OPTIMIZATION PROBLEM ====================
class AlphaProblem(Problem):
    def __init__(self, snn_csv_dict, input_freqs):
        super().__init__(n_var=4, n_obj=1, xl=0.1, xu=8.0)
        self.input_freqs = input_freqs
        self.snn_targets = {
            name: load_snn_csv(csv_path) for name, csv_path in snn_csv_dict.items()
        }

    def _evaluate(self, x, out, *args, **kwargs):
        lambda_weight = 0.5
        loss = []

        for i in range(x.shape[0]):
            alphas = x[i]
            pop_losses = []

            for pop_name in NAMES:
                inputs, means_target, _ = self.snn_targets[pop_name]
                sim_means = []

                for f in self.input_freqs:
                    X = run_simulation(alphas, f)
                    sim_mean = np.mean(X[:, COLS[pop_name]][1000:])
                    sim_means.append(sim_mean)
                    print('Alphas: ', alphas, 'sim mean: ', sim_mean)

                sim_means = np.array(sim_means)
                means_target_interp = np.interp(self.input_freqs, inputs, means_target)

                mse_mean = np.mean((sim_means - means_target_interp) ** 2)

                slope_mf = np.polyfit(self.input_freqs, sim_means, deg=1)[0]
                slope_snn = np.polyfit(self.input_freqs, means_target_interp, deg=1)[0]
                mse_slope = (slope_mf - slope_snn) ** 2

                total_loss = lambda_weight * mse_mean + (1 - lambda_weight) * mse_slope
                pop_losses.append(total_loss)

            loss.append(np.mean(pop_losses))

        out["F"] = np.array(loss).reshape(-1, 1)


# ================ LANCIO ====================
snn_csv_paths = {
    'GrC': './granule_cell_fr_for_TF_3.csv',
    'GoC': './golgi_cell_fr_for_TF_3.csv',
    'MLI': './MLI_cell_fr_for_TF_3.csv',
    'PC':  './purkinje_cell_fr_for_TF_3.csv'
}

problem = AlphaProblem(snn_csv_paths, input_freqs)

res = minimize(problem, CMAES(), termination=('n_gen', 50), verbose=True)

print("Best alpha:", res.X)
print("Final loss:", res.F)
