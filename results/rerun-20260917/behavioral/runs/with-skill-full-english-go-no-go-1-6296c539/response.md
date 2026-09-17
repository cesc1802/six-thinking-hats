# Mũ xanh lam — Xác định quyết định

**Chế độ:** `full`  
**Loại quyết định:** Go/no-go cho phát hành beta.

**Vấn đề:** Có nên phát hành bản beta vào thứ Sáu với 12 lỗi mức độ thấp đã biết, không có lỗi gây mất dữ liệu, có đội hỗ trợ cuối tuần và thời gian rollback 15 phút hay không?

**Các phương án:**

- **Option 0: do nothing / status quo** — hoãn phát hành để tiếp tục sửa lỗi và kiểm thử.
- **Go** — phát hành beta đầy đủ vào thứ Sáu.
- **Conditional Go** — phát hành có giới hạn, kèm cổng kiểm tra, giám sát và quyền rollback rõ ràng.

**Ràng buộc:**

- Mốc phát hành dự kiến: thứ Sáu.
- Phải duy trì hỗ trợ trong cuối tuần.
- Không chấp nhận lỗi mất dữ liệu hoặc lỗi nghiêm trọng chưa được kiểm soát.
- Rollback phải thực sự khả dụng trong điều kiện production, không chỉ đúng trên lý thuyết.

**Tiêu chí thành công:**

1. Không phát sinh lỗi mất dữ liệu, bảo mật nghiêm trọng hoặc gián đoạn diện rộng.
2. Các luồng chính của beta hoạt động sau khi triển khai.
3. Tỷ lệ lỗi và khối lượng yêu cầu hỗ trợ nằm trong ngưỡng đã thống nhất.
4. Sự cố có thể được phát hiện sớm, phân loại và rollback trong thời gian chấp nhận được.
5. Thu được phản hồi beta có giá trị mà không gây thiệt hại lớn về trải nghiệm hoặc uy tín.

**Trình tự:** Mũ xanh lam → Mũ trắng → Mũ vàng → Mũ đen → Mũ đỏ → Mũ xanh lam. Đây là trình tự dành cho quyết định go/no-go: xác lập quyết định, kiểm tra dữ kiện, đánh giá giá trị, xem xét rủi ro, kiểm tra trực giác rồi ra quyết định.

---

# Mũ trắng — Dữ kiện khách quan

## Thông tin đã biết

| Thông tin | Phân loại | Nguồn |
|---|---|---|
| Có 12 lỗi đã biết | `[FACT: user-provided launch brief]` | Thông tin do người yêu cầu cung cấp |
| 12 lỗi được phân loại là mức độ thấp | `[FACT: user-provided launch brief]` | Chưa có danh sách lỗi hoặc tiêu chí severity để xác minh độc lập |
| Không có lỗi gây mất dữ liệu đã biết | `[FACT: user-provided launch brief]` | Không đồng nghĩa với việc đã chứng minh không thể có lỗi mất dữ liệu |
| Có nhân sự hỗ trợ trong cuối tuần | `[FACT: user-provided launch brief]` | Chưa rõ số người, kỹ năng, ca trực và quyền xử lý |
| Rollback mất khoảng 15 phút | `[FACT: user-provided launch brief]` | Chưa rõ đây là kết quả diễn tập gần nhất hay ước lượng |
| Đây là bản beta, không phải phát hành ổn định rộng rãi | `[FACT: user request]` | Phạm vi người dùng beta chưa được cung cấp |
| Mục tiêu đang được xem xét là phát hành vào thứ Sáu | `[FACT: user request]` | Chưa có giờ phát hành và múi giờ |

## Thông tin chưa biết

- `[NEED-DATA: Release manager rà soát danh sách 12 bug trước cuộc họp go/no-go]` Xác nhận từng lỗi không ảnh hưởng luồng chính, bảo mật, quyền truy cập, thanh toán, dữ liệu hoặc khả năng rollback.
- `[NEED-DATA: QA chạy regression suite và smoke test trên release candidate cuối cùng]` Xác nhận trạng thái pass/fail của các luồng beta quan trọng.
- `[NEED-DATA: SRE thực hiện hoặc cung cấp log của lần rollback rehearsal gần nhất]` Xác minh mốc 15 phút bao gồm phát hiện, quyết định, thực thi và kiểm tra phục hồi hay chỉ thời gian chạy kỹ thuật.
- `[NEED-DATA: Product owner xác định cohort và số lượng người dùng beta]` Đo blast radius thực tế.
- `[NEED-DATA: Support lead công bố lịch trực, kênh escalation và thời gian phản hồi]` Xác nhận “support coverage” đủ năng lực xử lý sự cố.
- `[NEED-DATA: Engineering lead kiểm tra migration và backward compatibility]` Xác nhận rollback ứng dụng không để lại schema hoặc dữ liệu không tương thích.
- `[NEED-DATA: Product và SRE thống nhất dashboard cùng ngưỡng rollback trước khi deploy]` Xác định các chỉ số như error rate, latency, crash rate, ticket volume và lỗi luồng chính.
- `[NEED-DATA: Security owner kiểm tra kết quả security scan và các finding đang mở]` Loại trừ lỗ hổng nghiêm trọng chưa được tính trong 12 lỗi.
- `[NEED-DATA: Incident commander kiểm tra danh sách liên hệ và diễn tập quy trình escalation trước launch]` Xác nhận đội cuối tuần có quyền truy cập và quyền quyết định rollback.

