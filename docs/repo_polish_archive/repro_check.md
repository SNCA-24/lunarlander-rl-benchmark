# Reproducibility Check

## What was created or changed

- Added `requirements.txt` with pinned or tightly bounded dependencies for the lean reproducibility path.
- Added `.gitignore` to ignore local validation artifacts and environment clutter.
- Added minimal extracted modules:
  - `src/lunarlander_benchmark/__init__.py`
  - `src/lunarlander_benchmark/agents.py`
  - `src/lunarlander_benchmark/wrappers.py`
  - `src/lunarlander_benchmark/metrics.py`
  - `src/lunarlander_benchmark/plotting.py`
- Added script entry points:
  - `scripts/reproduce_plots.py`
  - `scripts/smoke_run.py`
- Added `configs/smoke.yaml`.

## Exact install command

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Exact plot reproduction command

```bash
.venv/bin/python scripts/reproduce_plots.py --output-dir results/reproduced_plots
```

Validated locally with the current system Python using:

```bash
python3 scripts/reproduce_plots.py --output-dir results/reproduced_plots_validation
```

## Exact smoke run command

```bash
.venv/bin/python scripts/smoke_run.py --config configs/smoke.yaml
```

Optional separate output directory:

```bash
.venv/bin/python scripts/smoke_run.py --config configs/smoke.yaml --output-dir results/smoke_run
```

## What worked

- The primary supported review path is implemented.
- Plot regeneration from the committed benchmark CSVs works.
- Regenerated plots were written to `results/reproduced_plots_validation/`, not into `results/final_benchmark/`.
- The preserved benchmark artifacts under `results/final_benchmark/` were left untouched.
- The smoke script is implemented and writes to a separate output directory by design.
- The smoke script now fails cleanly with an explicit `ImportError` when `gymnasium` is not installed, instead of failing at package import time.

## What remains unsupported

- Full 5-algorithm, 3-seed, 500-episode benchmark reruns are still unsupported as a default reproducibility path.
- The milestone video/GIF/gallery pipeline is still unsupported in the lean reproducibility path.
- No CI or smoke test runner is added yet in this stage.
- README has not been rewritten yet to present the new commands; that remains a later stage task.

## Fallback decisions taken

- The default smoke config uses `Vanilla_DQN` only.
- PPO was intentionally excluded from the default smoke path in Stage 4.
- Reason:
  - it keeps the smoke path small and credible
  - it avoids making the default validation path more brittle before CI is in place
  - it still exercises the extracted environment, agent, metrics, and logging path
- `stable-baselines3` remains pinned in `requirements.txt` so PPO can be reintroduced later if the smoke path proves stable enough.

## Fragile dependencies and caveats

- `gymnasium[box2d]` is the main fragile dependency.
- On this machine, the `.venv` install failed at `box2d-py` build time under Python `3.12.7` on macOS because the build could not find a usable `swig` executable inside the isolated build step.
- `shimmy>=2.0` conflicted with the practical `gymnasium==0.29.1` choice, so it was tightened to `shimmy>=1.3,<2.0`.
- `moviepy` is pinned conservatively because the archived notebook previously showed API-mismatch issues, but it is not part of the supported Stage 4 path.

## Local validation status

- Install:
  - partially validated
  - dependency resolution was fixed
  - full install still blocked locally by the Box2D build issue described above
- Plot reproduction:
  - validated successfully
- Smoke run:
  - implemented
  - not fully validated locally because `gymnasium[box2d]` could not be installed successfully in the isolated environment on this machine

## Conservative interpretation

- Stage 4 is credible for the results-based review path.
- Stage 4 is only partially validated for the smoke path because Box2D installation remains platform-sensitive.
- The smallest honest statement for this repo is:
  - plots can be regenerated from preserved benchmark CSVs
  - a tiny smoke path exists
  - local smoke execution still depends on resolving Box2D installation on the target machine
