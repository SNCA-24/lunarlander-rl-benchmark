# Findings

## Benchmark readout

The preserved LunarLander-v3 benchmark shows that the value-based methods outperform PPO within the fixed 500-episode training budget used in this project.

- Double DQN is the strongest overall tradeoff candidate.
- Vanilla DQN finishes with the highest final mean reward in the preserved milestone table.
- Dueling DQN is competitive but not the best efficiency/performance tradeoff.
- PPO improves gradually but underperforms the stronger DQN variants under the same budget.
- PER-DQN is the clearest failure case and should be kept visible as a negative result.

## Why Double DQN still matters most

Although Vanilla DQN ends with the highest preserved mean reward at episode 500, Double DQN remains the best overall benchmark story because it combines:

- the highest success rate in the preserved final milestone table
- better sample efficiency than Vanilla and Dueling DQN
- faster runtime than the stronger alternatives
- lower evaluation variance than Vanilla DQN

That makes Double DQN the most credible “best tradeoff” conclusion for portfolio storytelling.

## Repo-level implication

This repository is worth polishing because the benchmark itself is already substantive. The main repo problem was presentation:

- course artifacts were dominating the root
- the notebook was the main visible workflow
- results were hidden inside a course-named folder

After restructuring, the intended repo story is clearer:

- archived academic materials are separated from the main benchmark story
- preserved results are grouped under `results/final_benchmark/`
- the notebook is now supporting material rather than the main entry point

## Caution

- These findings are preserved from the original benchmark artifacts.
- Plot reproduction from the committed benchmark CSVs is the primary supported review path.
- A small smoke path exists for code-path verification, but it is intentionally limited and can be platform-sensitive.
- Full benchmark reruns are still not the default supported workflow.
