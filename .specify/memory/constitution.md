# Fin Whale Call Detection Constitution

## What this study is

**Question.** Between 2003 and 2013 the 20 Hz fin whale call at the Endeavour
segment slowed and dropped in pitch, and the song shifted from singlet to
doublet. Did those trends continue through to the present?

**Deliverable.** A follow-up paper to Weirathmueller et al. 2017, PLoS ONE
12(10) e0186127, reporting the extended series together with a measured bias
between the 2013 detection method and the one used here.

**Who does what.** Single author at present. Co-authors are intended but not
chosen; the choice is open and is recorded in `notes/index.md` when made. No
input arrives from a collaborator, so every input contract below is one this
study controls and could in principle change. The one exception is the 2017
archive, which is fixed by having been published.

## Core Principles

### I. Raw data is immutable

Raw inputs are never edited in place, never overwritten, never cleaned by hand.
Everything downstream is derived and therefore disposable. If a derived file
cannot be regenerated from raw data plus code, it is raw data that nobody
labelled as such, and it will eventually be lost.

### II. Every number traces to a script, an input, and a parameter set

A figure or table nobody can regenerate is a claim without evidence behind it.
This applies to numbers quoted in prose as much as to plotted ones.

### III. A clean rerun reproduces the numbers

Not approximately. Seeds are fixed and recorded wherever anything is random.
If a rerun does not reproduce, that is a defect to be understood, whether or
not the new numbers look reasonable.

### IV. Record what was examined, not only what was found

A case that was checked and came back empty and a case that was never checked
are different facts. A table holding only positive findings cannot tell them
apart, and analysis that treats the two as one silently invents data. Whatever
this study's unit of examination is, the complete list of units examined is an
input in its own right, and it is named in the Data sources section below.

### V. Time is UTC

Local or solar time appears only where the science needs it, such as diel or
lunar analysis. Where it does, the conversion is done in the open and the
convention is recorded here rather than assumed.

### VI. Known defects live with the data

When an input has a flaw, a gap, or a pending correction, it is written down
where the next person reads about that input. Not in a chat thread, not in
someone's memory. The Data sources section is that place.

## Data sources

### FDSN waveforms, NV.KEMF EHZ

- **What it is.** Continuous vertical-channel seismometer data at Main Endeavour
  Field, 47.9496N 129.0987W, 2190 m. Recording since 2010-09-30 and still
  running. GeoSENSE BH-1 corehole seismometer, Guralp DM24-MK3 datalogger.
- **Who produces it.** Ocean Networks Canada, network NV. Retrieved through the
  EarthScope FDSN web service.
- **Shape and resolution.** miniSEED, consumed as obspy Streams. 100 Hz until
  2013-03-01, 200 Hz after. One row per sample.
- **Version pinned.** Not pinned, and does not need to be: every retrieval
  writes a manifest to `manifests/` recording network, station, channel, time
  window, response epoch, sample rate and retrieval timestamp, so any cached
  file is reconstructible. The archive is not being revised.
- **Known defects.** None known in the record itself. The sample rate changes at
  2013-03-01 but the instrument does not, and the response is flat across the
  15-35 Hz analysis band: 0.20 dB total tilt, with the two sampling epochs
  differing by at most 0.004 dB. Evidence in
  `notes/probes/05-instrument-response.md`.

### Archived per-note detections from the 2017 study

- **What it is.** Every note the original matched filter found, across 23
  station-seasons, including KEMF 2011-2012 and 2012-2013. The validation
  baseline.
- **Who produces it.** The 2017 study. Published at
  `github.com/michellejw/fin-call-patterns`.
- **Shape and resolution.** 23 HDF5 files, one per station-season, one row per
  note. Columns `dettime, frequency, snr, siglevel, station, isseq, boutnum,
  seqnum, ipi`. They are pandas HDFStore *fixed-format* frames, pandas 0.15.2,
  so h5py needs the `df/axis0` to `df/blockN_items` block mapping. `dettime` is
  datetime64[ns] UTC stored as int64, `ipi` is timedelta64[ns] stored as int64,
  and `station` is a pickled object array best taken from the filename.
