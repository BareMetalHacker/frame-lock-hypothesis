# Frame-Lock Hypothesis: Testable Framework for Organizational Resilience

[![Status](https://img.shields.io/badge/Status-Publication%20Ready-brightgreen)](https://zenodo.org)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![Code](https://img.shields.io/badge/Language-Python-blue)]()

## What This Is

A testable, extensible framework explaining why centralized systems collapse under stress while distributed systems survive.

**Core Insight:** Systems become frame-locked—trapped in a particular mode, unaware of their vulnerability, actively walking into disasters while believing they're winning.

## Quick Start

### Read First
- **Papers:** See `/papers` folder for the complete trilogy
- **Framework:** See `docs/README_CROSS_DOMAIN.md` for 6 domains with examples
- **Research:** See `docs/RESEARCH_ROADMAP.md` for 47 experiments to try

### Run the Simulator
```bash
pip install -r requirements.txt
python3 experiments/experiments_baseline.py
```

## Key Results

Intent-based distributed systems are **5-10x more resilient** than command-following centralized systems under:
- Signal jamming
- Information corruption
- Cascading failures
- Trusted agent sabotage
- Multi-vector attacks

## Files & Folders

- **papers/** - 3-paper trilogy on substrate-independent life
- **simulator/** - Event-driven agent-based model
- **experiments/** - Baseline + adversary test suite (10 attacks)
- **docs/** - Documentation, guides, research roadmap
- **LICENSE** - CC BY 4.0 (share, modify, use freely with attribution)

## How to Use This

**For Understanding:**
Start with `docs/README_CROSS_DOMAIN.md` and pick your domain (military, corporate, supply chain, software, biology, infrastructure).

**For Running:**
See `experiments/EXPERIMENTS_GUIDE.md`

**For Extending:**
See `docs/EXTENSION_GUIDE.md` - add new attacks, test new domains

**For Contributing:**
See `docs/CONTRIBUTION_TEMPLATE.md`

## Cross-Domain Applications

This framework applies to:
- 🎖️ **Military Operations** (Auftragstaktik vs. centralized command)
- 🏢 **Corporate Organizations** (flat vs. hierarchical under crisis)
- 📦 **Supply Chains** (diversified vs. centralized sourcing)
- 💻 **Software Architecture** (microservices vs. monolithic)
- 🌿 **Biological Systems** (multi-modal vs. single-substrate communication)
- ⚡ **Infrastructure** (distributed microgrids vs. centralized power)

## Publications

Coming soon:
- Zenodo DOIs (permanent archive)
- arXiv preprint
- GitHub (you're here!)

## Cite This Work

```bibtex
@software{schulz2026framelock,
  author = {Schulz, Matthew},
  title = {Frame-Lock Hypothesis: Simulator and Experimental Framework},
  year = {2026},
  url = {https://github.com/BareMetalHacker/frame-lock-hypothesis},
  orcid = {0009-0000-0956-5743}
}
```

## Open Science

✅ **Reproducible:** All code + data included
✅ **Extensible:** Designed for community modifications
✅ **Transparent:** Known limitations documented
✅ **Testable:** Research roadmap invites validation

## License

CC BY 4.0 - Share, modify, use freely with attribution

## Questions?

Open an issue! I'm here to help.

---

**Ready to test this framework? Start with `docs/README_CROSS_DOMAIN.md`.**
