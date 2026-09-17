# The six hats — question bank, pitfalls, delivery-context prompts

Source: Vietnamese workbook "Tư duy toàn diện từ nhiều góc độ: Phương pháp 6 chiếc mũ tư duy" (pp. 14–18), based on de Bono. Each hat below lists the workbook's guiding questions (VN + EN), its visual frame, the failure modes to watch for, and prompts adapted to software delivery work.

---

## White hat — Mũ trắng: Khách quan (Người lý tính)

**Stance:** Only collect facts and data. No personal position.

**Guiding questions (workbook):**
- Hiện tại chúng ta đang có dữ liệu gì? — What data do we have now?
- Chúng ta còn cần thêm dữ liệu nào? — What data do we still need?
- Chúng ta sẽ lấy thông tin liên quan từ đâu? — Where will we get it?

**Frame (2×2):** Known information | Unknown information / Information source | Other people's viewpoints. Every statement goes into one cell. "Other people's viewpoints" is the trap cell: a sales manager saying "customers want X" is a viewpoint until backed by data.

**Pitfalls:**
- Presenting an estimate as a measurement.
- Quoting a figure without its source or date.
- Letting the person who owns the data also interpret it in this hat (interpretation is Yellow/Black).

**Delivery prompts:**
- What does the repo / ADR / ticket history actually say? (cite path:line)
- What do metrics say (latency p95, error rate, lead time, velocity, burn rate)?
- What is in the contract / SOW / RFP — scope, penalties, SLAs, payment milestones?
- Team capacity: who, how many FTE, until when, what leaves?
- What has been tried before and what happened?

---

## Red hat — Mũ đỏ: Chủ quan (Người cảm tính)

**Stance:** Express the true inner feeling; attend to intuition and personal judgment.

**Guiding question (workbook):** Bạn có cảm nhận gì về việc này? — How do you feel about this?

**Frame (workbook):** 30 seconds · intuitive emotion · express by intuition · do not deliberately overthink · **no explanation required** · **keep it short**.

**Pitfalls:**
- Justifying the feeling (that turns it into a disguised Black or Yellow).
- Skipping it because "we are engineers". Gut reactions predict resistance during execution; unspoken ones become passive resistance later.
- Letting one loud gut dominate — in `facilitate` mode collect every participant's reaction in writing before anyone speaks.

**Delivery prompts:**
- Does this plan excite the team or exhaust them?
- Does the deadline feel achievable or already lost?
- Do we trust this vendor / client / sponsor?

---

## Yellow hat — Mũ vàng: Tích cực (Người lạc quan)

**Stance:** From a positive attitude, produce optimistic **and constructive** views.

**Guiding questions (workbook):**
- Dự án hiện có lợi thế gì? — What advantage does the project have now?
- Có những giá trị nào có thể khai thác? — What value can be extracted?
- Có điểm sáng nào đủ sức hấp dẫn người khác không? — Is there a bright spot attractive enough to draw others in?

**Frame (workbook table):** rows Benefit / Value / Feasibility × columns Short term / Mid term / Long term. Fill every cell or write "none identified" — an empty cell is information.

**Pitfalls:**
- Vague optimism ("huge potential"). Every benefit needs a beneficiary, a horizon, and if possible a size.
- Feasibility row treated as a wish; it must be a *positive* argument for why this can be done (existing skills, reusable components, precedent), not a repeat of Black.

**Delivery prompts:**
- What do we already have that makes this cheaper than it looks (components, people, relationships)?
- Which stakeholder gains most, and can they sponsor it?
- If this works, what does it unlock next (accounts, capabilities, hiring)?

---

## Black hat — Mũ đen: Tiêu cực (Người phản biện)

**Stance:** Through reasoned negation and rational doubt, identify problems and latent risks.

**Guiding questions (workbook):**
- Điểm nào của phương án này có thể không khả thi? — Which part of this option may not be feasible?
- Chi phí hoặc thời gian đầu tư có quá cao không? — Is the cost or time investment too high?
- Nó có đi ngược lại nhu cầu của người dùng không? — Does it go against user needs?

**Frame (workbook):** three inputs — *Avoid overuse* · *Reasoned, with evidence* · *Anticipate future risk* — all feeding into **Logical consistency**. The book gives Black three explicit guardrails because it is the hat teams abuse most.

**Pitfalls:**
- Risk without mechanism ("it might fail").
- Only attacking change; never listing the risk of standing still.
- Treating Black as the decision. Black raises issues; Green answers them; Blue decides.
- Overuse: if Black is longer than the other five hats combined, cut it.

**Delivery prompts:**
- Single points of failure: one person, one vendor, one environment?
- Where do estimates historically slip on this team (integration, UAT, third-party)?
- Contractual exposure: penalties, acceptance criteria we cannot control, IP clauses.
- Migration / rollback: can we get back if this fails in production?
- Hidden cost: run cost, licence, support, retraining.

---

## Green hat — Mũ xanh lá: Sáng tạo (Người đổi mới)

**Stance:** Widen thinking to develop creative ideas; supply new methods and options.

**Guiding questions (workbook):**
- Có phương pháp nào có thể thay thế không? — Is there a method that could replace this?
- Có phương án nào thông minh hơn không? — Is there a smarter option?
- Điểm này còn có thể cải tiến như thế nào? — How can this point still be improved?

**Frame (workbook):** Creative capacity ↔ No evaluation ↔ Mental focus (a triangle: creativity needs both the absence of judgment and a concrete focus).

**Pitfalls:**
- Evaluating while generating ("that won't work because…"). Park it.
- Only incremental ideas. Force at least one that removes a constraint entirely.
- Ideas with no link to the Black/Yellow output — Green is most useful when it explicitly targets a listed risk or amplifies a listed benefit.

**Delivery prompts:**
- Phase it: what is the smallest slice that proves the riskiest assumption?
- Buy / build / partner / open-source?
- Feature flag, dark launch, parallel run, strangler pattern?
- Cut scope instead of adding people?
- Change the contract shape (T&M for discovery, fixed price after)?

---

## Blue hat — Mũ xanh lam: Bình tĩnh (Người quản lý)

**Stance:** Coordinate the thinking steps, manage the whole process, and finally draw the conclusion.

**Guiding questions (workbook):**
- Dự án sẽ được triển khai qua mấy bước? — How many steps will the project take?
- Trọng tâm của từng giai đoạn là gì? — What is the focus of each phase?
- Cuối cùng làm thế nào để hình thành kế hoạch hành động? — How does this become an action plan?

**Frame (workbook arrow):** Clarify the focus → Choose the right tool → Think within a time limit.

**Pitfalls:**
- Opening without success criteria — then Blue-close cannot tell whether the decision is good.
- Closing with "further discussion needed" and nothing else. Always output a next step with an owner and date, even if the step is "collect data X".
- Letting the facilitator (Blue) also be the strongest Black voice. In `facilitate` mode, name a separate Blue-hat owner.

**Delivery prompts:**
- Which decision gates (go/no-go) exist and what evidence opens each?
- Who has the decision right (RACI D)?
- When is the decision reviewed — set a date now.
