# LunarLander-v3 Benchmarking: DQN Family vs PPO

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SNCA-24/LunarLander_v3_Benchmarking_DQN_vs_PPO/blob/main/LunarLander_v5.ipynb)

A comprehensive benchmarking study comparing four Deep Q-Network (DQN) variants against Proximal Policy Optimization (PPO) on the OpenAI Gymnasium `LunarLander-v3` environment. The project was developed as part of **CSCE 5218 – Deep Learning (Group 4)**.

---

## 📁 Repository Structure

| File / Folder | Description |
|---|---|
| `LunarLander_v5.ipynb` | Main Jupyter notebook — contains all code, training logic, plots, and a 5×5 milestone video/GIF gallery. |
| `LunarLander_V3 - Final Project Summary.pdf` | Written project summary report. |
| `CSCE 5218 - DL Project Presentation - Group 4 .pptx` | Presentation slides for the course. |
| `DQN_vs_PPO_Group_4_CSCE_5218_DL_PROJECT.zip` | Archive of the full project submission. |
| `logs/` *(generated at runtime)* | Per-episode CSV logs: `master_full_training.csv` and `master_milestone_metrics.csv`. |
| `videos/` *(generated at runtime)* | MP4 clips recorded at milestone episodes, organized by algorithm and seed. |
| `plots/` *(generated at runtime)* | PNG charts: learning curves, milestone metrics, trajectory overlays, compute cost. |

---

## 🎯 Project Overview

### Environment

**LunarLander-v3** (Gymnasium `box2d`) is a continuous control task where a rocket-powered lander must safely touch down on a landing pad.

| Property | Value |
|---|---|
| Observation space | 8-dimensional continuous vector (x, y, vx, vy, angle, angular velocity, leg contact left, leg contact right) |
| Action space | 4 discrete actions: do nothing, fire left thruster, fire main engine, fire right thruster |
| Success threshold | Episode reward ≥ 200 |
| Max steps per episode (training) | 1,000 |
| Max steps per episode (evaluation) | 500 |

A custom `FuelTrackingWrapper` is applied to track remaining fuel per episode. Fuel is deducted each time a thruster action is selected: main engine −0.3 per action step, side thrusters (left/right) −0.03 per action step, no-op 0.0.

### Algorithms

| Algorithm | Description |
|---|---|
| **Vanilla DQN** | Standard Deep Q-Network with a fixed replay buffer and periodic target-network updates. |
| **Double DQN** | Decouples action selection (online network) from value estimation (target network) to reduce overestimation bias. |
| **Dueling DQN** | Separates the Q-network into value and advantage streams, improving learning in states where action choice matters less. |
| **PER-DQN** | Adds Prioritized Experience Replay — samples transitions proportionally to TD-error magnitude, focusing training on high-information transitions. |
| **PPO** | Proximal Policy Optimization from Stable-Baselines3; an on-policy actor-critic method with clipped surrogate objective. |

---

## ⚙️ Hyperparameters

### Shared (DQN variants)

| Parameter | Value |
|---|---|
| Training episodes | 500 |
| Seeds | 0, 1, 2 |
| Milestone checkpoints | 100, 200, 300, 400, 500 episodes |
| Batch size | 64 |
| Replay buffer size | 50,000 |
| Discount factor (γ) | 0.99 |
| ε-greedy start / end / decay | 1.0 / 0.01 / 1e-4 |
| Target network update frequency | Every 1,000 steps |
| Learning rate (DQN variants) | 1e-3 |
| Hidden layer size | 128 neurons (2 hidden layers) |

### DQN Variant-Specific

| Algorithm | Prioritized Replay | PER α | PER β (initial→final) |
|---|---|---|---|
| Vanilla DQN | No | — | — |
| Double DQN | No | — | — |
| Dueling DQN | No | — | — |
| PER-DQN | **Yes** | 0.6 | 0.4 → 1.0 (annealed over 500,000 steps) |

### PPO (Stable-Baselines3)

| Parameter | Value |
|---|---|
| Learning rate | 3e-4 |
| n_steps | 1,000 |
| Batch size | 50 |

---

## 🏗️ Code Architecture

The notebook (`LunarLander_v5.ipynb`) is organized into the following sections:

