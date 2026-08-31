# Probe 5: was instrument response corrected in the 2017 study?

2026-08-30. Answer: no. Settled from the original code.

## Why this was asked

The paper never mentions response correction or deconvolution, so whether it
was done and unreported or not done at all could not be settled from the text.

It is resolvable, from `DET_CODE` in `michellejw/fin-call-patterns`.

## Evidence

`run_detectfin.m` line 18:

```matlab
p.resp = 1; % Instrument response
```

`detectfin.m` line 68:

```matlab
data0 = data0/p.resp; % Correct for instrument response
```

The hook exists. It divides by a scalar, and that scalar is 1. A no-op.

## What this actually means

Two separate points, and the second matters more than the first.

**1. No response correction was applied.** The published peak-frequency values
are amplitude-weighted centroids of the raw, uncorrected spectrum.

**2. Even if `p.resp` had been set, it is a scalar, not a transfer function.**
The code never had frequency-dependent deconvolution available. A flat scalar
divides out of a normalised weighted mean entirely, so setting it correctly
would have changed nothing about the frequency numbers anyway.

## Consequences

- **To reproduce the published numbers, do not correct the response either.**
  Correcting it would produce different centroids and break comparability.
  This is a case where matching the old method means deliberately not doing
  the more correct thing in the reproduction leg.
- The interesting quantity is how much the response *slopes* across 15-35 Hz.
  If it is flat there, the uncorrected centroid is unbiased and everything is
  fine. If it slopes, every published frequency value carries a fixed offset,
  which cancels in a *trend* as long as the instrument never changed.
- At KEMF the instrument does not change across the whole record, so a sloped
  response biases the absolute frequency but not the trend. This is another
  argument for KEMF over Axial.
- The 2013-03-01 rate change at KEMF is the exception worth checking: pull the
  response for the 100 Hz and 200 Hz epochs and compare across 15-35 Hz.

## Recommended handling

Compute both. Report the uncorrected centroid as the comparable-to-2017 number,
and the response-corrected centroid alongside it as the physically correct one.
Publish the difference. That is strictly more useful than picking one, and it
turns an unresolved methodological worry into a measured quantity.

---

## Resolved 2026-08-30: the response is flat, so none of this bites

Measured from the actual FDSN response via obspy, `output="VEL"`, amplitude
normalised to 20 Hz:

| Frequency | dB re 20 Hz |
|---|---|
| 15 Hz | -0.04 |
| 20 Hz | +0.00 |
| 25 Hz | +0.05 |
| 30 Hz | +0.09 |
| 35 Hz | +0.15 |

**Total tilt across the 15-35 Hz analysis band: +0.20 dB.**

Sensor is a GeoSENSE BH-1 corehole seismometer with a Guralp DM24-MK3
datalogger, the same instrument in both epochs.

Across the 2013-03-01 rate change from 100 to 200 Hz:

| Epoch | Rate | Tilt 15-35 Hz |
|---|---|---|
| 2010-09-30 to 2013-03-01 | 100 Hz | +0.20 dB |
| 2013-03-01 onward | 200 Hz | +0.19 dB |

**Maximum difference between the two epochs anywhere in the band: 0.004 dB.**

### What this settles

- The uncorrected amplitude-weighted centroid is **unbiased**. A 0.2 dB tilt
  across 20 Hz of bandwidth cannot move a centroid meaningfully. The 2017
  study's `p.resp = 1` cost nothing at KEMF.
- The 2013 rate change introduces **no response discontinuity**. This was
  logged as "the one real risk the KEMF switch introduces". It is retired.
- The recommendation to compute corrected and uncorrected centroids side by
  side is now optional rather than necessary. Worth doing once to show the
  difference is nil, then dropping.
