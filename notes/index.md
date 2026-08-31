# OOI Fin Whale Call Detection

Project name: `ooi-fin-whales`. Renamed 2026-08-29 from `fin-whale-perch`,
which predated Perch being demoted to an optional spike.

Extending the 2003-2013 fin whale time series (Weirathmueller et al. 2017,
PLoS ONE 12(10) e0186127) into the OOI era using an automated detector.
Measuring inter-pulse interval (IPI) and peak frequency of the 20 Hz call.

Started 2026-08-29. Supersedes the Feb 2026 planning in `archive-2026-02/`.

## Status

Station, detector and validation design are settled. The pipeline itself is
not built. Next is the `fetch` stage and its manifest writer.

## The question

Between 2003 and 2013 peak frequency fell about 0.17 Hz/year and IPI rose
about 0.54 s/year, with the song shifting from singlet to doublet. OOI has
recorded continuously since 2015. Did the trends continue?

If they did, the thirteen years from the paper's end in 2013 to now imply
roughly 2.2 Hz of further frequency decline and 7.0 s of further IPI increase.
(Recomputed 2026-08-30 after the switch to KEMF. The earlier figures of 1.9 Hz
and 5.9 s assumed an eleven-year gap starting at OOI's 2015 deployment, which
no longer applies now that the record is continuous.)

## Decisions so far

| Decision | Rationale |
|---|---|
| Target station is NV.KEMF, channel EHZ | Continuous 2010 to now, no gap, same sensor throughout, one of the three instruments in the paper's own trend fit, and provably fetchable from IRIS (the 2013 download code did exactly that). Chosen over Axial, which has a 2013-2015 gap, an instrument change, and audio that is probably lost. Decided 2026-08-30, see `probes/04-kemf-continuity.md`. |
| Sparse years, both metrics | 3-4 well-separated years, one station, consistent season. Real answer in weeks rather than months. |
| IPI is the robust metric, peak frequency the risky one | Two independent arguments agree. Effect size: 7.0 s is huge against measurement error, 2.2 Hz is not. Instrument transition: timing survives a sensor swap, frequency depends on instrument response near 20 Hz. |
| Validate by re-running the new detector on the old data | Compare against published results. Upgrades the claim from "the trend continued" to "the trend continued, and here is the measured bias between the 2013 method and this one". |
| One pipeline, both eras | Detector consumes obspy Streams so old and new data take identical code paths. Costs a response-deconvolution step, buys a validation that proves the exact code used on the new years. |
| OpenSoundscape over Koogu | Koogu is TensorFlow, which is a known pain point on Apple Silicon. OpenSoundscape is PyTorch and comes from the same lab as the bioacoustics-model-zoo ONNX path. One ecosystem. |
| Perch dropped entirely | Its mel frontend starts at 60 Hz, so a 20 Hz call is below its first band. Ghani et al. 2023 removed fin whales from their transfer benchmark for exactly this. Time compression tops out around 12x; we would need 50-100x. Settled 2026-08-29, see `probes/03-perch-at-20hz.md`. |
| Whale-VAD is the detector | PyTorch, `torch.hub`, 4 MB, trained at 250 Hz against our 200 Hz, dedicated fin whale class, learnable frequency frontend so no mel floor. GPL-3.0. See `literature/detector-landscape.md`. |
| Schall's DSP detector is the day-one baseline | Pure signal processing, no training, published thresholds for this exact call, runs on 200 Hz unmodified. Something working before anything is trained. |
| Three storage tiers, split by row granularity | `data/` raw waveforms and `work/` intermediates are gitignored; `results/` is committed. The rule: one row per NOTE goes to `work/`, one row per SEASON goes to `results/`. Driven by size, Whale-VAD frame probabilities alone are ~121 MB/day and ~18 GB per Nov-Mar season. Per-note tables are only 5-10 MB/season and git would tolerate them, but they are exactly the artifact that belongs in a citable Zenodo archive rather than in git history forever. Enforced by `tests/test_repo_hygiene.py`, not by discipline. |
| Archive properly, with DOIs | Archival best practice throughout, for anything this project depends on or publishes. Mirror `fin-call-patterns` to Zenodo for a citable DOI before depending on it (currently a mutable `master` branch). Every derived dataset this project publishes gets the same treatment. |
| Numbers in prose are generated, never typed | The 2017 paper has five internal inconsistencies (site counts, dates, a percentage that does not divide), catalogued in `literature/2017-paper-data-section.md`. Any figure quoted in text comes from the data at build time. |
| MIT licence, GPL dependency behind an optional extra | Whale-VAD is GPL-3.0 and the conservative reading makes importers derivative works. It installs with `uv sync --extra whalevad` and sits behind the same detector interface as the Schall baseline, so nothing in `src/` is derived from it. The interface was required by the science anyway: comparing detectors on identical audio is the experiment. |
| Marimo notebooks are the pipeline | Reactive DAG, plain Python, no hidden execution order. Shared code moves to `src/` once used twice. |
| Reproducibility is offered as three rungs, not one | The storage tiers already are a reproducibility ladder, so say so in the README with the cost of each: re-plot the figures from `results/` (clone and run, seconds, no download); re-run aggregation from the per-note tables (minutes, ~40 MB from Zenodo); re-run detection from raw audio (days, ~73 GB via `manifests/`). Most repos offer only the third rung and are reproducible in principle and unused in practice. Nearly everyone checking the work does the first, a reviewer does the second. Agreed 2026-08-30. |
| The outreach layer consumes `results/`, it does not restate it | Extension of "numbers in prose are generated, never typed" to the shareable artifacts. The public-facing piece reads its numbers and its audio clips out of committed pipeline outputs, so it cannot drift from the science and updating it means re-running the pipeline rather than rewriting a post. Agreed 2026-08-30. |
| Exemplar audio clips are a `measure` stage output | The 20 Hz call is at or below the floor of human hearing; time-compressed 10-20x it is an audible pulse train, and 2003 against 2026 at the same compression makes the IPI change something a non-expert can hear rather than read off an axis. This is the only piece of the project with a plausible path past a few hundred people. Folded into `measure` scope so it falls out as a byproduct, because retrofitting outreach assets afterwards is how they never happen. `results/` gains a small table naming each exemplar: station-season, timestamp, compression factor. Agreed 2026-08-30. |
| Pin the Whale-VAD checkpoint the way `fin-call-patterns` was pinned | The checkpoint is a `torch.hub` pull from a third-party repo with no version guarantee: mutable upstream, no pin, same class of hole that the ground-truth mirror closed on 2026-08-30. Mirror it and record sha256 in a `kind: external-archive` manifest. It is the one remaining thing that would silently make the detection results unreproducible. |
| Scope stays on the existing hydrophone and seismometer record | Distributed acoustic sensing work is underway on the same cables and answers different questions. Extending the 2003-2013 series on the instruments that produced it is complementary, and runs on one desktop machine. |

