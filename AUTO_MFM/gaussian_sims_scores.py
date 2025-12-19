import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import csv
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import mutual_info_score
import seaborn as sns

def load_my_file(basepath, basename, sigma, amp):
    filename = os.path.join(basepath, f"{basename}{sigma}_{amp}.txt")
    data_txt = np.loadtxt(filename)

    inp_txt = data_txt[:, 0]          # input
    mfm_pred_txt = data_txt[:, 1:]    # MFM pred

    # I want to load only the activity
    signals = {
        "PC":  mfm_pred_txt[:, 10],
        "MLI": mfm_pred_txt[:, 9],
        "GoC": mfm_pred_txt[:, 1],
        "GrC": mfm_pred_txt[:, 0],
        "input": inp_txt
    }

    return {
        "sigma": sigma,
        "amp": amp,
        "signals": signals
    }

def load_all_files(basepath, basename, sigmas, amps):

    results = {}
    for sigma in sigmas:
        for amp in amps:
            try:
                results[(sigma, amp)] = load_my_file(basepath, basename, sigma, amp)
            except Exception as e:
                print(f"Error with sigma={sigma}, amp={amp}: {e}")
    return results


def peak_analysis(signal, prominence, t, ttrans, color='green', color_peak='black', name_fig='peak', save_img=True):
    t = t[ttrans:]
    signal_notrans = signal[ttrans:]  # to avoid that first point after transient is considered as a peak
    peaks, _ = find_peaks(signal_notrans, prominence=prominence)

    peak_act = signal_notrans[peaks]
    print('PeaksHz', peak_act)

    peak_max = peaks[np.argmax(signal_notrans[peaks])]
    max_act = round(signal_notrans[peak_max], 0)
    print('MaxHz: ', max_act)

    if len(peaks) > 1:
        valley_interval = signal_notrans[peaks[0]:peaks[-1]]  # interval between two peaks
        pause = np.argmin(valley_interval)
        valley_min = round(valley_interval[pause], 0)
        print('PauseHz', valley_min)
    else:
        valley_min = 0
        print('No Pause')

    diff_peak_max_pause = max_act - valley_min
    print('Pause_depthHz = Peak_max - Pause = ', diff_peak_max_pause)

    diff_pause_baseline = round(valley_min - signal_notrans[0], 0)  # assuming first point is the baseline
    print('Pause_depth respect to baseline [Hz] = Pause - baseline = ', diff_pause_baseline)

    AUC = round(np.trapz(signal_notrans, t), 0)
    print('AUC: ', AUC)

    plt.figure(figsize=(3.1, 2.4))
    plt.plot(t, signal_notrans, color=color, linewidth=0.9)
    plt.plot(t[peaks], signal_notrans[peaks], "*", color=color_peak)
    # plt.plot(t[pause], signal_notrans[pause], "x", color = color_peak)

    plt.ylabel('Activity [Hz]', fontsize=12)
    plt.yticks([np.min(signal_notrans), (max_act + np.min(signal_notrans))/2, max_act])

    plt.xticks([round(np.min(t), 2), round(np.max(t) / 2, 2), round(np.max(t), 2)])
    plt.xlabel('time [s]', fontsize=12)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    if save_img:
        plt.savefig(name_fig + '.png', dpi=300, bbox_inches="tight")
        plt.savefig(name_fig + '.pdf', dpi=300, bbox_inches="tight")

    plt.show()

    return peak_act, max_act, valley_min, diff_peak_max_pause, diff_pause_baseline, AUC

import csv


def run_peak_analysis_on_all(all_data, sigmas, amps, t, path_for_csv = "./", prominence=0.3, ttrans=100):
    """
    Run the function "peak_analysis" and save the results in three different CSV one per pop(PC, MLI, GoC, GrC).
    """

    populations = ["PC", "MLI", "GoC", "GrC"]

    # CSV init. sigma, amo and the scores are the name of the columns
    for pop in populations:
        with open(path_for_csv + f"{pop}_scores.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "sigma", "amp", "max_act", "valley_min",
                "diff_peak_max_pause", "diff_pause_baseline", "AUC"
            ])


    for sigma in sigmas:
        for amp in amps:

            signals = all_data[(sigma, amp)]["signals"]

            for pop in populations:
                signal = signals[pop]

                peak_act, max_act, valley_min, diff_peak_max_pause, diff_pause_baseline, AUC = \
                    peak_analysis(signal,
                                  prominence=prominence,
                                  t=t,
                                  ttrans=ttrans,
                                  save_img=False,
                                  name_fig=f"{pop}_sigma{sigma}_amp{amp}")

                # Save data in the csv
                with open(path_for_csv + f"{pop}_scores.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        sigma,
                        amp,
                        #list(peak_act),   # If I want to re-add I have to add also the names
                        max_act,
                        valley_min,
                        diff_peak_max_pause,
                        diff_pause_baseline,
                        AUC
                    ])


