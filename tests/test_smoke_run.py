from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lunarlander_benchmark.metrics import load_full_training_csv, load_milestone_metrics_csv


EXPECTED_PLOTS = {
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
}


def test_preserved_benchmark_csvs_load() -> None:
    results_dir = ROOT / "results" / "final_benchmark"

    full_df = load_full_training_csv(results_dir)
    milestone_df = load_milestone_metrics_csv(results_dir)

    assert not full_df.empty
    assert not milestone_df.empty
    assert set(full_df["algorithm"].unique()) == {
        "Vanilla_DQN",
        "Double_DQN",
        "Dueling_DQN",
        "PER_DQN",
        "PPO",
    }
    assert set(milestone_df["algorithm"].unique()) == {
        "Vanilla_DQN",
        "Double_DQN",
        "Dueling_DQN",
        "PER_DQN",
        "PPO",
    }


def test_plot_reproduction_script_generates_expected_outputs(tmp_path: Path) -> None:
    output_dir = tmp_path / "reproduced_plots"
    mpl_dir = tmp_path / "mplconfig"
    cache_dir = tmp_path / "xdg_cache"
    mpl_dir.mkdir()
    cache_dir.mkdir()

    final_benchmark_plots = ROOT / "results" / "final_benchmark" / "plots"
    before = sorted(path.name for path in final_benchmark_plots.glob("*.png"))

    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    env["MPLCONFIGDIR"] = str(mpl_dir)
    env["XDG_CACHE_HOME"] = str(cache_dir)

    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "reproduce_plots.py"),
            "--output-dir",
            str(output_dir),
        ],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout

    generated = {path.name for path in output_dir.glob("*.png")}
    assert generated == EXPECTED_PLOTS

    after = sorted(path.name for path in final_benchmark_plots.glob("*.png"))
    assert before == after
