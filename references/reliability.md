# Reliability and Resilience Review

Reliability is not only about preventing failure. Resilient systems should anticipate, detect, contain, recover from, and learn from adverse conditions. For the full domain-neutral adaptation loop see [`adaptive-systems.md`](adaptive-systems.md).

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
Define failure domains. A local defect, tenant spike, poison message, bad deployment, dependency failure, staffing gap, supplier failure, or broken handoff should not unnecessarily take down unrelated capabilities.

## Retry / repeated-work discipline
For digital systems, retries must be bounded, jittered/backed off where relevant, and paired with idempotency when side effects can repeat. Avoid retry storms and layered retries multiplying traffic.

For human/operational systems, define how failed or incomplete work is re-entered without duplication, silent loss, or endless escalation loops.

## Recovery
Define recovery for relevant failure states, including:
- process crash or interrupted work between mutation/action and acknowledgement
- duplicate or out-of-order work
- corrupt/poison inputs
- failed deployments or process changes
- data/resource restore
- third-party partial success
- owner unavailable or handoff missed
- capacity shortfall
- physical or supplier disruption

## Adaptive recovery
For material systems define:
- health/outcome signals;
- deviation thresholds;
- diagnosis evidence;
- a bounded response catalogue;
- who/what may authorize each response;
- rollback or contingency;
- recovery verification;
- escalation when confidence is low or the condition is novel.

Do not allow an adaptive mechanism to silently rewrite system purpose, critical controls, authority boundaries, or source-of-truth rules.

## Learning after failure
Capture incidents, near misses, recurring exceptions, manual workarounds, repeated escalations, and unsuccessful recoveries. Decide explicitly whether the evidence calls for no change, an operating adjustment, a capacity/control change, or a return to the full system-design workflow.

## Resilience verification
Where risk warrants it, test failure behavior through realistic drills. Depending on domain these may include dependency fault injection, retry/idempotency tests, restore drills, queue-overload tests, rollback exercises, staffing/supplier contingencies, exception-path simulations, or manual recovery rehearsals.
