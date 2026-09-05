# Data Systems and Consistency

Use this lens whenever state, transactions, events, replication, or multiple systems of record matter.

## Ownership and source of truth
For each important datum define:
- authoritative owner/system
- writers and readers
- lifecycle and retention
- sensitivity/residency
- derivations/copies
- reconciliation authority when systems disagree

## Transaction boundary
Ask:
- What is one logical business transaction?
- Which mutations must be atomic?
- What may complete asynchronously?
- What happens after partial success?
- Is compensation possible and correct?

## Consistency model
State the required semantics instead of saying “consistent”:
- strong consistency
- read-after-write
- monotonic reads
- bounded staleness
- eventual consistency
- causal/order-sensitive behavior

Use the weakest model that still satisfies the business invariant.

## Concurrency
Define:
- competing writers
- optimistic/pessimistic locking where justified
- uniqueness/invariant enforcement
- conflict detection/resolution
- duplicate request/message behavior

## Events and messages
For event-driven systems define:
- event owner
- schema/version
- ordering scope
- delivery semantics
- deduplication/idempotency boundary
- replay policy and retention
- poison/dead-letter handling
- compatibility rules for producers/consumers

Never claim “exactly once” without specifying the boundary and enforcement mechanism.

## Schema evolution and migrations
Design for:
- backward/forward compatibility
- expand-and-contract database migrations
- dual-read/write only when necessary and bounded
- rollback limitations
- online migration impact
- data backfill verification

## Reconciliation
For workflows spanning external systems, define how divergence is detected and repaired. Reconciliation is often more reliable than trying to make unrelated systems participate in one distributed transaction.
