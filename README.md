# LunarLander-v3 RL Benchmark: DQN Variants vs PPO

Benchmark and evaluation artifact comparing Vanilla DQN, Double DQN, Dueling DQN, PER-DQN, and PPO on Gymnasium `LunarLander-v3`. The repository preserves the final benchmark outputs and supports plot reproduction from committed CSV artifacts, with a small smoke path for code-path verification.

## Why This Repo Matters

This repo is strongest as an MLE portfolio artifact because it shows:

- custom RL implementation work rather than notebook-only library usage
- comparative benchmarking across multiple algorithms under a fixed budget
- multi-seed evaluation with milestone checkpoints instead of a single final score
- metrics beyond reward alone, including success rate, sample efficiency, fuel efficiency, and training stability
- reproducibility thinking focused on preserved artifacts, truthful run paths, and clear tradeoff analysis

## Benchmark Scope

- Environment: Gymnasium `LunarLander-v3`
- Algorithms:
  - Vanilla DQN
  - Double DQN
  - Dueling DQN
  - PER-DQN
  - PPO
- Training design:
  - 3 seeds
  - 500 training episodes per algorithm
  - milestone evaluations at episodes 100, 200, 300, 400, and 500
- Metrics tracked:
  - mean reward
  - success rate
  - landing precision / distance-to-pad
  - fuel efficiency
  - sample efficiency
  - training stability
  - evaluation variance
  - compute time

## Methods At A Glance

The benchmark compares value-based and policy-gradient methods under the same environment and a fixed training budget. The DQN family uses a shared implementation base with variant-specific changes for Double DQN, Dueling DQN, and prioritized replay. PPO is included as the policy-gradient baseline. Results are preserved as CSVs, plots, and milestone videos so the repo can be reviewed as a benchmark artifact even when the full benchmark is not rerun.

## Key Findings

Under the fixed 500-episode budget, Double DQN is the strongest overall tradeoff winner. Vanilla DQN reaches the highest preserved final mean reward in one summary view, but Double DQN combines better success rate, sample efficiency, runtime, and variance, which makes it the stronger overall benchmark conclusion.

| Algorithm | Outcome Summary | Strength | Limitation / Tradeoff |
| --- | --- | --- | --- |
| Double DQN | Best overall tradeoff under the fixed budget | Highest success rate, strong sample efficiency, lower runtime than the stronger alternatives | Does not have the single highest preserved final mean reward |
| Vanilla DQN | Competitive top-tier result | Highest preserved final mean reward at episode 500 | Slightly weaker overall tradeoff than Double DQN on efficiency and variance |
| Dueling DQN | Competitive but not dominant | Strong value-based baseline with solid final performance | Less efficient than Double DQN and slower in the preserved results |
| PPO | Improves, but trails the best DQN variants here | Useful policy-gradient baseline and important comparison point | Lower reward and efficiency under this training budget |
| PER-DQN | Important negative result | Preserves fuel and tests prioritized replay in the same setup | Performs poorly and never reaches the same reward regime as the stronger baselines |

More detail is summarized in [benchmark_summary.md](results/benchmark_summary.md) and [findings.md](docs/findings.md).

## Supported Paths

### Primary Review Path

The main supported path for this repo is reviewing the preserved benchmark and regenerating plots from the committed CSV artifacts.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/reproduce_plots.py --output-dir results/reproduced_plots
```

What this path does:

- installs the documented environment
- reads the committed CSV artifacts in `results/final_benchmark/`
- regenerates the plot set into a separate output directory
- avoids overwriting the preserved final benchmark artifacts by default

### Secondary Engineering Path

A tiny smoke run exists for code-path verification only:

```bash
.venv/bin/python scripts/smoke_run.py --config configs/smoke.yaml
```

What this path is and is not:

- it is a small sanity check for the extracted environment / agent / metrics path
- it is intentionally much smaller than the full benchmark
- it does not reproduce the final benchmark results
- it is more environment-sensitive than the plot reproduction path

### Archived Implementation Path

The original notebook workflow is preserved as supporting material:

- [lunarlander_v5_archive.ipynb](notebooks/lunarlander_v5_archive.ipynb)

This notebook is useful as a historical implementation reference, but it is not the primary supported path for reviewing the repo.

## Repository Structure

```text
repo/
├── README.md
├── requirements.txt
├── src/lunarlander_benchmark/
├── scripts/
├── configs/
├── results/
│   ├── benchmark_summary.md
│   └── final_benchmark/
├── docs/
│   ├── findings.md
│   └── academic_archive/
└── notebooks/
```

## Results And Artifacts

- [final_benchmark](results/final_benchmark/)
  - preserved benchmark CSVs, plots, and milestone videos from the original run
- [benchmark_summary.md](results/benchmark_summary.md)
  - compact artifact-level summary and final milestone snapshot
- [findings.md](docs/findings.md)
  - benchmark interpretation and tradeoff framing
- [lunarlander_v5_archive.ipynb](notebooks/lunarlander_v5_archive.ipynb)
  - archived notebook containing the original full workflow

## Tradeoffs And Limitations

- The strongest part of this repo is the preserved benchmark evidence, not a polished full-rerun framework.
- Full 5-algorithm, 3-seed, 500-episode reruns are not the default supported path yet.
- The primary supported reproducibility path is plot regeneration from committed CSV artifacts.
- The smoke path is intentionally tiny and should be read as a code-path check, not as a benchmark-quality check.
- `gymnasium[box2d]` / Box2D setup can be platform-sensitive.
  - If you want the least-friction local path, prefer Python `3.11`.
  - In local validation for this repo, Python `3.12` on macOS was the most brittle case.
- The media pipeline is preserved in the archive/results, but video and GIF generation are not part of the primary supported workflow.

## Academic Archive

Course-era reports and slides are preserved in:

- [academic_archive](docs/academic_archive/)

They are retained as background material, not as the main story of the repository.
