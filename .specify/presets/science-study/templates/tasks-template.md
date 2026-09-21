---

description: "Task list template for a study pipeline, grouped by stage"
---

# Tasks: [STUDY_OR_STAGE_NAME]

**Input**: Stage specifications from `specs/[###-stage-name]/`

**Prerequisites**: The stage spec, with its acceptance checks filled in. A stage
whose checks are still empty is not ready to have tasks written for it.

**Organization**: Tasks are grouped by pipeline stage, and within a stage they
follow a fixed order: write the checks, implement, verify, record.

## Format: `[ID] [P?] [Stage] Description`

- **[P]**: Can run in parallel. Different files, no shared state, neither one
  reads what the other writes.
- **[Stage]**: Which stage spec this belongs to, matching its directory number.
  Example: `S001` for `specs/001-ingest-delivery/`.
- Name exact paths. A task that says "load the data" is not actionable; a task
  that says "read `data/raw/indices/*.csv` into one frame" is.

<!--
  ============================================================================
  The tasks below are EXAMPLES showing the shape. Replace them entirely.

  Stages are not user stories. They are a dependency chain, and each one
  consumes the previous stage's output along with its defects. So the usual
  advice about independent slices that can be built in any order does not
  apply here, and neither does splitting work across people by stage.

  Real parallelism in a study is mostly WITHIN a stage: several inputs read at
  once, several figures drawn from one fitted model, several diagnostics run
  against one output. Mark those [P]. Do not mark two stages [P] because the
  second one's inputs do not exist until the first has run.
  ============================================================================
-->

## Stage S001: [STAGE_NAME]

**Goal**: [STAGE_GOAL]
<!-- One line, taken from the stage spec's Question section. -->

**Status check**: This stage's spec is `active`. If it is `blocked`, stop and
write down what it is blocked on instead of working around it.

### Checks first

<!-- The acceptance checks from the spec become runnable code BEFORE the thing
     they check exists. This is not test-driven development borrowed from
     software for its own sake. It is that a check written after seeing the
     output tends to be a check the output passes. -->

- [ ] T001 [S001] Write AC-001 as a runnable check in [path]
- [ ] T002 [P] [S001] Write AC-002 as a runnable check in [path]
- [ ] T003 [P] [S001] Write the row-accounting check from the spec in [path]

### Implement

- [ ] T004 [S001] [Implementation task with an exact path]
- [ ] T005 [P] [S001] [Another, parallel only if it touches different files]

### Verify

- [ ] T006 [S001] Run every acceptance check and record the numbers, not just
      pass or fail
- [ ] T007 [S001] Confirm a clean rerun reproduces the output
- [ ] T008 [S001] Account for every row lost at a join or filter
- [ ] T009 [S001] Mutation pass. For each invariant and external check, break
      the implementation in ONE small realistic way that violates it, confirm
      the test meant to catch it goes red, restore, and verify the tree is
      clean. Record the break and the result.

<!-- A stage is not done until its mutation pass is recorded. A passing test
     tells you two things agree. It does not tell you the test would have
     noticed if they did not.

     Three results worth acting on. Nothing goes red: that check is unverified.
     A different test goes red but not the intended one: the intended test is
     weak even though the suite caught the break. One test goes red for many
     unrelated mutations: low specificity, worth splitting.

     Measurement checks are exempt, because there is no break that makes a
     measurement wrong. That exemption is exactly why they have to be labelled
     in the spec rather than left to look like invariants. -->

### Record

- [ ] T009 [S001] Fill in the stage spec's Outcome: what happened, what was
      surprising, what changes upstream or downstream
- [ ] T010 [S001] Add any newly discovered input defect to the constitution's
      data sources
- [ ] T011 [S001] Set the stage spec's status to `done`

**Checkpoint**: Outputs exist at the paths the spec promised, every check has a
recorded result, and the Outcome is written. The next stage can now assume this
stage's output schema.

---

## Stage S002: [STAGE_NAME]

<!-- Same four-part shape. Repeat per stage. -->

---

## Dependencies

<!--
  ACTION REQUIRED: Draw the actual chain. Most stages depend on the one before,
  but not all, and the exceptions are worth naming because they are the only
  places where work can genuinely proceed in parallel.
-->

- S001 blocks S002 because [WHAT_S002_CONSUMES]
- [STAGE] does not depend on [STAGE], so they can run in either order

**Blocked stages**: [BLOCKED_STAGES]
<!-- Stages whose specs are `blocked`, and what each is waiting for. Keeping
     these visible stops the pipeline looking more finished than it is. -->

## Notes

- Within a stage, `[P]` means different files and no shared state. Across
  stages it almost never applies.
- Record what a check produced, not only that it passed. A row count in the
  record is worth more later than a green tick.
- A stage that turns out to answer a different question than its spec asked is
  a finding. Write it in the Outcome and leave the spec's original question
  standing, rather than editing the question to match the result.
- Slow stages are worth splitting so that a cheap fix downstream does not force
  an expensive rerun upstream. If a stage takes long enough that you avoid
  rerunning it, that is the signal.
- Avoid: tasks without paths, checks written after the output, and marking two
  stages parallel when the second reads the first one's output.
