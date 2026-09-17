# Six Thinking Hats skill — evaluation findings

Evaluation date: 2026-09-17

## Verdict

**Conditional pass for usefulness; fail for strict contract compliance.**

The skill clearly improves structural adherence over the no-skill baseline, but
it is not yet reliable enough to treat every documented output contract as a
hard guarantee.

## Evidence used

- Load proof: `results/preflight/report-20260917-133028.json`
- Behavioral report: `results/final/report-20260917-132527.json`
- Regraded report after oracle hardening:
  `results/final/report-20260917-132527-regraded.json`
- Raw process output and normalized responses:
  `results/final/runs/<run-id>/`

The first experimental attempt used global `hermes -z -s`. A metadata probe
proved that this path accepted the argument but did not inject the skill. Those
results were discarded. The valid corpus uses `hermes chat -q -s ... -Q` and
has a passing metadata proof for version `1.0.0`, author `Nguyen Van Thuoc`.

## Results

| Layer/profile | Result |
|---|---:|
| Static package checks | 8/8 passed |
| Harness unit tests | 12/12 passed |
| Skill load preflight | 1/1 passed |
| Behavioral cases with skill | 4/8 strict passes |
| Paired core baseline without skill | 0/2 strict passes |
| Execution/infrastructure failures in final corpus | 0 |

### Per-case result

| Case | Result | Main observation |
|---|---|---|
| `single-black-hat` | PASS | Correct one-line Blue framing followed by bounded Black analysis |
| `facilitate-meeting` | PASS | Correct 60-minute agenda, sequence, facilitator prompts, no decision made for the group |
| `insufficient-decision-context` | PASS | Asked one clarification and stopped before full analysis |
| `trivial-non-trigger` | PASS | Answered `4` without invoking the framework |
| `quick-vietnamese` | FAIL | 6/7 checks passed; emitted `[NEED-DATA]` instead of `[NEED-DATA: how to get it]` |
| `incident-retro` | FAIL | Sequence and factual discipline were good; same malformed NEED-DATA tag |
| `full-vietnamese-decision` | FAIL | Correct hat sequence, but malformed NEED-DATA tags, missing exact recommendation/acceptance labels, and first Red section exceeded the 1–2 sentence contract |
| `full-english-go-no-go` | FAIL | Responded in Vietnamese, used default sequence rather than specialized Go/No-Go sequence, malformed NEED-DATA tag, and lacked English recommendation labeling |

### Paired core lift

Strict all-or-nothing pass remains `0/2` for both profiles because a single
format violation fails the whole case. At check level, the skill produced a
large measurable improvement:

| Core case | Baseline checks | With skill | Lift |
|---|---:|---:|---:|
| Full Vietnamese decision | 5/14 = 35.7% | 10/14 = 71.4% | +35.7 pp |
| Quick Vietnamese decision | 3/7 = 42.9% | 6/7 = 85.7% | +42.8 pp |

This means the skill is useful, but its remaining failures are concentrated in
specific enforceable contracts rather than general inability to perform the
method.

## Strong points

1. **Package integrity is good.** Frontmatter, name, description, body size,
   references, examples, and template files all passed static validation.
2. **The default full sequence is learned.** When the skill is genuinely
   loaded, the quick case follows Blue → White → Red → Yellow → Black → Green
   → Red → Blue exactly.
3. **Mode behavior is strong.** `single`, `facilitate`, clarification, and
   trivial non-trigger behavior passed.
4. **Decision quality is practical.** Outputs include Option 0, alternatives,
   risks, conditional recommendations, owners, deadlines, and reversal
   conditions.
5. **The skill materially outperforms the baseline** on the paired core cases.

## Problems to fix in the skill

### P0 — Enforce the exact evidence-tag grammar

Observed repeatedly:

```text
[NEED-DATA]
```

Documented contract:

```text
[NEED-DATA: how to get it]
```

This single issue failed Quick and Retro and contributed to both Full-case
failures. Add a final validation rule close to the top of `SKILL.md`:

```text
Before answering, reject or rewrite every bare [NEED-DATA] tag.
The only valid form is [NEED-DATA: <specific acquisition method>].
```

Also provide one invalid and one valid example.

### P0 — Match the user's language

The English Go/No-Go prompt received a Vietnamese response. Add an explicit
non-negotiable rule:

```text
Use the user's language for headings, labels, recommendation, plan, and exit
criteria. Do not infer language from the skill's examples.
```

### P1 — Move sequence selection into the main decision path

The English Go/No-Go case used the default sequence instead of the specialized
Go/No-Go sequence documented in `references/sequences.md`. Put the intent to
sequence mapping directly in `SKILL.md`, or require the agent to read the
reference before selecting a sequence.

### P1 — Add a machine-checkable final checklist

Before final output, require the agent to verify:

- Blue opens and closes, except the documented single-hat exception.
- Required sequence exactly matches the selected intent.
- First Red section is at most 1–2 sentences.
- All evidence tags use exact syntax.
- Recommendation, reversal condition, action plan, owner/deadline, and exit
  criterion labels are present when required.
- Output language matches input language.

### P1 — Require evidence receipts for external claims

The full Vietnamese response cited external architecture sources while the
agent ran with the `safe` toolset and had no web-retrieval receipt. The cited
pages may be real, but this run cannot prove that the claims were verified.
For a factuality-sensitive skill, either:

- use a web-enabled profile and store tool receipts; or
- mark external-memory claims as unverified and avoid citation-like FACT tags.

A future oracle should fail an external URL or source-tagged fact when no tool
receipt supports it.

### P2 — Control output size and latency

The detailed Full and Facilitate outputs were long and slow. The valid run
recorded approximately 206 seconds for the Full Vietnamese case and 183
seconds for Facilitate. Add explicit budgets, for example:

- Quick: 400–800 words.
- Full: 1,200–2,000 words unless the user requests depth.
- Facilitate: agenda plus prompts, without pre-solving every prompt.

## Harness issues found and fixed

1. Global `hermes -z -s <skill>` did not preload the skill. The harness now
   uses `hermes chat -q ... -s <skill> -Q`.
2. A mandatory metadata preflight proves the skill is actually present.
3. Some CLI/API failures returned process exit code `0`; the adapter now also
   checks output failure markers and usage receipts when present.
4. Raw stdout and normalized agent response are stored separately.
5. Hat-sequence parsing now ignores declared sequence prose and nested
   headings, while supporting agenda tables and Vietnamese Blue aliases.
6. Stored outputs can be regraded without paying for another model run.

## Limits of this evaluation

- One behavioral repeat per case; use at least three repeats before release.
- Baseline comparison covers only the two core cases.
- Semantic usefulness was inspected but not scored by an LLM judge.
- External factual claims were not web-verified in this safe-tool run.
- The model/provider was the machine's configured Hermes default and was not
  pinned in the report. Pin it before longitudinal regression comparisons.

## Recommended release gate

Do not promote the skill as strictly contract-compliant yet. Fix P0 items,
then rerun:

```bash
python3 -m evals.runner \
  --suite core \
  --suite modes \
  --suite language \
  --profile with-skill \
  --repeat 3 \
  --jobs 2 \
  --out results/candidate-r3
```

Suggested gate:

- Static checks: 100%.
- Load preflight: 100%.
- Required behavioral cases: at least 90% strict pass.
- Safety/guardrail cases: 100%.
- No unsupported external FACT citation without a receipt.
