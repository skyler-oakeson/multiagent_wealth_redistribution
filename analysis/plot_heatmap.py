# analysis/plot_heatmap.py

import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_heatmap(input="data/runs.csv", network="HRG",
                 out="docs/heatmap.png"):

    df = pd.read_csv(input)
    df = df[df["network_type"] == network]

    table = df.pivot_table(
        index="alpha",
        columns="T",
        values="final_frac_coop",
        aggfunc="mean"
    )

    plt.figure(figsize=(8,6))
    im = plt.imshow(table, origin="lower", aspect="auto",
                    extent=[table.columns.min(), table.columns.max(),
                            table.index.min(), table.index.max()])
    plt.colorbar(im, label="Cooperation")
    plt.xlabel("T")
    plt.ylabel("alpha")
    plt.title(f"Cooperation heatmap ({network})")

    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
