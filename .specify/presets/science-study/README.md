# speckit-preset-science-study

A [spec-kit](https://github.com/github/spec-kit) preset that adapts spec-driven
development to a scientific analysis study.

Spec-kit is built around software features: independent slices, buildable in any
order, each one a branch and a spec. An analysis pipeline is not that. Its stages
are a dependency chain, each consuming the previous stage's output along with its
defects, and a stage can fail backward by showing that an earlier stage, or the
question itself, was wrong. This preset replaces the parts of the vocabulary that
assume the software shape.

## What it provides

| Kind | Name | Replaces |
|---|---|---|
| template | `constitution-template` | Study facts: data sources and their defects, runtimes, units, figure standards, how work is tracked |
| template | `spec-template` | One pipeline stage: question, inputs, method, outputs, acceptance checks, outcome |
| template | `tasks-template` | Tasks grouped by stage, in a fixed rhythm of checks, implement, verify, record |
| template | `checklist-template` | Scientific correctness gates rather than feature completeness |
| command | `speckit.pipeline` | New. Turns a research question into a dependency-ordered stage list |

`plan-template` is deliberately not overridden. A stage's plan is its method
section, and the stock template does no harm there.

## Install

Requires spec-kit 1.0 or later. Pass the preset to `init` by local path, in the
same command, so the constitution is seeded from this preset's template:

```bash
specify init --here --integration claude --preset /path/to/speckit-preset-science-study
specify preset resolve spec-template          # should print a path under .specify/presets/science-study/
```

Do not `init` first and add the preset afterwards. `init` writes
`.specify/memory/constitution.md` from the core template, and `preset add` does
not replace it, even when the file is missing. Verified on 1.0.5: only the
`--preset` flag on `init` seeds the constitution from an installed preset.

The install copies the directory rather than linking it, so after editing the
source you need to reinstall:

```bash
specify preset remove science-study
specify preset add --dev /path/to/speckit-preset-science-study
```

With the Claude integration, commands install as skills under
`.claude/skills/`, so the pipeline command is invoked as `/speckit-pipeline`
with a hyphen, matching the core ones.

**After installing, check for a broken submodule link before your first
commit.** `--dev` copies this directory including its own `.git`, so a plain
`git add` in the consuming project records `.specify/presets/science-study` as
a gitlink (mode `160000`) rather than committing the files. A clone then gets
an empty preset directory, silently missing every override, with no error.
Found 2026-09-08 in `pacific-indices`. Fix before committing:

```bash
rm -rf .specify/presets/science-study/.git
git rm --cached -r .specify/presets/science-study 2>/dev/null   # only if already added
git add .specify/presets/science-study
```

Confirm it worked with `git ls-tree HEAD .specify/presets/science-study/preset.yml`.
The mode should read `100644`, not `160000`.

## The two ideas worth knowing

**Status and outcome let the record survive non-linear work.** Spec-kit's model
runs forward: spec, plan, tasks, implement, done. In a study a result can show
that an earlier stage was wrong, which is a finding rather than a failure, and
it often ends up in the paper. So a stage spec can be `blocked`, `superseded by`
another, or `abandoned`, and every one of those carries a written outcome. A
superseded spec is never rewritten or deleted. The record of a branch not taken
is what stops someone re-deriving it later.

**The simple path is a subset of the full path, not a different path.** Stage
specs are numbered directories from day one in every project. A project that
wants more machinery adds issues on top, one per stage spec. A project that does
not want it never sees it: nothing in the stage spec template mentions GitHub,
and the vocabulary a newcomer meets is question, method, checks, outcome.

## Design notes

Two rules shaped what went where.

A line belongs in a template only if it holds across studies. Anything that
differs between projects is content and belongs in that project's constitution.
That is why the pipeline form, the stage list, and the work-tracking choice are
all slots rather than defaults, and why no file-naming scheme appears anywhere
in the principles.

Guidance is written as instructions rather than maxims. A comment that reads
well on a poster does not tell anyone what to do.

## Status

Early. Built against spec-kit 1.0.5, exercised on marine acoustics studies
first. Presets themselves are a young part of spec-kit, so expect some churn.
