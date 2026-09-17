# Mũ xanh lam — Mở phiên và xác định quyết định

**Chế độ:** `full`

**Vấn đề:** Đội 4 người cần quyết định có nên hoàn tất việc tách module thanh toán khỏi monolith thành một microservice độc lập ngay trong quý này hay không.

## Các phương án

- **Option 0: giữ nguyên hiện trạng** — không tách service, tiếp tục deploy toàn monolith trong 45 phút.
- **Phương án 1: tách hoàn toàn trong quý này** — service thanh toán có runtime, dữ liệu, pipeline deploy và vận hành độc lập.
- **Phương án 2: chuẩn bị và tách theo giai đoạn** — trong quý này tối ưu pipeline, xác lập boundary, bổ sung observability/test, triển khai skeleton hoặc shadow traffic; chỉ chuyển production khi qua cổng go/no-go.
- **Phương án 3: modular monolith** — tách payment thành module nội bộ có API và quyền sở hữu dữ liệu rõ ràng, nhưng chưa tạo distributed system.

## Ràng buộc cứng

- Đội chỉ có 4 người.
- Ngân sách không tăng.
- Deadline cuối quý.
- Hệ thống đang ổn định.
- Không nên hy sinh tính đúng đắn của thanh toán chỉ để đạt mục tiêu kiến trúc.

## Giả định

- “Tách thành microservice” nghĩa là payment có thể build, deploy, rollback và vận hành độc lập.
- Payment có giao dịch liên quan đến order, ledger, refund hoặc các callback từ cổng thanh toán.
- Chưa có bằng chứng rằng 45 phút deploy chủ yếu do payment gây ra.
- Chưa biết đội đã có nền tảng CI/CD, tracing, message broker, idempotency và khả năng vận hành nhiều service hay chưa.

## Tiêu chí thành công

1. Không phát sinh mất tiền, thu tiền hai lần, sai trạng thái hoặc giao dịch không đối soát được.
2. Có rollback hoặc kill switch được kiểm chứng.
3. Đường thanh toán mới có monitoring, tracing, audit và cảnh báo.
4. Payment thực sự deploy độc lập.
5. Không làm chậm roadmap sản phẩm ngoài phạm vi đã thống nhất.
6. Thời gian và blast radius của deploy được cải thiện đo lường được.

**Trình tự:** Mũ xanh lam → Mũ trắng → Mũ đỏ → Mũ vàng → Mũ đen → Mũ xanh lá → Mũ đỏ kiểm tra → Mũ xanh lam.

---

# Mũ trắng — Dữ kiện khách quan

## 1. Thông tin đã biết

| Thông tin | Phân loại và nguồn |
|---|---|
| Đội có 4 người | `[FACT: mô tả của người dùng]` |
| Ngân sách không tăng | `[FACT: mô tả của người dùng]` |
| Deadline là cuối quý | `[FACT: mô tả của người dùng]` |
| Hệ thống hiện ổn định | `[FACT: mô tả của người dùng]` |
| Deploy toàn hệ thống mất 45 phút | `[FACT: mô tả của người dùng]` |
| Microservice đòi hỏi khả năng triển khai nhanh, provisioning tự động, monitoring và phối hợp vận hành tốt | `[FACT: Martin Fowler, Microservice Prerequisites — https://martinfowler.com/bliki/MicroservicePrerequisites.html]` |
| Khi một nghiệp vụ đi qua nhiều service và nhiều nguồn dữ liệu, không còn một giao dịch ACID đơn giản bao phủ toàn bộ; cần cơ chế như Saga và compensating transaction | `[FACT: Microsoft Azure Architecture Center, Saga pattern — https://learn.microsoft.com/en-us/azure/architecture/patterns/saga]` |
| Strangler Fig cho phép chuyển đổi monolith từng phần, giảm gián đoạn so với thay thế một lần | `[FACT: AWS Prescriptive Guidance — https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html]` |
| Khi dùng messaging, transactional outbox giải quyết khoảng trống giữa cập nhật database và phát event; consumer thường cần idempotent vì message có thể được giao lại | `[FACT: Microservices.io, Transactional Outbox — https://microservices.io/patterns/data/transactional-outbox.html]` |

## 2. Thông tin chưa biết

