import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_heatmap(network_type: str) -> None:
    ROOT = Path(__file__).resolve().parents[1]

    runs_path = ROOT / "data" / "runs.csv"
    out_path = ROOT / "docs" / f"heatmap_{network_type}.png"

    df = pd.read_csv(runs_path)

    df = df[df["network_type"] == network_type]

    if df.empty:
        print(f"No rows for network_type='{network_type}' in runs.csv")
        return

    table = df.pivot_table(
        index="alpha",
        columns="T",
        values="final_frac_coop",
        aggfunc="mean",
    )

    table = table.sort_index(axis=0)  # alpha
    table = table.sort_index(axis=1)  # T

    plt.figure(figsize=(8, 6))
    im = plt.imshow(
        table.values,
        aspect="auto",
        origin="lower",
        extent=[
            table.columns.min(),
            table.columns.max(),
            table.index.min(),
            table.index.max(),
        ],
    )
    plt.colorbar(im, label="Final fraction of cooperators")
    plt.xlabel("Temptation T")
    plt.ylabel("Tax rate alpha")
    plt.title(f"Cooperation heatmap ({network_type})")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    for nt in ["HRG", "PAG"]:
        plot_heatmap(nt)
