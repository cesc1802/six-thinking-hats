# Mũ xanh lam — Mở phiên quyết định

**Chế độ:** Full — Go/No-Go review  
**Quyết định:** Có nên phát hành beta vào thứ Sáu hay không?

**Các phương án:**

- **Option 0 — No-Go:** Hoãn phát hành, tiếp tục sửa lỗi và kiểm thử.
- **Option 1 — Full Go:** Phát hành beta theo kế hoạch cho toàn bộ nhóm beta.
- **Option 2 — Controlled Go:** Phát hành giới hạn theo cohort/feature flag, giám sát chặt và sẵn sàng rollback.

**Ràng buộc đã biết:**

- Có 12 lỗi được phân loại low severity.
- Không có lỗi gây mất dữ liệu đã biết.
- Có đội support cuối tuần.
- Rollback mất khoảng 15 phút.
- Ngày phát hành dự kiến là thứ Sáu.

**Tiêu chí thành công:**

1. Không xuất hiện lỗi mất dữ liệu, bảo mật hoặc quyền truy cập nghiêm trọng.
2. Các luồng nghiệp vụ chính vẫn hoạt động.
3. Monitoring phát hiện được lỗi trước khi support bị quá tải.
4. Đội trực có quyền và khả năng rollback trong thời gian cam kết.
5. Beta tạo ra dữ liệu phản hồi có ích mà không gây tổn hại đáng kể cho người dùng.
6. Đến cuối tuần, trạng thái hệ thống phải là: ổn định, rollback thành công, hoặc có kế hoạch khắc phục rõ ràng.

**Giả định:**

- `[ASSUMPTION]` “Low severity” đã được đánh giá dựa trên ảnh hưởng người dùng, tần suất và khả năng workaround.
- `[ASSUMPTION]` Beta chỉ phục vụ một nhóm người dùng giới hạn, không phải general availability.
- `[ASSUMPTION]` Rollback 15 phút bao gồm cả thao tác vận hành và thời gian phiên bản cũ hoạt động trở lại.
- `[ASSUMPTION]` Thay đổi không chứa migration dữ liệu không tương thích ngược.

**Trình tự:** Mũ xanh lam → Mũ trắng → Mũ đỏ → Mũ vàng → Mũ đen → Mũ xanh lá → Mũ đỏ lần hai → Mũ xanh lam.

---

# Mũ trắng — Sự kiện và dữ liệu

## 1. Thông tin đã biết

| Thông tin | Phân loại | Nguồn |
|---|---|---|
| Có 12 lỗi đã biết | `[FACT: user-provided]` | Nội dung yêu cầu |
| Các lỗi được phân loại low severity | `[FACT: user-provided]` | Nội dung yêu cầu |
| Không có lỗi mất dữ liệu đã biết | `[FACT: user-provided]` | Nội dung yêu cầu |
| Có support coverage cuối tuần | `[FACT: user-provided]` | Nội dung yêu cầu |
| Rollback mất 15 phút | `[FACT: user-provided]` | Nội dung yêu cầu |
| Kế hoạch là phát hành beta vào thứ Sáu | `[FACT: user-provided]` | Nội dung yêu cầu |

## 2. Điều các dữ kiện chưa chứng minh

- `[FACT: user-provided]` Không có **lỗi mất dữ liệu đã biết** không đồng nghĩa với việc đã chứng minh không thể mất dữ liệu.
- `[FACT: user-provided]` Có support cuối tuần không tự động có nghĩa đội ngũ có đủ kỹ năng, quyền truy cập và người ra quyết định để xử lý sự cố.
- `[FACT: user-provided]` Rollback 15 phút không cho biết rollback đã được diễn tập trên release candidate hiện tại hay chưa.
- `[FACT: user-provided]` Có 12 lỗi low-severity không cho biết các lỗi có tập trung vào cùng một luồng người dùng hay có tác động cộng dồn hay không.

## 3. Thông tin còn thiếu

