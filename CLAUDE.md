# Working notes for this repository

Read `README.md` first: it covers the science, the four-stage design, the data,
and the validation approach. This file only carries what a contributor needs
that the README does not say.

## Where the reasoning lives

`notes/` carries the decision record and the evidence behind it. It is in the
repository rather than a private notebook, because a rationale nobody can read
is not a rationale.

- `notes/index.md` decisions table, each row with its rationale
- `notes/probes/` one file per question answered, with the evidence
- `notes/literature/2017-paper-data-section.md` what the 2017 paper actually
  used and reported, extracted from the full text
- `notes/literature/detector-landscape.md` the detector survey behind choosing
  Whale-VAD

## Things that will waste your time if rediscovered

- The metric is **IPI** (inter-pulse interval), not INI. The paper reserves
  "inter-note interval" for the sum of the two doublet IPIs, which carries no
  fitted trend.
- **"Peak frequency" is an amplitude-weighted centroid** over +/-0.5 s and
  15-35 Hz, defined by an equation in the paper's Methods. It is not an argmax
  peak pick. Pick spectral peaks and the numbers will not be comparable.
- **The archived frequency distribution is bimodal, and the taller mode is the
  wrong note.** On KEMF 2011-2012 the modes sit near 19.1 and 22.9 Hz, the
  higher one carrying roughly twice the counts, so a global argmax returns
  23.05 Hz against a published ~18.3 Hz. The A note is the lower mode. Select
  the mode, do not take the maximum. This is a separate error from the centroid
  one above and survives getting that one right.
- **Do not correct the instrument response** in the reproduction leg. The 2017
  study did not (`p.resp = 1`, a no-op), so its published centroids are of the
  uncorrected spectrum. Matching it means deliberately not doing the more
  correct thing. KEMF's response is flat to 0.20 dB across the band anyway.
- **Perch does not work here.** Its mel frontend starts at 60 Hz and the call is
  at 20 Hz. Settled with evidence in `probes/03-perch-at-20hz.md`. Do not revisit.
- The FDSN client name `IRIS` is deprecated in obspy; use `EARTHSCOPE`. The same
  rename 307-redirects on the web service, so `curl` needs `-L`.
- Whale-VAD's released checkpoint emits **7 classes**, not the 3 its README and
  `_class_mapping` describe. The label order is undocumented; resolve it by
  correlating against the archived ground-truth detections.

## Conventions

- `uv` for everything. Never pip or conda.
- Marimo notebooks are the pipeline. Code moves to `src/` once used twice.
- Storage tiers by row granularity: one row per note goes to `work/`
  (gitignored), one row per season to `results/` (committed). Enforced by
  `tests/test_repo_hygiene.py`.
- Conventional commits. `Assisted-by: <harness>:<model>` for AI assistance,
  never `Co-Authored-By`. See `AI_POLICY.md`.
- Project conventions follow the Scientific Python Development Guide. What was
  adopted and what was declined is recorded in `README.md`.

## Verification

Checks here have twice passed while being structurally unable to fail:
`git check-ignore` cannot report a tracked file as ignored without `--no-index`,
and `pre-commit run --all-files` does not see untracked files. Both looked green.

When adding a guard, break the condition it guards and confirm the test fails.
A guard that has never failed is unverified.
