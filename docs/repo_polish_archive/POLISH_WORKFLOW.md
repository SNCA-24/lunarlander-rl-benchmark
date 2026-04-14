# POLISH_WORKFLOW

## Objective
Polish the repository using a staged workflow instead of jumping directly into refactoring.

## Stage 1 — Audit
Deliver:
- concise diagnosis
- top issues hurting portfolio value
- target folder structure
- prioritized polish plan
- definition of done

Output file:
- repo_polish_audit.md

## Stage 2 — Plan
Deliver:
- files/folders to delete, move, archive, or keep
- final root structure
- README sections to add
- reproducibility fixes
- tests/CI to add
- results/assets to surface
- risks or breaking changes

Output file:
- repo_polish_plan.md

## Stage 3 — Restructure
Tasks:
- clean root
- move academic artifacts into docs/academic_archive/ where appropriate
- create/normalize src/, scripts/, tests/, configs/, assets/
- remove obvious clutter and junk
- minimize risk of breaking working code

Output file:
- repo_polish_progress.md

## Stage 4 — Reproducibility
Goal:
- one supported install path
- one supported run path
- one supported test path

Tasks:
- add/fix requirements.txt or pyproject.toml
- add .env.example if needed
- remove broken local or Colab assumptions
- add scripts/ entry points if needed
- keep improvements minimal but working

Output file:
- repro_check.md

## Stage 5 — README
Rewrite README for:
- recruiter skim
- technical deep dive

Must surface:
- problem
- why it matters
- architecture
- quickstart
- results
- tradeoffs

## Stage 6 — Engineering proof
Add:
- smoke test or small test suite
- basic CI
- config cleanup
- assets/screenshots/results summary if useful

Update:
- repo_polish_progress.md

## Stage 7 — Final review
Deliver:
- what improved
- remaining weaknesses
- repo classification:
  - Pin now
  - Polish more, then pin
  - Keep public but not pinned
  - Low priority
- top remaining improvements
- blunt final verdict

Output file:
- final_portfolio_review.md

## Operating rules
- one repo at a time
- one stage at a time
- prefer minimal working improvements over ambitious rewrites
- do not overstate maturity
- do not optimize for academic grading
- do not assume missing pieces exist
- preserve strongest technical substance