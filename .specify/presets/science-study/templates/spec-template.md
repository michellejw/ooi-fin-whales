# Stage Specification: [STAGE_NAME]
<!-- Example: Ingest delivered detections and indices; Fit seasonal GAMMs -->

**Stage directory**: `[###-stage-name]`

**Created**: [DATE]

**Status**: draft

**Input**: "$ARGUMENTS"

<!--
  One stage of the analysis pipeline. A stage is a step that takes named inputs,
  computes something, and writes named outputs that a later stage can consume.

  This is not a software feature. There are no user stories here, and the stages
  are not independent slices you could build in any order. They are a dependency
  chain, and each one inherits the last one's output along with its defects.

  Two sections do work that a software spec has no need for. Status lets a stage
  be blocked, superseded, or abandoned rather than only done. Outcome records
  what actually happened once the work ran. Together they let the record survive
  a result that shows an earlier stage, or the question itself, was wrong. That
  is a finding rather than a failure, and it is usually worth writing about.
-->

## Status *(mandatory)*

Set the Status field above to one of these. Anything other than `draft` or
`active` needs the reason written in Outcome.

| Status | Means |
|---|---|
| `draft` | Being written. Not agreed yet. |
| `blocked` | Cannot be specified or run until something arrives. Name it below. |
| `active` | Agreed, and being implemented. |
| `done` | Implemented, acceptance checks pass, Outcome written. |
| `superseded by [###-stage-name]` | A later stage replaces this one. Outcome says why. |
| `abandoned` | Will not be done. Outcome says why. |

**Blocked on.** [BLOCKING_DEPENDENCY]
<!-- Delete this line unless status is blocked. Name the specific thing you are
     waiting for and who or what provides it, so that its arrival is something
     anyone can recognise. "Waiting on the full index delivery, which sets the
     station and month list" is checkable. "Waiting on data" is not. -->

<!--
  Never delete or rewrite a superseded or abandoned spec. Change its status,
  write its Outcome, and leave the rest as it was. The record of a branch not
  taken is the thing that stops someone re-deriving it in six months, and it is
  often the part that ends up in the methods section.

  A document that quietly stops being true while still reading as authoritative
  does more damage than no document at all.
-->

## Question *(mandatory)*

**What this stage answers.** [STAGE_QUESTION]
<!-- One or two sentences, phrased as a question or a claim you could check.
     Not a task description. "Does index coverage support treating unreviewed
     files as silence?" is a question. "Load the indices files" is a task. -->

**Why this is a separate stage.** [WHY_SEPARATE]
<!-- If the honest answer is that it was convenient, merge it into a neighbour.
     Good reasons: it produces an artifact something else consumes; it can fail
     on its own terms; it is where a real decision gets made; it is slow enough
     that you do not want to rerun what precedes it. -->

## Inputs *(mandatory)*

<!--
  The study constitution holds the external data sources. Do not restate them.
  List what THIS stage consumes, which is usually a previous stage's output plus
  anything new, and record the defects that matter here specifically.
-->

### [INPUT_NAME]

- **Where it comes from.** [INPUT_SOURCE]
  <!-- A previous stage directory, or an external source named in the constitution. -->
- **Shape.** [INPUT_SCHEMA]
  <!-- Format, key columns, one row per what, resolution. -->
- **Defects that matter here.** [INPUT_DEFECTS]
  <!-- Not every known flaw. The ones that could change this stage's answer.
       Mark anything you have not measured as [NEEDS CLARIFICATION: ...] rather
       than guessing, and treat measuring it as part of the stage. -->

## Method *(mandatory)*

**What is computed.** [METHOD_DESCRIPTION]
<!-- Enough that someone could implement it without reading the code. Name the
     library or function where the choice is load-bearing. Skip the parts that
     any competent implementation would do the same way. -->

### Parameters that change the answer

<!--
  ACTION REQUIRED: List every parameter whose value would change the result, and
  the value chosen. This table is what makes the stage reproducible and what a
  methods section is eventually written from.

  A parameter with no justification is fine, as long as it says so. "Default,
  not examined" is honest and useful. A silently chosen value is neither.
-->

| Parameter | Value | Why this value |
|---|---|---|
| [PARAM_NAME] | [PARAM_VALUE] | [PARAM_JUSTIFICATION] |

**Anything random.** [RANDOMNESS]
<!-- Name the seed and where it is set, or write "nothing random here". A blank
     leaves the next reader unable to tell which one it was. -->

## Outputs *(mandatory)*

### [OUTPUT_NAME]

- **Path.** [OUTPUT_PATH]
- **Shape.** [OUTPUT_SCHEMA]
  <!-- Format, columns with types and units, one row per what. Downstream stages
       cite this, so it is a contract rather than a description. -->
- **Regenerable from.** [OUTPUT_PROVENANCE]
  <!-- The script plus the inputs plus the parameter set above. If an output
       cannot be regenerated, say so and explain why, because the constitution
       says every number traces to its inputs. -->

## Acceptance checks *(mandatory)*

