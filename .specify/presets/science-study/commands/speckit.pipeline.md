---
description: Turn a research question into a dependency-ordered list of pipeline stages, and seed one stage spec per stage.
handoffs:
  - label: Specify the first stage
    agent: speckit.plan
    prompt: Work up the method for the first unblocked stage.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## What this command is for

Stock spec-driven development assumes you arrive knowing what you are building.
A study does not work that way. The hard part comes before any single spec:
turning a research question into an ordered list of stages, where each stage
consumes the previous one's output.

This command does that. It interviews the researcher, proposes a stage list in
dependency order, marks which stages can be specified now and which are waiting
on something, and seeds one spec directory per stage.

It is deliberately conservative about what it fills in. A stage list is cheap to
revise; a spec full of invented parameter values is worse than an empty one,
because it reads as a decision someone made.

## Outline

### 1. Read what already exists

- If `.specify/memory/constitution.md` exists, read it. The data sources, their
  defects, and the technical environment are recorded there and must not be
  restated in stage specs.
- If `specs/` already contains stage directories, read their specs. This command
  can extend an existing pipeline. Do not renumber or rewrite existing stages.

### 2. Interview

Four things need answering. Ask them in two short rounds of two, and wait for
each round before asking the next. Do not present all four at once. A person
being asked four questions in one message tends to answer the easy ones and
lose the hard ones, and the hard ones are the ones that shape the pipeline.

**Round one, where the study is going:**

1. **What is the question?** The thing the study answers, not the methods used.
2. **What is the final artifact?** A paper, a report, a set of figures, a
   dataset. The stage list is built backwards from this.

**Round two, what it has to work with:**

3. **What data exists, and what is promised?** Distinguish the two clearly. Data
   that is promised but not in hand is the main source of blocked stages, and
   who is providing it matters as much as what it is.
4. **What modeling is anticipated?** Approximate is fine. "Probably GAMMs with a
   seasonal term" is enough to know a modeling stage exists and roughly what it
   consumes.

If the user's input already answers some of these, do not ask again. Say what
you took from it and ask only what is missing. If that leaves one question,
ask the one.

### 3. Propose the stage list

Work backwards from the final artifact. For each stage, name it, say what it
consumes and produces, and say why it is separate from its neighbours.

**What makes a stage boundary.** Any one of these is enough:

- It writes an artifact that something else reads.
- It is where a real decision gets made, such as a join policy or a bin width.
- It can fail on its own terms, so you would want to know it succeeded before
  building on it.
- It is expensive enough that you would not want to rerun what precedes it.

**What is not a stage boundary.** One script is not one stage. Neither is one
day of work, one person's contribution, or a convenient place to stop.

Aim for something between four and twelve stages. Fewer suggests stages are
hiding inside each other. More usually means scripts are being listed.

### 4. Mark each stage specifiable or blocked

This is the part with no equivalent in software work, and it must not be
skipped.

For each stage, decide whether it can be specified now. A stage is **blocked**
when its inputs, its method, or the decision it turns on depends on something
that has not arrived. Name the blocker specifically enough that its arrival is
something anyone could recognise.

Blocked stages stay in the list. Do not drop them and do not merge them into a
neighbour to avoid the problem. The shape of the pipeline is information even
where the detail is missing, and a list that shows only the specifiable stages
makes the study look further along than it is.

Present the proposed list to the user and get agreement **before creating any
directories**. Show it as a table: number, stage name, consumes, produces,
status, and what it is blocked on.

### 5. Seed one spec per stage

Only after the user agrees to the list.

For each stage, in dependency order:

- Determine the next directory number using the same rule the specify command
  uses: read `.specify/init-options.json` for `feature_numbering`, use a 3-digit
  sequential prefix when it is `sequential` or absent, and a timestamp prefix
  when it is `timestamp`. Numbering follows dependency order, so stage 001 is
  the first thing that runs.
- `mkdir -p specs/<prefix>-<short-name>`
- Resolve the active `spec-template` through the preset stack, the equivalent of
  `specify preset resolve spec-template`, and copy it to
  `specs/<prefix>-<short-name>/spec.md`.

Then fill in each seeded spec, and **only** these parts:

| Section | Fill it? |
|---|---|
| Status | Yes. `draft` if specifiable, `blocked` if not. |
| Blocked on | Yes, when blocked. Delete the line otherwise. |
| Question | Yes. Both the question and why it is a separate stage. |
| Inputs | Yes, where the source is known. Reference the constitution rather than restating it. |
| Method | Only a one-line sketch. Leave the parameters table empty. |
| Outputs | Path and rough shape only, if known. |
| Acceptance checks | No. Leave the placeholders. |
| Plain language | No. |
| Outcome | No. It is written after the stage runs. |

**Do not invent parameter values.** A bin width, a threshold, a filter cutoff or
a model family written into a spec by this command will later be read as a
choice someone made for a reason. Leave the parameters table empty and let the
stage's own specification fill it.

Use `[NEEDS CLARIFICATION: specific question]` for anything load-bearing that
you could not resolve, at most three per spec.

### 6. Point the tooling at the first stage

Write `.specify/feature.json` naming the first stage that is not blocked, so
that the next command has a target:

```json
{
  "feature_directory": "specs/001-<short-name>"
}
```

Write the resolved path, not the literal placeholder. If every stage is blocked,
skip this and say so in the report.

## Completion Report

Report to the user:

- The stage table as agreed, with each stage's directory path.
- How many stages are specifiable now and how many are blocked.
- For each blocked stage, the one thing that would unblock it, gathered into a
  single list. This list is the study's real critical path and is usually the
  most useful output of this command.
- Which stage `.specify/feature.json` now points at.
- The suggested next step: work up the method for the first unblocked stage.

## Guidelines

- The interview is four questions asked two at a time, not an interrogation and
  not a form. If the user has already written a design document or a proposal,
  read it and confirm rather than ask.
- This applies past the interview. Anywhere later in this command where you need
  something from the user, ask for one or two things and wait. Batching questions
  to save round trips costs more than it saves, because the answers come back
  thinner.
- Stages are a chain, not a backlog. Order matters, and the numbering carries it.
- A blocked stage with a vague blocker is barely better than a missing stage.
  "Waiting on data" is not a blocker. "Waiting on the station and month list,
  which sets the cross-validation blocks" is.
- Resist proposing a stage per script. The unit is a question answered and an
  artifact produced.
- When the study already has a pipeline and this command is being used to extend
  it, leave the existing numbering alone. A renumbered stage breaks every
  reference to it.

## Done When

- [ ] The four interview questions are answered, asked no more than two at a
      time, from the user or from a document they pointed at.
- [ ] A dependency-ordered stage list was presented and agreed before any
      directory was created.
- [ ] Every stage has a directory and a seeded spec.
- [ ] Every stage's status is `draft` or `blocked`, and every blocked one names
      a specific blocker.
- [ ] No parameter values were invented.
- [ ] `.specify/feature.json` points at the first unblocked stage, or the report
      says why it does not.
