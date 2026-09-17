# Mũ xanh lam — Mở phiên: xác định quyết định

**Chế độ:** `full`

**Vấn đề cần quyết định:** Đội 4 người có nên hoàn tất việc tách module thanh toán khỏi monolith thành một microservice độc lập ngay trong quý này hay không?

## Các phương án

- **Option 0 — Giữ nguyên:** Không thay đổi kiến trúc; tiếp tục deploy toàn bộ monolith trong 45 phút.
- **Option 1 — Tách hoàn toàn trong quý:** Payment service có codebase, database, pipeline, vận hành và deploy độc lập.
- **Option 2 — Tách theo giai đoạn:** Trong quý này chuẩn hóa boundary, API, observability và thử nghiệm strangler/shadow; chỉ chuyển production khi đạt các cổng kỹ thuật.
- **Option 3 — Không tách service:** Giữ modular monolith, tập trung giảm thời gian pipeline/deploy.

## Ràng buộc cứng

- Đội chỉ có 4 người.
- Ngân sách không tăng.
- Deadline cuối quý.
- Hệ thống đang ổn định.
- Thanh toán là miền nghiệp vụ có tác động tài chính cao.
- Không được làm suy giảm tính đúng đắn của giao dịch và khả năng khôi phục sự cố.

## Tiêu chí thành công

1. Không phát sinh charge trùng, mất giao dịch hoặc sai trạng thái thanh toán.
2. Có rollback/fallback đã được kiểm thử.
3. Thời gian deploy phần liên quan được giảm đáng kể so với baseline 45 phút.
4. Không làm tăng tỷ lệ lỗi production.
5. Đội 4 người có thể trực vận hành mà không cần thêm ngân sách.
6. Việc tách tạo ra khả năng deploy độc lập thật sự, không chỉ biến monolith thành “distributed monolith”.

**Trình tự:** Mũ xanh lam → trắng → đỏ → vàng → đen → xanh lá → đỏ lần hai → xanh lam.

---

# Mũ trắng — Thông tin khách quan

## 1. Thông tin đã biết

| Thông tin | Phân loại | Ý nghĩa |
|---|---|---|
| Đội có 4 người | `[FACT: user]` | Năng lực song song cho phát triển, kiểm thử, hạ tầng và vận hành bị giới hạn. |
| Ngân sách không tăng | `[FACT: user]` | Không thể mặc định mua thêm nền tảng observability, managed infrastructure hoặc nhân lực tư vấn. |
| Deadline cuối quý | `[FACT: user]` | Migration phải cạnh tranh năng lực với roadmap và vận hành hiện tại. |
| Hệ thống hiện ổn định | `[FACT: user]` | Migration là thay đổi chủ động, không phải biện pháp xử lý một sự cố cấp bách. |
| Deploy toàn hệ thống mất 45 phút | `[FACT: user]` | Có vấn đề về tốc độ delivery, nhưng chưa biết bottleneck nằm ở build, test, provisioning, migration database hay rollout. |
| Microservice cần khả năng provisioning, monitoring và deployment nhanh | `[FACT: Martin Fowler, “Microservice Prerequisites”]` | Nếu ba năng lực này chưa có, extraction sẽ tạo thêm gánh nặng vận hành. |
| Microservice có nhiều thành phần vận hành hơn; toàn hệ thống phức tạp hơn dù từng service có thể đơn giản hơn | `[FACT: Microsoft Azure Architecture Center, Microservices architecture style]` | Chi phí phối hợp, quan sát và xử lý lỗi phân tán cần được tính vào phạm vi. |
| Tách dữ liệu theo service khiến giao dịch ACID xuyên service không còn đơn giản; workflow liên service thường cần eventual consistency | `[FACT: Microsoft Learn, Data sovereignty/Data considerations for microservices]` | Đây là rủi ro đặc biệt quan trọng với thanh toán. |
| Strangler Fig cho phép thay thế dần monolith thay vì chuyển đổi một lần | `[FACT: AWS Prescriptive Guidance, Strangler Fig pattern]` | Có thể chạy song song, chuyển traffic có kiểm soát và duy trì đường fallback. |
| DORA đo hiệu năng delivery bằng nhiều chỉ số như deployment frequency, change lead time, change failure rate và recovery time | `[FACT: dora.dev, DORA metrics history]` | Chỉ số “deploy mất 45 phút” chưa đủ để kết luận microservice là giải pháp đúng. |

