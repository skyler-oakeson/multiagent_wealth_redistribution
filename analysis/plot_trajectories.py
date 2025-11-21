# analysis/plot_trajectories.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_trajectories(
        timeseries="data/timeseries.csv",
        runs="data/runs.csv",
        out="docs/trajectories.png",
        max_runs=5
    ):

    ts = pd.read_csv(timeseries)
    df = pd.read_csv(runs)

    chosen = df["run_id"].unique()[:max_runs]

    plt.figure(figsize=(8,6))
    for rid in chosen:
        sub = ts[ts["run_id"] == rid]
        plt.plot(sub["iter"], sub["frac_coop"], alpha=0.6)

    plt.xlabel("Iteration")
    plt.ylabel("Cooperation")
    plt.title("Cooperation Trajectories")

    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
