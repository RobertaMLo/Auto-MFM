import numpy as np
import os
import matplotlib.pyplot as plt

def select_solution(sol, obj1, obj2, threshold=0.05):
    """
    Easiest way -- threshold on obj 1 and min on obj2.
    e.g., threshold on slope and minimum on mse
    """
    mask = obj1 <= threshold #threshold su slope
    #print(mask)
    #print(obj1)
    valid_obj1 = obj1[mask]
    valid_obj2 = obj2[mask]
    valid_sol = sol[mask]
    #print(np.shape(valid_sol))

    idx_in_filtered = np.argmin(valid_obj2) # mi piglio il best di errore

    sol_best = valid_sol[idx_in_filtered]
    obj1_best = valid_obj1[idx_in_filtered]
    obj2_best = valid_obj2[idx_in_filtered]
    #print(obj2_best)

    valid_indices = np.where(mask)[0]
    best_idx_global = valid_indices[idx_in_filtered]

    return sol_best, obj1_best, obj2_best, best_idx_global

## HERE SOME STANDARD METHODS:
def select_solution_by_distance(alphas, mse, slope_error):
    """
    In this method , slope and mse must be normalized and it is based on computing distance from ideal point.
    Ideal point: (0,0): optimal slope and mse, so the best solution is the one closer to the ideal point.
    Why this method? Balance of both obj and no stiff thresholds.
    """
    norm_mse = (mse - np.min(mse)) / (np.max(mse) - np.min(mse) + 1e-12)
    norm_slope = (slope_error - np.min(slope_error)) / (np.max(slope_error) - np.min(slope_error) + 1e-12)
    # Euclidean distance
    distances = np.sqrt(norm_mse**2 + norm_slope**2)
    best_idx = np.argmin(distances)
    # Recupero la soluzione
    best_alpha = alphas[best_idx, :]
    best_mse = mse[best_idx]
    best_slope = slope_error[best_idx]

    return best_alpha, best_mse, best_slope, best_idx


def select_knee_point(alphas, mse, slope_error):
    """
    Knee-point detection: method to find out the MAXIMUM of the pareto front curvatur, i.e., the best trade-off of both obj
    Requirment nice-to-have: A well-distributed convex pareto front.

    It is based on the perpendicular distance from the extrems values
    """
    #need to have this kind of struct
    points = np.column_stack([mse, slope_error])

    # extrems of the pareto front
    p1 = points[np.argmin(mse)]     # min MSE
    p2 = points[np.argmin(slope_error)]  # min slope

    # mi costruisco il vettore tra gli estremi
    line_vec = p2 - p1
    line_vec_norm = line_vec / np.linalg.norm(line_vec)

    # Vettori da p1 a ciascun punto
    vec_from_p1 = points - p1

    # Prodotto vettoriale per calcolare la distanza perpendicolare
    projections = np.dot(vec_from_p1, line_vec_norm)
    proj_points = np.outer(projections, line_vec_norm)
    perpendiculars = vec_from_p1 - proj_points
    distances = np.linalg.norm(perpendiculars, axis=1)

    # Indice del punto con distanza massima: il knee
    knee_idx = np.argmax(distances)

    best_alpha = alphas[knee_idx, :]
    best_mse = mse[knee_idx]
    best_slope = slope_error[knee_idx]

    return best_alpha, best_mse, best_slope, knee_idx