Nguồn tham khảo:

- https://martinfowler.com/bliki/MicroservicePrerequisites.html
- https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/strangler-fig.html
- https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices
- https://learn.microsoft.com/en-us/azure/architecture/microservices/design/data-considerations
- https://dora.dev/insights/dora-metrics-history/

## 2. Các giả định đang được sử dụng

- `[ASSUMPTION]` Bốn người phải tiếp tục duy trì sản phẩm trong khi migration.
- `[ASSUMPTION]` Module thanh toán hiện dùng chung database hoặc transaction với các module khác.
- `[ASSUMPTION]` Chưa có đội platform/SRE riêng hỗ trợ microservice.
- `[ASSUMPTION]` “Tách thành microservice” bao gồm deploy và vận hành độc lập, không chỉ di chuyển code sang repository/process khác.
- `[ASSUMPTION]` Mục tiêu kinh doanh chính là rút ngắn vòng đời release và giảm blast radius của thay đổi thanh toán.

## 3. Thông tin chưa có

| `[NEED-DATA]` | Cách lấy | Vì sao cần |
|---|---|---|
| Tần suất thay đổi/deploy module thanh toán | Git log và release history 3–6 tháng | Nếu payment rất ít thay đổi, lợi ích deploy độc lập sẽ thấp. |
| 45 phút được dùng vào đâu | Instrument từng stage CI/CD | Xác định microservice có thật sự giải quyết bottleneck hay không. |
| Tỷ lệ release có thay đổi payment | Phân loại release gần đây | Đánh giá mức độ payment đang chặn deploy chung. |
| Dependency graph của payment | Static analysis và workshop domain | Phát hiện coupling với order, ledger, refund, promotion, user. |
| Transaction và ownership dữ liệu | Trace các transaction DB | Xác định có thể cắt boundary an toàn hay cần saga/outbox. |
| Test coverage cho payment | Báo cáo unit/integration/E2E | Đánh giá khả năng regression và rollback. |
| Change failure rate, MTTR, incident history | Log incident và deployment | Có baseline để so sánh trước/sau. |
| Hạ tầng hiện có | Kiểm kê CI/CD, secrets, tracing, alerting, service discovery | Tính khối lượng platform cần bổ sung. |
| Yêu cầu PCI/compliance/audit | Security review | Tách service có thể thay đổi compliance scope. |
| Traffic, latency budget và SLO | Metrics/APM | Xác định tác động của network hop và failure modes mới. |

## 4. Ý kiến thường bị trình bày như sự thật

- “Microservice luôn deploy nhanh hơn” — **ý kiến có điều kiện**, không phải sự thật. Pipeline và phạm vi artifact mới quyết định thời gian deploy.
- “Payment là domain riêng nên tách rất dễ” — **chưa được chứng minh**. Domain logic có thể riêng nhưng dữ liệu và transaction vẫn coupling.
- “Hệ thống ổn định nên migration ít rủi ro” — **không đúng về mặt suy luận**. Chính migration tạo ra failure modes mới.
- “45 phút là quá chậm nên phải dùng microservice” — **kết luận thiếu dữ liệu**. Có thể 45 phút chủ yếu do test tuần tự hoặc build/cache kém.

---

# Mũ đỏ — Cảm nhận ban đầu

Trực giác của tôi: **không nên cam kết tách hoàn toàn payment service trong quý này**. Với đội 4 người và hệ thống đang ổn định, phương án big-bang tạo cảm giác rủi ro vượt quá giá trị ngắn hạn.

---

# Mũ vàng — Giá trị và mặt tích cực

