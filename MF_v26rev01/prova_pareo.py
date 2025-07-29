import numpy as np
import os
import matplotlib.pyplot as plt

def plot_pareto_front(mse, slope):
    plt.figure(figsize=(6, 4))
    plt.scatter(mse, slope, c="blue", alpha=0.6)
    plt.xlabel("MSE")
    plt.ylabel("Slope error")
    plt.title("Pareto Front (Filtered)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

npz_path = "./pareto_solutions.npz"

if os.path.exists(npz_path):
    data = np.load(npz_path)

    alphas = data["alphas"]
    mse = data["mse"]
    slope = data["slope_error"]

    print(f"Shapes - alphas: {alphas.shape}, mse: {mse.shape}, slope: {slope.shape}")
    # I put this penalty when solution of mf are nan of inf
    mask = mse < 1e6
    mse_filtered = mse[mask]
    slope_filtered = slope[mask]
    alphas_filtered = alphas[mask]

    print(f"Filtered shapes - alphas: {alphas_filtered.shape}, mse: {mse_filtered.shape}, slope: {slope_filtered.shape}")

    plot_pareto_front(mse_filtered, slope_filtered)

else:
    print("File does not exist")