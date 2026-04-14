"""Reproduce committed benchmark plots from preserved CSV outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .metrics import load_full_training_csv, load_milestone_metrics_csv

PALETTE = {
    "Vanilla_DQN": "#1f77b4",
    "Double_DQN": "#ff7f0e",
    "Dueling_DQN": "#2ca02c",
    "PER_DQN": "#d62728",
    "PPO": "#9467bd",
}

PLOT_FILENAMES = [
    "learning_curve_by_algo.png",
    "reward_vs_fuel_by_algo.png",
    "reward_vs_time_by_algo.png",
    "milestones_reward_errorbar.png",
    "milestones_success_rate.png",
    "milestones_sample_efficiency_log.png",
    "trajectory_overlay.png",
    "trajectory_grid.png",
    "angular_velocity_overlay.png",
    "angular_velocity_grid.png",
    "q_value_overlay.png",
    "q_value_grid.png",
    "compute_cost.png",
]


def _prepare_output_dir(output_dir: str | Path, *, allow_overwrite: bool) -> Path:
    path = Path(output_dir)
    if path.exists() and any(path.iterdir()) and not allow_overwrite:
        raise FileExistsError(f"Output directory {path} already exists and is not empty. Use --allow-overwrite to reuse it.")
    path.mkdir(parents=True, exist_ok=True)
    return path


def _save(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def generate_all_plots(results_dir: str | Path, output_dir: str | Path, *, allow_overwrite: bool = False) -> list[Path]:
    results_dir = Path(results_dir)
    output_dir = _prepare_output_dir(output_dir, allow_overwrite=allow_overwrite)

    full_df = load_full_training_csv(results_dir)
    milestone_df = load_milestone_metrics_csv(results_dir)
    trajectory_df = pd.read_csv(results_dir / "trajectories.csv")
    angular_df = pd.read_csv(results_dir / "angular_velocities.csv")
    q_df = pd.read_csv(results_dir / "q_values.csv")

    generated: list[Path] = []

    plt.figure(figsize=(10, 6))
    for algo, group in full_df.groupby("algorithm"):
        group.groupby("episode")["reward"].mean().plot(color=PALETTE[algo], label=algo)
    plt.title("Mean Reward vs Episode")
    plt.xlabel("Episode")
    plt.ylabel("Mean Reward")
    plt.legend()
    path = output_dir / "learning_curve_by_algo.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(8, 6))
    for algo, group in full_df.groupby("algorithm"):
        plt.scatter(group.reward, group.fuel, s=10, alpha=0.6, color=PALETTE[algo], label=algo)
    plt.title("Reward vs Remaining Fuel")
    plt.xlabel("Reward")
    plt.ylabel("Fuel")
    plt.legend()
    path = output_dir / "reward_vs_fuel_by_algo.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(8, 6))
    for algo, group in full_df.groupby("algorithm"):
        plt.scatter(group.reward, group.time_sec, s=10, alpha=0.6, color=PALETTE[algo], label=algo)
    plt.title("Reward vs Time per Episode")
    plt.xlabel("Reward")
    plt.ylabel("Time (s)")
    plt.legend()
    path = output_dir / "reward_vs_time_by_algo.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(10, 6))
    for algo, group in milestone_df.groupby("algorithm"):
        plt.errorbar(group.episode, group.mean_reward, yerr=group.std_reward, marker="o", capsize=3, color=PALETTE[algo], label=algo)
    plt.title("Mean Reward ± Std by Milestone")
    plt.xlabel("Episode")
    plt.ylabel("Mean Reward")
    plt.legend()
    path = output_dir / "milestones_reward_errorbar.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(10, 6))
    for algo, group in milestone_df.groupby("algorithm"):
        plt.plot(group.episode, group.success_rate, marker="o", linestyle="-", color=PALETTE[algo], label=algo)
    plt.title("Success Rate by Milestone")
    plt.xlabel("Episode")
    plt.ylabel("Success Rate")
    plt.legend()
    path = output_dir / "milestones_success_rate.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(10, 6))
    for algo, group in milestone_df.groupby("algorithm"):
        plt.plot(group.episode, group.sample_efficiency, marker="o", linestyle="-", color=PALETTE[algo], label=algo)
    plt.yscale("log")
    plt.title("Sample Efficiency by Milestone (log scale)")
    plt.xlabel("Episode")
    plt.ylabel("Steps to ≥200 (log)")
    plt.legend()
    path = output_dir / "milestones_sample_efficiency_log.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(6, 6))
    for algo, group in trajectory_df.groupby("algorithm"):
        plt.plot(group.x, group.y, label=algo, color=PALETTE[algo], alpha=0.8)
    plt.title("Descent Trajectories Overlay")
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.legend()
    plt.grid(True)
    path = output_dir / "trajectory_overlay.png"
    _save(path)
    generated.append(path)

    fig, axes = plt.subplots(1, len(PALETTE), figsize=(4 * len(PALETTE), 4), sharex=True, sharey=True)
    for ax, (algo, group) in zip(axes, trajectory_df.groupby("algorithm")):
        ax.plot(group.x, group.y, color=PALETTE[algo])
        ax.set_title(algo)
        ax.set_xlabel("X")
        ax.grid(True)
    axes[0].set_ylabel("Y")
    fig.suptitle("Individual Descent Trajectories")
    path = output_dir / "trajectory_grid.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(8, 6))
    for algo, group in angular_df.groupby("algorithm"):
        plt.hist(group.angular_velocity, bins=50, density=True, alpha=0.5, label=algo, color=PALETTE[algo])
    plt.title("Angular Velocity Distribution Overlay")
    plt.xlabel("Angular Velocity")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    path = output_dir / "angular_velocity_overlay.png"
    _save(path)
    generated.append(path)

    fig, axes = plt.subplots(1, len(PALETTE), figsize=(4 * len(PALETTE), 4), sharex=True, sharey=True)
    for ax, (algo, group) in zip(axes, angular_df.groupby("algorithm")):
        ax.hist(group.angular_velocity, bins=50, density=True, color=PALETTE[algo])
        ax.set_title(algo)
        ax.set_xlabel("Angular Velocity")
        ax.grid(True)
    axes[0].set_ylabel("Density")
    fig.suptitle("Angular Velocity by Algorithm")
    path = output_dir / "angular_velocity_grid.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(8, 6))
    for algo, group in q_df.groupby("algorithm"):
        if algo == "PPO":
            continue
        plt.hist(group.q_value, bins=50, density=True, alpha=0.5, label=algo, color=PALETTE[algo])
    plt.title("Q-Value Distribution Overlay")
    plt.xlabel("Q value")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    path = output_dir / "q_value_overlay.png"
    _save(path)
    generated.append(path)

    dqn_algorithms = [algo for algo in PALETTE if algo != "PPO"]
    fig, axes = plt.subplots(1, len(dqn_algorithms), figsize=(4 * len(dqn_algorithms), 4), sharex=True, sharey=True)
    for ax, algo in zip(axes, dqn_algorithms):
        group = q_df[q_df.algorithm == algo]
        ax.hist(group.q_value, bins=50, density=True, color=PALETTE[algo])
        ax.set_title(algo)
        ax.set_xlabel("Q value")
        ax.grid(True)
    axes[0].set_ylabel("Density")
    fig.suptitle("Q-Value by DQN Algorithm")
    path = output_dir / "q_value_grid.png"
    _save(path)
    generated.append(path)

    plt.figure(figsize=(6, 5))
    cost = milestone_df.groupby("algorithm")["time_sec"].mean()
    cost.plot(kind="bar", color=[PALETTE[algo] for algo in cost.index])
    plt.title("Compute Time")
    plt.ylabel("Seconds")
    path = output_dir / "compute_cost.png"
    _save(path)
    generated.append(path)

    return generated