Bảng này tập trung vào **Option 2: tách theo giai đoạn**, vì đây là cách vẫn thu được giá trị của extraction trong giới hạn hiện tại.

| Trọng tâm | Ngắn hạn — trong quý | Trung hạn — 1–2 quý sau | Dài hạn |
|---|---|---|---|
| **Lợi ích** | Làm rõ boundary của payment; bóc dependency; xây regression suite; tìm chính xác bottleneck deploy | Có thể release payment độc lập; giới hạn blast radius; scale riêng khi cần | Payment trở thành capability độc lập, dễ tích hợp gateway hoặc kênh bán hàng mới |
| **Giá trị** | Cải thiện chất lượng monolith ngay cả khi chưa extraction; giảm rủi ro thay đổi payment | Giảm lead time cho thay đổi payment; ownership rõ hơn | Tăng khả năng thay thế provider, mở rộng kiến trúc và audit độc lập |
| **Tính khả thi** | Cao nếu giới hạn phạm vi ở discovery, modularization, contract và shadow path | Khả thi sau khi có observability, idempotency và ownership dữ liệu | Khả thi nếu năng lực vận hành tăng cùng số lượng service |

## Giá trị cụ thể theo phương án

### Option 1 — Tách hoàn toàn

- Có khả năng deploy payment độc lập ngay sau migration.
- Tạo ownership kỹ thuật rõ ràng.
- Có thể scale hoặc cô lập tài nguyên payment.
- Buộc đội chuẩn hóa API, audit và idempotency.

### Option 2 — Tách theo giai đoạn

- Thu được phần lớn tri thức kiến trúc ngay trong quý.
- Có deliverable có thể kiểm chứng ở mỗi giai đoạn.
- Giữ được quyền dừng nếu dữ liệu cho thấy extraction không kinh tế.
- Boundary và test mới vẫn có giá trị nếu quyết định cuối cùng là modular monolith.

### Option 3 — Modular monolith và tối ưu pipeline

- Có thể tác động trực tiếp vào vấn đề 45 phút.
- Giữ mô hình transaction và vận hành đơn giản.
- Ít hạ tầng mới, phù hợp với đội nhỏ.
- Tạo nền tảng để extraction sau này dễ hơn.

---

# Mũ đen — Rủi ro và giới hạn

## Option 1 — Tách hoàn toàn trong quý

| Rủi ro | Cơ chế và bằng chứng | Khả năng | Tác động | Điều làm rủi ro tăng |
|---|---|---:|---:|---|
| Sai lệch giao dịch | Transaction nội bộ trở thành workflow phân tán; khó giữ ACID xuyên service | Cao nếu đang dùng chung DB | Rất cao | Refund, retry, timeout, webhook đến sai thứ tự |
| Charge trùng | Client hoặc gateway retry sau timeout trong khi trạng thái phản hồi chưa rõ | Trung bình–cao | Rất cao | Không có idempotency key và unique constraint |
| Distributed monolith | Service mới vẫn gọi đồng bộ nhiều module hoặc dùng chung database | Cao | Cao | Chỉ di chuyển code mà không tách ownership dữ liệu |
| Không hoàn thành đúng quý | Phạm vi gồm code, dữ liệu, pipeline, monitoring, alerting, migration và runbook | Cao | Cao | Team vẫn phải làm roadmap và support |
| Gánh nặng trực vận hành | Thêm process, dashboard, alert, secrets, certificate, backup và incident path | Cao | Trung bình–cao | Không có platform/SRE và automation |
| Regression khó phát hiện | Payment có nhiều edge case nghiệp vụ và tích hợp ngoài hệ thống | Trung bình–cao | Rất cao | Thiếu contract test, replay hoặc shadow traffic |
| Rollback không thực tế | Sau khi dữ liệu được ghi ở hai nơi, rollback binary không phục hồi consistency | Trung bình | Rất cao | Cutover đồng thời code và database |
| Không giải quyết 45 phút | Pipeline của monolith vẫn chậm đối với các release khác | Trung bình–cao | Trung bình | Bottleneck là test/build chung chứ không phải payment |
| Chi phí cơ hội | Bốn người tập trung migration thay vì tính năng, bảo trì và tối ưu pipeline | Cao | Cao | Deadline kinh doanh khác vẫn giữ nguyên |

