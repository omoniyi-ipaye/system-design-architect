# Reliability and Resilience Review

## Dependency failure
For each critical dependency evaluate latency, outage, malformed/stale data, quota/rate-limit exhaustion, partial success, and recovery.

## Overload and backpressure
Ask:
- What happens when arrival rate exceeds processing capacity?
- Is work rejected, queued, shed, sampled, or degraded?
- Is queue growth bounded and observable?
- Can producers overwhelm consumers or downstream systems?

Prefer explicit load shedding/backpressure over uncontrolled resource exhaustion.

## Blast radius
Define failure domains. A local defect, tenant spike, poison message, bad deployment, or dependency failure should not unnecessarily take down unrelated capabilities or tenants.

## Retry discipline
Retries must be bounded, jittered/backed off where relevant, and paired with idempotency when side effects can repeat. Avoid retry storms and layered retries multiplying traffic.

## Recovery
Define recovery for:
- process crash between mutation and acknowledgement
- duplicate or out-of-order work
- corrupt/poison messages
- stale caches/replicas
- failed deployments
- data restore
- third-party partial success

## Resilience verification
Where risk warrants it, test failure behavior with dependency fault injection, retry/idempotency tests, restore drills, queue-overload tests, and rollback exercises.
