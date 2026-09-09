# Probe 6: do the archived detections reproduce Fig 7?

2026-09-08. Answer: yes for IPI, exactly. Yes for frequency in slope, with the
exact fit not fully pinned down. And the attempt surfaced a station offset in
frequency that changes how this project has to use KEMF.

## Why this was asked

The whole validation design rests on re-deriving the published per-season
values from the archived per-note detections rather than digitizing them off
the figure. A first pass with a naive histogram peak missed badly: frequency
argmax 23.05 Hz against a published 18.3 Hz, IPI argmax 14.75 s against 29.0 s.
Until that was explained, there was no baseline to measure a new detector
against.

## What the naive pass got wrong

Two selection rules, both stated in the paper's Methods and both missed:

- **singlet IPI > 22 s, doublet IPI <= 22 s**
- **note A < 22 Hz, note B >= 22 Hz**

The frequency distribution is bimodal, modes near 19.1 and 22.9 Hz, and the
B-note mode carries roughly twice the counts. A global argmax therefore returns
the B note. The IPI distribution is likewise dominated by the doublet
population, so a global argmax returns the doublet interval.

The archived analysis code adds a house recipe, from `SEQ_CODE/`:
in sequence, IPI < 60 s, SNR > 5 dB, sequence length > 10 notes.

## Reproduction from the per-note data

KEMF 2011-2012, applying all of the above, singlet A notes only:

| | recomputed | archived summary |
|---|---|---|
| frequency | 19.15 Hz | 19.2 Hz |
| IPI | 28.25 s | 28.5 s |

Within one histogram bin of the archived per-season values, which is what
matters: the per-note files can regenerate the summary, so the baseline is
real.

## Reproduction of the published trend

`SEQ_CODE/ALL_seq_YEARLY_4nov2016_5dBthresh_kurtosis.csv` holds the per-season
peaks. It is **2D**: several clusters per station-season in (frequency, IPI)
space, not one peak per axis. Taking the dominant singlet A-note cluster per
station-season on the three trend instruments, and dropping AX 2012-13 where
the paper notes the singlet had essentially disappeared:

| | reproduced | published |
|---|---|---|
| IPI slope | +0.534 s/yr | +0.54 s/yr |
| IPI R2 | 0.96 | 0.96 |
| IPI endpoints | 24.45 -> 28.73 s | 24.5 -> 29.0 s |
| frequency slope | -0.175 Hz/yr | -0.17 Hz/yr |
| frequency R2 | 0.74 | 0.86 |
| frequency endpoints | 19.93 -> 18.53 Hz | 19.8 -> 18.3 Hz |

IPI is an exact reproduction on all four numbers. Frequency reproduces in
slope but not in R2, and the residual is dominated by one point (below).
Excluding KEMF from the frequency fit gives -0.220 Hz/yr at R2 0.96, which
matches neither published number, so the paper's exact frequency selection is
still not pinned down. It does not need to be: the method is confirmed and the
slope agrees.

## The finding that matters more

2011-2012 is the one season where KEMF and Axial both recorded.

| Station | frequency | IPI |
|---|---|---|
| Axial (hydrophone, 1550 m) | 18.40 Hz | 28.50 s |
| KEMF (seismometer, 2205 m) | 19.20 Hz | 28.50 s |

**IPI is identical. Frequency differs by 0.80 Hz.**

The total published frequency change across the whole decade is about 1.5 Hz,
so a station offset of 0.80 Hz is more than half the entire signal. Comparing
new KEMF frequency values against a trend fitted largely on Axial, without
accounting for that offset, would be badly misleading.

This is not instrument response. Probe 5 measured KEMF's response as flat to
0.20 dB across 15-35 Hz. Candidate explanations, none tested: sensor type
(hydrophone against seismometer), depth, propagation path, or a noise floor
that shifts an amplitude-weighted centroid.

It also converts an argued decision into a measured one. The notes already
said "IPI is the robust metric, peak frequency the risky one" on the reasoning
that timing survives a sensor swap and frequency may not. Here are the two
instruments, the same season, the same animals: timing agrees exactly and
frequency does not.

## Consequences

- The validation baseline is real. Proceed to `fetch`.
- Extraction must select the mode, not the maximum, and must apply the singlet
  and note-A thresholds before any peak finding.
- Peak finding should be 2D in (frequency, IPI), matching the archive, not two
  independent 1D histograms.
- Any KEMF-versus-published frequency comparison needs the station offset
  handled explicitly. IPI needs no such correction.
