# The 2017 paper: what it actually used and reported

Extracted 2026-08-29 from the full text (PLOS HTML + JATS XML).
Weirathmueller et al. 2017, PLoS ONE 12(10) e0186127. CC0.

## The headline finding for this project

**The per-detection data is already public.**

`https://github.com/michellejw/fin-call-patterns/tree/master/DETECTION_DATA`

23 HDF5 files, one per station-season. Per-detection columns:
`dettime, frequency, snr, siglevel, station, isseq, boutnum, seqnum, ipi`.

This is raw per-note output, not summaries. So the published Fig 7 values can
be re-derived exactly by re-running the histogram-peak extraction (code is in
the same repo under `SEQ_CODE/`), rather than digitized off the figure.

Caveat: a GitHub `master` branch is not a durable archive. No DOI, no Zenodo
mirror, mutable. Mirrored and pinned by commit before being relied on, with a
sha256 per file, and destined for a Zenodo DOI. This project follows archival
best practice for anything it depends on or publishes.

## Three corrections to our working assumptions

**1. The metric is IPI, not INI.** The headline +0.54 s/year is inter-pulse
interval: the gap between successive detections regardless of note type. The
paper reserves "inter-note interval" for a different quantity, the sum of the
two doublet IPIs, which appears only as grey circles in Fig 7A and carries no
fitted trend. Our handover doc had this wrong throughout.

**2. "Peak frequency" is a weighted centroid, not an argmax.** Methods define
it as the amplitude-weighted mean of the spectrogram within ±0.5 s of the
detection and 15-35 Hz. A modern pipeline that picks spectral peaks will not
produce comparable numbers. This has to be reproduced as a centroid.

**3. No instrument response correction is mentioned anywhere.** Not in Methods,
not in the supplement. Cannot tell whether it was done and unreported or not
done at all. Since the metric is a normalised weighted-mean frequency, an
uncorrected response biases it. Resolved 2026-08-30 from the original MATLAB:
no correction was applied, and it would not have mattered at KEMF anyway. See
`probes/05-instrument-response.md`.

## Stations actually used (Table 1)

| Experiment | Station | Sensor | Years | Lat/Lon | Depth | Rate |
|---|---|---|---|---|---|---|
| NeMO | Axial | **Hydrophone** | 2006-2013 | 45.96N 130.01W | 1550 m | 100 Hz |
| Keck Endeavour | KENE | Seismometer | 2003-2006 | 47.97N 129.06W | 2330 m | 128 Hz |
| Ocean Networks Canada | KEMF | Seismometer | 2011-2013 | 47.95N 129.10W | 2205 m | 100 Hz |
| COLZA | OBS01 | Seismometer | 2007-2009 | 44.58N 125.56W | 2880 m | 100 Hz |
| Cascadia Initiative | J63A | Seismometer | 2011-2012 | 48.21N 130.00W | 2880 m | 50 Hz |
| Cascadia Initiative | J23A | Seismometer | 2011-2012 | 44.84N 129.68W | 2660 m | 50 Hz |
| Cascadia Initiative | J06A | Seismometer | 2011-2012 | 43.25N 128.80W | 3220 m | 50 Hz |
| Cascadia Initiative | G30A | Seismometer | 2011-2012 | 41.96N 128.32W | 3120 m | 50 Hz |
| Cascadia Initiative | G03A | Seismometer | 2011-2012 | 40.06N 126.16W | 4110 m | 50 Hz |

Only the vertical seismometer channel was used on the OBSs. The fourth channel
is a differential pressure gauge, insensitive above ~10 Hz and therefore useless
for fin whales. The five Cascadia stations were excluded from frequency analysis
entirely: 50 Hz sampling puts the anti-alias cutoff at 23.5 Hz, truncating the
note bandwidth and skewing the weighted-mean estimate low.

**No FDSN network codes appear anywhere in the paper.** Only project
abbreviations. So probe 1's network list cannot be mapped to these stations from
the paper alone.

**The decadal trends come from three instruments only**: Axial, KENE, KEMF
(Fig 7). Not the full nine. COLZA and the Cascadia stations contribute only to
single-season geographic comparisons in Figs 9 and 10.

## Why Axial is the obvious target

