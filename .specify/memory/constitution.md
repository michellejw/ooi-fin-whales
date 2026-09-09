# [PROJECT_NAME] Constitution
<!-- Example: Pacific Indices Constitution, Fin Whale Detection Constitution -->

<!--
  This is the study's standing record of facts and commitments. Everything a
  stage spec can assume without restating lives here.

  The principles below are fixed. Everything else is a slot for you to fill.
  That split is deliberate: the principles hold in any study that uses this
  preset, while the slots are where studies actually differ from one another.

  Fill it once at the start, amend it when a fact changes, and record the
  amendment. A constitution that silently drifts is worse than none, because
  the specs beneath it go on citing something that is no longer true.
-->

## What this study is

**Question.** [RESEARCH_QUESTION]
<!-- One or two sentences. The question the study answers, not the methods used. -->

**Deliverable.** [DELIVERABLE]
<!-- Example: a methods paper in Methods in Ecology and Evolution; a chapter; an internal report plus figures -->

**Who does what.** [DIVISION_OF_LABOUR]
<!-- Name the collaborators and what each one produces. Say explicitly which
     inputs arrive from someone else, because those set the input contract and
     you cannot change them unilaterally. -->

## Core Principles

<!--
  Do not edit or delete these per project. If one genuinely does not fit the
  study in front of you, that is worth a conversation and an amendment note,
  not a silent removal.
-->

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

<!--
  One entry per input. Fill the defects line even when it says "none known" so
  that a blank is unambiguous. If an input arrives from a collaborator, say who
  and in what format, because changing it means asking them.
-->

### [SOURCE_NAME]
<!-- Example: Acoustic indices from OSA; FDSN broadband waveforms; ERDDAP satellite covariates -->

- **What it is.** [SOURCE_DESCRIPTION]
- **Who produces it.** [SOURCE_OWNER]
- **Shape and resolution.** [SOURCE_SCHEMA]
  <!-- Format, key columns, one row per what, temporal and spatial resolution. -->
- **Version pinned.** [SOURCE_VERSION]
  <!-- A date, a DOI, an archive snapshot, a commit. If the upstream source is
       being revised while the study runs, this is the field that decides
       whether results are comparable later. Record the decision to pin or to
       recompute, and say which was chosen. -->
- **Known defects.** [SOURCE_DEFECTS]
  <!-- Gaps, duplicates, naming irregularities, values that are missing versus
       values that are genuinely zero. Measured numbers beat impressions. -->

### Record of examination

[EXAMINATION_RECORD]
<!-- Principle IV made concrete. Which input tells you what was examined, as
     distinct from what was found? Name the file or the field. If no such
     record exists yet, say so plainly and treat obtaining it as a blocking
     input rather than a detail, because nothing downstream can be a rate
     without it. -->

## Technical environment

**Runtimes.** [RUNTIMES]
<!-- Example: Python via uv, R via renv. Say what each is used for and why both
     are needed, if both are. -->

**Pipeline form.** [PIPELINE_FORM]
<!-- Staged scripts, or notebooks. This is a real fork: it changes what a stage
     spec's outputs look like and how a rerun is triggered. Pick one and say it. -->

**Where outputs go.** [OUTPUT_LAYOUT]
<!-- The directory convention for models, tables, figures and logs. -->

## Conventions

**Units and coordinate systems.** [UNITS_AND_CRS]
<!-- Include the reference for anything in decibels, since the reference is what
     makes the number meaningful. -->

**Time.** [TIME_CONVENTIONS]
<!-- UTC is the default under Principle V. Record any place local or solar time
     is used, and the parsing rules for any timestamp format that has bitten you. -->

**Naming.** [NAMING_CONVENTIONS]
<!-- Write down the conventions a reader needs in order to find things: script
     names, output names, anything with a pattern worth relying on. This is the
     right place for them, and leaving it blank helps nobody.

     They belong here rather than under Core Principles because a principle is
     something you would defend when it becomes inconvenient, and a convention
     is something you would happily swap for a better one. Filing a convention
     as a principle makes a cheap decision expensive to change, and it teaches
     readers that the principles list is not load-bearing.

     One practical caution, not a rule: script names that encode stage numbers
     desync the first time a stage is inserted, dropped or superseded, which
     this workflow expects to happen. The numbered spec directories already
     carry that ordering, so the scripts do not have to. -->

## Figure standards

[FIGURE_STANDARDS]
<!-- Palette, font sizes, dimensions, format, colour-vision safety, and where
     figures are written. Enough that two figures made months apart match. -->

## How this project works

**Decision record.** [DECISION_RECORD_LOCATION]
<!-- Where decisions and their reasons are written down, and what belongs there
     as opposed to in a stage spec's Outcome section. -->

**Work tracking.** [WORK_TRACKING]
<!-- Default is none: stage specs in numbered directories are the whole record,
     which is all a study needs and all a newcomer should have to learn.
     Set this to issues and the assistant creates and closes an issue per stage
     spec, numbered to match its directory, so the map stays current as a side
     effect of the work rather than as a chore. Choosing issues does not mean
     you type git commands. -->

**Voice.** [VOICE_GUIDE]
<!-- Point at whatever writing guidance you already keep, rather than restating
     its rules here, so that the two cannot drift apart. That might be a file in
     this repo, a note in your own reference system, or a shared house style.
     If there is none, say so, and the plain-language line in each stage spec is
     written in whatever voice the study's audience needs. -->

## Quality gates

<!-- These are checks that must pass, not aspirations. Add study-specific ones;
     do not remove the first three, which restate Principles I through III in a
     form you can actually run. -->

- A clean rerun reproduces every number in the current results.
- Every figure and table traces to a script, an input, and a parameter set.
- Raw data is unmodified since acquisition.
- Row counts survive every join, and every dropped row is accounted for
  deliberately rather than by default.
- [STUDY_SPECIFIC_GATES]
  <!-- Write these as checks someone could run and get a pass or fail from, not
       as statements of intent.

       Example: every model converges before anything downstream of it runs.
       Example: every index value falls inside the range documented for it.
       Example: every detection timestamp falls inside the time span of the
       recording it is attributed to, which catches both a mis-parsed timestamp
       and a join that put a detection on the wrong file. -->

## Governance

This constitution supersedes convenience. When a stage spec conflicts with it,
the constitution wins, or it gets amended on purpose and the amendment is
recorded below.

Amendments name what changed and why. A fact that turned out to be wrong is
amended rather than quietly overwritten, because the specs that cited it may
need revisiting.

[GOVERNANCE_NOTES]

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