| NEED-DATA | Cách lấy dữ liệu | Có chặn quyết định không? |
|---|---|---|
| Kết quả regression test của release candidate | QA chạy và ký xác nhận test suite | Có |
| Chi tiết 12 lỗi: luồng bị ảnh hưởng, tần suất, workaround | Review bug tracker với QA/Product | Có |
| Có lỗi security, privacy, authentication hoặc authorization không | Security checklist và review thay đổi | Có |
| Rollback đã được thử với đúng artifact/configuration chưa | Diễn tập rollback trong staging/canary | Có |
| Database migration có backward-compatible không | Engineering/DBA review migration | Có |
| Monitoring có bao phủ các critical user journeys không | Review dashboard, logs và alert test | Có |
| Quy mô và danh sách beta cohort | Product xác nhận rollout scope | Có đối với Controlled Go |
| Ai có quyền ra lệnh rollback cuối tuần | Incident RACI/on-call schedule | Có |
| Mức tải dự kiến và baseline lỗi hiện tại | Production metrics hoặc dữ liệu beta trước đây | Nên có |
| Người dùng beta đã được thông báo đây là bản thử nghiệm chưa | Product/Support kiểm tra communication | Nên có |

## 4. Ý kiến đang có thể bị trình bày như sự thật

- “12 lỗi low severity là chấp nhận được” là **đánh giá**, không phải dữ kiện.
- “Rollback 15 phút nên rủi ro thấp” là **suy luận**, vì rollback có thể không sửa được dữ liệu hoặc tác động bên ngoài.
- “Có support cuối tuần nên launch an toàn” là **ý kiến**, cho đến khi xác nhận quyền hạn, năng lực và escalation path.
- “Không có data-loss bug nên release-ready” là **ý kiến**, vì còn security, availability và critical-flow risks.

---

# Mũ đỏ — Cảm nhận ban đầu

Trực giác theo mẫu tình huống nghiêng về **Go có kiểm soát**, không phải Full Go. Mức độ lo ngại vừa phải vì phát hành vào thứ Sáu làm thời gian phản ứng và phối hợp khó hơn.

---

# Mũ vàng — Giá trị và mặt tích cực

| Trọng tâm | Ngắn hạn | Trung hạn | Dài hạn |
|---|---|---|---|
| **Lợi ích** | Thu nhận phản hồi thực tế sớm; giữ đúng lịch; kiểm chứng release process | Phát hiện vấn đề sử dụng thực tế trước GA; cải thiện backlog bằng dữ liệu beta | Xây dựng khả năng release thường xuyên và giảm tâm lý sợ phát hành |
| **Giá trị** | Support cuối tuần và rollback nhanh tạo một cửa sổ vận hành có bảo vệ | Dữ liệu beta giúp ưu tiên đúng lỗi thay vì sửa mọi lỗi theo phỏng đoán | Đội ngũ tích lũy năng lực rollout, monitoring và incident response |
| **Tính khả thi** | Không có data-loss bug đã biết; lỗi hiện tại được xếp low severity | Nếu cohort giới hạn, đội có thể quan sát và sửa theo từng vòng | Quy trình controlled rollout có thể tái sử dụng cho các release sau |

Các điểm sáng cụ thể:

- **Ngắn hạn:** Beta cho phép kiểm chứng sản phẩm với người dùng thật mà chưa cam kết mức ổn định của GA.
- **Trung hạn:** 12 lỗi đã biết có thể được theo dõi có chủ đích; feedback giúp xác định lỗi nào thực sự ảnh hưởng trải nghiệm.
- **Dài hạn:** Nếu rollback, monitoring và on-call hoạt động tốt, release này trở thành bài kiểm tra hữu ích cho năng lực vận hành.

---

# Mũ đen — Rủi ro

