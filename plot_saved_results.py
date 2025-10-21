import numpy as np
from plot import plot_data, plot_quarantained_bar

# Load saved results
data = np.load("10_run_test.npz", allow_pickle=True)
history_E = data["history_E"]
history_I = data["history_I"]
history_S = data["history_S"]
history_R = data["history_R"]
histore_quarantined = data["history_quarantaine"]
num_days = int(data["num_days"])
n_total = int(data["n_total"])

# Generate x-axis and plot
days = list(range(1, num_days + 1))
plot_data(days, history_E, history_I, history_S, history_R, n_total)
plot_quarantained_bar(histore_quarantined)