def compute_all_score_matrices(all_data, sigmas, amps, t, prominence=0.3, ttrans=100, pop="PC"):
    """
    Calcola tutte le matrici sigma × amp per:
    - AUC
    - peak_max
    - valley_min
    - diff_peak_pause
    - diff_pause_baseline
    con il controllo richiesto:
    se valley_min == 0 → diff_peak_pause e diff_baseline diventano NaN.
    """

    AUC_mat = np.zeros((len(amps), len(sigmas)))
    peak_mat = np.zeros((len(amps), len(sigmas)))
    valley_mat = np.zeros((len(amps), len(sigmas)))
    diff_peak_pause_mat = np.zeros((len(amps), len(sigmas)))
    diff_baseline_mat = np.zeros((len(amps), len(sigmas)))

    for i, amp in enumerate(amps):
        for j, sigma in enumerate(sigmas):

            signal = all_data[(sigma, amp)]["signals"][pop]

            peak_act, max_act, valley_min, diff_peak_max_pause, diff_pause_baseline, AUC = \
                peak_analysis(signal,
                              prominence=prominence,
                              t=t,
                              ttrans=ttrans,
                              save_img=False)

            AUC_mat[i, j] = AUC
            peak_mat[i, j] = max_act
            valley_mat[i, j] = valley_min

            # --- check for scored derved from peak and pause---
            if valley_min == 0:
                diff_peak_pause_mat[i, j] = np.nan
                diff_baseline_mat[i, j] = np.nan
            else:
                diff_peak_pause_mat[i, j] = diff_peak_max_pause
                diff_baseline_mat[i, j] = diff_pause_baseline

    return {
        "AUC": AUC_mat,
        "peak": peak_mat,
        "valley": valley_mat,
        "diff_peak_pause": diff_peak_pause_mat,
        "diff_baseline": diff_baseline_mat
    }



def plot_surface_3d(sigmas, amps, Z, title, zlabel):

    Sigma_grid, Amp_grid = np.meshgrid(sigmas, amps)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(Sigma_grid, Amp_grid, Z,
                           cmap="hot", edgecolor="none", alpha=0.9)

    ax.set_xlabel("Sigma", fontsize=12)
    ax.set_ylabel("Amp", fontsize=12)
    ax.set_zlabel(zlabel, fontsize=12)
    ax.set_title(title, fontsize=14)

    fig.colorbar(surf, shrink=0.6, label=zlabel)
    plt.show()