## Nhận định đang được trình bày như dữ kiện

- “Low severity” là kết quả phân loại, không tự chứng minh lỗi vô hại. Severity có thể bị đánh giá thấp nếu thiếu dữ liệu sử dụng thực tế.
- “Không có data-loss bug” chỉ mô tả lỗi đã biết; đây không phải bằng chứng rằng release không thể gây mất dữ liệu.
- “Rollback 15 phút” chưa cho biết tổng thời gian phục hồi. Thời gian phát hiện và ra quyết định có thể dài hơn thời gian thao tác rollback.
- “Có support cuối tuần” chưa chứng minh có đủ kỹ sư, quyền production, khả năng chẩn đoán và quyền rollback.

---

# Mũ vàng — Giá trị của việc phát hành

| Trọng tâm | Ngắn hạn | Trung hạn | Dài hạn |
|---|---|---|---|
| **Lợi ích** | Đưa sản phẩm đến người dùng beta đúng kế hoạch và bắt đầu thu phản hồi thực tế. | Phát hiện vấn đề về hành vi người dùng, khả năng vận hành và tải mà môi trường nội bộ khó tái tạo. | Xây dựng nhịp phát hành nhỏ, có kiểm soát thay vì tích lũy thay đổi thành một đợt lớn. |
| **Giá trị** | Tận dụng đội hỗ trợ cuối tuần và khả năng rollback tương đối nhanh. | Chuyển các giả định sản phẩm thành dữ liệu sử dụng thực tế để ưu tiên roadmap và bug backlog. | Tăng năng lực release, observability và incident response của đội ngũ. |
| **Tính khả thi** | Có vẻ khả thi nếu 12 lỗi thực sự có severity thấp, smoke test đạt và rollback đã được xác minh. | Một cohort beta giới hạn giúp thu giá trị trong khi giữ blast radius nhỏ. | Quy trình canary, feature flag và cổng go/no-go có thể tái sử dụng cho các lần phát hành sau. |

Điểm sáng quan trọng nhất là đây là **beta có khả năng hỗ trợ cuối tuần và rollback nhanh**, nên có thể biến việc phát hành thành một thử nghiệm được kiểm soát thay vì một lần triển khai không thể đảo ngược.

---

# Mũ đen — Rủi ro và giới hạn