| Cell | Name | Description |
|---|---|---|
| Cell 0 | Package installation | Installs Box2D, Stable-Baselines3, Gymnasium, Pygame, MoviePy. |
| Cell 1 | Imports | Loads all Python libraries (NumPy, PyTorch, Gymnasium, Matplotlib, etc.). |
| Cell 2 | Configuration & Hyperparameters | Defines `ENV_NAME`, `SEEDS`, `EPISODES`, `MILESTONES`, all training hyperparameters, and output directory paths (`logs/`, `videos/`, `plots/`). |
| Cell 3 | Replay Buffer | `ReplayBuffer` class supporting both uniform and prioritized (PER) sampling. Uses `namedtuple` `Transition` for storage. |
| Cell 4 | Q-Networks | `QNetwork` (standard MLP) and `DuelingQNetwork` (value + advantage streams) as PyTorch `nn.Module` subclasses. |
| Cell 5 | DQN Agent | `DQNAgent` base class — handles network selection, ε-greedy action selection, transition storage, TD-error optimization, and periodic target-network sync. |
| Cells 6–9 | Algorithm Factories | `make_vanilla_dqn_agent`, `make_double_dqn_agent`, `make_dueling_dqn_agent`, `make_per_dqn_agent` — thin wrappers that instantiate `DQNAgent` with the appropriate variant config. |
| Cell 10 | PPO Factory | `make_ppo_agent` — wraps the environment in a `DummyVecEnv` + `Monitor`, instantiates and returns an SB3 `PPO` model. |
| Cell 11 | Environment Wrapper & Factory | `FuelTrackingWrapper` (gym.Wrapper) and `make_env()` — builds the LunarLander-v3 environment with fuel tracking and optional video recording. |
| Cell 12 | Evaluation Utility | `evaluate()` — runs N evaluation episodes for any agent (DQN or PPO), collecting reward, success rate, distance-to-pad, and fuel metrics. Supports optional video recording. |
| Cell 13 | Training & Milestone Logging | `train_and_snapshot()` — the core training loop; trains each agent across all seeds, appends per-episode rows to `master_full_training.csv`, records milestone evaluations to `master_milestone_metrics.csv`, and saves video clips. |
| Cell 14 | GPU Timer | `GPUTimer` context-manager class — tracks CUDA memory usage and wall-clock runtime per training run. |
| Cell 15 | Orchestrator | Sequentially trains all five agents (Vanilla DQN → Double DQN → Dueling DQN → PER-DQN → PPO), prints GPU summaries, and stores agents for post-training visualization. |
| Cell 16 | Trajectory & Q-Value Export | Rolls out one episode per agent and saves position trajectories, angular velocities, and Q-value sequences to CSV files for overlay plots. |
| Cell 17 | Utility Functions | `compute_sample_efficiency()`, `compute_training_stability()`, `validate_log_file()` — shared helpers for metric calculation and log validation. |
| Cell 18 | Post-Training Plots | Reads the master CSV logs and generates all result charts (learning curves, milestone metrics, distribution overlays, compute-cost bar) as PNGs saved to `plots/`. |
| Cell 18b | MP4 → GIF Conversion | Converts each milestone MP4 (seed 0) to a lightweight GIF for GitHub-friendly inline display using MoviePy. |
| Cell 19 | 5×5 Milestone Gallery | Builds an HTML table (rows = milestones 100–500, columns = algorithms) embedding GIFs where available, base-64 MP4s for small clips, or external video tags otherwise. Displayed inline via `IPython.display.HTML`. |

---

## 🔧 Setup & Installation

### Prerequisites

- Python ≥ 3.9
- CUDA-capable GPU (optional; CPU training is supported but slower)

### Install Dependencies

```bash
pip install gymnasium[box2d]
pip install stable-baselines3
pip install "shimmy>=2.0"
pip install pygame
pip install moviepy
pip install torch matplotlib pandas
```

Or run the first notebook cell which installs all required packages automatically (recommended for Google Colab).

---

## ▶️ Quick Start

### Option 1 — Google Colab (Recommended)

1. Click the **Open in Colab** badge at the top of this README.
2. Select **Runtime → Run all** (estimated runtime: ~15 minutes on a free GPU).
3. Scroll to the relevant sections:
   - **Training logs** — per-episode reward and fuel metrics
   - **Result grids** — learning curves, milestone plots, overlays, compute cost
   - **5×5 Milestone Gallery** — visual comparison of agent behavior at each checkpoint

### Option 2 — Local Jupyter

```bash
git clone https://github.com/SNCA-24/LunarLander_v3_Benchmarking_DQN_vs_PPO.git
cd LunarLander_v3_Benchmarking_DQN_vs_PPO
pip install gymnasium[box2d] stable-baselines3 "shimmy>=2.0" pygame moviepy torch matplotlib pandas
jupyter notebook LunarLander_v5.ipynb
```

