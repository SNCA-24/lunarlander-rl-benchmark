#!/usr/bin/env python3
"""Run a tiny smoke path for the extracted benchmark code."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lunarlander_benchmark.agents import DQNAgent
from lunarlander_benchmark.metrics import compute_sample_efficiency
from lunarlander_benchmark.wrappers import make_env, set_global_seed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(ROOT / "configs" / "smoke.yaml"))
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional override for the smoke output directory.",
    )
    return parser.parse_args()


def load_config(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def run_vanilla_dqn_smoke(config: dict, output_dir: Path) -> tuple[Path, Path]:
    seed = int(config["seed"])
    episodes = int(config["episodes"])
    max_steps = int(config["train_max_steps"])
    eval_episodes = int(config["eval_episodes"])
    dqn_config = dict(config.get("dqn", {}))
    buffer_size = int(dqn_config.pop("buffer_size", 512))
    gamma = float(dqn_config.pop("gamma", 0.99))
    target_update_freq = int(dqn_config.pop("target_update_freq", 32))
    eps_start = float(dqn_config.pop("eps_start", 0.5))
    eps_end = float(dqn_config.pop("eps_end", 0.05))
    eps_decay = float(dqn_config.pop("eps_decay", 0.001))

    set_global_seed(seed)
    env = make_env(config["environment"], seed=seed, render_mode="rgb_array")
    agent = DQNAgent(
        env.observation_space.shape[0],
        env.action_space.n,
        variant="vanilla",
        config=dqn_config,
        buffer_size=buffer_size,
        gamma=gamma,
        target_update_freq=target_update_freq,
        eps_start=eps_start,
        eps_end=eps_end,
        eps_decay=eps_decay,
    )

    rows: list[dict] = []
    rewards_seen: list[float] = []
    for episode in range(1, episodes + 1):
        state, _ = env.reset(seed=seed + episode)
        start = time.time()
        total_reward = 0.0
        last_info = {"fuel": 0.0}
        steps = 0

        for step in range(1, max_steps + 1):
            action = agent.select_action(state)
            next_state, reward, terminated, truncated, info = env.step(action)
            done = bool(terminated or truncated)
            agent.store_transition(state, action, float(reward), next_state, done)
            agent.train_step()
            state = next_state
            total_reward += float(reward)
            last_info = info
            steps = step
            if done:
                break

        rewards_seen.append(total_reward)
        log_df = pd.DataFrame(
            {
                "reward": rewards_seen,
                "steps": [row["steps"] for row in rows] + [steps],
            }
        )
        rows.append(
            {
                "algorithm": "Vanilla_DQN",
                "seed": seed,
                "episode": episode,
                "reward": total_reward,
                "steps": steps,
                "time_sec": time.time() - start,
                "fuel": float(last_info.get("fuel", 0.0)),
                "sample_efficiency": compute_sample_efficiency(log_df),
                "training_std": float(pd.Series(rewards_seen[-10:]).std(ddof=0)),
            }
        )

    eval_rewards: list[float] = []
    eval_fuels: list[float] = []
    for eval_idx in range(eval_episodes):
        state, info = env.reset(seed=seed + 100 + eval_idx)
        episode_reward = 0.0
        fuel = float(info.get("fuel", 0.0))
        for _ in range(max_steps):
            action = agent.select_action(state, deterministic=True)
            state, reward, terminated, truncated, info = env.step(action)
            episode_reward += float(reward)
            fuel = float(info.get("fuel", fuel))
            if terminated or truncated:
                break
        eval_rewards.append(episode_reward)
        eval_fuels.append(fuel)

    env.close()

    training_csv = output_dir / "master_full_training.csv"
    pd.DataFrame(rows).to_csv(training_csv, index=False)

    summary_json = output_dir / "smoke_summary.json"
    summary_json.write_text(
        json.dumps(
            {
                "algorithm": "Vanilla_DQN",
                "seed": seed,
                "episodes": episodes,
                "eval_episodes": eval_episodes,
                "mean_eval_reward": float(pd.Series(eval_rewards).mean()),
                "mean_eval_fuel": float(pd.Series(eval_fuels).mean()),
                "output_csv": str(training_csv),
            },
            indent=2,
        )
    )
    return training_csv, summary_json


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    algorithms = config.get("algorithms", ["Vanilla_DQN"])
    if algorithms != ["Vanilla_DQN"]:
        raise ValueError("Stage 4 smoke path supports only ['Vanilla_DQN'] for stability.")

    output_dir = Path(args.output_dir or config.get("output_dir", ROOT / "results" / "smoke_run"))
    output_dir = output_dir if output_dir.is_absolute() else ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    training_csv, summary_json = run_vanilla_dqn_smoke(config, output_dir)
    print(f"Smoke training CSV: {training_csv}")
    print(f"Smoke summary JSON: {summary_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