| Khoảng trống | Vì sao quan trọng |
|---|---|
| 45 phút nằm ở build, test, provisioning, migration hay rollout | Nếu nút thắt không nằm ở payment, tách service có thể không giải quyết vấn đề |
| Tần suất deploy và chi phí thực của mỗi lần deploy | 45 phút chỉ đáng ưu tiên nếu nó thường xuyên cản trở delivery hoặc recovery |
| Payment đang phụ thuộc vào bao nhiêu bảng và module | Quyết định độ khó của boundary và migration dữ liệu |
| Giao dịch nào phải nhất quán giữa payment, order, inventory, invoice và refund | Quyết định có cần Saga, outbox, reconciliation hay không |
| Payment hiện có test tự động đến mức nào | Thiếu regression và contract test làm migration rủi ro |
| Mức độ sẵn sàng của logging, metrics, tracing và alerting | Microservice có thêm failure mode mạng và cần quan sát độc lập |
| Đội đã vận hành container/service độc lập hay chưa | Ảnh hưởng lớn đến khối lượng học tập và platform work |
| Còn bao nhiêu tuần thực tế trong quý | Không thể đánh giá chắc chắn khả năng hoàn thành nếu thiếu dữ liệu này |
| SLA, lưu lượng, tỷ lệ lỗi và yêu cầu compliance | Cần để thiết kế rollout, timeout, retry, audit và capacity |
| Khả năng chạy song song đường cũ và đường mới | Quyết định có thể dùng shadow/canary an toàn hay không |

## 3. Nhận định đang được trình bày như dữ kiện

- “Deploy mất 45 phút nên phải chuyển sang microservice” là **một giả thuyết**, không phải dữ kiện đã chứng minh.
- “Payment là bounded context rõ nên dễ tách” là **ý kiến kiến trúc**, cần dependency mapping xác nhận.
- “Microservice chắc chắn làm hệ thống nhanh hơn” là **ý kiến**; nó có thể cải thiện deploy độc lập nhưng cũng thêm network latency và vận hành phân tán.
- “Hệ thống đang ổn định nên migration sẽ dễ” là **ý kiến**; ổn định hiện tại không chứng minh boundary dữ liệu sạch.
- “Payment là ứng viên tốt nhất để tách đầu tiên” là **ý kiến**; tính quan trọng của payment cũng có thể khiến nó trở thành ứng viên rủi ro nhất.

## 4. Dữ liệu cần thu thập

- `[NEED-DATA: xuất timing của 20 pipeline gần nhất và phân rã theo build, test, image, migration, deploy, health check]` Xác định nguyên nhân thực của 45 phút.
- `[NEED-DATA: lập dependency map từ code, database schema và runtime tracing cho payment]` Đếm module, bảng, API và job nền liên quan.
- `[NEED-DATA: liệt kê payment workflow và failure path cùng Product/Finance]` Bao gồm authorize, capture, cancel, refund, timeout, webhook và reconciliation.
- `[NEED-DATA: chạy test coverage report và kiểm kê integration/contract tests cho payment]` Xác định khoảng trống an toàn.
- `[NEED-DATA: kiểm kê CI/CD, observability, secrets, service discovery và rollback hiện có]` Xác định platform gap.
- `[NEED-DATA: lấy số liệu ba tháng về deployment frequency, deployment failures, rollback time và payment incidents]` Xác định giá trị kinh doanh và baseline.
- `[NEED-DATA: xác nhận số tuần còn lại và roadmap bắt buộc của cả bốn thành viên]` Tính capacity thực tế.

---

# Mũ đỏ — Cảm nhận ban đầu

Trực giác theo mẫu hình cho thấy việc cam kết tách hoàn toàn payment ngay trong quý này là quá mạo hiểm đối với đội 4 người, trong khi nguyên nhân của 45 phút deploy còn chưa được xác định.

---

# Mũ vàng — Giá trị tích cực

| Trọng tâm | Ngắn hạn | Trung hạn | Dài hạn |
|---|---|---|---|
| **Lợi ích** | Payment có boundary và ownership rõ hơn; thay đổi payment có thể được kiểm thử riêng | Có khả năng deploy và rollback payment mà không triển khai toàn monolith | Payment có thể scale, bảo trì và phát hành độc lập |
| **Giá trị** | Dependency mapping và contract tests làm lộ technical debt hiện có | Giảm blast radius của các thay đổi payment; nhóm khác ít bị khóa bởi release chung | Tạo mẫu chuẩn để tách các bounded context tiếp theo |
| **Tính khả thi** | Modular hóa trong monolith và đo pipeline nằm trong tầm của đội nhỏ | Strangler, shadow traffic hoặc canary cho phép chuyển từng phần | Khi nền tảng CI/CD và observability đã dùng lại được, service tiếp theo có chi phí biên thấp hơn |

