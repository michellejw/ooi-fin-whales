# ooi-fin-whales

Extending a 2003-2013 fin whale call time series into the present using an
automated detector, on continuous seafloor seismometer data from the Endeavour
segment of the Juan de Fuca Ridge.

## Background

Fin whales (*Balaenoptera physalus*) produce a short downswept pulse centered
near 20 Hz. The pulses repeat in long sequences, and the interval between
successive pulses is regular enough to be measured. That interval is the
inter-pulse interval (IPI).

Weirathmueller et al. (2017) measured IPI and peak frequency from nine
instruments in the northeast Pacific between 2003 and 2013, and found that both
were changing:

| Quantity | Rate of change | R² | p |
|---|---|---|---|
| IPI, singlet A notes | +0.54 s/year | 0.96 | <0.001 |
| Peak frequency, singlet | -0.17 Hz/year | 0.86 | 1.1e-4 |

Over the same decade the song pattern shifted. Early in the record, sequences
had a single frequency and a single IPI (a singlet). Doublets, with two
frequencies and two intervals, appeared around 2005-2006, became established by
2008-2009, and by 2012-2013 the singlet had essentially disappeared.

The paper stops in 2013.

## The question

NV.KEMF, the Main Endeavour Field station of the Ocean Networks Canada cabled
observatory, has been recording continuously since September 2010 and is still
recording. It is one of the three instruments the 2017 trends were fitted to.

So the record did not stop in 2013. Only the analysis did.

If both trends continued at the published rates, the thirteen years since would
imply roughly 7 s of further IPI increase and 2.2 Hz of further frequency
decline. Whether they did is the question this repository answers.

The two quantities do not carry equal risk. An IPI shift of several seconds is
large relative to the measurement uncertainty published for it (0.5 s). A
frequency shift of about 2 Hz is closer to its own uncertainty (0.2 Hz) and
depends on reproducing the original spectral estimator exactly.

## Approach

The pipeline runs in four stages. Each reads the previous stage's output and
writes its own.

1. **fetch** retrieves waveform data from the FDSN web services and writes a
   manifest recording the exact query.
2. **detect** finds candidate pulses. Two detectors are run: a signal
   processing baseline, and a neural detector (Whale-VAD).
3. **measure** computes IPI and frequency per detected note, using the 2017
   study's definitions.
4. **aggregate** builds the two-dimensional frequency-IPI histograms the
   original analysis used, extracts their peaks per season, and fits trends.

Stages 3 and 4 reproduce the published method rather than improving on it. The
point of the comparison is that the measurement is unchanged and only the
detector differs, so any difference in the result is attributable to the
detector.

## Data

Station NV.KEMF, channel EHZ, 47.9496°N 129.0987°W, 2190 m depth. GeoSENSE BH-1
corehole seismometer with a Guralp DM24-MK3 datalogger. 100 Hz sampling until
2013-03-01, 200 Hz after.

The sample rate changes but the instrument does not. Its response is flat across
the 15-35 Hz analysis band, tilting 0.20 dB from end to end, and the two
sampling epochs differ from each other by 0.004 dB. Peak frequency can therefore
be compared across the whole record without deconvolving the response, which is
also what the original analysis did.

Raw waveforms are not stored in this repository. Every retrieval writes a
manifest to `manifests/`, which is committed, so any cached file can be
reconstructed exactly.

## Validation

The 2017 study archived its per-note detections at
[michellejw/fin-call-patterns](https://github.com/michellejw/fin-call-patterns),
including two seasons at KEMF (2011-2012 and 2012-2013). Those files give
detection times, measured frequency, and measured IPI for every note the
original matched filter found.

This allows a direct comparison. Running the new detector over the same windows
and measuring the same way produces two sets of numbers for identical audio on
identical hardware, so the difference between them is the difference between the
detectors, isolated from everything else.

The original detector's published performance, verified against manual review of
50 one-hour sequences, was 4.8% missed and 1.5% false detections. That is the
number a new detector has to beat.

The measurement stage is also tested directly against those files: given the
archived detection times, the IPI our code computes must match the archived IPI
column.

## Repository layout

```
src/ooi_fin_whales/   code used by more than one notebook
notebooks/            marimo notebooks, one per stage
manifests/            committed. one JSON per retrieval, the full query
results/              committed. per-season summaries and fit coefficients
work/                 gitignored. per-note tables and model output
data/                 gitignored. raw waveforms
tests/
```

Storage is split by granularity. One row per season goes in `results/` and is
committed. One row per note goes in `work/` and is not. The reason is size:
frame-level detector output runs to roughly 18 GB for a single November-March
season. Per-note detection tables are small enough that git would tolerate them,
but they belong in a citable archive with a DOI rather than in a repository's
history. `tests/test_repo_hygiene.py` enforces the split.

## Reproducing

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/michellejw/ooi-fin-whales
cd ooi-fin-whales
uv sync
uv run pytest
uv run marimo edit notebooks/ --port 2722
```

`data/` and `work/` are both rebuilt from `manifests/` and committed code, so a
fresh clone reproduces every published number without needing anything that is
not in the repository or on a public server.

## Status

Scoping complete. Station, detector, and validation design are settled. The
pipeline is not built yet.

## References

Weirathmueller, M.J., Stafford, K.M., Wilcock, W.S.D., Hilmo, R.S., Dziak, R.P.,
Tréhu, A.M. (2017). Spatial and temporal trends in fin whale vocalizations
recorded in the NE Pacific Ocean between 2003-2013. *PLoS ONE* 12(10), e0186127.
[doi:10.1371/journal.pone.0186127](https://doi.org/10.1371/journal.pone.0186127)

Geldenhuys, C.M., et al. Whale-VAD.
[github.com/CMGeldenhuys/Whale-VAD](https://github.com/CMGeldenhuys/Whale-VAD),
[doi:10.5281/zenodo.17251589](https://doi.org/10.5281/zenodo.17251589)

Madhusudhana, S., et al. (2021). Improve automatic detection of animal call
sequences with temporal context. *J. R. Soc. Interface* 18, 20210297.
[doi:10.1098/rsif.2021.0297](https://doi.org/10.1098/rsif.2021.0297)

Ocean Networks Canada. NEPTUNE cabled observatory, station NV.KEMF.
Data distributed by EarthScope.
