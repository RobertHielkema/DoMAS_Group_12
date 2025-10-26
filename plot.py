import matplotlib.pyplot as plt
import numpy as np


def plot_data(x, history_E, history_I, history_S, history_R, n_total, save_path=None):

    # uncomment to use moving average
    # count moving average with window size 2
    '''
    window_size = 3
    history_E = [
        sum(history_E[max(0, i - window_size): min(len(history_E), i + window_size + 1)]) /
        len(history_E[max(0, i - window_size): min(len(history_E), i + window_size + 1)])
        for i in range(len(history_E))
    ]

    history_I = [
        sum(history_I[max(0, i - window_size): min(len(history_I), i + window_size + 1)]) /
        len(history_I[max(0, i - window_size): min(len(history_I), i + window_size + 1)])
        for i in range(len(history_I))
    ]

    history_S = [
        sum(history_S[max(0, i - window_size): min(len(history_S), i + window_size + 1)]) /
        len(history_S[max(0, i - window_size): min(len(history_S), i + window_size + 1)])
        for i in range(len(history_S))
    ]

    history_R = [
        sum(history_R[max(0, i - window_size): min(len(history_R), i + window_size + 1)]) /
        len(history_R[max(0, i - window_size): min(len(history_R), i + window_size + 1)]) 
        for i in range(len(history_R))
    ]
    '''

    history_E, history_I, history_S, history_R =  np.array(history_E), np.array(history_I), np.array(history_S), np.array(history_R)
    history_E = history_E.mean(axis=0)
    history_I = history_I.mean(axis=0)
    history_S = history_S.mean(axis=0)
    history_R = history_R.mean(axis=0)

    fig, axs = plt.subplots(2, 1, figsize=(8, 6))  # 2 rows, 1 column

    axs[0].plot(x, history_E, color="#ffcc00", label='Exposed [E]')
    axs[0].plot(x, history_I, color="#ff0000", label='Infected [I]')
    axs[0].set_ylabel('Persons')
    axs[0].set_xlabel('Time [Days]')
    axs[0].legend(loc='upper right')
    axs[0].set_title('Average number of persons in [E] and [I] states')
    axs[0].set_xticks(range(1, 210, 10))


    history_E = [E / n_total * 100 for E in history_E]
    history_I = [I / n_total * 100 for I in history_I]
    history_S = [S / n_total * 100 for S in history_S]
    history_R = [R / n_total * 100 for R in history_R]
    axs[1].stackplot(x, history_E , history_I, history_S, history_R, colors=["#ffcc00", "#ff0000", "#1f77b4", "#90ee90"], labels=['Exposed [E]', 'Infected [I]', 'Susceptible [S]', 'Removed [R]'])

    axs[1].set_ylabel('Persons [%]')
    axs[1].set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    axs[1].set_yticklabels([f'{i}%' for i in range(0, 101, 10)])
    axs[1].legend(loc='upper right')
    axs[1].set_title('average percentage of persons in each state')
    axs[1].set_xlabel('Time [Days]')
    axs[1].set_ylabel('Persons')
    axs[1].set_xticks(range(1, 210, 5))
    axs[1].tick_params(axis='x', rotation=90)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()
    
def plot_quarantained_bar(history_quarantained, save_path=None):
    infected_means = []
    non_infected_means = []
    total_counts = []

    for run in history_quarantained:
        run = np.array(run)
        valid = run[run != -1]  # ignore padding
        if len(valid) == 0:
            continue

        infected_count = np.sum(valid == 1)
        non_infected_count = np.sum(valid == 0)
        total = infected_count + non_infected_count

        infected_means.append(infected_count / total)
        non_infected_means.append(non_infected_count / total)
        total_counts.append(total)

    # Mean of means (each run equally weighted)
    infected_ratio = np.mean(infected_means)
    non_infected_ratio = np.mean(non_infected_means)
    avg_total = np.mean(total_counts)

    # Convert back to expected number of persons (average total * mean ratio)
    infected_avg = infected_ratio * avg_total
    non_infected_avg = non_infected_ratio * avg_total

    # Convert to percentages for labels
    infected_pct = infected_ratio * 100
    non_infected_pct = non_infected_ratio * 100

    labels = ['Infected & quarantined', 'Healthy & quarantined']
    values = [infected_avg, non_infected_avg]
    colors = ['tomato', 'skyblue']

    plt.figure(figsize=(5, 4))
    bars = plt.bar(labels, values, color=colors)
    plt.ylabel('Average number of persons')
    plt.title('Average composition of quarantined population across runs')
    plt.grid(axis='y', linestyle='--', alpha=0.4)

    # Add inline percentage labels
    for bar, pct in zip(bars, [infected_pct, non_infected_pct]):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height / 2,
            f"{pct:.1f}%",
            ha='center', va='center', color='white', fontsize=12, fontweight='bold'
        )

    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()