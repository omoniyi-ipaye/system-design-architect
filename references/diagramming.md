# Architecture Diagramming Guidance

Use C4-style abstraction to avoid mixed-level “boxes and lines”.

## System Context
Show:
- primary users/roles
- system in scope
- external systems/dependencies
- labeled relationships

Do not show internal frameworks here.

## Container
Show major deployable/runtime units and data stores, for example:
- web/mobile app
- API/backend
- worker
- workflow engine
- database
- object store
- model gateway

Label technology only when it matters to understanding a decision.

## Component
Use only when a container is complex enough that internal responsibility boundaries matter.

## Dynamic/sequence
Use for critical paths such as:
- side-effecting write
- authentication
- async processing
- retrieval + model + tool execution
- failure/retry/reconciliation

## Deployment
Use when zones, regions, networks, edge, runtime isolation, or HA topology materially affects the design.

## Diagram quality checklist
- title and scope clear
- consistent abstraction level
- every box has a meaningful responsibility
- relationships labeled
- external vs internal clear
- trust boundaries indicated where relevant
- no unexplained acronyms
- no decorative infrastructure
