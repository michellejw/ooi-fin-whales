# Stage Specification: Fetch waveforms and record what was retrieved

**Stage directory**: `002-fetch`

**Created**: 2026-09-08

**Status**: draft

**Input**: "Retrieve NV.KEMF EHZ waveform data for the target seasons and write a manifest per retrieval."

## Status *(mandatory)*

| Status | Means |
|---|---|
| `draft` | Being written. Not agreed yet. |
| `blocked` | Cannot be specified or run until something arrives. Name it below. |
| `active` | Agreed, and being implemented. |
| `done` | Implemented, acceptance checks pass, Outcome written. |
| `superseded by [###-stage-name]` | A later stage replaces this one. Outcome says why. |
| `abandoned` | Will not be done. Outcome says why. |

## Question *(mandatory)*

**What this stage answers.** Can the waveform data for a named station-season
be retrieved reproducibly, and does the retrieved audio line up in time with
the archived 2017 detections?

**Why this is a separate stage.** It produces the artifact every later stage
consumes, it fails on its own terms (a gap in the record, a station identity
error, a timing convention mismatch), and it is slow enough that nothing
downstream should trigger a refetch. It is also where the timing convention is
verified against ground truth, which is the cheapest place to catch it: if
detection times from the archive do not land on visible calls in the fetched
spectrogram, everything downstream is measuring the wrong seconds.

## Inputs *(mandatory)*

### FDSN waveform service

- **Where it comes from.** EarthScope FDSN, network NV, station KEMF, channel
  EHZ. Named in the constitution.
- **Shape.** miniSEED, read as obspy Streams. 100 Hz before 2013-03-01, 200 Hz
  after.
- **Defects that matter here.** The client short name `IRIS` is deprecated in
  obspy and must be `EARTHSCOPE`; the same rename 307-redirects on the web
  service, so any direct HTTP call needs `-L`. Gaps in the returned Stream are
  expected and are data, not errors: they must be recorded rather than
  silently concatenated over. [NEEDS CLARIFICATION: the actual gap structure at
  KEMF across the target seasons has not been measured. Measuring it is part of
  this stage.]

### Archived detections for the same station-season

- **Where it comes from.** `data/fin-call-patterns/DETECTION_DATA/`, pinned in
  `manifests/ground-truth-fin-call-patterns.json`.
- **Shape.** One row per note. `dettime` is datetime64[ns] UTC.
- **Defects that matter here.** None for this use. Only `dettime` is consumed,
  and only to check alignment.

## Method *(mandatory)*

**What is computed.** For each requested station-season, request the waveform
in bounded chunks through `obspy.clients.fdsn.Client("EARTHSCOPE")`, write the
returned data to `data/`, and write one manifest JSON per retrieval to
`manifests/` recording network, station, channel, requested and actually
returned time spans, the response epoch in force, sample rate, any gaps, the
code version, and the retrieval timestamp. No filtering, no resampling, no
response correction: this stage stores what the service returned.

Alignment is then verified for one window per season by overlaying the archived
`dettime` values on a spectrogram of the fetched audio.

### Parameters that change the answer

| Parameter | Value | Why this value |
|---|---|---|
| Client | `EARTHSCOPE` | `IRIS` is deprecated in obspy and warns; `filterwarnings = ["error"]` turns that into a test failure. |
| Season window | 1 Nov to 31 Mar | Matches the archive's season convention, which dates each season to its November. |
| Chunk length | [NEEDS CLARIFICATION: not chosen. Pick from what the service tolerates without timing out, then record it.] | |
| Response correction | None | The constitution and `notes/probes/05-instrument-response.md`: the 2017 study applied none, and KEMF's response is flat to 0.20 dB across the band. |
| Merge/fill of gaps | None. Gaps recorded, not filled | Filling would invent samples and make a coverage gap indistinguishable from silence, which Principle IV forbids. |

**Anything random.** Nothing random here.

## Outputs *(mandatory)*

### Raw waveform cache

- **Path.** `data/<station>/<season>/` (gitignored)
- **Shape.** miniSEED as returned by the service, one file per chunk.
- **Regenerable from.** The matching manifest, replayed against the same
  service. Not byte-reproducible if the upstream archive is ever revised, which
  is what the manifest exists to detect.

### Retrieval manifest

- **Path.** `manifests/fdsn-<network>.<station>.<channel>-<season>.json`
- **Shape.** JSON with `kind: "fdsn-pull"`, network, station, channel,
  requested span, returned span, sample rate, response epoch, gap list as
  (start, end) pairs in UTC, code version, retrieval timestamp.
- **Regenerable from.** Nothing. This IS the provenance record, and it is
  committed for that reason.

## Acceptance checks *(mandatory)*

- **AC-001**: Every fetched file is covered by exactly one manifest, and every
  manifest names files that exist. No orphans in either direction.
- **AC-002**: The manifest's returned span plus its gap list accounts for the
  full requested span, with no unexplained seconds. This is the row-accounting
  check in time rather than in rows.
- **AC-003**: The sample rate recorded in the manifest matches the sample rate
  of the data on disk, and matches the FDSN response epoch for that date. This
  catches a mislabelled 2013-03-01 boundary.
- **AC-004**: For a KEMF 2011-2012 or 2012-2013 window, archived `dettime`
  values fall on visible energy in the spectrogram of the fetched audio. This
  verifies the fetch path, the timing convention and station identity together,
  against ground truth the study produced itself. It is the check this stage
  exists for.
- **AC-005**: Refetching a window already fetched produces the same data and a
  manifest differing only in retrieval timestamp.

**Rows that disappear.** No joins here. Time can disappear, and that is what
AC-002 guards: any second in the requested span is either in the returned data
or in the gap list, never missing from both.

## In plain language *(mandatory)*

This step pulls the raw underwater recordings off a public archive and writes
down exactly what was asked for and what came back, including the silences.
That record is what makes it possible, years later, to prove which sounds the
conclusions were drawn from.

## Outcome

Not yet run.
