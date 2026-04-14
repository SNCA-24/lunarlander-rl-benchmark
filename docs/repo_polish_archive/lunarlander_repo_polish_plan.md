# Stage 2 implementation goal

- Use [lunarlander_repo_polish_audit.md](/Users/chaitu/Downloads/LunarLander_v3_Benchmarking_DQN_vs_PPO-main/lunarlander_repo_polish_audit.md) as the Stage 1 source of truth.
- Convert the repository from a course-project-shaped notebook repo into a lean benchmark repo that is easy to scan, honest about what is reproducible, and strong enough to support MLE applications.
- Keep the benchmark identity narrow:
  - preserve existing benchmark outputs
  - preserve the algorithm lineup
  - preserve the metric framing
  - avoid building a reusable RL framework
- Define one truthful supported review path:
  - install dependencies
  - reproduce plots from committed benchmark CSVs
  - optionally run a tiny smoke run that exercises the extracted code path
- Explicit non-goal:
  - do not promise that a fresh clone will rerun the full 5-algorithm, 3-seed, 500-episode benchmark as the primary supported workflow

# Files and folders to keep

- Keep `README.md` as the root README file name, but rewrite its contents completely.
- Keep the benchmark result contents unchanged during migration:
  - `master_full_training.csv`
  - `master_milestone_metrics.csv`
  - `trajectories.csv`
  - `angular_velocities.csv`
  - `q_values.csv`
  - all committed `.png` plots
  - all committed `.mp4` milestone videos
- Keep the current academic artifacts unchanged in content, but archive them out of the root:
  - `Final_Report.pdf`
  - `LunarLander_V3 - Final Project Summary.pdf`
  - `CSCE 5218 - DL Project Presentation - Group 4 .pptx`
- Keep the notebook content as a historical artifact rather than rewriting it in place.
- Keep the existing benchmark findings and wording direction from the report/slides:
  - Double DQN as the strongest overall tradeoff
  - Dueling DQN and Vanilla DQN as competitive
  - PPO underperforming the best DQN variants under the fixed budget
  - PER-DQN as an important negative result
- Keep the existing file names for result artifacts where possible to avoid needless churn in scripts, docs, and references.

# Files and folders to archive

- Move `Final_Report.pdf` to `docs/academic_archive/Final_Report.pdf`.
- Move `LunarLander_V3 - Final Project Summary.pdf` to `docs/academic_archive/LunarLander_V3 - Final Project Summary.pdf`.
- Move `CSCE 5218 - DL Project Presentation - Group 4 .pptx` to `docs/academic_archive/CSCE 5218 - DL Project Presentation - Group 4 .pptx`.
- Move the current notebook to `notebooks/lunarlander_v5_archive.ipynb` as supporting material, not as the primary supported entry point.
- Do not put the notebook under `docs/academic_archive/`; it is still useful as a technical appendix and implementation record.
- Do not surface the archived academic files in the main README beyond a short “Academic archive” reference.

# Files and folders to move or rename

- Rename `DQN_vs_PPO_Group_4_CSCE_5218_DL_PROJECT/` to `results/final_benchmark/`.
- Inside `results/final_benchmark/`, normalize the layout:
  - move `*.png` files into `results/final_benchmark/plots/`
  - keep `videos/` as `results/final_benchmark/videos/`
  - keep the CSV benchmark outputs at the `results/final_benchmark/` root
- Rename `LunarLander_v5.ipynb` to `notebooks/lunarlander_v5_archive.ipynb`.
- Delete root `.DS_Store`.
- Delete `DQN_vs_PPO_Group_4_CSCE_5218_DL_PROJECT/.DS_Store`.
- Do not rename the CSV files unless a script or doc becomes clearer by doing so; current names are already specific enough.
- Do not rename the MP4 files; the algorithm/milestone/seed naming is useful and already descriptive.
- Keep `README.md` in the root.
- Keep the audit and workflow files untouched during implementation unless they start cluttering the public repo story; they are working docs, not benchmark artifacts.

# Minimum extraction plan

- Extract only the code needed for:
  - a credible `src/` surface
  - plot reproduction from committed results
  - a tiny smoke run
- Do not extract the full notebook one-to-one.
- Source notebook cells to extract:
  - replay buffer, networks, DQN agent, and algorithm factories from the current agent cells
  - fuel wrapper and environment factory from the current environment cell
  - metric helpers from the current utilities cell
  - plotting logic from the current post-training plotting cell
- `src/lunarlander_benchmark/agents.py`
  - `ReplayBuffer`
  - `QNetwork`
  - `DuelingQNetwork`
  - `DQNAgent`
  - minimal agent factory functions for:
    - Vanilla DQN
    - Double DQN
    - Dueling DQN
    - PER-DQN
  - minimal PPO wrapper/factory only if needed by the smoke path
  - do not add a generalized trainer class
- `src/lunarlander_benchmark/wrappers.py`
  - `FuelTrackingWrapper`
  - one `make_env(...)` helper for LunarLander-v3
  - optional seed helper if needed by smoke and tests