| Rủi ro | Cơ chế và bằng chứng | Khả năng | Tác động | Điều làm rủi ro xấu hơn |
|---|---|---:|---:|---|
| Phân loại sai một trong 12 lỗi | Chỉ biết nhãn “low severity”, chưa có bằng chứng về phạm vi hoặc tần suất | Trung bình | Trung bình–cao | Nhiều lỗi cùng ảnh hưởng một critical journey |
| Tác động cộng dồn của 12 lỗi | Từng lỗi nhỏ nhưng kết hợp có thể khiến sản phẩm khó sử dụng | Trung bình | Trung bình | Cohort tập trung vào đúng khu vực có nhiều lỗi |
| Lỗi chưa biết trong production | Không có data-loss bug đã biết chỉ bao phủ lỗi đã phát hiện | Trung bình | Cao | Test coverage thấp, thay đổi dữ liệu lớn hoặc thiếu observability |
| Rollback không thực sự hoàn tất trong 15 phút | Thời gian 15 phút có thể chỉ là deploy, không bao gồm kiểm tra phục hồi | Thấp–trung bình | Cao | Migration không tương thích ngược, cache/schema thay đổi |
| Support có mặt nhưng không xử lý được | Support có thể thiếu quyền deploy/rollback hoặc thiếu escalation contact | Trung bình | Trung bình–cao | Engineer chủ chốt không trực cuối tuần |
| Monitoring không phát hiện lỗi | Nếu không có alert cho critical journeys, đội chỉ biết qua ticket người dùng | Trung bình | Cao | Beta cohort nhỏ khiến lỗi khó thấy trong aggregate metrics |
| Cuối tuần làm chậm phối hợp | Các bên Product, Engineering, Security hoặc vendor có thể không sẵn sàng | Trung bình | Trung bình | Incident cần nhiều đội hoặc approval đặc biệt |
| Beta gây mất niềm tin | Người dùng beta vẫn có thể đánh giá tiêu cực nếu luồng chính hỏng | Thấp–trung bình | Trung bình | Không thông báo rõ kỳ vọng beta hoặc không có workaround |
| Rollback làm mất dữ liệu phát sinh sau launch | Phiên bản cũ có thể không đọc được dữ liệu do phiên bản mới tạo | Chưa biết | Cao | Có schema/data-format migration không tương thích |
| Support overload | Nhiều lỗi nhỏ có thể tạo nhiều ticket đồng thời | Chưa biết | Trung bình | Cohort quá lớn hoặc support không có runbook |

## Rủi ro của Option 0 — Hoãn phát hành

| Rủi ro | Cơ chế | Khả năng | Tác động |
|---|---|---:|---:|
| Mất cơ hội học hỏi | Tiếp tục sửa dựa trên giả định thay vì hành vi người dùng thật | Cao | Trung bình |
| Tạo tiền lệ “không được release khi còn bug” | Đội có thể trì hoãn vô hạn dù lỗi không phải blocker | Trung bình | Trung bình |
| Chi phí cơ hội | Feedback, validation và tiến độ roadmap bị lùi | Cao | Trung bình |
| Release sau lớn hơn | Tích lũy thêm thay đổi làm tăng blast radius của lần phát hành kế tiếp | Trung bình | Trung bình–cao |

---

# Mũ xanh lá — Các phương án và cải tiến

Không đánh giá hoặc xếp hạng trong phần này.

1. **Canary beta:** Mở cho một cohort rất nhỏ trước, sau một khoảng quan sát mới mở rộng.
2. **Feature flag:** Tách các phần rủi ro thành flag riêng để tắt mà không rollback toàn bộ.
3. **Launch theo critical journey:** Chỉ bật những luồng đã qua kiểm thử; giữ các luồng có bug phía sau flag.
4. **Read-only beta:** Nếu có nghi ngờ về write path hoặc migration, cho phép trải nghiệm các chức năng đọc trước.
5. **Friday internal beta, Monday external beta:** Dùng cuối tuần cho nhân viên/dogfooding, rồi mở người dùng bên ngoài khi đầy đủ đội ngũ.
6. **Shadow traffic hoặc replay:** Chạy release mới với traffic sao chép nhưng không trả kết quả cho người dùng.
7. **Pre-launch rollback drill:** Triển khai release candidate rồi rollback ngay trên staging/canary, đo end-to-end recovery time.
8. **Bug-budget gate:** Chấp nhận 12 lỗi nếu từng lỗi có owner, workaround và không tác động critical path.
9. **Dedicated launch room:** Engineering, Product, QA và Support dùng một kênh chung với một Incident Commander.
10. **Progressive expansion:** Mở rộng cohort theo nhiều bước, mỗi bước chỉ diễn ra sau khi đạt exit criteria.
11. **Unconventional option:** Tổ chức “beta game day” có chủ đích, mời người dùng thử phá các critical journeys và thưởng cho báo cáo tái hiện được.
12. **Loại bỏ ràng buộc thứ Sáu:** Nếu ngày phát hành không mang giá trị kinh doanh thực sự, chuyển launch sang đầu tuần nhưng vẫn hoàn tất release readiness vào thứ Sáu.