<!--
  ACTION REQUIRED: Write these as checks that pass or fail, and write them
  BEFORE implementing. The question to answer is not "how would I know this
  worked" but "how would I find out this was wrong".

  Every check carries a kind, because only two of the three can be written
  before the code exists. Getting this wrong is the most common way a study
  ends up with a green suite that proves nothing.

    invariant   Must hold regardless of what the data turns out to contain.
                Row counts survive a join, keys are unique, no timestamp falls
                outside the window. Write it first. Watch it fail.

    external    An expected value taken from a source OUTSIDE this pipeline: a
                collaborator's own report, a published figure, an instrument
                spec. Write it first. Watch it fail. These are the strongest
                checks you will ever have, because nothing in your code can
                bend them.

    measurement Something you cannot know until you look. Which formats appear,
                what the coverage is, how many rows fall in a gap. THIS IS NOT
                A TEST. It is an output. It belongs in the run log and in
                Outcome. Writing it as an assertion after seeing the answer
                produces something that looks exactly like an invariant, passes
                exactly as green, and can never fail.

  A measurement may later be pinned as a regression guard, to catch drift. Mark
  it `regression guard (pins the 2026-09-21 measurement)` so no one mistakes it
  for evidence the code is correct.

  Every claim in this spec that could be false needs a check. Those live in the
  parameter table's "Why this value" column, each input's "Defects that matter
  here", and the row-accounting line below. A claim with no check is either a
  check you owe or a claim you should delete.

  EVERY invariant and external check also names its MUTATION: the one small
  break that should make it fail, and the test expected to go red. Write it here
  with the check, before the code exists. Naming the break forces you to answer
  "how would this check fail" while you are writing the check, rather than after
  seeing output that already passes.

  A measurement check has no mutation, because there is no break that makes a
  measurement wrong. If you cannot name one, you have found a check that is not
  a test. That is the point of the field, not a gap in it.

  An invariant or external check with an empty Mutation line is an unverified
  row. The result of actually running it goes in Outcome.
-->

- **AC-001** *(invariant)*: [ACCEPTANCE_CHECK]
  - **Mutation**: [THE_BREAK]. Expect [TEST_NAME] to go red.
  <!-- Example check: every input row appears exactly once in the output, or in
       the dropped-rows log with a reason.
       Example mutation: change the per-file row count to len(df) - 1. -->
- **AC-002** *(external)*: [ACCEPTANCE_CHECK]
  - **Mutation**: [THE_BREAK]. Expect [TEST_NAME] to go red.
  <!-- Example check: per-instrument row counts match the figures in the
       provider's own summary report.
       Example mutation: relabel one row's instrument after the parse. -->
- **AC-003** *(measurement)*: [ACCEPTANCE_CHECK]
  - **Mutation**: none. A measurement cannot be broken into being wrong.
  <!-- Example: which filename formats actually occur. Not knowable until the
       data is read, so this is an output, not a test. It belongs in the run log
       and in Outcome. -->

**Rows that disappear.** [ROW_ACCOUNTING]
<!-- Any join or filter here that can drop rows: say how many you expect to
     lose and why. An unexplained drop is the single most common way a result
     turns out to be about a subset nobody meant to select. -->

## In plain language *(mandatory)*

[PLAIN_LANGUAGE_LINE]
<!-- One or two sentences on what this stage would tell someone outside the
     field. Not a summary of the method. What the reader learns, or what becomes
     possible, because this stage ran.

     It costs a sentence while the work is fresh, and it accumulates into the
     raw material for talks, abstracts, and anything written for a general
     audience. Written afterwards from the code, it is much harder. -->

## Outcome
<!--
  Left empty until the stage has run. Then fill it in, including when everything
  went as expected, because "no surprises" is itself worth recording.
-->

**What happened.** [OUTCOME_SUMMARY]
<!-- Did the checks pass? What did the numbers turn out to be? -->

**Mutation pass.** [OUTCOME_MUTATIONS]
<!-- One line per invariant and external check: the break applied, and whether
     the expected test went red. Three results are worth acting on rather than
     recording and moving past.

       Nothing went red. That check is unverified. Fix the test, not the record.
       A different test went red. The intended test is weak even though the
         suite happened to catch the break.
       One test goes red for many unrelated mutations. Low specificity, split it.

     This section is how a later reader knows which failure modes were probed.
     Without it, adding AC-010 next month tells you nothing about whether the
     suite was ever tested nine ways or zero. -->

**What was surprising.** [OUTCOME_SURPRISES]
<!-- The things you did not predict. This is the section most likely to end up
     in the paper, and the one most easily lost if it is not written down while
     it is still surprising. -->

**Does this change anything upstream.** [OUTCOME_UPSTREAM]
<!-- The section that lets a stage fail backward. If the result shows an earlier
     stage was wrong, or that the question was the wrong question, say so here
     and name the stage. That is a finding, not a failure. Do not go back and
     quietly edit the earlier spec; amend its status and let it keep its record. -->

**What this changes downstream.** [OUTCOME_DOWNSTREAM]
<!-- Anything a later stage must now assume, avoid, or handle. New defects
     discovered here belong in the constitution's data sources too. -->

**Which branch was taken.** [OUTCOME_BRANCH]
<!-- Only if there was a fork. Name the option chosen, the options left, and
     why. Leaving this blank when a real choice was made is how a study ends up
     unable to explain itself later. -->
