# The Red Queen's Prison — Frame-Lock and Organizational Collapse

![status](https://img.shields.io/badge/status-preprint%2C%20not%20peer--reviewed-orange) ![license](https://img.shields.io/badge/license-CC%20BY%204.0-green)

A speculative, openly-licensed framework for one question: **why do systems that
are optimized for a single mode of coordination collapse when that mode is
compromised — and why does *not knowing* you're compromised make it worse?**

This repository holds the paper, plus the **one experiment we actually ran** and
the code and data to reproduce it. It is built to be checked and broken, not
believed.

> The deepest trap isn't being attacked. It's not knowing your channel is
> compromised — so you trust it *more*, lean on it *harder*, and walk into
> prepared traps believing you're winning. The paper calls that the **False Rung**.

---

## What we actually ran (and what we found)

One claim in the paper is stated as a falsifiable prediction with an experiment:
*centralized (hub-and-spoke) coordination has a single point of failure under
corruption that distributed (mesh) coordination does not.* We tested it with a
deliberately minimal, **deliberately falsifiable** agent model
(`experiment/topology_experiment.py`).

The two arms differ in **one thing only — the communication graph.** No agent is
hand-set to ignore information. The same corruption attack hits both. We swept
corruption from 0–50% over 200 random seeds per point, under a *random* adversary
(topology-blind) and a *targeted* one (corrupts the most-connected node first).

![Figure 1](experiment/topology_result.png)

**Result (coordination error during attack — lower is better):**

| Condition | Centralized (mean) | Centralized (median) | Distributed (mesh) |
|---|---|---|---|
| **No corruption (control)** | **0.10** | 0.12 | 0.53 |
| Targeted, 10% corrupted | 29.98 | 29.98 | **9.59** |
| Random, 30% corrupted | 22.93 | 21.94 | **17.55** |

Three things to read off it:

1. **The control passes.** With *no* corruption, the centralized arm wins —
   pooling everyone's reports cancels noise. A model that favored distribution
   even here would be rigged. This one isn't.
2. **Then it crosses over.** Once corruption appears, distribution wins, and how
   sharply depends on the adversary. Against a *targeted* adversary the centralized
   arm collapses to chance-level error the instant the hub is hit; the mesh
   degrades gracefully (~3× lower error at 10%).
3. **A smarter aggregator doesn't save the center.** Giving the hub a *robust
   (median)* rule changes nothing under the targeted attack — because when the
   corrupted node **is** the hub, the aggregator is the source of the lie.

This is the paper's §10 trade-off, *earned* as a measured crossover rather than
asserted.

### What this result is NOT

- It is a statement **about this model**, not about crabs, armies, or companies.
- It tests the **topological** sub-claim only (a single aggregating node is a
  single point of failure). It does **not** establish the broader mission-command
  thesis — there is no intent-verification or agency here; the mesh is a stand-in
  for distributed decision-making.
- The targeted-star collapse is partly **true by construction** (corrupt the hub
  and the star must fail). The non-trivial findings are the clean-conditions
  crossover, the random-vs-targeted gap, and the median-can't-save-the-center result.
- **One parameter set.** A sweep over agent count, connectivity, noise, drift, and
  attack magnitude is open work (see *Open questions*).

There are **no** "5–10×" or "70–90% effectiveness" numbers here. Earlier drafts
circulated those; they were never measured and have been withdrawn from the paper.

---

## Reproduce it

```bash
pip install -r requirements.txt
cd experiment

# rerun the full sweep (≈ under a minute); writes topology_results.json
python topology_experiment.py

# regenerate Figure 1 from the data
python plot_results.py
```

`topology_results.json` in this repo is the output of the 200-seed run reported
above. Change the parameters at the top of `run_trial(...)` and tell us what
breaks.

---

## Repository contents

```
.
├── README.md                     ← you are here
├── LICENSE                       ← CC BY 4.0
├── requirements.txt
├── papers/
│   └── The_Red_Queens_Prison_v4.pdf
│       (companions, separately deposited on Zenodo:
│        Turtles, or Crystals      — DOI 10.5281/zenodo.20484438
│        Turtles, All the Way Up   — DOI 10.5281/zenodo.20486047)
└── experiment/
    ├── topology_experiment.py    ← the model (runs, documented, not rigged)
    ├── plot_results.py           ← regenerates Figure 1 from the data
    ├── topology_results.json     ← output of the 200-seed run
    └── topology_result.png       ← Figure 1 in the paper
```

That's the whole package. If a file isn't listed here, it isn't part of this work.

---

## The six domains — test *templates*, not results

The centralized-vs-distributed axis can be mapped onto many fields. **None of
these mappings have been tested.** They are starting points for *you* to set up a
test in your domain by adapting `topology_experiment.py` — not findings, and not
claims that the paper makes.

| Domain | "Hub" (centralized) | "Mesh" (distributed) | What you'd test |
|---|---|---|---|
| Military C2 | orders specify position/time/route | mission command (specify *intent*) | error/effectiveness under jamming + spoofing |
| Corporate | all decisions via one executive | departments act on shared goals | continuity when the center is removed |
| Software | single API gateway / monolith | service mesh | request success when a node is compromised |
| Supply chain | single-source supplier | diversified regional sourcing | output when a key node fails |
| Infrastructure | central grid hub | islanding microgrids | nodes online after a hub failure |
| Ecology *(contested)* | single coordination channel | multiple channels | robustness to channel disruption |

A direct note on the ecology row: the paper **deliberately makes no biological
claims** (an earlier draft's crab/orca examples were cut — see the paper's change
log — because the biology is contested and better explained by kin selection than
by communication). If you work in this area, the genuinely open question is
whether multi-channel species are more robust to channel disruption. We do not
assert that they are.

---

## Open questions (where we'd love help)

- **Parameter sweep.** Does the crossover survive changes in agent count, mesh
  connectivity, sensing noise, target drift, and attack magnitude? Where does it
  break?
- **Layer compounding.** The paper claims the five "layers" compound; that
  interaction is asserted, not modeled. Build a model where it's explicit.
- **Corruption vs. destruction.** The paper argues a degraded-but-trusted node is
  worse than a dead one. The current experiment tests corruption; add a clean
  destruction comparison.
- **Your domain.** Adapt the experiment using the templates above and report what
  you find — including a null result. A "no difference" is a real result.

To contribute: fork, change one thing, document it, and open a pull request with
your code, data, and what it showed (even if it contradicts the paper).

---

## Papers (trilogy on substrate-independent life)

1. *Turtles, or Crystals* — Zenodo DOI [10.5281/zenodo.20484438](https://doi.org/10.5281/zenodo.20484438)
2. *Turtles, All the Way Up* — Zenodo DOI [10.5281/zenodo.20486047](https://doi.org/10.5281/zenodo.20486047)
3. *The Red Queen's Prison* (this repository) — Zenodo DOI [10.5281/zenodo.20500531](https://doi.org/10.5281/zenodo.20500531)

---

## How to cite

> Schulz, M. (2026). *The Red Queen's Prison: Frame-Lock and the Architecture of
> Organizational Collapse in Evolutionary Warfare.* Working Draft v4. Zenodo.
> DOI 10.5281/zenodo.20500531. CC BY 4.0.

---

## License

Everything here — paper, code, data — is released under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Share, adapt, and use
freely with attribution.

**Contact:** mattschulz97@protonmail.com · ORCID 0009-0000-0956-5743

*Built to be broken. If you break it, tell us how.*
