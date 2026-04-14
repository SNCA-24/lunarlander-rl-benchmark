"""Metric and CSV helpers for preserved benchmark artifacts."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED_FULL_COLUMNS = [
    "algorithm",
    "seed",
    "episode",
    "reward",
    "steps",
    "time_sec",
    "fuel",
    "sample_efficiency",
    "training_std",
]

REQUIRED_MILESTONE_COLUMNS = [
    "algorithm",
    "seed",
    "episode",
    "mean_reward",
    "success_rate",
    "mean_dist",
    "mean_fuel",
    "sample_efficiency",
    "training_std",
    "eval_variance",
    "time_sec",
    "gpu_bytes",
]


def compute_sample_efficiency(log_df: pd.DataFrame, reward_threshold: float = 200) -> float:
    success_rows = log_df[log_df["reward"] >= reward_threshold]["steps"].cumsum()
    return float(success_rows.iloc[0]) if not success_rows.empty else float("inf")


def compute_training_stability(log_df: pd.DataFrame, window: int = 10) -> float:
    if len(log_df) < window:
        return 0.0
    return float(np.var(log_df["reward"].tail(window)))


def validate_log_file(file_path: str | Path, required_cols: list[str] | None = None) -> pd.DataFrame | None:
    path = Path(file_path)
    if not path.exists():
        return None

    try:
        df = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, FileNotFoundError):
        return None

    expected = required_cols or REQUIRED_FULL_COLUMNS
    if not all(col in df.columns for col in expected):
        return None
    if df.empty:
        return None
    return df


def parse_mean_std_series(series: pd.Series) -> pd.DataFrame:
    parts = series.astype(str).str.split(" ± ", expand=True)
    if parts.shape[1] != 2:
        raise ValueError("Expected milestone values in '<mean> ± <std>' format.")
    return pd.DataFrame({"mean": pd.to_numeric(parts[0], errors="coerce"), "std": pd.to_numeric(parts[1], errors="coerce")})


def load_full_training_csv(results_dir: str | Path) -> pd.DataFrame:
    path = Path(results_dir) / "master_full_training.csv"
    df = validate_log_file(path, REQUIRED_FULL_COLUMNS)
    if df is None:
        raise FileNotFoundError(f"Could not load a valid full training CSV from {path}.")

    numeric_cols = ["episode", "reward", "fuel", "time_sec", "sample_efficiency", "training_std", "steps"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["episode", "reward"]).copy()


def load_milestone_metrics_csv(results_dir: str | Path) -> pd.DataFrame:
    path = Path(results_dir) / "master_milestone_metrics.csv"
    df = validate_log_file(path, REQUIRED_MILESTONE_COLUMNS)
    if df is None:
        raise FileNotFoundError(f"Could not load a valid milestone metrics CSV from {path}.")

    df = df[df["episode"].astype(str) != "episode"].copy().reset_index(drop=True)
    parsed = parse_mean_std_series(df["mean_reward"])
    df["mean_reward"] = parsed["mean"]
    df["std_reward"] = parsed["std"]

    numeric_cols = [
        "episode",
        "mean_reward",
        "std_reward",
        "success_rate",
        "mean_fuel",
        "sample_efficiency",
        "training_std",
        "eval_variance",
        "time_sec",
        "gpu_bytes",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["episode", "mean_reward"]).copy()
