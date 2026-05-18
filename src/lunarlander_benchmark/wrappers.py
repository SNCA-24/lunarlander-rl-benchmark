"""Environment helpers for the lean benchmark surface."""

from __future__ import annotations

import random

import numpy as np

try:
    import torch
except ImportError:  # pragma: no cover - exercised in install validation, not import-time tests
    torch = None

try:
    import gymnasium as gym
except ImportError:  # pragma: no cover - exercised in install validation, not import-time tests
    gym = None

GymWrapperBase = gym.Wrapper if gym is not None else object


def set_global_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    if torch is not None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)


class FuelTrackingWrapper(GymWrapperBase):
    """Track remaining fuel using the same action-cost framing as the notebook."""

    def __init__(self, env):
        super().__init__(env)
        self.initial_fuel = 1000.0
        self.fuel = 0.0
        self.fuel_costs = {0: 0.0, 1: -0.03, 2: -0.3, 3: -0.03}

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        self.fuel += self.fuel_costs[int(action)]
        info["fuel"] = self.initial_fuel + self.fuel
        return obs, reward, terminated, truncated, info

    def reset(self, **kwargs):
        self.fuel = 0.0
        obs, info = self.env.reset(**kwargs)
        info["fuel"] = self.initial_fuel
        return obs, info


def make_env(env_name: str = "LunarLander-v3", *, seed: int | None = None, render_mode: str = "rgb_array"):
    if gym is None:
        raise ImportError("gymnasium is required to create the benchmark environment.")

    env = gym.make(env_name, render_mode=render_mode)
    env = FuelTrackingWrapper(env)
    if seed is not None:
        env.reset(seed=seed)
    return env