## Option 0 — Không làm gì

| Rủi ro | Cơ chế | Khả năng | Tác động |
|---|---|---:|---:|
| Lead time tiếp tục dài | Mọi thay đổi vẫn đi qua pipeline 45 phút | Chắc chắn | Trung bình |
| Coupling tiếp tục tăng | Tính năng mới tiếp tục gọi trực tiếp vào payment internals | Trung bình–cao | Cao về dài hạn |
| Migration sau này khó hơn | Data model và dependency mở rộng | Trung bình | Cao |
| Blast radius không giảm | Release nhỏ vẫn phụ thuộc toàn hệ thống | Cao | Trung bình–cao |
| Đội quen với pain hiện tại | Không có baseline và owner cải tiến | Trung bình | Trung bình |

## Option 3 — Chỉ tối ưu modular monolith/pipeline

- Có thể cải thiện tốc độ deploy nhưng không cung cấp deployment independence thực sự.
- Nếu payment thay đổi rất thường xuyên, lợi ích có thể không đủ.
- Boundary chỉ tồn tại ở mức code nếu không có enforcement test hoặc ownership rule.
- Đội có thể trì hoãn extraction vô thời hạn dù nhu cầu đã rõ.

---

# Mũ xanh lá — Các phương án và cải tiến sáng tạo

Phần này chỉ tạo lựa chọn, chưa xếp hạng.

1. **Strangler theo chiều đọc trước, ghi sau**
   - Tạo Payment API.
   - Chuyển query/status sang service trước.
   - Giữ command/charge trong monolith cho tới khi consistency được chứng minh.

2. **Service façade nhưng chưa tách database**
   - Tạo interface và process độc lập.
   - Sử dụng schema ownership rõ ràng trong database hiện tại.
   - Tách vật lý database ở giai đoạn sau.

3. **Modular monolith có “fitness tests”**
   - Payment thành module nội bộ với public interface duy nhất.
   - CI fail nếu module khác truy cập trực tiếp bảng hoặc package nội bộ của payment.
   - Giữ một deployable trong khi chuẩn bị boundary thật.

4. **Shadow payment service**
   - Monolith vẫn là nguồn quyết định.
   - Nhân bản event sang service mới.
   - So sánh kết quả state machine mà chưa cho service mới charge thật.

5. **Canary theo loại giao dịch**
   - Chỉ chuyển một payment provider, tenant nội bộ hoặc loại giao dịch rủi ro thấp.
   - Các luồng còn lại tiếp tục qua monolith.

6. **Outbox + inbox/idempotency trước khi extraction**
   - Chuẩn hóa durable event publication trong monolith.
   - Service mới xử lý message bằng inbox và idempotency key.
   - Replay được sự kiện để phục hồi.

7. **Tách deployment unit nhưng dùng chung repository**
   - Monorepo, shared tooling, hai pipeline.
   - Không buộc đội 4 người quản lý thêm nhiều repository.

8. **Tối ưu pipeline trước**
   - Cache dependency/build.
   - Chạy test song song.
   - Chỉ chạy test theo affected modules.
   - Tách database migration khỏi application rollout khi an toàn.

9. **Đảo ngược câu hỏi**
   - Không hỏi “làm sao tách payment trong quý”.
   - Hỏi “làm sao đưa thay đổi payment lên production trong dưới N phút với mức rủi ro chấp nhận được”.
   - Microservice chỉ là một trong các cơ chế.

10. **Ý tưởng phi truyền thống: internal payment simulator**
    - Ghi lại và ẩn danh webhook/event production.
    - Replay vào implementation mới để đối chiếu state transition.
    - Dùng kết quả đối chiếu làm cổng cutover.