- `src/lunarlander_benchmark/metrics.py`
  - `compute_sample_efficiency`
  - `compute_training_stability`
  - small helpers for reading/validating committed CSVs
  - small helper for parsing `"mean ± std"` milestone values
- `src/lunarlander_benchmark/plotting.py`
  - functions that read the committed CSV outputs and regenerate the existing plot set
  - plotting code only for the plots that already exist in `results/final_benchmark/plots/`
  - do not include GIF generation, HTML video gallery generation, or notebook-only composite displays
- `scripts/reproduce_plots.py`
  - thin CLI wrapper over `plotting.py`
  - primary supported review path for the repo
  - input: committed CSVs under `results/final_benchmark/`
  - output: regenerated plots in a caller-specified output directory
- `scripts/smoke_run.py`
  - intentionally tiny orchestration script
  - exercises extracted modules with a very small run budget
  - no video recording
  - no GIF generation
  - no full multi-seed benchmark logic
  - no attempt to reproduce final benchmark numbers
- Partial extraction boundary:
  - leave `train_and_snapshot()` in the notebook/archive
  - do not port the full milestone recording pipeline unless smoke work makes that unavoidable

# What stays in the notebook/archive

- The full benchmark orchestration loop across all 5 algorithms, 3 seeds, and 500 episodes.
- The milestone video generation path.
- The MP4-to-GIF conversion code.
- The HTML 5x5 gallery code.
- The trajectory / angular velocity / Q-value export pipeline from trained models.
- Any notebook-only exploratory cells and presentation-oriented cells.
- The exact executed outputs already embedded in the notebook.
- The Colab-specific install cell as historical context only.
- The stale in-notebook documentation block may remain in the archived notebook, but it should not be treated as a supported source of truth after the README/docs rewrite.
- The archived notebook should be referenced as:
  - implementation appendix
  - historical record of the original benchmark workflow
  - not the recommended first run path

# New files to create

- `LICENSE`
- `.gitignore`
- `requirements.txt`
- `src/lunarlander_benchmark/__init__.py`
- `src/lunarlander_benchmark/agents.py`
- `src/lunarlander_benchmark/wrappers.py`
- `src/lunarlander_benchmark/metrics.py`
- `src/lunarlander_benchmark/plotting.py`
- `scripts/smoke_run.py`
- `scripts/reproduce_plots.py`
- `configs/smoke.yaml`
- `tests/test_smoke_run.py`
- `results/benchmark_summary.md`
- `docs/methodology.md`
- `docs/metrics.md`
- `docs/findings.md`
- `.github/workflows/smoke.yml`

# README plan

- Replace the current course-project README with a benchmark-first README.
- Required top section for recruiter skim:
  - project title
  - one-line benchmark summary
  - why this benchmark matters
  - algorithm lineup
  - one short “headline findings” table
  - one supported review command
- Add these sections:
  - `Overview`
  - `Why This Repo Matters`
  - `Benchmark Scope`
  - `Methods At A Glance`
  - `Key Findings`
  - `Metrics`
  - `Supported Paths`
  - `Repository Structure`
  - `Results And Artifacts`
  - `Tradeoffs And Limitations`
  - `Academic Archive`
- `Key Findings` should include a compact table with columns like:
  - algorithm
  - relative outcome
  - success-rate / reward takeaway
  - tradeoff note
- `Supported Paths` should explicitly distinguish:
  - `python scripts/reproduce_plots.py ...` as the primary review path
  - `python scripts/smoke_run.py --config configs/smoke.yaml` as the engineering smoke path
  - archived notebook as supporting material only
- `Results And Artifacts` should point to:
  - `results/final_benchmark/`
  - `results/benchmark_summary.md`
  - `docs/findings.md`
- `Tradeoffs And Limitations` should state:
  - results are preserved from the original benchmark run
  - the full benchmark rerun is not the default supported path yet
  - only a smoke run is supported as code-path verification
- Do not keep:
  - “Open in Colab” as the lead action
  - references to nonexistent files
  - wrong repo names
  - claims about folders that do not exist

# Reproducibility plan

- Add `requirements.txt` with tested package versions or tightly bounded versions.
- Pin the fragile libraries that already showed mismatch risk:
  - `moviepy`
  - `stable-baselines3`
  - `gymnasium[box2d]`
  - `shimmy`
  - `pygame`
  - `torch`
  - `matplotlib`
  - `pandas`
  - `numpy`
- Make one truthful install path:
  - `pip install -r requirements.txt`
- Make one truthful review path:
  - reproduce plots from the committed final CSVs
- Make one truthful engineering verification path:
  - run the smoke config
- Reproducibility should focus on:
  - being able to inspect and regenerate plots from the preserved results
  - being able to run a tiny sanity-check benchmark path
  - not promising full benchmark regeneration by default
- `scripts/reproduce_plots.py` should default to writing into a separate output directory so it does not overwrite preserved final artifacts unless explicitly requested.
- `scripts/smoke_run.py` should write into a temporary or dedicated smoke output directory, not into `results/final_benchmark/`.
- Do not make the GIF/video pipeline part of the supported reproducibility path.
- Do not make Colab the documented default path.
- If `src/` imports become awkward under `requirements.txt` only, use the smallest possible solution needed for this repo. Do not introduce a larger packaging setup unless import reliability becomes a blocker.

