import os
import re
import numpy as np
from plot import plot_data, plot_quarantained_bar

folder_path = "results/"

plots_folder = os.path.join(folder_path, "plots")
os.makedirs(plots_folder, exist_ok=True)

simulation_files = [f for f in os.listdir(folder_path) if f.endswith(".npz")]

for sim_file in simulation_files:
    file_path = os.path.join(folder_path, sim_file)
    data = np.load(file_path, allow_pickle=True)
    
    history_E = data["history_E"]
    history_I = data["history_I"]
    history_S = data["history_S"]
    history_R = data["history_R"]
    history_quarantined = data["history_quarantaine"]
    num_days = int(data["num_days"])
    n_total = int(data["n_total"])
    
    days = list(range(1, num_days + 1))
    
    # Shorten filename: remove 'simulation_results_' prefix and any datetime digits at the end
    base_name = sim_file.replace("simulation_results_", "")
    base_name = re.sub(r"\d{8}_\d{6}", "", base_name)  # remove date/time like 20251025_152525
    base_name = base_name.replace(".npz", "")
    
    # Optional: replace some parts to make filename shorter, e.g., underscores for clarity
    base_name = base_name.replace("A=", "_A=").replace("Q=", "Q=")  # example tweak
    
    plot_file1 = os.path.join(plots_folder, f"{base_name}_states.png")
    plot_file2 = os.path.join(plots_folder, f"{base_name}_quarantine.png")
    
    plot_data(days, history_E, history_I, history_S, history_R, n_total, save_path=plot_file1)
    plot_quarantained_bar(history_quarantined, save_path=plot_file2)