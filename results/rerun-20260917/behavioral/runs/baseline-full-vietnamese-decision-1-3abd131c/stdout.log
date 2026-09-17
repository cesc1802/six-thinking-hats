# Kết luận điều hành

**Không nên tách toàn bộ module thanh toán thành microservice và chuyển production ngay trong quý này.**

Nên chọn phương án:

> **Giữ luồng thanh toán hiện tại trong monolith, nhưng trong quý này chuẩn hóa ranh giới module, cải thiện pipeline deploy và xây dựng một “đường tách” có thể kiểm chứng.**  
> Chỉ triển khai microservice theo kiểu pilot/shadow nếu đạt đủ tiêu chí an toàn; chưa chuyển toàn bộ traffic.

Lý do chính: hệ thống đang ổn định, đội chỉ có 4 người, ngân sách không tăng và thanh toán là miền nghiệp vụ có rủi ro cao. Deploy mất 45 phút là vấn đề thật, nhưng **chưa đủ để chứng minh microservice là giải pháp đúng**—vì việc tách có thể thay một vấn đề deploy bằng nhiều vấn đề khó hơn: giao dịch phân tán, retry, idempotency, quan sát hệ thống, bảo mật, vận hành và đối soát.

---

# Phân tích theo 6 chiếc mũ

## 1. Mũ trắng – Dữ kiện và thông tin còn thiếu

### Dữ kiện đã biết

- Đội có **4 người**.
- **Không tăng ngân sách**.
- Deadline vào **cuối quý**.
- Hệ thống hiện tại **ổn định**.
- Deploy toàn hệ thống mất **45 phút**.
- Module cần xem xét là **thanh toán**, thuộc nhóm nghiệp vụ quan trọng và nhạy cảm.

### Điều chưa biết nhưng ảnh hưởng trực tiếp đến quyết định

Cần thu thập ngay:

- Tần suất deploy hiện tại.
- Trong 45 phút, thời gian nằm ở build, test, migration, rollout hay kiểm tra thủ công.
- Payment có thường xuyên làm chậm hoặc chặn release của phần khác không.
- Số lượng sự cố thanh toán và tỷ lệ giao dịch lỗi.
- Kiến trúc dữ liệu:
  - Payment có sở hữu bảng riêng không?
  - Có bao nhiêu bảng dùng chung với order, invoice, user?
  - Có transaction xuyên nhiều module không?
- Tích hợp với cổng thanh toán có hỗ trợ idempotency, webhook retry và reconciliation không.
- Hạ tầng hiện tại có sẵn:
  - CI/CD cho nhiều service;
  - service discovery;
  - secret management;
  - centralized logging;
  - tracing;
  - metrics và alerting;
  - container orchestration hoặc cơ chế deploy độc lập.
- Đội đã từng vận hành microservice production chưa.
- Mục tiêu thực tế của việc tách:
  - giảm thời gian deploy;
  - deploy độc lập;
  - tăng độ ổn định;
  - tăng tốc phát triển;
  - đáp ứng tải;
  - hay phân tách quyền sở hữu?

### Nhận định từ dữ kiện hiện có

Hiện tại chỉ có một pain point định lượng được: **deploy 45 phút**. Chưa có bằng chứng rằng payment cần scale riêng, gây sự cố, hoặc làm nghẽn phát triển. Vì vậy chưa đủ cơ sở để chấp nhận rủi ro của một cuộc di chuyển hoàn chỉnh.

---

## 2. Mũ đỏ – Cảm nhận và trực giác

- Việc động vào payment trước deadline cuối quý tạo cảm giác rủi ro cao.
- Đội 4 người dễ bị quá tải khi vừa phát triển, vừa migration, vừa trực vận hành.
- Hệ thống đang ổn định nên một cuộc tách lớn có nguy cơ “sửa thứ chưa hỏng”.
- Deploy 45 phút gây khó chịu, nhưng trực giác cho thấy nên tối ưu pipeline trước khi đổi kiến trúc.
- Microservice có thể hấp dẫn về mặt kỹ thuật, nhưng dễ trở thành dự án hạ tầng trá hình thay vì tạo giá trị trong quý.

Cảm nhận tổng thể: **không nên cược độ ổn định của thanh toán vào một deadline cố định khi chưa có dữ liệu chứng minh lợi ích.**

---

## 3. Mũ đen – Rủi ro và lý do phản đối

### Rủi ro kỹ thuật

