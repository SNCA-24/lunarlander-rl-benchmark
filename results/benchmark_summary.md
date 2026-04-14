# Benchmark Summary

This directory contains the preserved final benchmark artifacts from the original LunarLander-v3 comparison across:

- Vanilla DQN
- Double DQN
- Dueling DQN
- PER-DQN
- PPO

The benchmark outputs were reorganized for portfolio presentation without changing the preserved CSV, plot, or video artifacts.

## Contents

- `final_benchmark/master_full_training.csv`
- `final_benchmark/master_milestone_metrics.csv`
- `final_benchmark/trajectories.csv`
- `final_benchmark/angular_velocities.csv`
- `final_benchmark/q_values.csv`
- `final_benchmark/plots/`
- `final_benchmark/videos/`

## Headline takeaways

- The strongest overall results come from the DQN family rather than PPO under the fixed 500-episode budget.
- Double DQN shows the best overall tradeoff on success rate, sample efficiency, and runtime.
- Vanilla DQN finishes with the highest mean reward at episode 500 in the preserved milestone table.
- Dueling DQN remains competitive but less efficient than Double DQN on this benchmark.
- PPO improves, but trails the stronger DQN variants under the same budget.
- PER-DQN is an informative negative result: it preserves fuel but performs poorly and never reaches the same reward regime.

## Preserved final-milestone snapshot

Values below are averaged across seeds at episode 500 from `master_milestone_metrics.csv`.

| Algorithm | Mean reward | Success rate | Mean fuel | Sample efficiency | Mean time (s) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Vanilla_DQN | 238.75 | 0.833 | 969.48 | 274559.67 | 4.39 |
| Double_DQN | 216.85 | 0.867 | 965.03 | 247508.33 | 3.72 |
| Dueling_DQN | 194.81 | 0.667 | 949.49 | 318407.33 | 6.16 |
| PPO | 69.98 | 0.167 | 930.09 | 472093.33 | 9.53 |
| PER_DQN | -162.79 | 0.167 | 983.79 | inf | 0.96 |

## Notes

- This directory is the preserved benchmark artifact set, not a regenerated output folder.
- The primary supported reproducibility path is plot regeneration from the committed CSVs.
- A small smoke path also exists for code-path verification, but it is intentionally limited and more environment-sensitive than plot reproduction.
- Full benchmark reruns are still not the default supported workflow.