Axial Seamount, 45.96N 130.01W, is a hydrophone, is the longest continuous
record in the paper (2006-2013), and is also an OOI Regional Cabled Array site.
Same location, same sensor type, both eras, with a two-year gap (2013 to 2015).
100 Hz then, 200 Hz now, and decimating 200 to 100 is trivial.

That is about as clean a continuation as this kind of study ever gets.

## Method, in enough detail to reproduce

**Detection: time-domain matched filter.** Template is a linear chirp falling
30 to 15 Hz over 2.25 s. Pre-filter 14-35 Hz bandpass at rates >=100 Hz, 14 Hz
highpass at 50 Hz. Cross-correlation in 30-minute segments, noise level set at
the 90th percentile, peaks retained at >=12 dB above noise (SNR >= 4).
Detection times debiased up to +/-0.5 s against a Hilbert envelope peak.
Earthquakes rejected when 7-14 Hz power exceeds 14-35 Hz power in a 1 s window.
Multipath rejected by enforcing 5 s minimum spacing at Axial, 10 s elsewhere.

**Frequency:** spectrogram with 1 s Hann window, 90% overlap. Amplitude-weighted
mean over +/-0.5 s and 15-35 Hz.

**IPI:** time difference between successive detections, assigned to the later
note. Discard IPI > 40 s. Keep only sequences of >= 20 IPIs with no gap longer
than 20 minutes.

**Singlet/doublet split is post-hoc**, from 2-D histograms per month and per
season. IPI binned 5-40 s at 1 s, frequency binned 15-26 Hz at 0.4 Hz. Peaks
found with a SciPy maximum filter, retained above 2% per 1s-1Hz area.
Definitions: singlet IPI > 22 s, doublet IPI <= 22 s; note A < 22 Hz, note B >= 22 Hz.

Software named: SciPy only. No XBAT, Raven, or MATLAB mentioned.

## Published performance (Table 2)

50 one-hour song sequences, manual vs automated.

| | Singlet | Doublet | All |
|---|---|---|---|
| Manual | 1335 | 1404 | 2739 |
| Automated | 1290 | 1357 | 2647 |
| Missed | 59 (4.4%) | 72 (5.1%) | 131 (4.8%) |
| False | 14 | 25 | 39 (1.5%) |

Timing consistent within 0.1 s across 100+ calls. Total surviving the full
pipeline: over 1.8 million notes from more than 8,000 song sequences.

**This is the bar a new detector has to clear**: 4.8% missed, 1.5% false.

## Published trends

| Metric | Slope | R2 | p | Window |
|---|---|---|---|---|
| IPI, singlet A notes | +0.54 s/yr | 0.96 | <0.001 | 2003-2013 |
| Frequency, singlet | -0.17 Hz/yr | 0.86 | 1.1e-4 | 2003-2013 |
| IPI, doublet A notes | +0.73 s/yr | 0.91 | 0.001 | 2007-08 on |
| IPI, doublet B notes | +0.86 s/yr | 0.90 | 0.001 | 2007-08 on |
| Frequency, doublet | not significant | | | 2007-08 on |

No slope confidence intervals published, only R2 and p. Per-point uncertainty
is given as 0.5 s for IPI and 0.2 Hz for frequency (half the histogram bin).

Endpoints, 2003-04 to 2011-12 season: singlet IPI 24.5 to 29.0 s, peak frequency
19.8 to 18.3 Hz.

Singlet-to-doublet: doublets appear at very low levels as early as 2005-06,
well established by 2008-09, and by 2012-13 the singlet had essentially
disappeared.

## Discrepancies in the published paper

Recorded because they will cause confusion later, not because they matter much.

- Results say "8 sites", Table 1 lists nine.
- KEMF dates given as 2010-2012 in Methods, 2011-2013 in Table 1 and Results.
  Archived filenames support 2011-2013.
- KENE-KEMF separation given as 4 km in Methods, 14 km in Results. Coordinates
  give ~3.5 km.
- Table 1 names one COLZA station; the archive has three COLZA prefixes.
- Table 2 singlet false rate printed as 0.4%, but 14/1290 is 1.1%.
None of these change the paper's conclusions. The false-rate arithmetic is
the one worth a formal correction, because this project benchmarks its new
detector against that number and 0.4% against 1.1% is a 2.75x difference in
the thing being compared. The general lesson is adopted here as a rule:
numbers quoted in prose are generated from the data, never typed.
