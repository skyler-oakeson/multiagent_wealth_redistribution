import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_curves(network_type: str, alphas) -> None:
    ROOT = Path(__file__).resolve().parents[1]
    runs_path = ROOT / "data" / "runs.csv"
    out_path = ROOT / "docs" / f"curves_{network_type}.png"

    df = pd.read_csv(runs_path)
    df = df[df["network_type"] == network_type]

    if df.empty:
        print(f"No rows for network_type='{network_type}' in runs.csv")
        return

    plt.figure(figsize=(8, 6))

    for alpha in alphas:
        sub = df[np.isclose(df["alpha"], alpha)]
        if sub.empty:
            continue
        g = sub.groupby("T")["final_frac_coop"].mean().sort_index()
        plt.plot(g.index.values, g.values, marker="o", label=f"alpha={alpha:.2f}")

    plt.xlabel("Temptation T")
    plt.ylabel("Final fraction of cooperators")
    plt.title(f"Cooperation vs T ({network_type})")
    plt.legend()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    alphas = [0.0, 0.3, 0.5, 0.7, 0.9]
    for nt in ["HRG", "PAG"]:
        plot_curves(nt, alphas)
