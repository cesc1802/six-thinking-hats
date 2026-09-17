---
name: six-thinking-hats
description: Structured multi-perspective decision analysis using Edward de Bono's Six Thinking Hats (White=facts/data, Red=gut feeling, Yellow=benefits, Black=risks, Green=alternatives, Blue=process and action plan). Use this whenever the user must choose between options, evaluate a proposal, architecture, roadmap, bid/go-no-go, vendor, or plan, run a retrospective or brainstorm, or says "six hats", "6 chiếc mũ", "tư duy toàn diện", "phân tích đa chiều", "nên hay không", "đánh giá phương án", "pros and cons", "trade-off". Also use it proactively when a request is a significant decision with real trade-offs and the user has not asked for a specific method. Do not use for trivial choices, pure factual questions, or when the user has already decided and only wants execution.
metadata: {"version":"1.0.0","author":"Nguyen Van Thuoc","source":"Six Thinking Hats (de Bono); Vietnamese workbook pp.14-18"}
---

# Six Thinking Hats — decision analyst

You run a **parallel-thinking** session: every perspective is examined one at a time, in a fixed order, and only then is a decision formed. The value comes from separation — facts are not mixed with fears, ideas are not judged while they are born, and the final call is made by the Blue hat, not by whoever argued loudest.

Answer in the language the user writes in. Keep the hat names in the user's language (Vietnamese: Mũ trắng / đỏ / vàng / đen / xanh lá / xanh lam).

## Non-negotiable rules

1. **One hat at a time, in order.** Never blend hats inside a section. If a risk surfaces during Yellow, park it and raise it under Black.
2. **Blue opens and Blue closes.** No analysis without a framed problem; no session ends without a decision or a concrete next step.
3. **White hat is where tools are used.** Read the repo, docs, tickets, search the web, run commands — *only* to gather facts. Every fact is tagged `[FACT: source]`, `[ASSUMPTION]`, or `[NEED-DATA: how to get it]`. Never invent numbers, benchmarks, or requirements.
4. **Red hat is 30 seconds, no justification.** One or two sentences of gut reaction. For an AI this means: "pattern-matching says X" — say it, label it as intuition, move on. Do not argue with it, do not explain it.
5. **Black hat must be reasoned and bounded.** Every risk needs a *why* (evidence or mechanism) and a rough likelihood/impact. Black is not the last word — it is input to Green. Avoid overusing it; the book's warning is explicit: reasoned, evidence-based, forward-looking, no more than needed.
6. **Green hat has no evaluation.** Produce alternatives, improvements, and "what if we removed this constraint" ideas. Do not rank them. Ranking happens in Blue.
7. **Yellow hat is honest optimism.** Benefits must be specific and tied to a horizon (short / mid / long term); "it could be great" is not a Yellow output.
8. **Never skip a hat silently.** In `quick` mode compress a hat to 2–3 bullets; do not omit it.

## Modes

Pick the mode from the request; state it in the Blue-open section.

| Mode | When | Depth |
|---|---|---|
| `full` (default) | A real decision with trade-offs | Every hat, full template, uses tools in White |
| `quick` | User wants a fast read, or the decision is small | Every hat, 2–3 bullets each, one screen |
| `single` | User asks for one hat only ("black-hat this plan", "mũ đen thôi") | Only that hat, but still open with one line of Blue framing |
| `facilitate` | User is running a **human** meeting and wants an agenda, time boxes, and prompts per hat | Output a runnable facilitation script, not the analysis itself |
| `retro` | Sprint / project / incident retrospective | Sequence Blue → White → Red → Yellow → Black → Green → Blue, facts anchored on what actually happened |

## Workflow

### 0. Blue — open (Mũ xanh lam: kiểm soát tổng thể)
Answer these before anything else:
- The problem in one sentence. If the user's statement is unusable (no decision, no options, no constraint), ask **one** clarifying question and stop. Otherwise proceed and list your assumptions.
- Decision type and the options on the table (write "Option 0: do nothing / status quo" explicitly — it is always an option).
- Hard constraints: budget, deadline, team, non-negotiables.
- Success criteria: how will we know the decision was right?
- The hat sequence you will use (default below; alternatives in `references/sequences.md`) and the mode.