Các điểm sáng cụ thể:

- **Ngắn hạn:** Ngay cả khi chưa cutover, việc định nghĩa API, ownership và test boundary vẫn làm payment an toàn hơn.
- **Trung hạn:** Nếu payment thay đổi thường xuyên, independent deployment có thể rút ngắn lead time và giảm số thành phần bị ảnh hưởng.
- **Dài hạn:** Một “golden path” cho service—pipeline, dashboard, alert, secret, rollback—có thể tái sử dụng cho kiến trúc tương lai.
- Tách theo Strangler cho phép giữ đường cũ làm fallback trong thời gian xác minh đường mới.

---

# Mũ đen — Rủi ro

| Phương án / rủi ro | Cơ chế và bằng chứng | Khả năng | Tác động | Yếu tố làm xấu hơn |
|---|---|---:|---:|---|
| **Phương án 1: sai nhất quán giao dịch** | Payment và order chuyển từ transaction cục bộ sang giao tiếp phân tán; Saga cần compensation và xử lý lỗi từng bước | Cao nếu đang dùng chung DB | Rất cao | Boundary dữ liệu mơ hồ, thiếu reconciliation |
| **Phương án 1: thu tiền lặp hoặc mất event** | Retry, timeout và giao message lại có thể tạo duplicate; update DB và publish event không nguyên tử nếu thiếu outbox | Trung bình–cao | Rất cao | Không có idempotency key, inbox/outbox và audit log |
| **Phương án 1: hoàn thành “bề ngoài”** | Áp lực cuối quý có thể tạo distributed monolith: service riêng nhưng vẫn dùng chung DB và release phụ thuộc | Cao | Cao | Deadline cố định, thiếu platform automation |
| **Phương án 1: quá tải đội 4 người** | Đội phải đồng thời làm domain split, data migration, API, CI/CD, observability, bảo mật và trực vận hành | Cao | Cao | Vẫn giữ nguyên roadmap tính năng |
| **Phương án 1: cải thiện sai vấn đề** | 45 phút có thể nằm ở test suite hoặc provisioning chung, không nằm ở payment | Trung bình–cao | Trung bình–cao | Không phân tích pipeline trước |
| **Phương án 1: hồi quy trên hệ thống đang ổn định** | Migration tạo thêm đường mạng, timeout và partial failure | Trung bình | Rất cao | Cutover một lần, không shadow/canary |
| **Phương án 2: kéo dài trạng thái kép** | Hai đường xử lý hoặc compatibility layer làm tăng độ phức tạp tạm thời | Trung bình | Trung bình | Không đặt ngày xóa đường cũ |
| **Phương án 3: chưa đạt deploy độc lập** | Modular monolith cải thiện cấu trúc nhưng vẫn deploy cùng ứng dụng | Chắc chắn | Trung bình | Tổ chức coi modularization là kết quả cuối cùng |
| **Option 0: tiếp tục mất 45 phút mỗi deploy** | Pipeline hiện tại giữ nguyên | Cao | Trung bình | Deploy thường xuyên hoặc cần hotfix gấp |
| **Option 0: coupling tiếp tục tăng** | Không có boundary enforcement khiến payment ngày càng khó tách | Trung bình | Cao về dài hạn | Tính năng mới tiếp tục truy cập trực tiếp dữ liệu payment |
| **Option 0: thời gian phục hồi có thể chậm** | Nếu hotfix phải đi qua toàn pipeline 45 phút, sự cố payment bị kéo dài | Trung bình | Cao | Không có fast-track rollback/hotfix |

Rủi ro trọng yếu không phải là viết API mới, mà là bảo toàn **tính đúng đắn tài chính trong partial failure** và gánh nặng vận hành sau cutover.

---

# Mũ xanh lá — Các cách làm khác và cải tiến