| Rủi ro | Cơ chế và bằng chứng | Khả năng | Tác động | Điều làm rủi ro tăng |
|---|---|---:|---:|---|
| Một trong 12 lỗi bị đánh giá severity thấp hơn thực tế | Phân loại severity chưa được đối chiếu với danh sách lỗi và luồng người dùng; lỗi “nhỏ” có thể kết hợp thành lỗi lớn | Trung bình | Trung bình–cao | Lỗi nằm trong authentication, authorization, billing, migration hoặc luồng chính |
| Có lỗi mất dữ liệu chưa được phát hiện | “Không có data-loss bug” chỉ bao phủ lỗi đã biết; beta vẫn có thể kích hoạt đường chạy chưa được kiểm thử | Thấp–trung bình | Rất cao | Migration không tương thích ngược, ghi dữ liệu mới hoặc thiếu backup/restore verification |
| Rollback 15 phút không phục hồi hoàn toàn | Rollback code không nhất thiết rollback schema, queue, cache hoặc dữ liệu đã ghi | Trung bình nếu chưa diễn tập | Cao | Deployment có migration phá vỡ tương thích hoặc side effect không thể đảo ngược |
| Phát hành thứ Sáu kéo sự cố sang cuối tuần | Nhân sự có mặt không đồng nghĩa với đầy đủ chuyên môn và quyền xử lý | Trung bình | Trung bình–cao | Người sở hữu hệ thống vắng mặt, escalation không rõ, alert không hoạt động |
| Monitoring phát hiện sự cố quá muộn | Rollback nhanh không hữu ích nếu mất nhiều giờ mới phát hiện bất thường | Trung bình nếu chưa có ngưỡng | Cao | Không có dashboard, alert hoặc baseline trước launch |
| Trải nghiệm beta kém do 12 lỗi cộng dồn | Từng lỗi có thể nhẹ nhưng tổng hợp làm sản phẩm thiếu ổn định và tăng ticket support | Trung bình | Trung bình | Các lỗi tập trung vào cùng một hành trình người dùng |
| Blast radius không được kiểm soát | “Beta” có thể vẫn bao gồm số lượng lớn người dùng hoặc khách hàng quan trọng | Chưa xác định | Cao | Tự động mở beta cho toàn bộ người dùng thay vì cohort giới hạn |
| Rủi ro của Option 0: mất phản hồi và chậm tiến độ | Hoãn mà không có tiêu chí thoát rõ ràng có thể chỉ dịch chuyển rủi ro sang tuần sau | Trung bình | Trung bình | Tiếp tục thêm thay đổi vào release hoặc yêu cầu sửa toàn bộ lỗi nhẹ trước khi thử nghiệm |
| Rủi ro của Option 0: release tiếp theo lớn hơn | Tích lũy thêm code làm tăng phạm vi regression và độ khó xác định nguyên nhân | Trung bình | Trung bình | Không đóng băng release candidate trong thời gian trì hoãn |

**Rủi ro quyết định:** Lỗ hổng lớn nhất không phải là con số 12 lỗi, mà là việc chưa biết liệu severity, rollback, observability và support coverage đã được xác minh ở mức vận hành hay chưa.

---

# Mũ đỏ — Kiểm tra trực giác

Trực giác từ mẫu tình huống nghiêng về **Conditional Go**, không phải phát hành rộng rãi và cũng chưa cần hoãn hoàn toàn.

---

# Mũ xanh lam — Quyết định và hành động

## Khuyến nghị

**Conditional Go: phát hành beta vào thứ Sáu dưới dạng rollout giới hạn**, với điều kiện tất cả cổng bắt buộc bên dưới đều đạt trước giờ triển khai.

Không nên chọn “Go” không điều kiện vì còn thiếu bằng chứng về regression, tính khả dụng thực tế của rollback, phạm vi beta và ngưỡng giám sát. Tuy nhiên, các dữ kiện hiện có không tạo thành lý do đủ mạnh để no-go ngay: lỗi đã biết được báo cáo là mức thấp, không có lỗi mất dữ liệu đã biết, có hỗ trợ cuối tuần và có đường rollback tương đối nhanh.

### Cổng bắt buộc trước khi Go

1. 12 lỗi được triage lại; không lỗi nào ảnh hưởng bảo mật, dữ liệu, quyền truy cập, migration hoặc luồng beta cốt lõi.
2. Release candidate cuối cùng vượt qua smoke test và regression bắt buộc.
3. Rollback được xác minh, bao gồm tương thích database và kiểm tra hệ thống sau rollback.
4. Beta chỉ mở cho cohort giới hạn; có thể dừng hoặc mở rộng độc lập.
5. Dashboard, alert và ngưỡng rollback đã được thống nhất.
6. Có incident commander, release owner và on-call engineer được chỉ định rõ.
7. Đội cuối tuần có quyền truy cập production, log, dashboard và quyền rollback.
8. Không còn finding bảo mật nghiêm trọng hoặc blocker chưa xử lý.

Nếu bất kỳ cổng nào không đạt, quyết định chuyển thành **No-Go cho thứ Sáu**, giữ nguyên release candidate và lên lịch lại sau khi blocker được xử lý.

## Điều kiện đảo chiều

Chuyển từ **Conditional Go** sang **No-Go** nếu:

- Phát hiện lỗi data loss, security nghiêm trọng, privilege escalation hoặc corruption.
- Có lỗi chặn luồng cốt lõi của beta.
- Regression hoặc smoke test không đạt.
- Database migration không tương thích ngược hoặc rollback chưa được diễn tập/xác minh.
- Không thể giới hạn cohort hay tắt tính năng nhanh.
- Không có monitoring hoặc chưa xác định ngưỡng rollback.
- Nhân sự hỗ trợ không có đủ quyền hoặc thiếu người có thể xử lý hệ thống.
- Rollback thực tế vượt quá giới hạn phục hồi mà đội chấp nhận.

Có thể chuyển từ **Conditional Go** sang rollout rộng hơn nếu:

