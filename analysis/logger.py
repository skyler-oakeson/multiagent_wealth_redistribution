import csv
import os

RUNS_FILE= "data/runs.csv"
TIMESERIES_FILE= "data/timeseries.csv"


def ensure(path):
    os.makedirs(os.path.dirname(path),exist_ok=True)


def write_row(path, fieldnames, row):
    ensure(path)
    exists = os.path.isfile(path)
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def log_run_summary(run_id, params, stats):
    fieldnames = [
    "run_id",
    "seed",
    "network_type",
    "N",
    "avg_degree",
    "T",
    "alpha",
    "theta",
    "beta",
    "beneficiary_rule",
    "init_frac_coop",
    "converged",
    "iters_to_conv",
    "final_frac_coop",
]

    row = {"run_id":run_id}
    row.update(params)
    row.update(stats)
    write_row(RUNS_FILE, fieldnames, row)




def log_timeseries(run_id, coop_list):
    fields = ["run_id", "iter", "frac_coop"]
    ensure(TIMESERIES_FILE)


    exists = os.path.isfile(TIMESERIES_FILE)
    with open(TIMESERIES_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            writer.writeheader()
        
        for i, val in enumerate(coop_list):
            writer.writerow({
                "run_id": run_id,
                "iter": i,
                "frac_coop": float(val)

            })