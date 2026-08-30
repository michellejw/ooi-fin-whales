Gitignored. Intermediate products, reconstructible from manifests/ plus code.

What belongs here:
  - Whale-VAD frame-level probabilities (~121 MB/day, ~18 GB per season)
  - spectrogram and feature caches
  - per-note detection tables (one row per detected note)

The dividing line against results/ is granularity:
  one row per NOTE    -> work/     (gitignored, archived to Zenodo when published)
  one row per SEASON  -> results/  (committed)

Per-note tables are only 5-10 MB per season, so git would tolerate them. They
live here anyway, because they are exactly the artifact that belongs in a
citable archive with a DOI rather than in a repository's history forever.
