from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_trajectories(max_runs: int = 5) -> None:
    ROOT = Path(__file__).resolve().parents[1]
    ts_path = ROOT / "data" / "timeseries.csv"
    runs_path = ROOT / "data" / "runs.csv"
    out_path = ROOT / "docs" / "trajectories_example.png"

    ts = pd.read_csv(ts_path)
    runs = pd.read_csv(runs_path)

    run_ids = runs["run_id"].unique()[:max_runs]

    if len(run_ids) == 0:
        print("No runs found in runs.csv")
        return

    plt.figure(figsize=(8, 6))

    for rid in run_ids:
        sub = ts[ts["run_id"] == rid].sort_values("iter")
        plt.plot(sub["iter"], sub["frac_coop"], alpha=0.5, label=rid)

    plt.xlabel("Iteration")
    plt.ylabel("Fraction cooperators")
    plt.title("Example cooperation trajectories")
    plt.legend(fontsize=6)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    plot_trajectories()
