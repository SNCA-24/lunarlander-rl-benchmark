# PORTFOLIO_CONTEXT

## Candidate profile
- Final semester MS in AI student
- Target hiring order: MLE first, DE second, DS third
- Applying for full-time roles
- Portfolio goal: appear engineering-first, reproducible, recruiter-friendly, and technically credible
- Main GitHub objective: show end-to-end ownership, architecture clarity, evaluation rigor, and practical relevance

## Portfolio positioning
This GitHub should communicate:
- Applied AI/ML engineer with strong data foundations
- Can build end-to-end ML systems, data pipelines, search/ranking workflows, and modern AI systems
- Stronger portfolio emphasis on MLE and DE than notebook-heavy DS work

## Repo polishing goal
This repository is being polished as a GitHub portfolio artifact, not as an academic submission.
The goal is to:
- remove academic / course-submission feel
- improve engineering clarity
- improve reproducibility
- surface the strongest technical signals quickly
- make the repo understandable to both recruiter skim and technical deep dive

## Repo-specific context
- Repo name: LunarLander_v3_Benchmarking_DQN_vs_PPO
- One-line repo purpose: Benchmark DQN variants and PPO on Gymnasium LunarLander-v3 using multi-seed training, milestone evaluations, custom metrics, and comparative analysis.
- Why this repo matters for hiring: This repo can strengthen the MLE side of the portfolio by showing custom reinforcement learning implementation, benchmarking discipline, experiment design, reproducibility thinking, and evaluation under multiple performance criteria rather than just final reward.
- Current state: Strong academic/research artifact but weak GitHub artifact. Most execution is concentrated in a large notebook, the repo is still course-project-shaped, reproducibility is weak, and the current structure does not make the engineering and evaluation quality easy to see quickly.
- Target end state: A research-grade benchmark repository with clean repo structure, extracted experiment modules/scripts, one reproducible run path, clear metric definitions, visible result artifacts, and a recruiter-friendly README that highlights the experimental design, benchmark results, tradeoffs, and lessons learned.
- Likely role relevance: Strongest for MLE, moderate for DS, weak for DE. Good as a supporting repo for experimentation rigor and evaluation discipline, but not as a primary systems/data-engineering showcase.

## Repo identity
This repository should be polished as a benchmark/evaluation artifact, not as a product repository.
The main hiring value should come from:
- experiment design
- algorithm comparison
- reproducibility
- metric clarity
- tradeoff analysis
- clean technical storytelling

## What to preserve
- Preserve the core benchmarking scope: Vanilla DQN, Double DQN, Dueling DQN, PER-DQN, and PPO on LunarLander-v3
- Preserve the multi-seed training setup, milestone evaluations, and custom metrics such as reward, success rate, landing precision, fuel efficiency, sample efficiency, and training stability
- Preserve key result artifacts: plots, milestone outputs, CSV logs, videos, and the academic report
- Preserve the strongest final findings, especially the comparative insights around Double-DQN, Dueling-DQN, PPO, and PER-DQN
- Preserve useful academic reports, but move them out of the repo root if needed

## What to avoid
- Do not try to force this repo into a product/app framing
- Do not pretend this is a deployment-serving project
- Do not keep the notebook as the only supported execution path
- Do not over-polish visuals while leaving reproducibility broken
- Do not keep course-submission clutter in the repo root
- Do not invent fake engineering complexity that was never part of the project

## Pin-worthiness intent
- This repo is not expected to become one of the first pinned repos immediately
- The realistic target is: strong supporting portfolio repo that may become pin-worthy later if the benchmark framework, reproducibility, README, and results presentation become clean enough

## Final decision target
At the end of polishing, the ideal classification for this repo is:
- Keep public but not pinned, OR
- Polish more, then pin later if the benchmark framework becomes clean and credible enough