- **Version pinned.** Yes. Commit `5ba449c42939aeb3f44068de3cf26a9b1e7b754c`,
  with a sha256 per file, recorded in
  `manifests/ground-truth-fin-call-patterns.json`. Pinning was necessary: the
  upstream has no licence, no DOI, and a mutable `master`.
- **Known defects.** The `boutnum` column is all zeros at KEMF 2011-2012 and
  carries no information. The published per-season summary in
  `SEQ_CODE/ALL_seq_YEARLY_4nov2016_5dBthresh_kurtosis.csv` contains rows with
  `peakcounts` of zero and minor clusters that are not the singlet A note, so
  selecting the dominant cluster per station-season is required rather than
  optional. Five small internal inconsistencies in the paper's text are
  reconciled in `notes/literature/2017-paper-data-section.md`; the archive is
  authoritative where they disagree.

### Whale-VAD detector checkpoint

- **What it is.** The neural detector's released weights, loaded via
  `torch.hub`.
- **Who produces it.** `github.com/CMGeldenhuys/Whale-VAD`, GPL-3.0, kept behind
  the optional `whalevad` extra.
- **Shape and resolution.** Frame-level class probabilities, hop 5 at 250 Hz,
  so 50 frames per second.
- **Version pinned.** **NOT YET PINNED. This is an open defect.** It is a
  `torch.hub` pull from a third-party repository with no version guarantee, and
  it is the one remaining input that could silently make detection results
  unreproducible. Pin it and record a sha256 in a `kind: external-archive`
  manifest, as was done for the 2017 archive.
- **Known defects.** The released checkpoint emits seven classes, not the three
  its README and `_class_mapping` describe. The label order is undocumented and
  must be resolved by correlating each channel against the archived ground-truth
  detections.

### Record of examination

`manifests/` is the record. Each JSON records a retrieval and the exact time
window it covers, so a window that was fetched and yielded no detections is
distinguishable from a window that was never fetched. This distinction is
load-bearing here: call rates and seasonal presence are meaningless without it,
and a season absent from the results could otherwise mean either silence or an
unprocessed gap. No detection table may be interpreted as a rate without the
matching manifest coverage.

## Technical environment

**Runtimes.** Python only, managed with `uv`. Never pip, never conda. The
original 2017 analysis code is MATLAB and is read for reference, in the pinned
archive, but is not executed as part of this study.

**Pipeline form.** Marimo notebooks, one per stage, in `notebooks/`. Reactive
DAG, plain Python on disk, no hidden execution order. Code moves to
`src/ooi_fin_whales/` once used by more than one notebook. A rerun is triggered
by running the notebook for a stage and those downstream of it.

**Where outputs go.** Four tiers, split by row granularity and enforced by
`tests/test_repo_hygiene.py`:

- `data/` raw waveforms. Gitignored, reconstructible from `manifests/`.
- `work/` one row per note, plus frame probabilities and caches. Gitignored,
  destined for a Zenodo archive with a DOI.
- `results/` one row per season, plus trend fits and exemplar clip tables.
  Committed, and held under 1 MB per file by test.
- `manifests/` one JSON per retrieval. Committed.

## Conventions

**Units and coordinate systems.** Frequency in Hz, intervals in seconds,
positions in decimal degrees WGS84, depth in metres. The `snr` column in the
archive is a ratio in dB and needs no reference. The `siglevel` column is in dB
but its reference is not documented in the paper and has not been recovered;
it is not used quantitatively anywhere in this study, and if that changes the
reference must be established first rather than assumed.

**Time.** UTC throughout, with no exception so far. Neither diel nor lunar
analysis is planned. Seasons run November to March and are labelled by the
starting year, so "2011-2012" begins in November 2011, matching the archive's
`datevec` convention of dating each season to its November.

