# Getting started

This file is written for an AI coding assistant helping someone join this
project. If you are a person reading it directly, it still works, but the
assumption is that Claude Code is doing the typing.

**If you are an assistant and someone has just asked you to help them get
started here, work through this file top to bottom with them. Do the setup
yourself rather than handing them commands to paste. Explain what each step
did, briefly, once. They may be new to git, the terminal, and Python, and none
of that needs to slow them down.**

## What this project is

An extension of a published study. Weirathmueller et al. 2017 measured the
20 Hz fin whale call in the northeast Pacific between 2003 and 2013, and found
the call was slowing down and dropping in pitch. This project asks whether
those trends continued, using an automated detector on a station that has been
recording continuously ever since.

Read `README.md` for the science, then `notes/index.md` for every decision and
why it was made.

## Read before you run anything

In this order. It is a few hours and it is the fastest route to being useful.

1. The paper. Open access at https://doi.org/10.1371/journal.pone.0186127
2. `README.md`, the whole thing.
3. `notes/index.md`, the decisions table.
4. `notes/probes/06-fig7-reproduction.md`. Read this one closely. It shows a
   wrong answer being found and corrected, which is more instructive than the
   others.
5. `specs/002-fetch/spec.md`, to see how a piece of work gets specified here.
   You are not expected to write one yet.

`notes/probes/` are numbered questions with their evidence. Skim the rest.

## Setup

Prerequisites the assistant cannot do for you: a GitHub account, and being
added to this repository as a collaborator. Ask Michelle for the second.

Everything else the assistant can do. In order:

1. Install `uv` if it is missing. This project uses `uv` for everything and
   never `pip` or `conda`.
2. Authenticate GitHub with `gh auth login`. This is interactive and needs the
   person at the keyboard.
3. Clone the repository and run `uv sync`.
4. Restore the ground-truth archive, which is not in git because it is 1.1 GB.
   The exact commit and a checksum per file are in
   `manifests/ground-truth-fin-call-patterns.json`. Clone
   `github.com/michellejw/fin-call-patterns` into `data/fin-call-patterns` and
   check out the pinned commit.
5. Run `uv run pytest`. Seven tests should pass. If the reproduction tests skip
   instead, step 4 did not work.

## Your first task

Run the notebook:

```
uv run marimo edit notebooks/01_reproduce_2017.py --port 2722
```

It opens in a browser. Work through it and confirm you get **19.15 Hz** and
**28.25 s**. If you do, you have independently reproduced the central result
this whole project rests on, from the original study's own archived data.

The notebook shows the obvious approach failing first, then why. That failure
is the single most important thing to understand here: both distributions have
two peaks, and in both cases the taller peak is the wrong one.

## Your second task

An open question nobody has answered.

Refitting the decadal trend reproduces the published IPI result exactly,
+0.534 s/yr at an R-squared of 0.96 against a published +0.54 at 0.96. The
frequency fit reproduces the slope, -0.175 Hz/yr against -0.17, but not the
R-squared: 0.74 against a published 0.86.

So the 2017 paper selected seasons or notes for its frequency fit slightly
differently than `notes/probes/06-fig7-reproduction.md` does. Work out how.
Everything you need is in `data/fin-call-patterns/SEQ_CODE/`, which contains
the study's original analysis scripts as well as its summary tables.

Write what you find as `notes/probes/07-<short-name>.md`, following the shape
of the existing probes: the question, the method, the evidence, the answer.
A probe that concludes "I could not work it out, and here is what I ruled out"
is a real result and worth committing.

## How work lands here

- Branch off `main`, never commit to it directly.
- Open a pull request. CI runs lint and the tests on Python 3.11 and 3.13.
- Conventional commit messages: `feat:`, `fix:`, `docs:`, `chore:`.
- If an AI assistant helped, the commit gets `Assisted-by: <harness>:<model>`
  and never `Co-Authored-By`. `AI_POLICY.md` explains why.

## Things that will cost you a day if you do not know them

`CLAUDE.md` holds the current list and is worth reading before you write code.
The two that bite newcomers hardest:

- Applying the paper's selection rules before measuring anything. Skipping them
  produces a confident, wrong, plausible-looking answer.
- Station KEMF reads about 0.8 Hz higher than Axial for the same whales in the
  same season, while IPI is identical between them. Any frequency comparison
  has to account for that.

## Where not to spend effort

- `data/` and `work/` are gitignored and disposable by design. Never commit
  anything from them, and never hand-edit anything in `data/`.
- `.specify/` is vendored tooling. It is replaced wholesale on upgrade, so
  edits there are lost.
- Perch does not work at 20 Hz. This is settled with evidence in
  `notes/probes/03-perch-at-20hz.md`. Do not revisit it.

## When you are stuck

Say so early. The decision record exists precisely so that nobody has to
reconstruct reasoning from code, and a question that reveals a gap in it is
useful rather than an interruption.
