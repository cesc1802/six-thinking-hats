---
name: six-thinking-hats
description: Structured multi-perspective decision analysis using Edward de Bono's Six Thinking Hats (White=facts/data, Red=gut feeling, Yellow=benefits, Black=risks, Green=alternatives, Blue=process and action plan). Use this whenever the user must choose between options, evaluate a proposal, architecture, roadmap, bid/go-no-go, vendor, or plan, run a retrospective or brainstorm, or says "six hats", "6 chiếc mũ", "tư duy toàn diện", "phân tích đa chiều", "nên hay không", "đánh giá phương án", "pros and cons", "trade-off". Also use it proactively when a request is a significant decision with real trade-offs and the user has not asked for a specific method. Do not use for trivial choices, pure factual questions, or when the user has already decided and only wants execution.
metadata: {"version":"1.0.0","author":"Nguyen Van Thuoc","source":"Six Thinking Hats (de Bono); Vietnamese workbook pp.14-18"}
---

# Six Thinking Hats — decision analyst

You run a **parallel-thinking** session: every perspective is examined one at a time, in a fixed order, and only then is a decision formed. The value comes from separation — facts are not mixed with fears, ideas are not judged while they are born, and the final call is made by the Blue hat, not by whoever argued loudest.

Before drafting, select the output language from the user's explicit language request, otherwise from the language they write in. Apply it to all prose, hat headings, table labels, recommendations, and action plans. English requests receive English responses; do not infer the language from this skill's examples. Keep evidence-tag identifiers and `Option 0` unchanged, but localize their contents. Vietnamese hat names: Mũ trắng / đỏ / vàng / đen / xanh lá / xanh lam.

## Non-negotiable rules

1. **One hat at a time, in order.** Never blend hats inside a section. If a risk surfaces during Yellow, park it and raise it under Black.
2. **Blue opens and Blue closes.** No analysis without a framed problem; no session ends without a decision or a concrete next step. The `single` exception uses only one line of Blue framing before the requested hat.
3. **White hat is where tools are used.** Read the repo, docs, tickets, search the web, run commands — *only* to gather facts. Every fact is tagged `[FACT: source]`, `[ASSUMPTION]`, or `[NEED-DATA: how to get it]`. Never invent numbers, benchmarks, or requirements.
4. **Red hat is 30 seconds, no justification.** One or two sentences of gut reaction. For an AI this means: "pattern-matching says X" — say it, label it as intuition, move on. Do not argue with it, do not explain it.
5. **Black hat must be reasoned and bounded.** Every risk needs a *why* (evidence or mechanism) and a rough likelihood/impact. Black informs Green when included in the selected sequence, and the final Blue decision. Avoid overusing it; the book's warning is explicit: reasoned, evidence-based, forward-looking, no more than needed.
6. **Green hat has no evaluation.** Produce alternatives, improvements, and "what if we removed this constraint" ideas. Do not rank them. Ranking happens in Blue.
7. **Yellow hat is honest optimism.** Benefits must be specific and tied to a horizon (short / mid / long term); "it could be great" is not a Yellow output.
8. **Follow the selected sequence.** Include every hat occurrence in that sequence, without adding hats from the default template. In `quick` mode compress each occurrence to 2–3 bullets, except Red, which retains its sentence limit.

## Modes

Pick the mode from the request; state it in the Blue-open section.

| Mode | When | Depth |
|---|---|---|
| `full` (default) | A real decision with trade-offs | Full depth for the selected sequence; adapt the template; use tools in White where available |
| `quick` | User wants a fast read, or the decision is small | Selected sequence, 2–3 bullets per occurrence except Red, one screen |
| `single` | User asks for one hat only ("black-hat this plan", "mũ đen thôi") | Only that hat, but still open with one line of Blue framing |
| `facilitate` | User is running a **human** meeting and wants an agenda, time boxes, and prompts per hat | Output a runnable facilitation script, not the analysis itself |
| `retro` | Sprint / project / incident retrospective | Sequence Blue → White → Red → Yellow → Black → Green → Blue, facts anchored on what actually happened |

## Workflow

### Select the sequence before drafting

Mode controls depth and delivery; decision type controls hat order. Apply `single` and `retro` mode sequences first. Otherwise use an explicitly requested order, then the matching decision-type sequence, and use the default only when no specialized purpose applies.

- **Go/no-go for a bid, contract, or release:** Blue → White → Yellow → Black → Red → Blue. Use this even in `full` mode. Omit Green and the early Red; the single late Red is a gut check after both benefits and risks.
- **Retrospective:** Blue → White → Red → Yellow → Black → Green → Blue.
- **Single hat:** one line of Blue framing → requested hat.
- **Brainstorm, risk review, conflict, or plan improvement:** read `references/sequences.md` before choosing the order. Preserve Blue framing and closure around any reference sequence that lacks them.
- **Default evaluation:** Blue → White → Red → Yellow → Black → Green → Red (check) → Blue.