---

# Mũ đỏ — Kiểm tra cảm nhận lần hai

Sau phân tích, trực giác chuyển từ “không nên tách” sang **“nên bắt đầu extraction nhưng tuyệt đối không cam kết big-bang hoàn tất trong quý”**. Điểm còn gây bất an lớn nhất là ownership dữ liệu và consistency của các luồng charge/refund.

---

# Mũ xanh lam — Kết luận và kế hoạch hành động

## 1. Quyết định

**Không nên chọn Option 1: tách hoàn toàn payment thành production microservice trong quý này với một deadline cố định.**

**Nên chọn Option 2 kết hợp Option 3:**

> Trong quý này, thực hiện một chương trình extraction có cổng kiểm soát: đo và tối ưu pipeline, modularize payment, thiết lập contract/idempotency/observability, sau đó chạy shadow hoặc canary. Chỉ cutover production nếu tất cả tiêu chí go/no-go đạt; nếu không, kết thúc quý với một modular monolith tốt hơn và kế hoạch extraction đã được chứng minh.

Lý do quyết định:

- Vấn đề quan sát được là deploy 45 phút, chưa có bằng chứng microservice là nguyên nhân hoặc giải pháp trực tiếp.
- Hệ thống đang ổn định nên không có lý do để chấp nhận cutover cưỡng bức.
- Payment có mức tác động tài chính lớn.
- Đội 4 người, không thêm ngân sách, khó đồng thời xây feature, nền tảng microservice và năng lực vận hành.
- Phương án theo giai đoạn giữ được lợi ích kiến trúc nhưng có khả năng dừng và rollback.

## 2. Phạm vi cam kết cuối quý

### Bắt buộc hoàn thành

- Có baseline CI/CD và DORA-like metrics.
- Xác định payment boundary và dependency graph.
- Payment có internal API/contract rõ ràng.
- Có idempotency cho charge/refund.
- Có regression và contract tests cho luồng quan trọng.
- Có correlation ID, structured log, metrics và alert cơ bản.
- Có thiết kế ownership dữ liệu và migration.
- Có proof-of-concept shadow hoặc canary.
- Có runbook rollback/fallback đã diễn tập.

### Không cam kết vô điều kiện

- Chuyển 100% production traffic.
- Tách hoàn toàn database.
- Xóa implementation payment cũ khỏi monolith.
- Đạt service autonomy hoàn chỉnh trong cùng quý.

## 3. Kế hoạch 8 bước

Thời gian dưới đây nên co giãn theo số tuần thực tế còn lại của quý.

| Bước | Thời lượng | Owner chính | Công việc | Tiêu chí thoát |
|---|---:|---|---|---|
| 1. Baseline | 2–3 ngày | Tech lead + platform owner | Đo từng stage trong 45 phút; lấy deployment frequency, failure rate, MTTR; thống kê release có payment | Biết ít nhất 80% thời gian deploy đang nằm ở đâu |
| 2. Domain mapping | 3–5 ngày | Tech lead + backend | Vẽ dependency, transaction, bảng dữ liệu, webhook, refund/reconcile flow | Không còn dependency payment quan trọng chưa được phân loại |
| 3. Pipeline quick wins | 3–5 ngày | Platform/full-stack | Cache, parallel test, affected-test, build artifact một lần | Có số liệu trước/sau; pipeline giảm mà không bỏ quality gate |
| 4. Modularize | 1–2 tuần | Hai backend | Đóng payment sau interface; chặn truy cập trực tiếp package/table; tạo API contract | Monolith chỉ gọi payment qua contract công khai |
| 5. Safety foundation | 1–2 tuần, chạy song song | Backend + QA | Idempotency, outbox/inbox nếu cần, contract/integration tests, failure injection | Retry không charge trùng; event replay an toàn |
| 6. Service skeleton | 1 tuần | Backend + platform | Runtime, CI/CD, config/secrets, health check, tracing, dashboard | Deploy service độc lập và quan sát được ở staging |
| 7. Shadow/canary | 1 tuần | Cả đội | Replay/shadow traffic hoặc canary một luồng nhỏ; đối chiếu trạng thái | Không có mismatch chưa giải thích; SLO đạt |
| 8. Go/no-go | 1 ngày | Tech lead + product/risk owner | Xem số liệu và diễn tập rollback | Quyết định cutover, kéo dài thử nghiệm hoặc giữ modular monolith |

