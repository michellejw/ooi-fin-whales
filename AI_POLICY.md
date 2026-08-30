# AI policy

This repository follows the [Scientific Python Development Guide's guidance on
agentic AI](https://learn.scientific-python.org/development/guides/ai/).

## Disclosure

AI tools were used substantially in this project, for literature search, code,
and drafting documentation. Where AI assistance produced a commit, that commit
carries a trailer naming the harness and model:

```
Assisted-by: claude-code:claude-opus-5
```

Naming the model is deliberate rather than ceremonial. A reviewer who knows
which model produced something can check it with a model from a different
family, which catches a class of error that re-reading with the same model
does not.

The first two commits in this repository predate the convention and carry
`Co-Authored-By` instead, which is the trailer this policy says not to use.
They were left as they are rather than rewritten. The history is more useful
showing a convention being found and adopted than it would be showing a repo
that got it right from the start, and rewriting published history to look
tidier is a worse habit than the trailer was a mistake.

## Attribution

AI tools are not listed as authors or co-authors. `Co-Authored-By` records a
copyright holder taking responsibility for a contribution, and a model is
neither. The author is responsible for everything in this repository regardless
of how it was produced.

`Signed-off-by` is never added by an AI tool, for the same reason: certifying
the Developer Certificate of Origin is an act only a person can perform.

## Prose

Documentation here, including `README.md` and this file, was drafted with AI
assistance and edited by the author. Project notes distinguish claims that were
verified, meaning a source was fetched and read, from claims that were relayed
without independent checking.

## Verification

Numbers that results depend on are computed rather than accepted from a summary.
Two examples from the scoping phase:

- The instrument response figures in `README.md` come from evaluating the FDSN
  response directly, not from a description of it.
- Whale-VAD's output class count was established by loading the model. Its
  documentation states three classes; the released weights emit seven.

Both cases changed a decision. The second contradicted the model's own README.

## Scientific decisions

Study design was not delegated. The choice of station, the scope, and the
validation design (running a modern detector over data whose published answer
already exists, so the difference between old and new is attributable to the
detector alone) were the author's.

## Publication

Any publication arising from this work will carry an equivalent disclosure in
its methods or acknowledgements, consistent with ICMJE and COPE guidance that
AI tools cannot be authors.