def plot_pareto_front(mse, slope):
    """
    For super quock check
    """
    plt.figure(figsize=(6, 4))
    plt.scatter(mse, slope, c="blue", alpha=0.6)
    plt.xlabel("MSE")
    plt.ylabel("Slope error")
    plt.title("Pareto Front (Filtered)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_pareto_with_selection(mse, slope, idx_best, alphas_best, method, threshold=0.05):
    """
    Plot for papers
    """
    fig, ax = plt.subplots(figsize=(4.1, 3))
    ax.scatter(mse, slope, c="black", alpha=0.6, label="Pareto solutions")

    # Evidenzia il punto selezionato
    ax.scatter(mse[idx_best], slope[idx_best],
                c="red", s=80, label="Selected solution",
                edgecolors="black", linewidths=0.7, zorder=5)

    alpha_str = ", ".join([f"{a:.2f}" for a in alphas_best])
    ax.set_title(f"Best solution α = [{alpha_str}]", fontsize=9)
    #ax.axhline(threshold, color="gray", linestyle="--", alpha=0.4, label=f"Slope threshold = {threshold}")
    ax.axhline(threshold, color="gray", linestyle="--", alpha=0.4)

    ax.set_xlabel("Global error", fontsize=10)
    ax.set_ylabel("PC slope error", fontsize=10)
    ax.tick_params(labelsize=8)
    #ax.legend(fontsize=9)
    ax.grid(True)
    plt.tight_layout()
    plt.savefig("pareto_front_"+method+alpha_str+".pdf", dpi=300)
    plt.show()

##### AAAAAAA TO DO VERY IMPORTANT: CAPIRE BEST TRADEOFF NPOP NGEN

npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/cerebellum_zmin_plv_Ie780_debug_corrected/final_pareto_front_bello_NEW_CONFIG_52450.npz"
#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/cerebellum_zmin_plv_Ie780_debug_corrected/final_pareto_front_bello_NEW_CONFIG_42450.npz"
#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/cerebellum_zmin_plv_Ie780_debug_corrected/final_pareto_front_bello_NEW_CONFIG_6_2450.npz"


#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/cerebellum_zmin_plv_Ie780_debug_corrected/final_pareto_front_bello_NEW_CONFIG_3NEW_24_50.npz"
#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/cerebellum_zmin_plv_Ie780_debug_corrected/final_pareto_front_bello_NEW_CONFIG_3NEW_NOUPLIMIT810.npz"

#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/cerebellum_zmin_plv_Ie780_debug_corrected/final_pareto_front_bello_NEW_CONFIG_6_810.npz"


#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_sim1/home/neuro_sim1/marialaura/MF_v26rev01/final_pareto_front_24_100.npz"
#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/MF_v26rev01/final_pareto_front_bello_MAE_8_100.npz"
#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/MF_v26rev01/final_pareto_front_bello_MAE_8_100_RMSE.npz"
#npz_path = "final_pareto_front_bello_2.npz" #prove_2 per vedere se va quello bello a classi
#npz_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/MF_v26rev01/final_pareto_front_bello_MAE_24_50_RMSE_2.npz"

method = 'knee'
#method = 'thrs'
#method = 'dist'

if os.path.exists(npz_path):
    data = np.load(npz_path)

    alphas = data["alphas"]
    mse = data["mse"]
    slope = data["slope"]

    print(f"Shapes - alphas: {alphas.shape}, mse: {mse.shape}, slope: {slope.shape}")
    # I put this penalty when solution of mf are nan of inf
    mask = mse < 1e6
    print(mask)
    mse_filtered = mse[mask]
    slope_filtered = slope[mask]
    alphas_filtered = alphas[mask]

    print(f"Filtered shapes - alphas: {alphas_filtered.shape}, mse: {mse_filtered.shape}, slope: {slope_filtered.shape}")

    #plot_pareto_front(mse_filtered, slope_filtered)

    if method == 'thrs':
        thrs = 0.0025
        sol_best, slope_best, mse_best, idx_best = select_solution(alphas_filtered, slope_filtered, mse_filtered, threshold=thrs)
    elif method == 'dist':
        sol_best, mse_best, slope_best, idx_best = select_solution_by_distance(alphas_filtered, mse_filtered, slope_filtered)
        thrs = 0 #only for plot
    elif method == 'knee':
        sol_best, mse_best, slope_best, idx_best = select_knee_point(alphas_filtered, mse_filtered,slope_filtered)
        thrs = 0  # only for plot
    else:
        print(" INVALID METHOD FOR SELECTION")
        exit()

    plot_pareto_with_selection(mse_filtered, slope_filtered, idx_best, sol_best, method, threshold=thrs)

    print('sol_best ', sol_best, 'slope_best', slope_best, 'mse_best', mse_best)

else:
    print("File does not exist")