# System Design Architect Plugin

This is the installable **full System Design Architect skill**.

It does **not require MCP**. Installing the plugin gives the complete reasoning system: visual-first design, evidence-grounded AS-IS reconstruction, canonical modeling, granular BUILD READY process specifications, verification/validation, resilience, health, bounded self-healing, and governed adaptation.

## What is bundled

`skills/system-design-architect/` contains the complete skill package:

- `SKILL.md` — governing operating contract
- `references/` — full methodology and daily-use guidance
- `templates/` — design, review, health, threat, fitness, and visual packs
- `model/` — canonical schema and worked example
- `examples/` — software, AI, and non-software examples
- `evals/` — behavioral/evaluation guidance
- `scripts/` — scaffold, model validation, rendering, and skill validation helpers
- `LICENSE` / changelog materials

## Core principle

Anyone who installs this plugin should get the **same full System Design Architect capability** as the open-source repository. The optional interactive app is an enhancement only; it must never be required to access methodology or BUILD READY reasoning.

## Example prompts

- `Build this system end to end. Show it visually and take it to BUILD READY granularity.`
- `Review this existing process. Reconstruct AS-IS from evidence, then design TARGET and transition.`
- `Teach me this system progressively, unfolding the graph one layer at a time.`
- `Assess this running system's health and design bounded recovery and adaptation.`

## Optional interactive app

The repository also contains a separate `app/` package with an MCP + React visual workspace. It can add interactive drill-down and richer UI, but it is not part of the core plugin dependency chain.
