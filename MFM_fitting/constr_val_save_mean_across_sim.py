import numpy as np
import os
from tqdm import tqdm

# Configurazione percorsi
base_path = "/run/user/1000/gvfs/sftp:host=90.147.108.122,user=neuro_img/home/neuro_img/Users/Roberta/cerebellum_zmin_plv_Ie780_debug_corrected"
out_path = "/home/bcc/projects/BSB4_demo/cerebellum_zmin_plv_Ie780_debug_corrected_GrCexploration"
base_folder_name = "20250930_CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_THRS0025s_CLUST"

# Parametri
n_simulations = 100  # Cartelle da _1 a _100
subfolder_range = np.arange(4.0, 80.1, 4.0)  # Da 4.0 a 80.0 con step 4
populations = ['GrC_act_sd.npz', 'GoC_act_sd.npz', 'MLI_act_sd.npz', 'PC_act_sd.npz']

# Output directory
output_dir = out_path + '/' + f"{base_folder_name}_averaged"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Inizio elaborazione di {n_simulations} simulazioni...")
print(f"Sottocartelle: {len(subfolder_range)} (da 4.0 a 80.0)")
print(f"Popolazioni: {len(populations)}")

# Per ogni sottocartella (4.0, 8.0, ..., 80.0)
for subfolder_val in tqdm(subfolder_range, desc="Sottocartelle"):
    subfolder_name = f"{subfolder_val}_CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5"
    
    # Dizionario per accumulare i dati di tutte le simulazioni
    data_accumulated = {pop: [] for pop in populations}
    
    # Itera sulle 100 simulazioni
    for sim_idx in range(1, n_simulations + 1):
        main_folder = base_path + '/' + f"{base_folder_name}_{sim_idx}"
        subfolder_path = main_folder + '/' + subfolder_name
        
        # Carica i file per ogni popolazione
        for pop_file in populations:
            file_path = subfolder_path + '/' + pop_file
            
            if os.path.exists(file_path):
                try:
                    data = np.load(file_path)
                    arr = data['arr_0']  # Shape (2, 5000): [0,:] = avg, [1,:] = sd
                    
                    # Prendi solo la riga avg (indice 0)
                    avg_data = arr[0, :]
                    data_accumulated[pop_file].append(avg_data)
                    
                except Exception as e:
                    print(f"Errore caricando {file_path}: {e}")
            else:
                print(f"File non trovato: {file_path}")
    
    # Calcola la media su tutte le simulazioni e salva
    for pop_file in populations:
        if len(data_accumulated[pop_file]) > 0:
            # Stack tutti gli avg e calcola la media
            all_avgs = np.array(data_accumulated[pop_file])  # Shape: (n_sims, 5000)
            mean_avg = np.mean(all_avgs, axis=0)  # Shape: (5000,)
            std_avg = np.std(all_avgs, axis=0)    # Shape: (5000,) - sd tra le simulazioni
            
            # Crea array 2x5000 come formato originale
            result = np.stack([mean_avg, std_avg], axis=0)
            
            # Nome file di output
            pop_name = pop_file.replace('.npz', '')
            output_file = output_dir + '/' + f"{subfolder_name}_{pop_name}_averaged.npz"
            
            # Salva
            np.savez(output_file, arr_0=result)
            
            print(f"Salvato: {os.path.basename(output_file)} (media di {len(data_accumulated[pop_file])} simulazioni)")
        else:
            print(f"Nessun dato trovato per {pop_file} nella sottocartella {subfolder_name}")

print(f"\nElaborazione completata! File salvati in: {output_dir}")
print(f"Totale sottocartelle elaborate: {len(subfolder_range)}")
print(f"File per sottocartella: {len(populations)}")
print(f"Totale file creati: {len([f for f in os.listdir(output_dir) if f.endswith('.npz')])}")