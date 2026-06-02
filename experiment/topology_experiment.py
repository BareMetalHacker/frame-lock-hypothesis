"""
Topology-only resilience experiment for "The Red Queen's Prison".

Tests ONE falsifiable sub-claim: that centralized (star) coordination has a
single-point-of-failure under corruption that distributed (mesh) coordination
does not, and that this trade-off reverses with how clean the channel is.

Design rules (anti-rigging):
  * The ONLY structural difference between arms is the communication graph.
  * Both arms try to do the same thing: estimate a drifting true state and act on it.
  * Centralized aggregation is OPTIMAL in clean conditions (averages out noise),
    so the star is *expected* to win when corruption is low. If it didn't, the
    model would be suspect.
  * The same corruption (fraction f, same adversarial magnitude) hits both arms.
  * Two adversaries: RANDOM (topology-blind) and TARGETED (hits highest-degree node first).
  * 'star'        = centralized hub aggregating reports by MEAN.
    'star_median' = same, but hub aggregates by MEDIAN (a robustness check).
    'mesh'        = distributed: each agent blends own sensing with neighbours'.

The result is a statement about THIS MODEL, not about the real world.

Run:  python topology_experiment.py   ->  writes topology_results.json
Plot: python plot_results.py          ->  writes topology_result.png
"""
import numpy as np
import json


def run_trial(arch, f, adversary, N=100, T=80, atk=(30, 60),
              sigma_sense=1.0, sigma_drift=0.2, adv_value=30.0,
              k_side=2, rng=None):
    rng = rng or np.random.default_rng()
    theta = np.cumsum(rng.normal(0, sigma_drift, T))      # drifting true state, starts ~0
    n_corr = int(round(f * N))
    is_star = arch.startswith('star')
    if adversary == 'targeted':                            # highest-degree node first
        order = ([0] + list(range(1, N))) if is_star else list(range(N))  # star hub = node 0
        corr_idx = np.array(order[:n_corr], dtype=int)
    else:                                                  # random: topology-blind
        corr_idx = rng.choice(N, size=n_corr, replace=False) if n_corr > 0 else np.array([], dtype=int)
    corrupted = np.zeros(N, dtype=bool)
    corrupted[corr_idx] = True

    est = np.zeros(N)                                      # mesh state

    def nbr_mean(v):                                       # ring-lattice neighbour mean
        acc = np.zeros_like(v)
        for s in range(1, k_side + 1):
            acc += np.roll(v, s) + np.roll(v, -s)
        return acc / (2 * k_side)

    errs = np.zeros(T)
    for t in range(T):
        attacking = atk[0] <= t < atk[1]
        senses = theta[t] + rng.normal(0, sigma_sense, N)
        if attacking:
            senses = senses.copy()
            senses[corrupted] = adv_value                  # corrupted nodes: degraded but still reporting
        if is_star:
            if attacking and corrupted[0]:
                broadcast = adv_value                      # hub itself corrupted -> aggregation can't help
            else:
                broadcast = np.median(senses) if arch == 'star_median' else senses.mean()
            actions = np.full(N, broadcast)                # followers adopt the broadcast order
            if attacking:
                actions = actions.copy()
                actions[corrupted] = adv_value             # corrupted units also act adversarially
        else:  # mesh
            new = 0.5 * senses + 0.5 * nbr_mean(est)       # blend own sensing with neighbours
            if attacking:
                new = new.copy()
                new[corrupted] = adv_value
            est = new
            actions = est
        errs[t] = np.mean((actions - theta[t]) ** 2)
    during = float(np.sqrt(errs[atk[0]:atk[1]].mean()))    # RMSE during attack
    after = float(np.sqrt(errs[atk[1]:].mean()))           # RMSE after (recovery)
    return during, after


def sweep(seeds=200):
    fs = [0.0, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50]
    out = {}
    for adversary in ['random', 'targeted']:
        for arch in ['star', 'star_median', 'mesh']:
            key = f"{arch}_{adversary}"
            out[key] = {'f': fs, 'during_rmse': [], 'during_sd': [], 'after_rmse': []}
            for f in fs:
                ds, as_ = [], []
                for s in range(seeds):
                    rng = np.random.default_rng(1000 * int(f * 100) + s)  # reproducible
                    d, a = run_trial(arch, f, adversary, rng=rng)
                    ds.append(d); as_.append(a)
                out[key]['during_rmse'].append(round(float(np.mean(ds)), 3))
                out[key]['during_sd'].append(round(float(np.std(ds)), 3))
                out[key]['after_rmse'].append(round(float(np.mean(as_)), 3))
    return fs, out


if __name__ == '__main__':
    fs, out = sweep(seeds=200)
    json.dump({'config': {'N': 100, 'T': 80, 'attack_window': [30, 60], 'seeds': 200,
                          'sigma_sense': 1.0, 'sigma_drift': 0.2, 'adv_value': 30.0,
                          'mesh': 'ring k=2/side'},
               'results': out},
              open('topology_results.json', 'w'), indent=2)
    print("RMSE DURING ATTACK (lower = better; same units as the target value).\n")
    for adversary in ['random', 'targeted']:
        print(f"--- {adversary.upper()} adversary ---")
        print("  f      star   star_med   mesh")
        for i, f in enumerate(fs):
            s = out[f'star_{adversary}']['during_rmse'][i]
            sm = out[f'star_median_{adversary}']['during_rmse'][i]
            m = out[f'mesh_{adversary}']['during_rmse'][i]
            print(f"  {f:.2f}  {s:6.2f}   {sm:6.2f}   {m:6.2f}")
        print()