**Naming.** Archived station-season files are `<STATION>_<YYYY>_<YYYY>.h5`, and
the station is taken from the filename rather than the pickled column. Manifests
are named for what they record and carry a `kind` field, either `fdsn-pull` or
`external-archive`. Stage ordering lives in the numbered spec directories, not
in script or notebook names, so that inserting or superseding a stage does not
desync anything.

## Figure standards

Not yet established. No figure has been produced. This section is a known gap
and must be filled before the first figure intended for the paper, not after,
because two figures made months apart will not otherwise match. The one fixed
requirement so far is that every plotted number comes from a file in `results/`
rather than from a value typed into the plotting code.

## How this project works

**Decision record.** `notes/index.md` holds a decisions table, one row per
decision with its rationale. `notes/probes/` holds one file per question
answered, with the evidence, and `notes/literature/` holds notes on the source
paper and the detector survey. A decision that shapes more than one stage
belongs there. A finding confined to one stage belongs in that stage spec's
Outcome section.

**Work tracking.** None. Stage specs in numbered directories are the whole
record. This is a single-author study and adding an issue tracker would create
a second place for the truth to live.

**Voice.** Technical and explanatory, aimed at a reader who knows acoustics but
not this dataset. Precision over simplification: name real quantities and real
column names rather than gesturing at them. No em dashes. State findings
directly rather than building up to them. The repository's existing prose,
particularly `README.md` and the probe notes, is the reference for tone.

## Quality gates

- A clean rerun reproduces every number in the current results.
- Every figure and table traces to a script, an input, and a parameter set.
- Raw data is unmodified since acquisition.
- Row counts survive every join, and every dropped row is accounted for
  deliberately rather than by default.
- **The Fig 7 reproduction still holds.** Extracting from the archived per-note
  file for KEMF 2011-2012, under the study's own selection rules, returns
  19.2 Hz and 28.5 s to within one histogram bin. Refitting the decadal trend on
  the dominant singlet A-note cluster per station-season across Axial, KENE and
  KEMF, excluding AX 2012-13, returns +0.534 s/yr at an R-squared of 0.96
  against a published +0.54 at 0.96. If this stops passing, the measurement
  path has drifted. Established in `notes/probes/06-fig7-reproduction.md`.
- **Selection rules are applied before any peak extraction.** Singlet is
  IPI > 22 s, note A is frequency < 22 Hz, and the archived recipe adds in
  sequence, IPI < 60 s, SNR > 5 dB, sequence length > 10 notes. Both
  distributions are bimodal with the wrong mode taller, so an extraction that
  omits these returns the B note and the doublet interval while looking
  entirely reasonable.
- **Peak extraction is two-dimensional in (frequency, IPI).** Two independent
  one-dimensional histograms are not equivalent and do not reproduce the
  archive.
- **Any frequency comparison between KEMF and the published trend states how
  the station offset was handled.** Axial and KEMF differ by 0.80 Hz in the one
  season both recorded, against a total decadal change of about 1.5 Hz, while
  IPI is identical. A frequency result that does not address this is not
  reportable. IPI requires no such statement.
- **IPI computed by this code from archived detection times matches the
  archive's own `ipi` column.** This tests the measurement stage directly,
  independently of any detector.
- **Every detection timestamp falls inside the time span of the manifest
  window it is attributed to.** Catches both a mis-parsed timestamp and a join
  that put a detection on the wrong retrieval.

## Governance

This constitution supersedes convenience. When a stage spec conflicts with it,
the constitution wins, or it gets amended on purpose and the amendment is
recorded below.

Amendments name what changed and why. A fact that turned out to be wrong is
amended rather than quietly overwritten, because the specs that cited it may
need revisiting.

Two sections are knowingly incomplete at ratification and are tracked as gaps
rather than left to be noticed later: the Whale-VAD checkpoint is not pinned,
and no figure standards exist. Both are named in place above.

**Version**: 1.0.0 | **Ratified**: 2026-09-08 | **Last Amended**: 2026-09-08
