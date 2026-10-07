# Behavioral Evaluation Harness

The eval JSON files define scenarios and assertions. `scripts/run_evals.py` can send those scenarios to any local agent runtime and a separate judge runtime through command adapters, then record evidence-backed pass/fail results and compare them with a previous report.

## Check suite structure

```bash
python3 scripts/run_evals.py --check
```

## Command adapter contract

The runner starts the configured command without a shell, sends one JSON object on stdin, and reads stdout. This keeps model vendors and SDKs out of the repository and lets a team reuse its approved authentication and runtime setup. Adapter stderr is suppressed from reports because provider errors can contain sensitive request context.

An agent adapter receives:

```json
{
  "task": "run_behavioral_eval",
  "scenario_id": "evals.json:1",
  "prompt": "The scenario prompt",
  "skill": {"name": "system-design-architect", "root": "...", "main_file": "SKILL.md", "content": "..."}
}
```

It writes either plain response text or `{"output":"...","model":"model-name"}` to stdout. Do not return credentials or other secrets in the response.

The repository includes [`scripts/eval_adapters/ollama.py`](../scripts/eval_adapters/ollama.py) for a local Ollama server. It supports the [official non-streaming `/api/chat` response format and structured JSON output](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion). The included adapter only accepts a loopback URL, disables extended thinking by default, and caps generated output. Pass `--think` to enable extended reasoning, or adjust `--max-tokens` and `--timeout` for the installed model.

A judge adapter receives the scenario prompt, expected behavior, all assertions, and the candidate response. It must return one JSON object with every assertion exactly once:

```json
{"results":[
  {"assertion_id":"A01","passed":true,"evidence":"short exact quote from the candidate response","reason":""},
  {"assertion_id":"A02","passed":false,"evidence":"","reason":"The response omits the recovery authority."}
]}
```

The runner checks that every passing assertion includes an exact substring from the candidate response. This prevents a judge from passing an assertion with a fabricated quote. A matching excerpt can still be irrelevant to the assertion, so review the excerpt and reasoning before treating a model-judge score as acceptance.

## Run and compare

```bash
python3 scripts/run_evals.py \
  --agent-command "python3 adapters/my_agent.py" \
  --judge-command "python3 adapters/my_judge.py" \
  --agent-name "My agent" \
  --judge-name "My judge" \
  --out eval-results/current.json \
  --markdown-out eval-results/current.md

python3 scripts/run_evals.py \
  --agent-command "python3 adapters/my_agent.py" \
  --judge-command "python3 adapters/my_judge.py" \
  --baseline eval-results/current.json \
  --fail-on-regression \
  --out eval-results/next.json
```

For deterministic replay, `--responses-file` accepts a JSON object keyed by `suite.json:scenario-id`; `--judgments-file` accepts the judge `results` object under the same key. Reports may contain model output and should be handled as private evaluation data. The runner does not transmit results anywhere.

Run one scenario while connecting an adapter:

```bash
python3 scripts/run_evals.py --suite evals/visual-daily-evals.json --limit 1 \
  --agent-command "python3 adapters/my_agent.py" \
  --judge-command "python3 adapters/my_judge.py"
```

With local Ollama models installed, an end-to-end run can use:

```bash
python3 scripts/run_evals.py \
  --agent-command "python3 scripts/eval_adapters/ollama.py agent --model <installed-agent-model>" \
  --judge-command "python3 scripts/eval_adapters/ollama.py judge --model <installed-judge-model>" \
  --agent-name "Local agent" \
  --judge-name "Local judge" \
  --out eval-results/local-run.json
```

To run just the self-healing onboarding scenario, add `--suite evals/evals.json --scenario evals.json:9`. If using a large local model, set the runner's `--timeout` and the adapter command's `--timeout` high enough for that model to respond.

Use a separate judge model where possible, review its evidence, and record the model tags. The report is a reproducible aid to review, not independent proof of quality.

The harness does not claim an eval has passed merely because a suite is valid JSON. A run report identifies the configured agent and judge, scenario-level outcomes, assertion evidence, and version-to-version regressions and improvements.