---

# Mũ đỏ — Kiểm tra lần hai

Sau phân tích, trực giác vẫn là **Go có kiểm soát**, nhưng chỉ khi rollback được diễn tập và các câu hỏi về migration, security, critical journeys và quyền xử lý cuối tuần đã được đóng.

---

# Mũ xanh lam — Quyết định và hành động

## Khuyến nghị

**Conditional GO — phát hành beta vào thứ Sáu dưới hình thức controlled rollout.**

Không nên chọn Full Go ngay từ đầu. Quyết định cuối cùng tại go/no-go gate là:

- **GO** nếu tất cả điều kiện bắt buộc bên dưới đạt.
- **NO-GO** nếu bất kỳ điều kiện bắt buộc nào không đạt hoặc chưa xác minh.
- Sau khi GO, mở cohort nhỏ trước và chỉ mở rộng nếu hệ thống ổn định.

## Điều kiện bắt buộc trước launch

1. **12 lỗi đã được triage lại**
   - Không lỗi nào liên quan đến data integrity, security, privacy, authentication hoặc authorization.
   - Không lỗi nào chặn critical user journey.
   - Mỗi lỗi có owner, workaround hoặc quyết định chấp nhận rõ ràng.

2. **Release candidate vượt qua kiểm thử**
   - Smoke test và regression cho các critical journeys đều pass.
   - Không dùng một artifact khác với artifact sẽ deploy.

3. **Rollback đã được diễn tập**
   - Dùng đúng release artifact, cấu hình và migration path.
   - Xác minh phiên bản cũ hoạt động lại, không chỉ xác minh deployment command hoàn tất.
   - Không có migration/data-format không tương thích ngược.

4. **Observability sẵn sàng**
   - Có dashboard cho error rate, latency, availability và các critical journeys.
   - Alert được test.
   - Logs đủ thông tin để phân biệt lỗi đã biết và lỗi mới.

5. **Weekend coverage đã được xác nhận**
   - Có Incident Commander.
   - Có kỹ sư có quyền deploy/rollback.
   - Product, QA và Support có escalation path rõ ràng.
   - Các thành viên xác nhận nhận ca, không chỉ xuất hiện trên lịch.

6. **Scope beta được giới hạn**
   - Cohort ban đầu nhỏ và xác định trước.
   - Có feature flag hoặc cơ chế dừng mở rộng.
   - Người dùng được thông báo rõ đây là beta.

7. **Ngưỡng rollback được thống nhất trước launch**
   - Các threshold phải dựa trên baseline của sản phẩm và được Product/Engineering ký xác nhận.
   - Không đợi đến khi xảy ra incident mới tranh luận mức độ nghiêm trọng.

## Điều kiện khiến khuyến nghị chuyển thành No-Go

- Phát hiện bất kỳ nguy cơ data loss, security, privacy hoặc unauthorized access nào.
- Migration không backward-compatible hoặc rollback chưa được thử.
- Có lỗi chặn luồng chính dù workaround tồn tại.
- Không có kỹ sư đủ quyền và năng lực trực cuối tuần.
- Không quan sát được health của critical journeys.
- Không thể giới hạn cohort hoặc dừng rollout.
- Rollback thực tế vượt quá giới hạn được đội ngũ chấp nhận.
- Các bên chưa thống nhất ai có quyền ra quyết định rollback.

## Kế hoạch hành động