def get_stimulus_window(t, sigma):
    mu = t[len(t)//2]
    t_start = mu - 3*sigma
    t_end   = mu + 3*sigma

    # Indici corrispondenti
    idx_start = np.searchsorted(t, t_start)
    idx_end   = np.searchsorted(t, t_end)

    return idx_start, idx_end


def dynamic_pcc(x, y, window_size, step):
    pcc_values = []
    for start in range(0, len(x) - window_size, step):
        end = start + window_size
        r, _ = pearsonr(x[start:end], y[start:end])
        pcc_values.append(r)
    return np.array(pcc_values)


def dynamic_mutual_information(x, y, window_size, step, bins=20):
    mi_values = []
    for start in range(0, len(x) - window_size, step):
        end = start + window_size

        x_win = x[start:end]
        y_win = y[start:end]

        x_binned = np.digitize(x_win, np.histogram(x_win, bins=bins)[1])
        y_binned = np.digitize(y_win, np.histogram(y_win, bins=bins)[1])

        mi = mutual_info_score(x_binned, y_binned)
        mi_values.append(mi)

    return np.array(mi_values)


def compute_pcc_mi_all(all_data, sigmas, amps, window_size, step, pop="PC"):
    """
    Calcola PCC dinamico e MI dinamica tra input e PC
    per tutte le combinazioni sigma × amp.
    Ogni cella della matrice corrisponde a:
    input(sigma, amp) vs PC(sigma, amp)
    """

    PCC_mat = np.zeros((len(amps), len(sigmas)))
    MI_mat  = np.zeros((len(amps), len(sigmas)))

    for i, amp in enumerate(amps):
        for j, sigma in enumerate(sigmas):

            # --- QUI GARANTIAMO LA CORRISPONDENZA ---
            inp = all_data[(sigma, amp)]["signals"]["input"]
            pc  = all_data[(sigma, amp)]["signals"][pop]

            # Calcolo dinamico
            pcc_values = dynamic_pcc(inp, pc, window_size, step)
            mi_values  = dynamic_mutual_information(inp, pc, window_size, step)

            # Salviamo la media (puoi cambiare in max, min, ecc.)
            PCC_mat[i, j] = np.nanmean(pcc_values)
            MI_mat[i, j]  = np.nanmean(mi_values)

    return PCC_mat, MI_mat



def compute_pcc_mi_all_stimulus_window(all_data, sigmas, amps, t, window_size, step, pop="PC"):
    PCC_mat = np.zeros((len(amps), len(sigmas)))
    MI_mat  = np.zeros((len(amps), len(sigmas)))

    for i, amp in enumerate(amps):
        for j, sigma in enumerate(sigmas):

            inp = all_data[(sigma, amp)]["signals"]["input"]
            pc  = all_data[(sigma, amp)]["signals"][pop]

            # --- Finestra dello stimolo ---
            idx_start, idx_end = get_stimulus_window(t, sigma)
            inp_win = inp[idx_start:idx_end]
            pc_win  = pc[idx_start:idx_end]

            # --- Calcolo dinamico ---
            pcc_values = dynamic_pcc(inp_win, pc_win, window_size, step)
            mi_values  = dynamic_mutual_information(inp_win, pc_win, window_size, step)

            PCC_mat[i, j] = np.nanmean(pcc_values)
            MI_mat[i, j]  = np.nanmean(mi_values)

    return PCC_mat, MI_mat


def extract_dynamic_xy_stimulus(all_data, sigma, amp, t, window_size, step, pop="PC"):
    inp = all_data[(sigma, amp)]["signals"]["input"]
    pc  = all_data[(sigma, amp)]["signals"][pop]

    idx_start, idx_end = get_stimulus_window(t, sigma)
    inp_win = inp[idx_start:idx_end]
    pc_win  = pc[idx_start:idx_end]

    x_centers = []
    y_centers = []

    for start in range(0, len(inp_win) - window_size, step):
        end = start + window_size
        x_centers.append(np.mean(inp_win[start:end]))
        y_centers.append(np.mean(pc_win[start:end]))

    return np.array(x_centers), np.array(y_centers)


def plot_heatmap(sigmas, amps, Z, title, label):
    plt.figure(figsize=(8,6))
    sns.heatmap(Z,
                xticklabels=sigmas,
                yticklabels=amps,
                cmap="magma",
                annot=False)
    plt.xlabel("Sigma")
    plt.ylabel("Amp")
    plt.title(title)
    plt.show()




if __name__ == '__main__':

    ## the parameters required to be known a priori are: sigmas and amps values and
    ## the length & resolution of the simulations
    sigmas = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    amps = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]

    # this actually needed only to plot the images...
    dt = 1e-4
    sim_len = 0.5
    t = np.arange(0, sim_len, dt)


    basepath = "gaussian_input_output"
    basename = "gaussian_input"
    all_data = load_all_files(basepath, basename, sigmas, amps)

    pc_signal = all_data[(0.05, 100)]["signals"]["PC"]
    goc_signal = all_data[(0.05, 100)]["signals"]["GoC"]

    #print(np.shape(pc_signal))

    #run_peak_analysis_on_all(all_data, sigmas, amps, t, path_for_csv=basepath + '/', prominence=0.9)

    #peak_analysis(signal=all_data[(0.1, 150)]["signals"]["PC"], prominence=0.9, t=t, ttrans=100, color='green',
    #              color_peak='black', name_fig='peak_PC_01_150', save_img=True)

    #scores = compute_all_score_matrices(all_data, sigmas, amps, t, prominence=0.9, ttrans=100, pop="PC")

    """
    plot_surface_3d(sigmas, amps, scores["AUC"],
                    title="AUC",
                    zlabel="AUC")

    plot_surface_3d(sigmas, amps, scores["peak"],
                    title="Max Peak",
                    zlabel="Peak max [Hz]")

    plot_surface_3d(sigmas, amps, scores["valley"],
                    title="Pause",
                    zlabel="Pausa [Hz]")

    plot_surface_3d(sigmas, amps, scores["diff_peak_pause"],
                    title="Peak-Pause difference",
                    zlabel="Peak - Pause [Hz]")

    plot_surface_3d(sigmas, amps, scores["diff_baseline"],
                    title="Pause-baseline difference",
                    zlabel="Pause - Baseline [Hz]")
    """

    window_size = 500
    step = 100
    PCC_mat, MI_mat = compute_pcc_mi_all_stimulus_window(all_data, sigmas, amps, t, window_size=window_size, step=step, pop="PC")

    plot_heatmap(sigmas, amps, PCC_mat,
                 title="PCC dynamic (input mu +-3 sdev)",
                 label="PCC")

    plot_heatmap(sigmas, amps, MI_mat,
                 title="Mutual info dynamic (input mu +-3 sdev)",
                 label="MI")


    PCC_mat, MI_mat = compute_pcc_mi_all(all_data, sigmas, amps, window_size=window_size, step=step,
                                                         pop="PC")

    plot_heatmap(sigmas, amps, PCC_mat,
                 title="PCC dynamic (all input)",
                 label="PCC")

    plot_heatmap(sigmas, amps, MI_mat,
                 title="Mutual Information dynamic (all input)",
                 label="MI")




