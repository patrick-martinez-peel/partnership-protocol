# The Partnership Protocol

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

**A Game-Theoretic Simulation of AI Governance & Liability**

This repository contains the source code, simulation data, and reproducibility materials for the white paper:
**"The Partnership Protocol: Mitigating Agency Costs in AI Governance"**
*By Patrick Martinez Peel, Ph.D.*

### 📄 [Read the Full White Paper (PDF)](./The_Partnership_Protocol_Whitepaper.pdf)

---

## Overview
Governing autonomous agents at scale presents a "monitoring cost crisis." As agent populations grow, the cost of centralized human oversight becomes prohibitive.

This project uses **Evolutionary Game Theory** to simulate a **Cyber-Defense Swarm** scenario, testing how different liability structures affect safety outcomes. The simulation compares two governance models:

1.  **Limited Liability (LLC):** Agents face capped penalties for failure.
2.  **Joint Liability (Partnership):** Agents face existential penalties for group failure ("slashing").

## Key Findings: The Efficiency Gap
The simulation demonstrates that liability structures drastically alter the monitoring requirements for safety.

* **Limited Liability** requires **~60% audit probability** to suppress the "Lazy Patcher" strategy.
* **Joint Liability** achieves the same safety equilibrium with only **~20% audit probability**.

![Efficiency Gap Simulation Result](./efficiency_gap.png)
*Figure 1: Comparison of safe behavior adoption under different audit intensities.*

---

## Repository Structure
* `simulation.py`: The core evolutionary game engine. Handles agent strategies, pairwise interactions, and population updates.
* `The_Partnership_Protocol_Whitepaper.pdf`: The complete research paper explaining the mechanism design and theoretical framework.
* `requirements.txt`: List of necessary Python dependencies.

## Reproducibility
This codebase is designed to be deterministic and reproducible. Running the script will:
1.  Initialize a population of 1,000 agents.
2.  Run evolutionary cycles across 20 distinct audit probability intervals.
3.  Generate the primary figure reporting the "Efficiency Gap."

## How to Run

### Prerequisites
- Python 3.8+
- Numpy
- Matplotlib

### Installation
```bash
git clone https://github.com/patrick-martinez-peel/partnership-protocol.git
cd partnership-protocol
pip install -r requirements.txt

```

### Execution

```bash
python simulation.py

```

## Cite This Work

If you use this simulation or build on the Partnership Protocol framework, please cite the white paper:

> Peel, Patrick Martinez. "The Partnership Protocol: Mitigating Agency Costs in AI Governance." (2025).

## License

Released under the MIT License. See `LICENSE` for details.

---

*Created by Patrick Martinez Peel, Ph.D. - December 2025*

```

```
