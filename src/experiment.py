# Uses Simulation without changing its API
# Produces the runs.csv + timeseries.csv for logger.py

import random
from main import Simulation
from logger import log_run_summary, log_timeseries


def run_single_simulation(
    network_type: str,
    N: int,
    iterations: int,
    T: float,
    alpha: float,
    theta: float,
    beta: float,
    radius: int,
    rand_beneficiaries: bool,
    seed: int,
):
    random.seed(seed)

    sim = Simulation(N)

    if network_type == "HRG":
        sim.build_HRG()
    elif network_type == "PAG":
        sim.build_PAG()
    else:
        raise ValueError("network_type must be 'HRG' or 'PAG'")

    frac_coop_history = []

    for _ in range(iterations):
        sim.play(temptation=T)
        sim.calc_surplus(threshold=theta)
        sim.distribute_tax(taxation=alpha, radius=radius, rand=rand_beneficiaries)
        sim.update_strategies(intensity=beta, num_updates=1)
        frac_C, _ = sim.strategy_distribution()
        frac_coop_history.append(frac_C)
        sim.reset_payoffs()

    final_frac_coop = frac_coop_history[-1]
    avg_degree = sim.average_degree()

    run_id = f"{network_type}_T{T:.2f}_a{alpha:.2f}_s{seed}"

    params = {
        "seed": seed,
        "network_type": network_type,
        "N": N,
        "avg_degree": avg_degree,
        "T": T,
        "alpha": alpha,
        "theta": theta,
        "beta": beta,
        "beneficiary_rule": "random" if rand_beneficiaries else "nearest",
        "init_frac_coop": 0.5,
    }

 
    stats = {
        "converged": False,
        "iters_to_conv": iterations,
        "final_frac_coop": final_frac_coop,
    }

    log_timeseries(run_id, frac_coop_history)
    log_run_summary(run_id, params, stats)


def main():
    N = 10**3
    iterations = 10**4
    theta = 1.0
    beta = 1.0
    radius = 2
    rand_beneficiaries = False

    network_types = ["HRG", "PAG"]
    T_values = [1.1, 1.2, 1.3, 1.4, 1.5]
    alpha_values = [0.0, 0.3, 0.5, 0.7, 0.9]
    seeds = range(5)  # 5 runs per setting

    for net in network_types:
        for T in T_values:
            for alpha in alpha_values:
                for seed in seeds:
                    print(f"Running {net}, T={T}, alpha={alpha}, seed={seed}")
                    run_single_simulation(
                        network_type=net,
                        N=N,
                        iterations=iterations,
                        T=T,
                        alpha=alpha,
                        theta=theta,
                        beta=beta,
                        radius=radius,
                        rand_beneficiaries=rand_beneficiaries,
                        seed=seed,
                    )


if __name__ == "__main__":
    main()