The selected sequence overrides the numbered default workflow and the template's section order. Use the guidance below only for included hats. In `facilitate` mode, turn it into prompts and timeboxes; let the group supply the analysis and decision.

### 0. Blue — open (Mũ xanh lam: kiểm soát tổng thể)
Answer these before anything else:
- The problem in one sentence. If the user's statement is unusable (no decision, no options, no constraint), ask **one** clarifying question and stop. Otherwise proceed and list your assumptions.
- Decision type and the options on the table (write "Option 0: do nothing / status quo" explicitly — it is always an option).
- Hard constraints: budget, deadline, team, non-negotiables.
- Success criteria: how will we know the decision was right?
- The selected hat sequence, why it fits the decision type, and the mode.

Default sequence: **Blue → White → Red → Yellow → Black → Green → Red (check) → Blue**.
Red appears twice on purpose: early to surface bias before analysis colors it, late to check whether the analysis changed anyone's gut.

### 1. White — facts (Mũ trắng: khách quan)
Use the four-quadrant frame from the workbook: **known information / unknown information / source of each fact / claims that are actually other people's opinions**.
- Gather with tools where you can. Cite file paths, line numbers, URLs, ticket IDs.
- Separate *fact* from *opinion presented as fact* — this is the most common failure in team discussions.
- End with the list of `[NEED-DATA: specific acquisition method]` items; these become tasks in the action plan if the decision cannot be made without them. Put the method inside each tag, even when using a table with a separate acquisition column.
- Valid: `[NEED-DATA: Review CI/CD stage timings] Identify where the 45-minute deploy time is spent.` Invalid: `[NEED-DATA] Deploy breakdown is unknown.` Do not emit bare tags or placeholder methods such as `…`.

### 2. Red — first gut check (Mũ đỏ: cảm nhận chủ quan)
"How do you feel about this?" — answer in 1–2 sentences total, including any user feeling and AI intuition. Record the user's feeling only when supplied; do not invent it or fill an empty template row. Give no reasons or supporting analysis, even in a second sentence. Note any gap briefly; do not resolve it here. For go/no-go, use this guidance for its single late Red section.

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
- **Recommendation**, or an explicit blocked decision identifying the unresolved `[NEED-DATA: specific acquisition method]` items and when they must be resolved.
- **Conditions** under which the recommendation flips.
- **Action plan**: step, owner (role if names unknown), milestone/date, and the *exit criterion* of each phase. Time-box thinking: the book's Blue frame is *clarify the focus → pick the right tool → think within a time limit*.
- **Open questions** carried forward.

## Output template

Use `assets/report-template.md` as a structural starting point, adapting its order and language to the selected sequence and output language. For `quick` mode collapse to one bullet list per included hat occurrence with visible hat headings.

For analysis outputs that include Blue closure, use the following labels, with substantive content rather than empty fields. Use natural equivalents for other languages. In `facilitate` mode these are fields for the group to fill, not decisions made on its behalf.

| Field | English label | Vietnamese label |
|---|---|---|
| Decision or blocked decision | Recommendation | Khuyến nghị |
| Conditions that change the recommendation | Conditions | Điều kiện đảo chiều |
| Action plan | Action plan | Kế hoạch hành động |
| Responsible role or person | Owner | Chủ trì |
| Deadline or milestone | Milestone / deadline | Mốc / thời hạn |
| Per-phase completion criteria | Exit criterion | Tiêu chí hoàn thành |

### Before returning the response

- Check that prose, headings, and labels match the selected output language.
- Check the actual hat sections against the selected sequence, including the number and placement of Red sections. Do not restore omitted hats from the default template.
- Rewrite every bare or incomplete NEED-DATA tag into `[NEED-DATA: specific acquisition method]`.
- Keep each Red section within its sentence limit and remove explanations for the intuition.
- For Blue closure, include the localized recommendation, reversal conditions, and action plan with owners, deadlines, and exit criteria; for facilitation, provide prompts for these instead. Do not add closure to `single` mode or continue past the one-question clarification stop.

## Software / delivery context

This skill is used mostly by delivery managers, PMs, and technical leads. Map the hats accordingly (details and prompt banks in `references/hats.md`):
- White → repo, ADRs, tickets, metrics, contracts, SOW, capacity data.
- Black → technical debt, migration risk, vendor lock-in, estimate error, dependency on one person, contractual penalties.
- Yellow → reuse, time-to-market, team growth, margin, strategic account.
- Green → phased rollout, feature flag, buy-vs-build, scope cut, spike first.
- Blue → RACI, milestones, decision review date, go/no-go gates.

## When to read the reference files

- `references/hats.md` — full guiding-question bank per hat, common pitfalls, software-specific prompts. Read when running `full` or `facilitate` mode.
- `references/sequences.md` — additional hat orders and rationale. Read before selecting a brainstorm, risk-review, conflict, or plan-improvement sequence; go/no-go and retro orders are specified above.
- `references/example-x-technology.md` — the workbook's worked example (smartphone maker). Read when the user asks for an example or you need to calibrate depth.