1. **Pipeline-first:** dành đầu quý để phân rã 45 phút; cache dependency, chạy test song song, tách smoke test, tối ưu image và rollout.
2. **Modular monolith trước:** tạo `PaymentFacade` hoặc application API; cấm module khác đọc/ghi trực tiếp bảng payment.
3. **Strangler theo capability nhỏ:** tách webhook ingestion, payment status query hoặc reconciliation worker trước luồng charge chính.
4. **Skeleton service:** dựng service, pipeline, dashboard và health check nhưng chưa nhận production traffic.
5. **Shadow traffic:** gửi bản sao request hoặc event sang service mới, không cho phép service mới tạo side effect; so sánh kết quả.
6. **Canary theo merchant hoặc tỷ lệ nhỏ:** route một phạm vi giới hạn, luôn có kill switch quay về monolith.
7. **Shared database tạm thời có thời hạn:** tạo schema ownership và cấm cross-write, rồi tách database ở phase sau.
8. **Outbox trong monolith trước:** xuất domain event đáng tin cậy rồi mới thêm service consumer.
9. **Tách deploy unit nhưng chưa tách dữ liệu:** dùng như một bước chuyển tiếp có ADR và hạn chót loại bỏ coupling.
10. **Thay đổi mục tiêu quý:** thay “hoàn tất microservice” bằng “đạt production readiness và chứng minh một vertical slice”.
11. **Ý tưởng khác thường:** giữ payment core trong monolith, nhưng tạo “deployment cell” chỉ build và kiểm thử phần bị thay đổi để đạt lợi ích lead time mà chưa tạo distributed system.
12. **Nếu bỏ ràng buộc deadline:** chạy một chu kỳ đầy đủ qua staging, shadow, canary và reconciliation trước khi chuyển toàn bộ traffic.

---

# Mũ đỏ — Kiểm tra lại

Sau phân tích, trực giác chuyển từ “không nên tách” sang “nên bắt đầu tách có kiểm soát, nhưng không cam kết cutover toàn bộ trong quý này”.

---

# Mũ xanh lam — Quyết định và kế hoạch hành động

## Khuyến nghị

**Không nên cam kết hoàn tất việc tách toàn bộ module thanh toán thành microservice production trong quý này.**

**Nên chọn Phương án 2:** thực hiện một chương trình tách theo giai đoạn, với mục tiêu quý là:

1. Xác định nguyên nhân của pipeline 45 phút và tối ưu phần có thể tối ưu.
2. Cô lập payment thành boundary rõ trong monolith.
3. Hoàn thiện contract test, idempotency, audit, reconciliation và observability.
4. Dựng service cùng pipeline deploy độc lập.
5. Chứng minh một vertical slice qua shadow hoặc canary.
6. Chỉ cutover production trong quý nếu vượt qua cổng go/no-go; nếu không, giữ monolith làm đường chính.

Đây không phải là trì hoãn vô thời hạn. Đây là **đổi từ deadline theo kiến trúc sang deadline theo bằng chứng an toàn**.

## Điều kiện đảo chiều

Có thể chuyển sang **Phương án 1 — cutover hoàn toàn trong quý** nếu, sau discovery:

- Payment đã có boundary sạch, ít shared table và ít transaction xuyên module.
- Đội đã có sẵn pipeline, deployment automation, tracing, alerting và rollback cho service độc lập.
- Test tự động bao phủ toàn bộ payment workflow quan trọng.
- Shadow/canary không phát hiện sai lệch về trạng thái và số tiền.
- Có idempotency, outbox/inbox hoặc cơ chế tương đương.
- Có reconciliation tự động và kill switch đã diễn tập.
- Capacity còn lại đủ mà không bỏ các cam kết kinh doanh bắt buộc.

Chuyển sang **Phương án 3 — chỉ modular monolith trong quý** nếu:

- Dependency map cho thấy payment dùng chung dữ liệu sâu với order hoặc accounting.
- Pipeline analysis cho thấy tách payment không cải thiện đáng kể thời gian deploy.
- Đội thiếu nền tảng observability hoặc kinh nghiệm vận hành service độc lập.
- Không thể xây dựng fallback và reconciliation trước cuối quý.

## Kế hoạch hành động

