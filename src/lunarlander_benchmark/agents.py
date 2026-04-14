"""Minimal agent implementations extracted from the archived notebook."""

from __future__ import annotations

import math
import random
from collections import namedtuple
from typing import Any

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

Transition = namedtuple("Transition", ("state", "action", "reward", "next_state", "done"))

DEFAULT_DQN_CONFIGS: dict[str, dict[str, Any]] = {
    "vanilla": {"lr": 1e-3, "batch_size": 64, "prioritized": False},
    "double": {"lr": 1e-3, "batch_size": 64, "prioritized": False},
    "dueling": {"lr": 1e-3, "batch_size": 64, "prioritized": False},
    "per": {"lr": 1e-3, "batch_size": 64, "prioritized": True, "alpha": 0.6, "beta": 0.4},
}

DEFAULT_PPO_CONFIG: dict[str, Any] = {
    "n_steps": 128,
    "learning_rate": 3e-4,
    "batch_size": 32,
}


class ReplayBuffer:
    def __init__(self, capacity: int, prioritized: bool = False, alpha: float = 0.6, beta: float = 0.4):
        self.capacity = capacity
        self.prioritized = prioritized
        self.alpha = alpha
        self.beta = beta
        self.buffer: list[Transition] = []
        self.priorities: list[float] = []
        self.position = 0

    def push(self, *args: Any) -> None:
        if len(self.buffer) < self.capacity:
            self.buffer.append(Transition(*args))
            self.priorities.append(max(self.priorities, default=1.0))
        else:
            self.buffer[self.position] = Transition(*args)
            self.priorities[self.position] = max(self.priorities, default=1.0)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size: int) -> tuple[list[Transition], np.ndarray | None, torch.Tensor | None]:
        if self.prioritized and len(self.buffer) >= batch_size:
            probs = np.array(self.priorities, dtype=np.float32) ** self.alpha
            probs /= probs.sum()
            indices = np.random.choice(len(self.buffer), batch_size, p=probs)
            weights = (len(self.buffer) * probs[indices]) ** (-self.beta)
            weights /= weights.max()
            samples = [self.buffer[int(i)] for i in indices]
            return samples, indices, torch.tensor(weights, dtype=torch.float32)

        samples = random.sample(self.buffer, batch_size)
        return samples, None, None

    def update_priorities(self, indices: np.ndarray, errors: np.ndarray) -> None:
        for idx, err in zip(indices, errors):
            self.priorities[int(idx)] = abs(float(err)) + 1e-6

    def __len__(self) -> int:
        return len(self.buffer)


class QNetwork(nn.Module):
    def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class DuelingQNetwork(nn.Module):
    def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = 128):
        super().__init__()
        self.value_net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.advantage_net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        value = self.value_net(x)
        advantage = self.advantage_net(x)
        return value + (advantage - advantage.mean(dim=1, keepdim=True))


