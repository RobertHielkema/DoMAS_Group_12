import os
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder_path = "results/"


def get_average_number_days_epidemic(history_I, history_E):
    days_epidemic = []
    for i in range(history_I.shape[0]):
        mask = (history_I[i] == 0) & (history_E[i] == 0)
        if np.any(mask):
            days_epidemic.append(np.flatnonzero(mask)[0])
        else:
            days_epidemic.append(np.nan)  # Use NaN if no zeros in the row

    # Compute average, ignoring rows with no zeros
    average_days_epidemic = int(np.ceil(np.nanmean(days_epidemic)))
    return average_days_epidemic

def get_average_max_infections(history_I):
    # Get the max value of each row
    max_values = np.max(history_I, axis=1)
    
    # Compute the average of these max values
    avg_max = int(np.ceil(np.mean(max_values)))
    
    return avg_max

def get_total_infections(history_R):
    # Get the last value of each row
    last_values = history_R[:, -1]
    
    # Compute the average
    avg_last = int(np.ceil(np.mean(last_values)))
    
    return avg_last

if __name__ == "__main__":
    simulation_files = [f for f in os.listdir(folder_path) if f.endswith(".npz")]
    rows = []
    for sim_file in simulation_files:
        file_path = os.path.join(folder_path, sim_file)
        data = np.load(file_path, allow_pickle=True)
        
        history_E = data["history_E"]
        history_I = data["history_I"]
        history_S = data["history_S"]
        history_R = data["history_R"]
        history_quarantined = data["history_quarantaine"]
        
        num_days = get_average_number_days_epidemic(history_I, history_E)
        max_infections = get_average_max_infections(history_I)
        total_infections = get_total_infections(history_R)

        basename = os.path.basename(file_path)
        q_match = re.search(r"Q=([0-9.]+)", basename)
        a_match = re.search(r"A=([0-9.]+)", basename)
        selftest_match = re.search(r"selftest=(True|False)", basename)

        # Extract values
        Q_value = float(q_match.group(1)) if q_match else None
        A_value = float(a_match.group(1)) if a_match else None
        self_test_value = selftest_match.group(1) == "True" if selftest_match else None
        
        # print(Q_value, A_value, self_test_value)
        # --- Add row to the list ---
        rows.append({
            "Q": Q_value,
            "A": A_value,
            "self_test": self_test_value,
            "num_days": num_days,
            "max_infections": max_infections,
            "total_infections": total_infections
        })

        
    # --- Create DataFrame ---
    df_results = pd.DataFrame(rows)

    print(df_results)
    save_folderpath = os.path.join(folder_path, "heatmaps")
    os.makedirs(save_folderpath, exist_ok=True)

    # Filter for self_test=False
    df_false = df_results[df_results['self_test'] == False].pivot(
        index="Q", columns="A", values="max_infections"
    )

    plt.figure(figsize=(8,6))
    sns.heatmap(df_false, annot=True, fmt=".1f", cmap="RdYlGn_r", vmin=0, vmax=280)  # 280 is the maximum number of max infections
    plt.title("Max Infections excluding self test")
    plt.xlabel("App adoption probability")
    plt.ylabel("Compliance probability")
    plt.savefig(os.path.join(save_folderpath, "max_infections_ex_selftest.png"), dpi=300, bbox_inches='tight')

    # Filter for self_test=True
    df_false = df_results[df_results['self_test'] == True].pivot(
        index="Q", columns="A", values="max_infections"
    )

    plt.figure(figsize=(8,6))
    sns.heatmap(df_false, annot=True, fmt=".1f", cmap="RdYlGn_r", vmin=0, vmax=280)  # 280 is the maximum number of max infections
    plt.title("Max Infections including self test")
    plt.xlabel("App adoption probability")
    plt.ylabel("Compliance probability")
    plt.savefig(os.path.join(save_folderpath, "max_infections_inc_selftest.png"), dpi=300, bbox_inches='tight')


    df_false = df_results[df_results['self_test'] == False].pivot(
        index="Q", columns="A", values="num_days"
    )

    plt.figure(figsize=(8,6))
    sns.heatmap(df_false, annot=True, fmt=".1f", cmap="RdYlGn_r", vmin=0, vmax=150)
    plt.title("Epidemic duration excluding self test")
    plt.xlabel("App adoption probability")
    plt.ylabel("Compliance probability")
    plt.savefig(os.path.join(save_folderpath, "epi_duration_ex_selftest.png"), dpi=300, bbox_inches='tight')

    # Filter for self_test=True
    df_false = df_results[df_results['self_test'] == True].pivot(
        index="Q", columns="A", values="num_days"
    )

    plt.figure(figsize=(8,6))
    sns.heatmap(df_false, annot=True, fmt=".1f", cmap="RdYlGn_r", vmin=0, vmax=150)
    plt.title("Epidemic duration including self test")
    plt.xlabel("App adoption probability")
    plt.ylabel("Compliance probability")
    plt.savefig(os.path.join(save_folderpath, "epi_duration_inc_selftest.png"), dpi=300, bbox_inches='tight')

    df_false = df_results[df_results['self_test'] == False].pivot(
        index="Q", columns="A", values="total_infections"
    )

    plt.figure(figsize=(8,6))
    sns.heatmap(df_false, annot=True, fmt=".1f", cmap="RdYlGn_r", vmin=0, vmax=5000)
    plt.title("Total infections excluding self test")
    plt.xlabel("App adoption probability")
    plt.ylabel("Compliance probability")
    plt.savefig(os.path.join(save_folderpath, "tot_infections_ex_selftest.png"), dpi=300, bbox_inches='tight')

    # Filter for self_test=True
    df_false = df_results[df_results['self_test'] == True].pivot(
        index="Q", columns="A", values="total_infections"
    )

    plt.figure(figsize=(8,6))
    sns.heatmap(df_false, annot=True, fmt=".1f", cmap="RdYlGn_r", vmin=0, vmax=5000)
    plt.title("Total infections including self test")
    plt.xlabel("App adoption probability")
    plt.ylabel("Compliance probability")
    plt.savefig(os.path.join(save_folderpath, "tot_infections_inc_selftest.png"), dpi=300, bbox_inches='tight')