1. **Giao dịch phân tán**

   Trong monolith, order và payment có thể cùng nằm trong một database transaction. Sau khi tách, cần xử lý:

   - payment thành công nhưng order chưa cập nhật;
   - order bị hủy nhưng payment vẫn hoàn tất;
   - timeout nhưng không biết giao dịch ở cổng thanh toán đã thành công hay chưa;
   - webhook đến chậm, trùng hoặc sai thứ tự.

2. **Duplicate charge**

   Retry không đúng hoặc thiếu idempotency có thể khiến khách hàng bị tính tiền nhiều lần. Đây là rủi ro nghiêm trọng hơn việc deploy chậm.

3. **Dữ liệu dùng chung**

   Nếu payment dùng chung schema hoặc join trực tiếp với order, user, invoice, việc tách sẽ kéo theo:

   - thay đổi schema;
   - backfill dữ liệu;
   - đồng bộ dữ liệu;
   - dual-write hoặc event;
   - kế hoạch rollback phức tạp.

4. **Tăng số điểm lỗi**

   Thay vì một tiến trình và một database, hệ thống có thêm:

   - network call;
   - timeout;
   - circuit breaker;
   - queue hoặc event broker;
   - service deployment;
   - service credentials;
   - dashboard và alert riêng.

5. **Khả năng quan sát chưa đủ**

   Nếu chưa có correlation ID, tracing, metrics và log tập trung, điều tra một giao dịch lỗi xuyên qua hai hệ thống sẽ khó hơn đáng kể.

6. **Migration bị ép theo deadline**

   Deadline cuối quý có thể dẫn đến:

   - bỏ qua load test;
   - rollback chưa được diễn tập;
   - chưa chạy reconciliation;
   - cutover một lần;
   - chấp nhận nợ kỹ thuật mới.

### Rủi ro nhân sự

Với 4 người, vẫn phải duy trì sản phẩm hiện tại. Migration có thể chiếm hầu hết năng lực của đội và tạo bus factor thấp: chỉ một hoặc hai người hiểu service mới.

### Rủi ro kinh doanh

- Thanh toán gián đoạn ảnh hưởng trực tiếp đến doanh thu và niềm tin khách hàng.
- Đối soát sai có thể không phát hiện ngay.
- Thành công kỹ thuật nhưng không cải thiện lead time nếu bottleneck thực sự nằm ở test suite hoặc quy trình phê duyệt chung.

---

## 4. Mũ vàng – Lợi ích nếu tách đúng cách

Việc tách vẫn có giá trị dài hạn nếu có nhu cầu thật:

- Payment có thể deploy độc lập với monolith.
- Giảm blast radius của các thay đổi không liên quan.
- Có thể scale payment theo tải riêng.
- Ranh giới bảo mật và quyền truy cập rõ hơn.
- Dễ cô lập tích hợp với nhiều payment provider.
- Có thể thiết kế retry, reconciliation và audit chuyên biệt.
- Nhóm khác có thể phát hành monolith mà không cần chờ thay đổi payment.
- Nếu payment có vòng đời phát triển riêng, service độc lập có thể tăng tốc độ delivery về lâu dài.

Tuy nhiên, các lợi ích này chỉ xuất hiện khi service có:

- quyền sở hữu dữ liệu rõ ràng;
- API contract ổn định;
- vận hành độc lập thật sự;
- CI/CD độc lập;
- monitoring và on-call phù hợp.

Nếu chỉ chuyển code sang repository hoặc process khác nhưng vẫn dùng chung database và deploy phụ thuộc monolith, đội sẽ nhận phần lớn chi phí mà chưa nhận được lợi ích.

---

## 5. Mũ xanh – Các phương án sáng tạo

### Phương án A: Tách toàn bộ ngay trong quý

Bao gồm service mới, database riêng, migration dữ liệu và cutover toàn bộ.

**Không khuyến nghị.** Quá nhiều thay đổi đồng thời so với quy mô đội và mức độ cấp bách.

### Phương án B: Modular monolith trước

- Tạo interface rõ ràng giữa payment và phần còn lại.
- Cấm truy cập trực tiếp vào bảng hoặc class nội bộ của payment.
- Gom logic payment vào một module có ownership rõ.
- Đưa side effect qua application service hoặc outbox.
- Viết contract test tại ranh giới.

Đây là bước có giá trị ngay cả khi sau này quyết định không dùng microservice.

### Phương án C: Tối ưu pipeline deploy

Phân tích 45 phút và xử lý nguyên nhân thực:

- cache dependency và build artifacts;
- chạy test song song;
- chỉ chạy test bị ảnh hưởng, nhưng vẫn giữ full suite theo lịch;
- tách migration khỏi startup;
- giảm bước thủ công;
- sử dụng rolling/canary deployment;
- tạo immutable artifact và promote cùng artifact giữa các môi trường.