| Giai đoạn | Việc thực hiện | Owner | Thời điểm | Exit criterion |
|---|---|---|---|---|
| 1. Bug gate | Review cả 12 lỗi, kiểm tra severity, critical path, workaround và owner | QA Lead + Product + Engineering Lead | Trước go/no-go meeting | 12/12 lỗi có disposition; không có blocker |
| 2. Security/data gate | Review auth, permissions, privacy, writes và migration | Engineering Lead/Security/DB owner | Trước launch | Không có security/data-integrity blocker; migration rollback-safe |
| 3. Release verification | Chạy smoke và regression trên release candidate chính xác | QA Lead | Trước launch | Tất cả test bắt buộc pass; kết quả được lưu |
| 4. Rollback drill | Deploy và rollback trên staging/canary; đo thời gian phục hồi end-to-end | Release Engineer | Trước launch | Phiên bản cũ hoạt động bình thường; dữ liệu vẫn hợp lệ |
| 5. Monitoring gate | Kiểm tra dashboard, logs, alerts và critical journey probes | SRE/Engineering | Trước launch | Alert test thành công; dashboard truy cập được |
| 6. Incident readiness | Chốt RACI, kênh liên lạc, on-call và quyền rollback | Incident Commander | Trước launch | Từng vai trò xác nhận; escalation path được thử |
| 7. Go/No-Go review | Kiểm tra bằng chứng từ sáu gate trên | Release Owner | Ngay trước deploy | Tất cả gate đạt; quyết định được ghi lại |
| 8. Canary launch | Bật beta cho cohort nhỏ nhất có ý nghĩa | Release Engineer | Thứ Sáu | Deploy thành công; smoke test production pass |
| 9. Observation window | Theo dõi metrics, support tickets và critical journeys | Incident Commander + Support | Ngay sau canary | Không chạm rollback threshold; không có blocker mới |
| 10. Controlled expansion | Mở rộng từng cohort qua feature flag | Product + Release Owner | Sau mỗi cửa sổ quan sát đạt yêu cầu | Mỗi cohort đạt cùng health criteria |
| 11. Weekend operations | Theo dõi, xử lý ticket, cập nhật incident log | On-call team | Cuối tuần | Không có incident mở vượt ngưỡng; trạng thái rõ ràng |
| 12. Review | Tổng hợp lỗi, phản hồi, metrics và quyết định bước tiếp theo | Product + Engineering + Support | Đầu tuần kế tiếp | Có danh sách fix, owner, priority và quyết định tiếp tục/dừng beta |

## Quyền quyết định trong lúc launch

- **Incident Commander:** Có quyền dừng rollout và yêu cầu rollback.
- **On-call Engineer:** Có quyền thực hiện rollback ngay khi đạt trigger đã thống nhất.
- **Product Owner:** Quyết định cohort và việc mở rộng, nhưng không được phủ quyết rollback vì lý do an toàn.
- **Support Lead:** Tổng hợp mức độ và tần suất phản hồi người dùng.
- **QA Lead:** Xác minh lỗi mới và quyết định liệu critical journey có bị chặn hay không.

## Trigger rollback

Rollback ngay khi xảy ra một trong các trường hợp:

- Có bằng chứng mất hoặc sai lệch dữ liệu.
- Có lỗ hổng security/privacy hoặc truy cập trái phép.
- Critical user journey không hoạt động và không có workaround an toàn.
- Error/latency/availability vượt ngưỡng đã thống nhất.
- Support volume vượt khả năng xử lý đã định trước.
- Monitoring không còn đáng tin cậy, khiến đội không thể đánh giá tình trạng hệ thống.
- Không thể giới hạn blast radius hoặc tắt tính năng lỗi.
- Incident Commander đánh giá việc tiếp tục làm tăng đáng kể thiệt hại.

## Kết luận

**Go — nhưng chỉ với controlled beta, cohort nhỏ, progressive rollout và các gate bắt buộc.**

Các dữ kiện hiện tại khá thuận lợi: lỗi đã biết đều low severity, chưa có lỗi mất dữ liệu, có support cuối tuần và rollback tương đối nhanh. Tuy nhiên, chúng chưa đủ để biện minh cho Full Go. Điểm quyết định không phải là con số “12 lỗi”, mà là bằng chứng rằng:

- severity được phân loại đúng,
- critical journeys đã pass,
- migration có thể đảo ngược,
- rollback 15 phút đã được xác minh,
- và đội trực cuối tuần thực sự có quyền hành động.

Nếu không đóng được các mục đó trước thời điểm go/no-go, quyết định mặc định phải là **No-Go và chuyển launch sang cửa sổ tiếp theo**.
