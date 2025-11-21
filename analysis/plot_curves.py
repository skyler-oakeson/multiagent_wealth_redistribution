# analysis/plot_curves.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_curves(input="data/runs.csv", network="HRG",
                alphas=[0.0, 0.5, 0.9],
                out="docs/curves.png"):

    df = pd.read_csv(input)
    df = df[df["network_type"] == network]

    plt.figure(figsize=(8,6))

    for a in alphas:
        sub = df[df["alpha"] == a]
        g = sub.groupby("T")["final_frac_coop"].mean().sort_index()
        plt.plot(g.index, g.values, marker="o", label=f"α={a}")

    plt.xlabel("T")
    plt.ylabel("Cooperation")
    plt.title(f"Cooperation vs T ({network})")
    plt.legend()

    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
