Committed. Small enough that every number in a figure or a post can cite a
file in this directory.

What belongs here:
  - per-season frequency/IPI histogram peaks (the Fig 7 equivalent)
  - trend fit coefficients and their uncertainties
  - detector performance summaries against the archived 2017 detections

The rule, against work/:
  one row per NOTE    -> work/     (gitignored)
  one row per SEASON  -> results/  (here)

Enforced by tests/test_repo_hygiene.py, which fails if anything here exceeds
1 MB. If a file trips that limit it is almost certainly per-note data that
belongs in work/.