## Structural limitation, and how it dissolved

Originally: the series ends 2013, OOI RCA starts 2015, so no temporal overlap
and the instrument transition could not be validated by simultaneous recording.

**This was an artefact of choosing Axial.** NV.KEMF has recorded continuously
on the same channel since 2010 and is still running, and it is one of the three
instruments in the paper's own trend fit. At KEMF there is no gap and no
instrument transition, so the old-versus-new comparison becomes purely a
detector comparison on identical hardware. See `probes/04-kemf-continuity.md`.

## Resolved 2026-08-29 by the paper extraction

See `literature/2017-paper-data-section.md` for detail.

- Stations: Axial (NeMO hydrophone, 100 Hz, 2006-2013), KENE and KEMF
  (seismometers). The decadal trends come from these three only, not all nine.
- Per-year values are figure-only, BUT the per-detection HDF5 files are public
  at `github.com/michellejw/fin-call-patterns`. Published values can be
  re-derived exactly instead of digitized.
- Target station is **NV.KEMF**, decided 2026-08-30. Superseded the earlier
  Axial choice.
- Metric is IPI (inter-pulse interval), not INI.
- "Peak frequency" is an amplitude-weighted centroid over +/-0.5 s and
  15-35 Hz, not an argmax. Must be reproduced as a centroid.
- The bar to clear: 4.8% missed, 1.5% false detections.

## Resolved 2026-08-30 from the original MATLAB code

- The paper's missing FDSN codes are in `DET_CODE/IRISdownload_mseed.m`:
  KEMF is network **NV**, channel **EHZ**. 7D is the Cascadia Initiative.
  KEMF was downloaded from IRIS, not delivered on a drive.
- Instrument response was **not** corrected. `run_detectfin.m` sets
  `p.resp = 1` and `detectfin.m` divides by it. A no-op, and a scalar rather
  than a transfer function in any case. See `probes/05-instrument-response.md`.
- NV.KEMF EHZ has run continuously since 2010-09-30 and is still recording.
  100 Hz until 2013-03-01, 200 Hz after. See `probes/04-kemf-continuity.md`.

## Open

- Whether KEMF's response changes across 15-35 Hz at the 2013-03-01 rate
  change. The one real risk the KEMF switch introduces.
- Whether the NeMO Axial 2006-2013 audio is at PMEL or NCEI. Not needed for a
  first result; matters only if Axial is chosen or added later.
## Folders

- `probes/` one file per probe, question and answer
- `literature/` paper notes
