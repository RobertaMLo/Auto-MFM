import numpy as np
import os
import pandas as pd
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.cmaes import CMAES
from load_config_TF import *
from master_equation_CRBL_MF import find_fixed_point_mossy

# ======= CONFIG =======
root_path = os.getcwd()+'/' #folder where P coefficients were stored

NRN = {'GrC': 'GrC', 'GoC': 'GoC', 'MLI': 'MLI', 'PC': 'PC'}
NTWK = 'CRBL_CONFIG_PLV_ONLYK_GoCautoinib_asorev00_debugQmliPC'

FILE = {
    'GrC': root_path  + '20250605_163824_GrC_CRBL_CONFIG_PLV_ONLYK_tsim5_alpha2.0_fit.npy',
    'GoC': root_path + '20250624_200053_GoC_CRBL_CONFIG_PLV_ONLYK_new_tsim5_alpha2.0_fit.npy',
    'MLI': root_path + '20250625_151658_MLI_CRBL_CONFIG_PLV_ONLYK_GoCasorev00_tsim5_alpha1.8_fit.npy',
    'PC':  root_path + '20250702_235209_PC_CRBL_CONFIG_PLV_ONLYK_GoCautoinib_asorev00_debugQmliPC_tsim5_alpha2.3_fit.npy'
}

# pop:    GrC     GoC     MLI     PC
COLS = {'GrC': 0, 'GoC': 1, 'MLI': 9, 'PC': 10}
NAMES = ['GrC', 'GoC', 'MLI', 'PC']

Ngrc, Ngoc, Nmossy, Nmli, Npc = 29916, 71, 2340, 452, 69
dt, sim_len = 1e-4, 0.5
T, w = 3.5e-3, 0.0
time = np.arange(0, sim_len, dt)

def load_snn_csv(path):
    df = pd.read_csv(path)
    return df.iloc[:,0].values, df.iloc[:,1].values, df.iloc[:,2].values

# === EVALUATION ===
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

# === OPTIMIZATION PROBLEM ===
class AlphaProblem(Problem):
    def __init__(self, snn_csv_dict):
        super().__init__(n_var=4, n_obj=1, xl=0.1, xu=8.0)
        self.snn_targets = {
            name: load_snn_csv(csv_path) for name, csv_path in snn_csv_dict.items()
        }

    def _evaluate(self, x, out, *args, **kwargs):
        lambda_weight = 0.5  # ⬅️ puoi regolare questo valore per bilanciare tra media e slope
        loss = []

        for i in range(x.shape[0]):
            alphas = x[i]
            pop_losses = []

            for pop_name in NAMES:
                inputs, means_target, _ = self.snn_targets[pop_name]
                sim_means = []

                for inp in inputs:
                    X = run_simulation(alphas, inp)
                    sim_mean = np.mean(X[:, COLS[pop_name]][1000:])  # salta primi 100ms
                    sim_means.append(sim_mean)

                sim_means = np.array(sim_means)

                # Errore medio (mean squared error tra MF e SNN)
                mse_mean = np.mean((sim_means - means_target) ** 2)

                # Errore sulla pendenza
                slope_mf = np.polyfit(inputs, sim_means, deg=1)[0]
                slope_snn = np.polyfit(inputs, means_target, deg=1)[0]
                mse_slope = (slope_mf - slope_snn) ** 2

                # Loss combinata
                total_loss = lambda_weight * mse_mean + (1 - lambda_weight) * mse_slope
                pop_losses.append(total_loss)

            # Media tra popolazioni
            loss.append(np.mean(pop_losses))

        out["F"] = np.array(loss).reshape(-1, 1)


# === USO ===
snn_csv_paths = {
    'GrC': './granule_cell_fr_for_TF.csv',
    'GoC': './golgi_cell_fr_for_TF.csv',
    'MLI': './MLI_cell_fr_for_TF.csv',
    'PC':  './purkinje_cell_fr_for_TF.csv'
}

problem = AlphaProblem(snn_csv_paths)

res = minimize(problem,
               CMAES(),
               termination=('n_gen', 50),
               verbose=True)

print("Best alpha:", res.X)
print("MSE totale:", res.F)