Nếu có thể giảm đáng kể thời gian deploy với chi phí thấp, động lực tách microservice sẽ yếu đi.

### Phương án D: Tách theo “strangler pattern”

Tạo payment service nhưng ban đầu chỉ xử lý một phần ít rủi ro, chẳng hạn:

- truy vấn trạng thái thanh toán;
- tiếp nhận và lưu webhook;
- reconciliation;
- adapter tới một provider mới;
- một loại thanh toán nội bộ hoặc nhóm traffic nhỏ.

Monolith vẫn là đường xử lý chính, cho phép rollback nhanh.

### Phương án E: Shadow mode

Monolith vẫn quyết định kết quả. Service mới nhận bản sao request/event và xử lý song song nhưng không gây side effect tài chính. So sánh kết quả giữa hai hệ thống để phát hiện khác biệt.

Lưu ý: không được gửi lệnh charge thật lần thứ hai trong shadow mode.

### Phương án F: Branch by abstraction

Đặt một interface payment trong monolith:

- implementation hiện tại gọi code cũ;
- implementation mới gọi service qua API;
- feature flag chọn implementation;
- rollback bằng cách chuyển flag thay vì redeploy lớn.

Đây là phương án phù hợp nhất nếu sau giai đoạn chuẩn bị đội quyết định cutover dần.

---

## 6. Mũ xanh dương – Tổng hợp và quyết định

### Quyết định

**Không phê duyệt việc tách hoàn chỉnh và chuyển toàn bộ payment sang microservice trong quý này.**

**Phê duyệt một chương trình “extraction readiness” có giới hạn**, gồm:

1. đo và tối ưu pipeline deploy;
2. biến payment thành module có ranh giới rõ trong monolith;
3. xây dựng các năng lực an toàn bắt buộc;
4. thực hiện proof of concept hoặc shadow deployment nếu còn đủ năng lực;
5. ra quyết định cutover ở cổng kiểm soát cuối quý.

Đây không phải là trì hoãn vô thời hạn. Đây là cách biến quyết định kiến trúc thành quyết định dựa trên bằng chứng.

---

# Kế hoạch hành động trong quý

## Giai đoạn 1: Baseline và quyết định phạm vi

### Công việc

- Phân rã 45 phút deploy theo từng bước.
- Thu thập baseline:
  - deploy duration;
  - deploy frequency;
  - change failure rate;
  - rollback time;
  - payment error rate;
  - số sự cố và thời gian khôi phục;
  - tỷ lệ giao dịch phải đối soát thủ công.
- Vẽ luồng payment từ request đến provider, webhook, order update và reconciliation.
- Liệt kê database table và transaction mà payment đang dùng.
- Xác định API và event contract dự kiến.
- Lập risk register và runbook rollback.

### Đầu ra

- Sơ đồ phụ thuộc.
- Danh sách transaction xuyên ranh giới.
- Baseline đo được.
- Phạm vi extraction nhỏ nhất.
- Tiêu chí go/no-go được cả đội và stakeholder chấp thuận.

---

## Giai đoạn 2: Giảm pain point trước khi đổi kiến trúc

### Công việc

- Tối ưu các bước tốn thời gian nhất trong CI/CD.
- Tách build artifact khỏi deployment.
- Song song hóa test phù hợp.
- Loại bỏ bước thủ công không cần thiết.
- Kiểm tra khả năng deploy/rollback an toàn hơn.
- Đo lại thời gian deploy sau mỗi thay đổi.

### Quy tắc quyết định

Nếu pipeline có thể được cải thiện đủ để đáp ứng nhu cầu phát hành, không cần vội tách service chỉ để giải quyết thời gian deploy.

---

## Giai đoạn 3: Làm sạch ranh giới payment trong monolith

### Công việc

- Tạo payment interface/API nội bộ.
- Chuyển tất cả caller sang interface đó.
- Ngăn module khác truy cập trực tiếp dữ liệu nội bộ của payment.
- Định nghĩa payment state machine rõ ràng.
- Bổ sung:
  - idempotency key;
  - timeout;
  - retry có giới hạn;
  - xử lý webhook trùng;
  - audit trail;
  - reconciliation job;
  - correlation ID.
- Viết contract test và integration test cho các luồng:
  - thanh toán thành công;
  - thất bại;
  - timeout không rõ kết quả;
  - webhook trùng;
  - webhook đến sai thứ tự;
  - refund;
  - rollback hoặc provider outage.

### Giá trị

Ngay cả khi không tách service, monolith trở nên an toàn và dễ bảo trì hơn.

---

## Giai đoạn 4: Pilot hoặc shadow service

