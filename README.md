# aero-ocl

A working sample of a **git-based knowledge base** for an engineering AI assistant —
an alternative to vector-RAG when answers must be *traceable*.

## The idea

Instead of chunking documents into a vector store, the knowledge lives as
**plain-text files in a repository** with provenance headers and numbered,
citable lines. Every number an assistant reports carries a chain:

```
answer → formula → sources/<file>:L<line> → executed code → cross-check
```

Formulas are never "remembered" by the model — they are **executed by code**
that references its source line explicitly.

## What's inside

```
sources/nasa-glenn/
  lift-equation.md      # NASA Glenn "Lift Equation", fetched 2026-11-21,
  lift-coefficient.md   # provenance URL + numbered lines [L10], [L12], ...
calc/
  lift_calc.py          # deterministic computation; formula citation in docstring
```

Example run (wing area 16.2 m², Cl 0.6, V 50 m/s, ρ 1.225 kg/m³):

```
$ python calc/lift_calc.py
{
  "динамічний_тиск_q_Па": 1531.25,
  "підйомна_сила_L_Н": 14883.8,
  "підйомна_сила_L_kgf": 1517.7,
  "зворотна_перевірка_Cl": 0.6,
  "джерела": [
    "sources/nasa-glenn/lift-equation.md:L12",
    "sources/nasa-glenn/lift-coefficient.md:L13"
  ]
}
OK: зворотна перевірка зійшлась
```

The reverse check (`Cl = L / (q·A)`) uses a *second* source line — if the two
sources or the code ever disagree, the assertion fails loudly.

## Why git beats vector-RAG for engineering numbers

| | vector RAG | git-based knowledge |
|---|---|---|
| source of an answer | "similar chunks", score-ranked | exact `file:line` |
| source version | unknown | tag / blame |
| source update | re-index, opaque | diff: what changed is visible |
| tabular data | blurred into chunks | CSV in git, reviewable |
| hallucinated numbers | high risk | formula executed by code |

## Scaling to a full aerodynamics library

Textbook PDFs (Anderson, Raymer), NACA/NASA reports and CFD tool docs
(OpenFOAM, SU2) convert to text and land in the repo directly; profile
tables (Abbott & von Doenhoff) get digitized into CSV; scanned plots stay
as referenced attachments. Roughly 80% of a typical aerodynamics library
fits the git pattern natively.

In production each source import is a tagged commit (`nasa-glenn-2024-07`,
`anderson-6ed`), every answer carries `file:line@version`, and updating a
textbook is a pull request whose diff shows exactly which older answers it
may affect.

## Credits

Sources are public NASA Glenn Research Center pages (Beginner's Guide to
Aeronautics), referenced with their URLs and retrieval dates in each file.
This repository adds structure and tooling only.
