from pymoo.core.problem import Problem
from pymoo.termination.default import DefaultMultiObjectiveTermination
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.soo.nonconvex.cmaes import CMAES
from pymoo.core.mixed import MixedVariableGA
import numpy as np
import pandas as pd
import os

from load_config_TF import *
from master_equation_CRBL_MF import find_fixed_point_mossy

from mpi4py import MPI

## PARALLELIZATION BABY!!!
comm = MPI.COMM_WORLD
size = comm.Get_size()   # Number of Processes I want to run (NB; EACH process simulates ONLY a bunch of freqs)
rank = comm.Get_rank()   # ID of a process - so RANK = PROCESS NAME (kinda of)

def optimization(problem, algorithm, xtol=1e-8, cvtol=1e-8, ftol=25e-4, period=30,
                 n_gen=100, n_max_evals=10000):

    termination = DefaultMultiObjectiveTermination(
        xtol=xtol, cvtol=cvtol, ftol=ftol, period=period, n_max_gen=n_gen, n_max_evals=n_max_evals
    )
    results = minimize(problem, algorithm, termination, seed=1, verbose=True) #STANDARD FOR NSGA2
    #results = minimize(problem, algorithm, ('n_gen', 100), seed=1, verbose=True)  # STANDARD FOR NSGA
    #results = minimize(problem, algorithm, ('n_gen', 40), seed=1, verbose=True)
    return results


xl = np.array([1.8, 1.8, 1.6, 2.2])
xu = np.array([2.2, 2.2, 2.0, 10.0])
x0 = np.array([2.0, 2.0, 1.8, 2.3])
sigma = 0.3 * (xu - xl)

class AlphaOptimizationMF(Problem):
    def __init__(self, snn_data_path, input_freqs, ci_vec_base, fixed_args):
        super().__init__(n_var=4,
                         n_obj=1,
                         xl=xl,
                         xu = xu
                         )

        self.FMOSSY_IDX = 8

        self.freqs = input_freqs
        self.snn_data = self.load_snn_ground_truth(snn_data_path)
        self.ci_vec_base = ci_vec_base
        self.fixed_args = fixed_args  # dict with TF loading & sim setup args

    def load_snn_ground_truth(self, folder_path):
        # Load SNN stats: assumes 4 CSV files: GrC.csv, GoC.csv, MLI.csv, PC.csv
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

        input_vec[self.FMOSSY_IDX] = input_freq  # Set mossy fiber freq index
        f_backnoise = np.random.rand(len(t)) * input_freq

        X = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, input_vec, t, w, f_backnoise,
                                   Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)
        X_grc=np.average(X[:,0])
        X_goc=np.average(X[:,1])
        X_mli=np.average(X[:,9])
        X_pc=np.average(X[:,10])

        aa = np.average(X[:, [0, 1, 9, 10]], axis =0)

        print('========================DEBUG -----------------\n FREQ:', f_backnoise,'\n ALPHA= ', alphas,
              '\n MEAN ACT', X_grc, X_goc, X_mli, X_pc, '\n MEAN ACT RETURNED', aa, np.shape(aa))

        return np.average(X[:, [0, 1, 9, 10]], axis = 0)

    def _evaluate(self, X, out, *args, **kwargs):
        errors = []

        for alpha_set in X:
            total_err = 0
            invalid = False

            local_errors = []  # Each rank = error (i.e., local error)

            for i, f in enumerate(self.freqs):
                if i % size != rank:
                    continue  # Non è il mio turno quindi aspetto

                # Mi printo un po' di cose che non si sa mai se ho capito
                print(f"[RANK {rank}] Simulating for freq: {f}")
                mf_rates = self.simulate_MF(alpha_set, f)

                if np.any(np.isnan(mf_rates)) or np.any(np.isinf(mf_rates)):
                    print(f"[RANK {rank}] INVALID MF RATES → alphas: {alpha_set}, freq: {f}, rates: {mf_rates}")
                    local_errors.append((f, 1e6 * 4))  # Penalizzazione forte if I have nan in mse part of equation
                    continue

                err_f = 0
                for i_cell, cell in enumerate(['granule_cell', 'golgi_cell', 'MLI_cell', 'purkinje_cell']):

                    snn_mean = np.interp(f, self.snn_data[cell]['freqs'], self.snn_data[cell]['mean'])
                    snn_std = np.interp(f, self.snn_data[cell]['freqs'], self.snn_data[cell]['std'])

                    #print('========================DEBUG -----------------SNN MEAN SD:', snn_mean, snn_std)

                    safe_std = snn_std if snn_std > 1e-6 else 1e-6

                    err = ((mf_rates[i_cell] - snn_mean) / safe_std) ** 2
                    #err = (mf_rates[i_cell] - snn_mean) ** 2
                    err_f += err

                local_errors.append((f, err_f))

            # Raccoglie risultati da tutti i processi!!! N.B. Remember that a process do only a bunch of freqs.
            all_errors = comm.gather(local_errors, root=0)

            if rank == 0:
                merged = {}
                for err_list in all_errors:
                    for f_val, err in err_list:
                        merged[f_val] = err
                total_err = sum(merged.values())

                print(f"\n[RANK 0] Alphas: {alpha_set} → Total Error: {total_err:.4f}")
                errors.append(total_err)

        # Solo il rank 0 aggiorna i risultati finali
        if rank == 0:
            out["F"] = np.array(errors).reshape(-1, 1)


# # Here problem is defined as a class
problem = AlphaOptimizationMF(
    snn_data_path='./',

    #input_freqs=np.arange(4, 84, 4),
    input_freqs=np.array([4, 40, 80]),

    ci_vec_base= [0.5, 5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 4, 15, 38, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # dal tuo codice
    fixed_args={
        'load_transfer_functions': load_transfer_functions,
        'find_fixed_point_mossy': find_fixed_point_mossy,
        't': np.arange(0, 0.5, 1e-4), 'w': 0., 'T': 3.5e-3,
        'Ngrc': 29916, 'Ngoc': 71, 'Nmossy': 2340, 'Nmli': 302+150, 'Npc': 69
    }
)

## value to test the algorithm (i.e., high tol and low popsize)
tol = 1e-5
pops = 8 #default is 24
n_gen = 50 #default 100

# NSGA2 doesn't want the init, but here I wanna put my priori knowledge on the fitting.
algorithm = NSGA2(pop_size=pops)

#algorithm = CMAES(x0=x0,sigma=1.0,bounds=(xl, xu),CMA_stds=sigma)



#Default option : cvtol=1e-8, ftol=25e-4, period=30, n_gen=100, n_max_evals=10000
# In function oprimization, during each generation, pymoo call function _evaluate! NO NEED TO DO EXPLICITLY
results = optimization(problem, algorithm, xtol=tol, n_gen=n_gen)

best_idx = np.argmin(results.F)
best_alphas = results.X[best_idx]
print("Best alpha values:", best_alphas)
