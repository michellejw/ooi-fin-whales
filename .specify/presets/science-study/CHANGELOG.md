# Changelog

## 0.2.0 (2026-09-21)

Testing rules, adapted for analysis work rather than copied from software TDD.

- **spec-template**: every acceptance check now declares a kind. `invariant` and
  `external` must be written before the code and watched to fail. `measurement`
  is not a test at all, it is an output, and belongs in the run log and Outcome.
  A measurement pinned afterwards is a regression guard and must say so, because
  it looks identical to an invariant and passes just as green while proving
  nothing.
- **spec-template**: states where a spec's falsifiable claims live, so the rule
  "every claim gets a check" is actionable: the parameter table's "Why this
  value", each input's "Defects that matter here", and the row-accounting line.
- **tasks-template**: adds T009, a mutation pass. A stage is not done until it is
  recorded. Break the implementation in one small realistic way, confirm the
  intended test goes red, restore, verify the tree is clean.

Why: a passing test tells you two things agree, not that the test would have
noticed if they did not. On a sibling project, five tests were found that could
not fail, each because the fixture was symmetric under the exact transformation
being tested. One had been hand-verified by a human. Verifying test logic by hand
is not verifying test power.

Companion issues on `acoustic-workbench-animat`: #304 (a test must exist for
every claim) and #310 (a test must be able to fail).

## 0.1.0

Initial preset: four templates and the `speckit.pipeline` command.
