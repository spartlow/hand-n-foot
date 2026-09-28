# ADR 0001: Use ADRs for significant architecture decisions

Status: Accepted

Context
When building this project, we expect to make tradeoffs about simulation determinism, strategy interfaces, and UI designs. These decisions should be recorded to help future contributors understand why a particular approach was chosen.

Decision
Create an `_context/ADRS/` directory and record each architecture decision as a separate markdown file named with an incrementing number, a short slug, and contents that follow the problem/decision/rationale format.

Consequences
- Important decisions are discoverable in the repo and can be linked from issues and PRs.
- Reviewers can quickly check why a design exists and whether it should be revisited.