Chỉ bắt đầu khi giai đoạn trước đạt yêu cầu.

### Phạm vi pilot nên nhỏ

Ưu tiên chức năng read-only hoặc không trực tiếp tạo charge. Nếu phải thử luồng write, chỉ dùng một nhóm traffic nhỏ và có feature flag.

### Yêu cầu bắt buộc

- Deploy độc lập.
- Health check và readiness check.
- Metrics, logs và alert.
- Secret management.
- API versioning.
- Idempotency.
- Reconciliation.
- Feature flag.
- Kill switch.
- Fallback về implementation cũ.
- Dashboard so sánh monolith với service mới.
- Không dual-write mù quáng vào hai database nếu chưa có chiến lược nhất quán rõ ràng.

---

## Giai đoạn 5: Đánh giá cuối quý

Có ba kết quả hợp lệ:

1. **Dừng extraction**

   Pipeline đã được cải thiện đủ; lợi ích của service không bù chi phí.

2. **Tiếp tục pilot ở quý sau**

   Ranh giới đã rõ nhưng chưa đủ bằng chứng an toàn để cutover.

3. **Cho phép cutover tăng dần**

   Chỉ khi đạt toàn bộ tiêu chí go/no-go.

Không xem việc “chưa cutover” là thất bại. Mục tiêu quý này là giảm rủi ro và tạo bằng chứng, không phải ép kiến trúc mới vào production.

---

# Phân công cho đội 4 người

Có thể chia ownership như sau, nhưng vẫn review chéo để tránh silo:

- **Người 1 – Payment domain:** state machine, idempotency, provider behavior, reconciliation.
- **Người 2 – Data và migration:** data ownership, outbox/event, backfill, consistency.
- **Người 3 – Platform:** CI/CD, deployment, logging, metrics, alerting, feature flag.
- **Người 4 – Quality và integration:** contract test, failure test, shadow comparison, runbook.

Cả bốn người vẫn cùng chịu trách nhiệm về thiết kế và diễn tập rollback; không để microservice mới trở thành kiến thức của một cá nhân.

---

# Tiêu chí Go/No-Go

## Chỉ cho phép chuyển traffic thật nếu

- Payment service có data ownership rõ ràng.
- Không còn transaction đồng bộ xuyên service mà chưa có chiến lược xử lý.
- Mọi lệnh tạo giao dịch đều idempotent.
- Có xử lý webhook trùng và sai thứ tự.
- Có reconciliation tự động.
- Có metrics, log, alert và correlation ID.
- Contract test và failure test đều đạt.
- Đã kiểm thử provider timeout, network failure và service restart.
- Có feature flag và kill switch.
- Rollback được diễn tập, không chỉ viết trên tài liệu.
- Shadow/pilot không xuất hiện sai lệch chưa giải thích được.
- On-call có thể chẩn đoán một giao dịch từ đầu đến cuối.
- Service có thể deploy độc lập mà không yêu cầu deploy monolith cùng lúc.

## No-Go nếu còn một trong các tình trạng sau

- Vẫn dùng chung database theo cách hai bên cùng ghi vào cùng bảng.
- Chưa giải quyết duplicate charge.
- Không thể đối soát kết quả với provider.
- Không có rollback nhanh.
- Cutover yêu cầu “big bang”.
- Phải hy sinh test hoặc observability để kịp deadline.
- Service mới không làm giảm coupling hoặc thời gian phát hành.
- Đội phải làm thêm giờ kéo dài để hoàn thành.

---

# Chỉ số thành công

Không đo thành công bằng việc “đã có microservice”. Nên đo bằng:

- thời gian deploy giảm;
- payment và phần còn lại có thể phát hành độc lập;
- tỷ lệ deploy lỗi không tăng;
- thời gian rollback hoặc khôi phục được cải thiện;
- không tăng duplicate charge hoặc giao dịch cần xử lý thủ công;
- thời gian điều tra một payment lỗi giảm;
- số dependency trực tiếp giữa payment và các module khác giảm;
- không phát sinh sự cố nghiêm trọng do migration.

---

# Quyết định cuối cùng

**No-Go cho full extraction trong quý này.**

**Go cho modularization, tối ưu CI/CD và pilot có kiểm soát.** Cuối quý, dùng số liệu và các tiêu chí trên để quyết định có chuyển traffic dần trong quý tiếp theo hay không.

Nếu buộc phải có một kết quả production trong quý, chỉ nên chọn **một lát cắt ít rủi ro, có feature flag và rollback tức thời**; không chuyển toàn bộ luồng charge, webhook, refund và reconciliation cùng một lúc.
