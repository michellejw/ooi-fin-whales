# [CHECKLIST_TYPE] Checklist: [STUDY_OR_STAGE_NAME]

**Purpose**: [CHECKLIST_PURPOSE]
**Created**: [DATE]
**Covers**: [Link to the stage spec, or the whole pipeline]

**Marker semantics**: `[x]` means someone ran the check and it passed, on the
current outputs. It does not mean the check exists, is planned, or passed last
month. If the outputs have changed since, the marks are stale and the honest
move is to clear them and rerun.

<!--
  ============================================================================
  This checklist is about scientific correctness, not feature completeness. It
  asks whether the results are right and whether anyone else could get them
  again, which is a different question from whether the work is finished.

  That is a deliberate departure from the stock checklist, which reviews the
  quality of requirements before implementation. Items here are checked against
  outputs that exist.

  The items below are the standing ones. Keep them. Add study-specific items in
  their own category at the end, taken from the stage specs' acceptance checks.
  ============================================================================
-->

## Raw data

- [ ] CHK001 Raw inputs are unmodified since acquisition, verified rather than
      assumed. A checksum or an untouched read-only copy counts; remembering
      that nobody edited them does not.
- [ ] CHK002 Every input is pinned to a version, a date, or a snapshot, and the
      pin is recorded in the constitution.
- [ ] CHK003 Where an upstream source is being revised while this study runs,
      the decision to pin or to recompute is written down, with its date.

## Reproducibility

- [ ] CHK004 A clean rerun from raw inputs reproduces the current numbers. Not
      approximately, and not only the numbers someone happened to look at.
- [ ] CHK005 Every source of randomness has a seed that is fixed and recorded
      in the stage spec that uses it.
- [ ] CHK006 The runtime environment is captured well enough to rebuild, with
      versions pinned rather than floating.

### Reproducibility rungs

<!--
  ACTION REQUIRED: State the ladder for this study, then place every output on
  it. A rung is a level someone else could start from, and its cost is what
  decides whether they will actually try.

  Example from a related study:
    Rung 1, replot from committed results: seconds, no download.
    Rung 2, re-aggregate from the archived per-unit tables: minutes, 40 MB.
    Rung 3, re-detect from raw audio: days, 73 GB.

  The point of naming rungs is that "reproducible" is not one thing. An outside
  reader who can redraw your figures in seconds is in a different position from
  one who would need a week of compute, and a paper that does not say which is
  available is making a claim it has not earned.
-->

- [ ] CHK007 The rungs are stated, each with what it starts from and what it
      costs in time and data volume.
- [ ] CHK008 Every output names the rung it sits on.
- [ ] CHK009 The lowest rung actually works, tested from a clean checkout by
      someone following only the written instructions.

## Provenance

- [ ] CHK010 Every figure traces to a script, its inputs, and a parameter set.
- [ ] CHK011 Every number quoted in prose traces the same way, including ones
      in an abstract or a summary.
- [ ] CHK012 No output exists whose generating code has since changed without
      the output being regenerated.

## Counts and coverage

- [ ] CHK013 Row counts survive every join, and every dropped row is accounted
      for deliberately rather than by default.
- [ ] CHK014 The record of what was examined is present and distinguishable
      from the record of what was found, so that a genuine zero and an absence
      of looking are not being treated as the same value.
- [ ] CHK015 Coverage is stated as a measured fraction rather than assumed to
      be complete.
- [ ] CHK016 Values that are missing are distinguishable from values that are
      genuinely zero, everywhere it matters.

## The written record

- [ ] CHK017 Every stage spec's status is current, including the ones that were
      superseded or abandoned.
- [ ] CHK018 Every completed stage has its Outcome written, including the ones
      where nothing surprising happened.
- [ ] CHK019 No document still reads as authoritative while describing a branch
      that was not taken.
- [ ] CHK020 Defects discovered mid-study were added to the constitution's data
      sources, not left in the stage spec that found them.

## [STUDY_SPECIFIC_CATEGORY]

<!-- Items drawn from the stage specs' acceptance checks, and anything this
     particular study can get wrong that a general checklist would not catch. -->

- [ ] CHK021 [STUDY_SPECIFIC_ITEM]

## Notes

- Mark an item `[x]` only after running the check against current outputs.
- An item that cannot be checked yet stays unchecked. Do not mark it and add a
  caveat, because the caveat will be read later as a passing mark.
- Record what a check produced, not only that it passed. A coverage fraction is
  worth more in six months than a tick.
- An item that fails is information. Write what failed and what it means into
  the relevant stage spec's Outcome rather than fixing it silently.