## 4. Phân công gợi ý cho đội 4 người

| Vai trò | Trách nhiệm |
|---|---|
| Người 1 — Tech lead/backend | Boundary, ADR, transaction model, go/no-go |
| Người 2 — Backend | Payment contract, idempotency, outbox/inbox, service implementation |
| Người 3 — Platform/full-stack | CI/CD, deployment, secrets, tracing, dashboard, rollback |
| Người 4 — QA/product-capable engineer | Test matrix, contract/E2E, replay, reconciliation và acceptance |

Không nên để cả bốn người cùng tập trung vào extraction toàn thời gian; cần duy trì ít nhất một rotation để xử lý vận hành và sản phẩm hiện tại.

## 5. Cổng go/no-go trước khi nhận traffic thật

Chỉ cutover nếu **tất cả** điều kiện sau đạt:

1. Không còn transaction ACID xuyên boundary mà chưa có giải pháp cụ thể.
2. Charge, refund và webhook đều có idempotency.
3. Contract/integration tests cho các luồng tiền quan trọng đều pass.
4. Shadow/replay không có mismatch chưa giải thích.
5. Có reconciliation job phát hiện giao dịch lệch.
6. Có dashboard, alert, trace xuyên monolith–service.
7. Có timeout, retry và circuit-breaking policy rõ ràng.
8. Có fallback route về monolith.
9. Đã diễn tập rollback bằng staging/canary.
10. Đội xác nhận trực vận hành được bằng nguồn lực hiện tại.
11. Service deploy độc lập thật sự; không yêu cầu deploy monolith cùng lúc.
12. Kết quả đo chứng minh thay đổi này cải thiện mục tiêu delivery hoặc reliability đã thống nhất.

Nếu một trong các điều kiện 1–9 không đạt, quyết định mặc định là **không cutover trong quý**.

## 6. Khi nào quyết định sẽ đảo chiều?

### Chuyển sang “tách hoàn toàn ngay trong quý” nếu

- Payment chiếm tỷ lệ lớn trong các release.
- Coupling và transaction boundary đơn giản hơn giả định.
- Đã có sẵn CI/CD, monitoring, tracing và container platform.
- Test automation đủ mạnh.
- Có thể dành phần lớn capacity của đội cho migration.
- Shadow/canary đạt toàn bộ gate sớm.

### Chuyển sang “không cần microservice” nếu

- Phần lớn 45 phút nằm ở pipeline có thể tối ưu trực tiếp.
- Payment ít thay đổi.
- Không có nhu cầu scale hoặc deploy riêng.
- Tách dữ liệu buộc tạo quá nhiều transaction phân tán.
- Chi phí vận hành service lớn hơn lợi ích delivery đo được.

## 7. Mốc quyết định đề xuất

- **Gate A — sau baseline và domain mapping:** microservice có giải quyết đúng vấn đề không?
- **Gate B — sau modularization:** boundary có đủ sạch để tách không?
- **Gate C — sau shadow/canary:** implementation mới có đúng và vận hành được không?
- **Gate D — trước cuối quý:** cutover giới hạn, tiếp tục shadow ở quý sau, hoặc dừng tại modular monolith.

## Kết luận ngắn

**Không tách hoàn toàn bằng deadline cưỡng bức trong quý này.**  
**Có bắt đầu tách theo Strangler, với mục tiêu quý này là tạo boundary, safety foundation, pipeline độc lập và shadow/canary.** Production cutover là kết quả của các cổng kỹ thuật, không phải mục tiêu phải đạt bằng mọi giá.