class DQNAgent:
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        variant: str = "vanilla",
        config: dict[str, Any] | None = None,
        *,
        buffer_size: int = 50_000,
        gamma: float = 0.99,
        target_update_freq: int = 1_000,
        eps_start: float = 1.0,
        eps_end: float = 0.01,
        eps_decay: float = 1e-4,
        device: str = "cpu",
    ):
        self.variant = variant
        self.config = dict(DEFAULT_DQN_CONFIGS[variant])
        if config:
            self.config.update(config)

        self.gamma = gamma
        self.target_update_freq = target_update_freq
        self.eps_start = eps_start
        self.eps_end = eps_end
        self.eps_decay = eps_decay
        self.device = torch.device(device)
        self.action_dim = action_dim
        self.steps_done = 0

        network_cls = DuelingQNetwork if variant == "dueling" else QNetwork
        self.q_net = network_cls(state_dim, action_dim).to(self.device)
        self.target_net = network_cls(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.q_net.state_dict())
        self.target_net.eval()

        self.buffer = ReplayBuffer(
            buffer_size,
            prioritized=self.config.get("prioritized", False),
            alpha=self.config.get("alpha", 0.6),
            beta=self.config.get("beta", 0.4),
        )
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=float(self.config["lr"]))

    def _current_epsilon(self) -> float:
        return self.eps_end + (self.eps_start - self.eps_end) * math.exp(-self.steps_done * self.eps_decay)

    def select_action(self, state: np.ndarray, deterministic: bool = False) -> int:
        if not deterministic and random.random() < self._current_epsilon():
            action = random.randrange(self.action_dim)
        else:
            state_t = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
            with torch.no_grad():
                action = int(self.q_net(state_t).argmax(dim=1).item())

        if not deterministic:
            self.steps_done += 1
        return action

    def store_transition(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        self.buffer.push(state, action, reward, next_state, done)

    def train_step(self) -> float | None:
        batch_size = int(self.config["batch_size"])
        if self.variant == "per":
            self.buffer.beta = min(1.0, 0.4 + (1.0 - 0.4) * (self.steps_done / 500_000))

        if len(self.buffer) < batch_size:
            return None

        transitions, indices, weights = self.buffer.sample(batch_size)
        states, actions, rewards, next_states, dones = zip(*transitions)

        state_tensor = torch.tensor(np.stack(states), dtype=torch.float32, device=self.device)
        action_tensor = torch.tensor(actions, dtype=torch.int64, device=self.device).unsqueeze(-1)
        reward_tensor = torch.tensor(rewards, dtype=torch.float32, device=self.device).unsqueeze(-1)
        next_state_tensor = torch.tensor(np.stack(next_states), dtype=torch.float32, device=self.device)
        done_tensor = torch.tensor(dones, dtype=torch.float32, device=self.device).unsqueeze(-1)

        q_current = self.q_net(state_tensor).gather(1, action_tensor)
        with torch.no_grad():
            if self.variant == "double":
                next_actions = self.q_net(next_state_tensor).argmax(dim=1, keepdim=True)
                q_next = self.target_net(next_state_tensor).gather(1, next_actions)
            else:
                q_next = self.target_net(next_state_tensor).max(1, keepdim=True)[0]
            q_target = reward_tensor + self.gamma * (1 - done_tensor) * q_next

        if self.buffer.prioritized and indices is not None and weights is not None:
            td_errors = (q_current - q_target).detach().squeeze().abs().cpu().numpy()
            self.buffer.update_priorities(indices, td_errors)
            loss = ((q_current - q_target).pow(2) * weights.to(self.device).unsqueeze(1)).mean()
        else:
            loss = F.mse_loss(q_current, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.steps_done % self.target_update_freq == 0:
            self.target_net.load_state_dict(self.q_net.state_dict())

        return float(loss.item())


def create_dqn_agent(env: Any, variant: str = "vanilla", config: dict[str, Any] | None = None) -> DQNAgent:
    state_dim = int(env.observation_space.shape[0])
    action_dim = int(env.action_space.n)
    return DQNAgent(state_dim, action_dim, variant=variant, config=config)


def create_vanilla_dqn_agent(env: Any, config: dict[str, Any] | None = None) -> DQNAgent:
    return create_dqn_agent(env, variant="vanilla", config=config)


def create_double_dqn_agent(env: Any, config: dict[str, Any] | None = None) -> DQNAgent:
    return create_dqn_agent(env, variant="double", config=config)


def create_dueling_dqn_agent(env: Any, config: dict[str, Any] | None = None) -> DQNAgent:
    return create_dqn_agent(env, variant="dueling", config=config)


def create_per_dqn_agent(env: Any, config: dict[str, Any] | None = None) -> DQNAgent:
    return create_dqn_agent(env, variant="per", config=config)


def create_ppo_model(env: Any, config: dict[str, Any] | None = None, *, seed: int = 0) -> Any:
    """Optional helper for later smoke/CI work; not used by the default Stage 4 path."""
    try:
        from stable_baselines3 import PPO
    except ImportError as exc:
        raise ImportError("stable-baselines3 is required to create a PPO model.") from exc

    merged = dict(DEFAULT_PPO_CONFIG)
    if config:
        merged.update(config)

    return PPO(
        "MlpPolicy",
        env,
        verbose=0,
        seed=seed,
        n_steps=int(merged["n_steps"]),
        batch_size=int(merged["batch_size"]),
        learning_rate=float(merged["learning_rate"]),
    )
