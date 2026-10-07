# LinkedIn demo pack

## Post draft

An architecture diagram can show how a system is supposed to work. I wanted a practical way to ask a harder question: what does the operating evidence say about its health today?

I’ve been building System Design Architect, an open-source, vendor-neutral skill for designing and operating systems across software, services, teams and business processes.

The latest demo follows an employee-onboarding system. It reads aggregate operational signals, compares them with a historical baseline, checks explicit thresholds, and makes the difference between observed evidence and a possible explanation visible. In the synthetic example, Day 1 readiness is 82% against a 95% target, while late manager inputs are 24% against a 10% limit.

The system flags the pattern for investigation. It does not claim the late inputs caused the readiness gap. It proposes a small, reversible response for the People Ops lead to review, names how to verify recovery, and keeps the action behind human authority.

I also added a behavioral evaluation runner so the same design scenarios can be sent to different agent setups, graded with evidence quotes, and compared across versions. It rejects judge passes without an exact quote; people still review whether that quote supports the assertion.

The demo uses synthetic data. The adapters support read-only JSON endpoints and Prometheus-compatible metrics, with a normalized evidence contract for extending to other sources.

I’d value feedback from people building AI systems that need to stay understandable and governable after launch.

#SystemDesign #AIEngineering #SystemsThinking #AgentSkills

## 75-second walkthrough

1. **0:00–0:08 — Frame the problem.** “A design can be correct on paper and still drift in operation. This demo connects system health to observable evidence.”
2. **0:08–0:22 — Show the source.** Run `python3 examples/health-demo/run_demo.py`. Explain that the local endpoint serves aggregate synthetic onboarding data and the adapter fetches it with a read-only GET.
3. **0:22–0:40 — Show the signal table.** Point to 82% readiness vs a 95% target and 24% late manager inputs vs a 10% limit. Show the 30-day baseline beside each current value.
4. **0:40–0:55 — Show the inference.** Read the caveat: the pattern is a lead for investigation, not proof of cause. The report keeps source observations and the inferred explanation in separate sections.
5. **0:55–1:07 — Show the boundary.** Point to the named human authority, bounded cohort, reversal, verification, and escalation. Confirm that no action was executed.
6. **1:07–1:15 — Show the eval runner.** Open `evals/README.md`: agent and judge adapters make the behavioral suite provider-neutral and support version comparison.

## Demo claim boundaries

- Say “synthetic demo data”; do not imply this is a live employer or customer system.
- Say “read-only adapters for JSON endpoints and Prometheus-compatible metrics”; additional vendors require an adapter.
- Describe the causal explanation as a low-confidence inference, not an established cause.
- Describe the eval harness as executable with a configured agent and judge adapter; a passing JSON validation is not a model evaluation run.