| Giai đoạn | Công việc chính | Chủ trì | Mốc / thời hạn | Tiêu chí hoàn thành |
|---|---|---|---|---|
| **1. Đo baseline** | Phân rã 20 pipeline; đo frequency, failure và rollback; lập dependency map payment | Tech Lead + DevOps owner | Tuần 1 | Có báo cáo nguyên nhân 45 phút và sơ đồ dependency/data flow |
| **2. Chốt boundary** | Vẽ workflow authorize/capture/refund/webhook; định nghĩa API, event, ownership dữ liệu và failure handling | Tech Lead + Backend engineer | Tuần 2 | ADR được duyệt; không còn transaction quan trọng chưa có owner hoặc chiến lược consistency |
| **3. Tăng safety net** | Contract test, integration test, idempotency key, audit log, reconciliation và dashboard | Hai backend engineers + QA owner luân phiên | Tuần 3–4 | Các workflow quan trọng có test; duplicate và timeout được mô phỏng thành công |
| **4. Tối ưu deploy hiện tại** | Cải thiện các stage chậm đã xác định; tạo fast rollback hoặc hotfix path | DevOps owner + một engineer | Tuần 3–4, song song | Có số đo trước/sau; pipeline giảm theo mục tiêu do đội đặt từ baseline |
| **5. Dựng vertical slice** | Tạo payment service skeleton, pipeline độc lập, secrets, health check, tracing; di chuyển một capability nhỏ | Hai engineers | Tuần 5–7 | Service deploy độc lập trên staging; monolith vẫn là fallback |
| **6. Shadow và đối soát** | Nhân bản traffic không side effect hoặc replay dữ liệu đã ẩn thông tin nhạy cảm; so sánh kết quả | Cả đội, Tech Lead chịu trách nhiệm | Tuần 8–9 | Không có sai lệch chưa giải thích; dashboard và alert hoạt động |
| **7. Cổng go/no-go** | Đánh giá correctness, rollback, capacity, vận hành và tác động roadmap | Tech Lead + Product owner + Finance/Operations | Cuối tuần 9 | Biên bản quyết định cutover, canary tiếp, hoặc dừng ở modular monolith |
| **8. Canary có điều kiện** | Chuyển phạm vi nhỏ, theo dõi, diễn tập kill switch và reconciliation | On-call owner + Tech Lead | Phần còn lại của quý | Không có sai lệch tài chính; rollback đạt yêu cầu; vận hành chấp nhận được |
| **9. Kết thúc quý** | Chốt ADR, runbook, backlog xóa compatibility layer và kế hoạch phase tiếp theo | Tech Lead | Cuối quý | Không còn trạng thái thử nghiệm không có owner hoặc hạn xử lý |

## Phân công gợi ý cho đội 4 người

- **Người 1 — Tech Lead/domain:** boundary, ADR, consistency, go/no-go.
- **Người 2 — Payment implementation:** API, idempotency, workflow.
- **Người 3 — Data/integration:** outbox, reconciliation, migration, contract tests.
- **Người 4 — Delivery/reliability:** CI/CD, metrics, tracing, alerts, rollout và rollback.

Mỗi người vẫn review chéo; không để một cá nhân trở thành người duy nhất hiểu luồng tiền.

## Cổng go/no-go bắt buộc trước khi nhận tiền thật

Chỉ cho phép canary có side effect khi tất cả điều sau đều đạt:

- API và event contract đã version hóa.
- Idempotency được kiểm thử bằng request lặp.
- Timeout, retry và callback đến sai thứ tự đã được kiểm thử.
- Có audit trail nối được order, payment intent, provider transaction và refund.
- Có reconciliation phát hiện sai lệch.
- Có dashboard business và technical.
- Có kill switch và rollback được diễn tập.
- Không có dual-write không kiểm soát.
- Có người trực và runbook xử lý partial failure.

## Câu hỏi còn mở

Các `[NEED-DATA]` quan trọng nhất phải được giải quyết trước cuối Tuần 2:

1. Phần nào thực sự chiếm 45 phút deploy?
2. Payment có bao nhiêu shared table và transaction xuyên boundary?
3. Đội hiện có những năng lực CI/CD và observability nào?
4. Còn bao nhiêu capacity thực trong quý?
5. Tần suất deploy và sự cố hiện tại có đủ lớn để biện minh cho chi phí phân tán không?

**Kết luận ngắn:** Bắt đầu quá trình tách trong quý này, nhưng không lấy “microservice đã cutover 100%” làm cam kết. Cam kết đúng là **đạt đủ bằng chứng kỹ thuật để cutover an toàn**, đồng thời xử lý trực tiếp nút thắt deploy 45 phút.
