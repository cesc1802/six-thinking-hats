# Six Thinking Hats — skill eval pack

Evidence-centric evaluation pack for the supplied `six-thinking-hats` skill.
It tests the skill package itself and its behavior when preloaded into Hermes.

## What is tested

### Static contract

- `SKILL.md` exists and has valid frontmatter.
- Skill name is lowercase kebab-case.
- Description and body are present and bounded.
- Referenced files exist.
- Required references and report template are packaged.

### Behavioral contract

Eight deterministic cases cover:

- Full Vietnamese decision analysis.
- Quick mode.
- Single Black-hat mode.
- Facilitation mode.
- Incident retrospective mode.
- Insufficient context: ask one question and stop.
- Trivial non-trigger behavior.
- Full English go/no-go analysis.

The deterministic oracle checks observable response evidence, including:

- Hat section sequence.
- Blue opening and closing.
- Explicit Option 0.
- `[FACT: ...]` and `[NEED-DATA: ...]` tags.
- Required mode-specific fields.
- Green idea count.
- Language and response-size bounds.
- Forbidden recommendations in facilitation mode.

## Experiment profiles

| Profile | Treatment |
|---|---|
| `with-skill` | Runs `hermes chat -q` and preloads the installed `six-thinking-hats` skill |
| `baseline` | Runs the same chat adapter with `--ignore-rules` and no skill |

Only the two core cases run against the baseline. The purpose is to measure
whether the skill improves compliance beyond the model's unaided behavior.
Both profiles use the same configured model/provider and the `safe` toolset.

## Run

The Hermes CLI resolves `-s six-thinking-hats` from its installed skill
catalog. Install the bundled subject before running and remove it afterward if
you do not want to keep it:

```bash
# Refuses to overwrite an existing skill; inspect/backup first if this fails.
test ! -e "$HOME/.hermes/skills/six-thinking-hats"
cp -a subject/six-thinking-hats "$HOME/.hermes/skills/six-thinking-hats"
hermes skills list | grep six-thinking-hats
```

Use `hermes chat -q`, not global `hermes -z`, for this eval. On the tested
Hermes build, `-z` accepted `-s` but did not inject the preloaded skill. The
chat adapter was verified with an exact metadata probe before the corpus ran.

```bash
cd /home/cesc/Documents/personal-workspace/six-thinking-hats-eval

# Oracle and harness unit tests
python3 -m unittest discover -s tests -v

# Static package validation only
python3 -m evals.runner --static-only

# One smoke case
python3 -m evals.runner \
  --case quick-vietnamese \
  --profile with-skill

# Mandatory load proof (run before the behavioral corpus)
python3 -m evals.runner \
  --case preflight-skill-load \
  --profile with-skill \
  --out results/preflight

# Complete evaluation (three independent runs in parallel)
python3 -m evals.runner --jobs 3 --out results/full

# Selected suite, repeated trials
python3 -m evals.runner \
  --suite core \
  --profile with-skill \
  --profile baseline \
  --repeat 3 \
  --out results/core-r3

# Optional cleanup when the skill was installed only for this eval
rm -rf "$HOME/.hermes/skills/six-thinking-hats"
```

A non-zero exit code means at least one required static, execution, or
behavioral check failed. This is expected when the candidate skill has a
regression; inspect the generated report rather than treating the harness as
broken.

## Evidence and replay

Each run stores:

```text
results/<experiment>/
├── report-<timestamp>.json
└── runs/<run-id>/
    ├── stdout.log
    ├── response.md
    ├── stderr.log
    └── usage.json        # present only for adapters that emit a receipt
```

The report records:

- Skill tree SHA-256 digest.
- Exact case and profile selection.
- Process command/argv without shell interpolation.
- Exit code, timeout and duration.
- Adapter profile and exact executable argv.
- Optional model/provider/token usage when the adapter emits a usage receipt.
- Every oracle check with expected and actual values.
- Paths to raw response evidence.

## Interpretation

A passing process execution is not a passing eval. A run passes only when:

1. The agent process exits successfully.
2. Required evidence is present.
3. Every deterministic oracle check passes.

The response is treated as agent evidence, not proof about an external world.
This skill is a reasoning/reporting skill and has no external side effects;
therefore output-structure and factual-discipline contracts are the primary
observable state.

## Limitations

- A single trial measures one stochastic sample. Use `--repeat 3` or higher
  before making release decisions.
- Language checks are intentionally shallow and deterministic.
- The evaluator does not judge whether the final business recommendation is
  objectively correct; it checks whether the prescribed decision process was
  followed.
- Semantic quality such as originality of Green-hat ideas remains a candidate
  for a rubric-based judge, but is not allowed to override deterministic
  contract failures.
- The baseline disables project/user rules with `--ignore-rules`; provider
  credentials and the configured inference service remain shared.