Then run all cells in order from the top.

---

## 📊 Evaluation Metrics

Each algorithm is evaluated at every milestone (every 100 episodes) across three seeds (0, 1, 2) using 10 evaluation episodes per checkpoint.

| Metric | Definition |
|---|---|
| **Mean reward** | Average total episode reward (mean ± std across evaluation episodes) |
| **Success rate** | Fraction of evaluation episodes where reward ≥ 200 |
| **Sample efficiency** | Cumulative environment steps at the first episode achieving reward ≥ 200 |
| **Training stability** | Variance of rewards over the last 10 training episodes |
| **Evaluation variance** | Variance of rewards across the 10 evaluation episodes at each milestone |
| **Fuel efficiency** | Mean remaining fuel at episode end (higher = more fuel-efficient) |
| **Compute cost** | Mean wall-clock seconds per training run; GPU peak memory (if CUDA available) |

---

## 📂 Output Artifacts

After running the notebook, the following directories are created:

```
logs/
├── master_full_training.csv        # Per-episode: algorithm, seed, episode, reward, steps, time_sec, fuel, sample_efficiency (running), training_std
├── master_milestone_metrics.csv    # Per-milestone: algorithm, seed, episode, mean_reward, success_rate, mean_dist, mean_fuel, ...
├── Vanilla_DQN/seed0/              # Per-seed monitor logs (DQN)
├── Double_DQN/seed0/
├── Dueling_DQN/seed0/
├── PER_DQN/seed0/
└── PPO/seed0/                      # Monitor CSV from SB3 Monitor wrapper

videos/
└── timeline_comparisons/
    ├── milestone_100_eps/seed0/    # MP4 clips and GIFs for milestone 100, seed 0
    ├── milestone_200_eps/seed0/
    ├── milestone_300_eps/seed0/
    ├── milestone_400_eps/seed0/
    └── milestone_500_eps/seed0/

plots/
├── learning_curve_by_algo.png
├── reward_vs_time_by_algo.png
├── reward_vs_fuel_by_algo.png
├── milestones_reward_errorbar.png
├── milestones_success_rate.png
├── milestones_sample_efficiency_log.png
├── trajectory_overlay.png
├── angular_velocity_overlay.png
├── q_value_overlay.png
└── compute_cost.png
```

---

## ❓ FAQ

**Why don't MP4s autoplay on GitHub?**
GitHub's renderer blocks inline `<video>` tags for security reasons. The notebook automatically generates lightweight GIF previews that render everywhere. Open the notebook in Google Colab or [nbviewer](https://nbviewer.org/) for full video playback.

**How do I change the number of training episodes or milestones?**
Edit `EPISODES` and `MILESTONES` in Cell 2 (Configuration & Hyperparameters) and re-run the notebook from Cell 13 onwards.

**How do I add a new algorithm?**
1. Implement an agent factory function (see Cells 6–10 for examples).
2. Add an entry to the `agents` list in Cell 15 (Orchestrator).
3. Re-run Cells 15 onwards.

**Can I run on CPU only?**
Yes. The code automatically detects whether CUDA is available and falls back to CPU. Training will be slower but fully functional.

**How are seeds used?**
Seeds 0, 1, 2 are used for both environment resets and agent initialization to ensure reproducible results across runs. The `set_global_seed()` function seeds Python's `random`, NumPy, and PyTorch at the start of each seed iteration.

---

## 📚 References

- [Gymnasium LunarLander-v3 Documentation](https://gymnasium.farama.org/environments/box2d/lunar_lander/)
- [Stable-Baselines3 Documentation](https://stable-baselines3.readthedocs.io/)
- Mnih et al. (2015) — *Human-level control through deep reinforcement learning*. Nature, 518, 529–533. (DQN)
- van Hasselt et al. (2016) — *Deep Reinforcement Learning with Double Q-learning*. AAAI 2016. (Double DQN)
- Wang et al. (2016) — *Dueling Network Architectures for Deep Reinforcement Learning*. ICML 2016. (Dueling DQN)
- Schaul et al. (2016) — *Prioritized Experience Replay*. ICLR 2016. (PER-DQN)
- Schulman et al. (2017) — *Proximal Policy Optimization Algorithms*. arXiv:1707.06347. (PPO)

---

© 2025 Group 4, CSCE 5218 — Deep Learning. MIT License.