- Cohort đầu tiên ổn định qua cửa sổ theo dõi đã định.
- Không có lỗi nghiêm trọng mới.
- Error rate, latency, crash rate và ticket volume đều dưới ngưỡng.
- Support và engineering cùng xác nhận sẵn sàng mở rộng.

## Kế hoạch hành động

| Bước | Chủ trì | Mốc / thời hạn | Tiêu chí hoàn thành |
|---|---|---|---|
| 1. Triage lại 12 lỗi | QA lead + Engineering lead + Product owner | Trước cuộc họp go/no-go | Mỗi lỗi có owner, severity, phạm vi ảnh hưởng và quyết định accept/fix; không có blocker |
| 2. Đóng băng release candidate | Release manager | Sau khi triage | Commit/artifact triển khai được định danh; chỉ blocker mới được phép thay đổi |
| 3. Chạy regression và smoke test | QA lead | Trước quyết định cuối cùng | Tất cả test bắt buộc đạt; failure được phân loại và xử lý |
| 4. Kiểm tra security và migration | Security owner + Database owner | Trước quyết định cuối cùng | Không có finding nghiêm trọng; migration tương thích ngược; backup/restore phù hợp |
| 5. Xác minh rollback | SRE/DevOps lead | Trước launch | Có bằng chứng rollback rehearsal; hệ thống và dữ liệu được kiểm tra sau rollback; thời gian thực tế được ghi nhận |
| 6. Chuẩn bị observability | SRE + Engineering lead | Trước launch | Dashboard và alert hoạt động; baseline và ngưỡng rollback được ghi thành văn bản |
| 7. Chốt kế hoạch trực cuối tuần | Support lead + Incident commander | Trước launch | Có lịch trực, kênh liên lạc, quyền truy cập, escalation tree và người có quyền rollback |
| 8. Họp go/no-go | Release manager | Ngay trước cửa sổ triển khai | Tất cả cổng được đánh dấu pass; các vai trò xác nhận sẵn sàng; quyết định được ghi lại |
| 9. Triển khai cho cohort nhỏ | Release owner | Đầu cửa sổ phát hành thứ Sáu, tránh cuối ngày | Deployment thành công; smoke test production đạt; cohort nằm trong giới hạn đã định |
| 10. Theo dõi ổn định ban đầu | SRE + Support + Product | Ngay sau triển khai | Chỉ số ổn định trong cửa sổ quan sát đã thống nhất; không có blocker hoặc dấu hiệu data loss |
| 11. Mở rộng, giữ nguyên hoặc rollback | Incident commander + Product owner | Sau cửa sổ quan sát | Quyết định dựa trên ngưỡng định trước, không dựa vào tranh luận ad hoc |
| 12. Theo dõi cuối tuần | On-call engineering + Support | Suốt cuối tuần | Alert và ticket được phản hồi trong SLA nội bộ; mọi incident có nhật ký và owner |
| 13. Đánh giá sau beta | Product owner + Engineering lead | Ngày làm việc kế tiếp | Tổng hợp chỉ số, phản hồi, incident, bug mới và quyết định bước rollout tiếp theo |

## Quy tắc rollback đề xuất

Rollback ngay, không chờ điều tra hoàn tất, nếu xuất hiện một trong các dấu hiệu:

- Mất hoặc hỏng dữ liệu.
- Lỗ hổng bảo mật nghiêm trọng.
- Authentication/authorization hoạt động sai.
- Luồng cốt lõi không sử dụng được.
- Error rate, crash rate hoặc latency vượt ngưỡng đã thống nhất trong khoảng thời gian quy định.
- Khối lượng ticket nghiêm trọng vượt khả năng xử lý.
- Không thể quan sát đủ để xác định hệ thống có an toàn hay không.

## Các câu hỏi còn mở

1. Cohort beta gồm bao nhiêu người và có khách hàng quan trọng hay không?
2. 12 lỗi nằm ở những luồng nào?
3. Con số rollback 15 phút đã được đo trong lần rehearsal nào?
4. Rollback có bao gồm database/schema và side effect hay chỉ phiên bản ứng dụng?
5. Ngưỡng cụ thể cho error rate, latency, crash rate và support volume là gì?
6. Ai là người duy nhất có quyền ra lệnh rollback?
7. Cửa sổ quan sát tối thiểu trước khi mở rộng cohort là bao lâu?

**Kết luận cuối cùng: Conditional Go vào thứ Sáu với cohort giới hạn. Không triển khai nếu các cổng kiểm thử, rollback, monitoring, migration hoặc staffing chưa được xác minh trước cửa sổ phát hành.**
