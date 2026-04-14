# REPO_STANDARD

## Goal
Every serious repository should feel:
- engineered
- reproducible
- quickly understandable
- results-backed
- recruiter-friendly
- technically credible

## Required top-level files/folders
Every serious repo should ideally have:
- README.md
- LICENSE
- .gitignore
- requirements.txt or pyproject.toml
- .env.example if needed
- src/
- scripts/
- tests/
- configs/ if needed
- assets/
- results/ or reports/
- .github/workflows/

## Preferred top-level structure
repo/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt or pyproject.toml
├── .env.example
├── src/
├── scripts/
├── tests/
├── configs/
├── assets/
├── results/ or reports/
└── .github/workflows/

## README standard
Every repo README should include:
1. Project title and one-line summary
2. Why this project matters
3. Key features
4. Architecture / workflow
5. Tech stack
6. Quickstart
7. Results / metrics / outputs
8. Repo structure
9. Tradeoffs / limitations
10. Future improvements

## Two-layer README rule
### Layer 1 — recruiter skim
Top section must answer quickly:
- what problem this solves
- what stack is used
- what result is achieved
- what architecture/workflow looks like
- how to run it

### Layer 2 — technical deep dive
Lower section should include:
- methodology
- design choices
- evaluation
- failure cases
- tradeoffs
- limitations

## Pin-worthy quality bar
A repo should be pinned only if it has:
- strong README
- clean repo root
- reproducible setup
- one supported run path
- tests or smoke tests
- basic CI
- visible results/assets
- minimal repo hygiene issues
- clear story in under 60 seconds

## Things to avoid
- committed .env files
- committed secrets
- giant raw datasets in git
- caches and local OS/editor junk
- course reports in repo root
- placeholder README text
- notebook-only main flow
- hardcoded localhost or local machine paths unless configurable
- broken imports / sys.path hacks in the supported path

## Academic repo rule
For rescued academic repos:
- keep raw course/submission material under docs/academic_archive/
- keep repo root focused on the portfolio story
- supported path should feel professional, not submission-oriented

## Notebook repo rule
If a repo started in notebooks:
- notebooks may remain
- supported path should move toward src/ + scripts/
- notebook should become supporting material, not the main entry path