# Smoke test and CI plan

- Smoke path scope:
  - purpose: prove that the extracted code works end-to-end on a tiny budget
  - not intended to validate benchmark quality
- `configs/smoke.yaml` should define:
  - environment: `LunarLander-v3`
  - algorithms: `Vanilla_DQN` and `PPO`
  - seeds: `[0]`
  - episodes: very small, such as `2` or `3`
  - train max steps: small
  - eval episodes: `1` or `2`
  - video recording: `false`
  - output dir: temporary smoke directory
- Why `Vanilla_DQN` and `PPO`:
  - covers the custom DQN path
  - covers the SB3 PPO path
  - keeps runtime much smaller than testing all five algorithms
- `tests/test_smoke_run.py` should verify:
  - smoke script completes successfully
  - output CSVs are created
  - output CSVs contain expected core columns
  - at least one plot can be generated from the smoke outputs or from a tiny synthetic fixture
- `.github/workflows/smoke.yml` should run:
  - checkout
  - Python setup
  - dependency install
  - plot reproduction command
  - pytest smoke test
- Minimum CI success bar:
  - imports work
  - committed benchmark CSVs can regenerate plots
  - smoke script runs on a tiny config
- CI should not:
  - rerun the full benchmark
  - generate videos or GIFs
  - compare output rewards to the preserved final benchmark

# Risks and breaking changes

- Moving the results folder will break existing README and notebook path references until docs are updated.
- Moving the notebook will break the current Colab badge path unless it is removed or replaced.
- The plotting code depends on the current CSV schema, including the `"mean ± std"` string format in milestone metrics.
- `moviepy` already showed API mismatch in the notebook; if the supported path touches it at all, version pinning is mandatory.
- `gymnasium[box2d]` and `pygame` can be CI-fragile, especially on GitHub Actions.
- PPO in the smoke path may be slower or more brittle than the DQN path; if CI stability becomes poor, reduce smoke budget further before expanding architecture.
- Extracted code may drift from the archived notebook behavior because the full benchmark will not be rerun immediately.
- Results must not be overwritten accidentally during plot reproduction or smoke runs.
- The archived notebook will still contain old paths and historical assumptions unless it is explicitly scrubbed, so README/docs must clearly mark it as archival.

# Deferred work to avoid over-refactoring

- Do not build a generalized RL experiment framework.
- Do not add a full trainer module hierarchy unless the lean scripts become unmaintainable.
- Do not add a sweep manager, Hydra, Ray Tune, MLflow, or Weights & Biases integration.
- Do not add Docker unless dependency installation proves unmanageable without it.
- Do not add model-serving or inference APIs.
- Do not add a dashboard or interactive frontend.
- Do not port the notebook’s video/GIF/gallery pipeline into the supported path.
- Do not rerun the full final benchmark just to “clean up” the codebase.
- Do not broaden the benchmark scope beyond:
  - Vanilla DQN
  - Double DQN
  - Dueling DQN
  - PER-DQN
  - PPO
- Do not over-split the code into many files just to look more engineered.
- Do not rewrite the benchmark into a library-first design.

# Final implementation order

1. Create the target folders and housekeeping files:
   - `src/`
   - `scripts/`
   - `configs/`
   - `tests/`
   - `results/`
   - `notebooks/`
   - `docs/`
   - `.github/workflows/`
   - `LICENSE`
   - `.gitignore`
   - `requirements.txt`

2. Clean the root:
   - delete `.DS_Store`
   - move academic files into `docs/academic_archive/`
   - move notebook into `notebooks/lunarlander_v5_archive.ipynb`

3. Move and normalize benchmark artifacts:
   - rename `DQN_vs_PPO_Group_4_CSCE_5218_DL_PROJECT/` to `results/final_benchmark/`
   - move plot PNGs into `results/final_benchmark/plots/`
   - keep videos under `results/final_benchmark/videos/`
   - keep benchmark CSVs at `results/final_benchmark/`

4. Extract the minimum shared code into `src/lunarlander_benchmark/`.

5. Create `scripts/reproduce_plots.py` and make it work against the preserved benchmark CSVs first.

6. Create `results/benchmark_summary.md`, `docs/methodology.md`, `docs/metrics.md`, and `docs/findings.md` from the preserved results and report evidence.

7. Create `configs/smoke.yaml` and `scripts/smoke_run.py`.

8. Create `tests/test_smoke_run.py`.

9. Rewrite `README.md` around:
   - benchmark scope
   - headline findings
   - results location
   - supported review path
   - smoke verification path

10. Add `.github/workflows/smoke.yml`.

11. Run final checks:
   - plot reproduction works
   - smoke path works
   - README paths match real files
   - root no longer looks course-project-shaped

12. Stop after the lean benchmark repo is credible; do not continue into broader framework work unless a real blocker remains.
