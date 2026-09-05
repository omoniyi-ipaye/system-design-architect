# Contributing

Thank you for improving System Design Architect.

## Principles for contributions

Changes should preserve these properties:
- vendor-neutral
- requirement-driven
- evidence-aware
- simplicity-first
- security/reliability conscious
- useful for both AI and non-AI systems
- evolutionary for existing systems

## Proposing methodology changes

For a new mandatory design step, explain:
1. what failure it prevents
2. which systems need it
3. why it belongs in the core flow rather than an optional reference
4. how it affects lightweight systems

Avoid adding a framework merely because it is popular.

## Pull requests

- keep `SKILL.md` concise enough for agent loading
- put deep guidance in `references/`
- add or update examples for behavioral changes
- run `python scripts/validate_skill.py`
- cite primary/official methodology sources in `references/sources.md`
