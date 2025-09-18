import matplotlib.pyplot as plt


def plot_data(x, history_E, history_I, history_S, history_R, n_total):

    # count moving average with window size 2
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


    fig, axs = plt.subplots(2, 1, figsize=(8, 6))  # 2 rows, 1 column

    axs[0].plot(x, history_E, color="#ffcc00", label='Exposed [E]')
    axs[0].plot(x, history_I, color="#ff0000", label='Infected [I]')
    axs[0].set_ylabel('Persons')
    axs[0].set_xlabel('Time [Days]')
    axs[0].set_title('Average number of persons in [E] and [I] states')


    history_E = [E / n_total * 100 for E in history_E]
    history_I = [I / n_total * 100 for I in history_I]
    history_S = [S / n_total * 100 for S in history_S]
    history_R = [R / n_total * 100 for R in history_R]
    axs[1].stackplot(x, history_E , history_I, history_S, history_R, colors=["#ffcc00", "#ff0000", "#1f77b4", "#90ee90"], labels=['Exposed [E]', 'Infected [I]', 'Susceptible [S]', 'Removed [R]'])

    axs[1].set_ylabel('Persons [%]')
    axs[1].set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    axs[1].set_yticklabels([f'{i}%' for i in range(0, 101, 10)])
    axs[1].set_title('Infected [I]')
    axs[1].set_xlabel('Time [Days]')
    axs[1].set_ylabel('Persons')

    plt.tight_layout()

    plt.show()