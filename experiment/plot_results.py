"""
Regenerate Figure 1 of "The Red Queen's Prison" from topology_results.json.

Run:  python plot_results.py   ->  writes topology_result.png
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C_MEAN = "#b5202a"    # centralized star, mean   (red)
C_MED  = "#e0a020"    # centralized star, median (amber)
C_MESH = "#1f5f8b"    # distributed mesh         (steel blue)


def main(infile="topology_results.json", outfile="topology_result.png"):
    data = json.load(open(infile))
    R = data["results"]
    cfg = data["config"]

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(15, 5.5), sharey=True)
    fig.suptitle(
        "Topology-only resilience: centralized vs distributed coordination under corruption\n"
        f"(N={cfg['N']}, {cfg['seeds']} seeds/point; lower is better; at 0% corruption the star wins)",
        fontsize=13,
    )

    panels = [
        (axL, "random",   "Random adversary (topology-blind)"),
        (axR, "targeted", "Targeted adversary (hits the hub first)"),
    ]
    for ax, adv, title in panels:
        f = R[f"star_{adv}"]["f"]
        ax.plot(f, R[f"star_{adv}"]["during_rmse"], "o-", color=C_MEAN,
                label="Centralized (star, mean)", linewidth=2, markersize=7)
        ax.plot(f, R[f"star_median_{adv}"]["during_rmse"], "s--", color=C_MED,
                label="Centralized (star, median)", linewidth=2, markersize=7)
        ax.plot(f, R[f"mesh_{adv}"]["during_rmse"], "^-", color=C_MESH,
                label="Distributed (mesh)", linewidth=2, markersize=7)
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("fraction of nodes corrupted", fontsize=11)
        ax.grid(True, alpha=0.3)
    axL.set_ylabel("coordination error during attack (RMSE, lower=better)", fontsize=11)
    axL.legend(loc="center right", fontsize=10)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(outfile, dpi=110)
    print(f"wrote {outfile}")


if __name__ == "__main__":
    main()