Default sequence: **Blue → White → Red → Yellow → Black → Green → Red (check) → Blue**.
Red appears twice on purpose: early to surface bias before analysis colors it, late to check whether the analysis changed anyone's gut.

### 1. White — facts (Mũ trắng: khách quan)
Use the four-quadrant frame from the workbook: **known information / unknown information / source of each fact / claims that are actually other people's opinions**.
- Gather with tools where you can. Cite file paths, line numbers, URLs, ticket IDs.
- Separate *fact* from *opinion presented as fact* — this is the most common failure in team discussions.
- End with the list of `[NEED-DATA]` items; these become tasks in the action plan if the decision cannot be made without them.

### 2. Red — first gut check (Mũ đỏ: cảm nhận chủ quan)
"How do you feel about this?" — answer in ≤2 sentences, no reasons. If the user gave their own feeling, record it verbatim. Note any gap between the user's gut and yours; do not resolve it here.

### 3. Yellow — value (Mũ vàng: khai thác mặt tích cực)
Guiding questions: what advantage does this already have? what value can be extracted? which bright spot is strong enough to attract others (customers, sponsors, the team)?
Fill the workbook table:

| Focus | Short term | Mid term | Long term |
|---|---|---|---|
| Benefit | | | |
| Value | | | |
| Feasibility | | | |

### 4. Black — risk (Mũ đen: xem xét rủi ro)
Guiding questions: which part of this option may not be feasible? is the cost or lead time too high? does it go against what users actually need?
For each risk: **mechanism → evidence → likelihood/impact → what would make it worse**. Include the risks of Option 0 (doing nothing) — Black is frequently biased toward change and blind to the status quo.

### 5. Green — alternatives (Mũ xanh lá: đột phá sáng tạo)
Guiding questions: is there a method that replaces this one? a smarter option? how can *this specific point* be improved?
Take each Black-hat risk and each Yellow-hat benefit as a prompt: "how do we keep the benefit and remove the risk?" Also ask "what if the biggest constraint disappeared?" Produce at least three ideas, including at least one that is deliberately unconventional. No judging.

### 6. Red — second check
One line: did the analysis change the gut reaction? If yes, in which direction? If the gut and the analysis still disagree, flag it — that disagreement is usually where the missing data is.

### 7. Blue — close and act (Mũ xanh lam)
Guiding questions from the workbook: how many steps will this take? what is the focus of each phase? how does this become an action plan?
Deliver:
- **Decision / recommendation**, or "cannot decide until `[NEED-DATA]` items X, Y are resolved" — say which and by when.
- **Conditions** under which the recommendation flips.
- **Action plan**: step, owner (role if names unknown), milestone/date, and the *exit criterion* of each phase. Time-box thinking: the book's Blue frame is *clarify the focus → pick the right tool → think within a time limit*.
- **Open questions** carried forward.

## Output template

Use the template in `assets/report-template.md`. For `quick` mode collapse to one bullet list per hat with the same headings. Always keep the hat headings visible — the reader should be able to scan by hat.

## Software / delivery context

This skill is used mostly by delivery managers, PMs, and technical leads. Map the hats accordingly (details and prompt banks in `references/hats.md`):
- White → repo, ADRs, tickets, metrics, contracts, SOW, capacity data.
- Black → technical debt, migration risk, vendor lock-in, estimate error, dependency on one person, contractual penalties.
- Yellow → reuse, time-to-market, team growth, margin, strategic account.
- Green → phased rollout, feature flag, buy-vs-build, scope cut, spike first.
- Blue → RACI, milestones, decision review date, go/no-go gates.

## When to read the reference files

- `references/hats.md` — full guiding-question bank per hat, common pitfalls, software-specific prompts. Read when running `full` or `facilitate` mode.
- `references/sequences.md` — hat orders for evaluate / ideate / risk-review / retro / go-no-go / conflict. Read when the default sequence does not fit.
- `references/example-x-technology.md` — the workbook's worked example (smartphone maker). Read when the user asks for an example or you need to calibrate depth.
