### Mũ xanh lam — định khung

Chế độ `single`: chỉ dùng Mũ đen để kiểm tra rủi ro của phương án rewrite toàn bộ backend trong 8 tuần, với team 5 người đồng thời phải phát triển feature mới; phương án đối chiếu là `Option 0: giữ backend hiện tại và tiếp tục cải tiến từng phần`.

## Mũ đen — xem xét rủi ro

[FACT: thông tin người dùng] Phạm vi là toàn bộ backend, thời hạn 8 tuần, team 5 người và feature mới vẫn phải tiếp tục. Chưa có dữ liệu về quy mô codebase, mức độ test tự động, yêu cầu tương thích, chiến lược migration và tỷ lệ nhân lực dành cho feature.

| Rủi ro | Cơ chế và căn cứ | Khả năng | Tác động | Điều làm rủi ro nặng hơn |
|---|---|---:|---:|---|
| Không hoàn thành trong 8 tuần | “Toàn bộ backend” thường bao gồm API, business logic, database, integration, authentication, jobs, monitoring và deployment; trong khi cùng một team phải chia năng lực cho feature mới | Rất cao | Rất cao | Scope chưa được kiểm kê; deadline cố định; không được giảm feature |
| Rewrite xong nhưng thiếu feature parity | Các hành vi ngầm, edge case và workaround trong hệ thống cũ dễ không xuất hiện trong tài liệu; implementation mới có thể “đúng thiết kế” nhưng sai hành vi thực tế | Cao | Rất cao | Test coverage thấp; thiếu contract test; phụ thuộc người có kiến thức ngầm |
| Backend cũ và mới liên tục phân kỳ | Feature mới được thêm vào hệ thống cũ trong lúc rewrite; team phải port lại sang backend mới hoặc duy trì hai implementation | Rất cao | Cao | Không có cutoff hoặc quy tắc feature nào phải implement ở đâu |
| Chất lượng feature mới suy giảm | Cùng 5 người phải giữ production, xử lý bug, viết feature và rewrite; context switching làm giảm thời gian review, test và xử lý thiết kế | Cao | Cao | On-call nhiều; feature có deadline thương mại; nhiều người cùng làm hai luồng |
| Rewrite trở thành “big bang” khó kiểm chứng | Nếu chỉ có thể release khi toàn bộ backend hoàn tất, lỗi tích tụ lâu và feedback production đến quá muộn | Cao | Rất cao | Không chia được bounded context; không có strangler rollout, shadow traffic hoặc feature flag |
| Migration dữ liệu thất bại | Thay đổi schema hoặc semantics có thể làm mất dữ liệu, sai mapping, downtime hoặc khó rollback | Trung bình–cao | Rất cao | Dữ liệu lớn/bẩn; migration một lần; không diễn tập restore và rollback |
| Regression tại integration bên ngoài | Client, webhook, payment, identity hoặc đối tác có thể phụ thuộc vào những chi tiết API không được ghi thành contract | Cao | Rất cao | Thiếu API versioning; sandbox không tương đương production; đối tác khó phối hợp |
| Ước lượng tạo cảm giác chắc chắn giả | Mốc 8 tuần có thể chỉ bao phủ coding, nhưng bỏ sót discovery, parity validation, migration rehearsal, hardening và vận hành sau release | Cao | Cao | Cam kết deadline trước khi inventory; định nghĩa “xong” chỉ là code complete |
| Kiến trúc mới chưa được chứng minh | Rewrite đồng thời nhiều thành phần khiến team đặt cược vào các quyết định thiết kế chưa được kiểm nghiệm dưới tải và dữ liệu thật | Trung bình–cao | Cao | Đổi cả framework, database và deployment model cùng lúc |
| Rollback không khả thi | Khi code mới đi cùng schema hoặc semantics mới, quay về phiên bản cũ có thể làm dữ liệu không tương thích | Trung bình–cao | Rất cao | Migration phá hủy dữ liệu; dual-write không được kiểm chứng; không có checkpoint |
| Gánh nặng vận hành tăng tạm thời | Trong giai đoạn chuyển đổi, team có thể phải monitor, deploy và sửa lỗi cả hai backend | Cao | Cao | Hai stack công nghệ khác nhau; observability chưa đạt parity |
| Burnout và “bus factor” | Deadline ngắn tạo áp lực làm ngoài giờ; kiến thức có thể tập trung vào một vài người viết lõi hoặc migration | Cao | Cao | Một người giữ vai trò kiến trúc hoặc database duy nhất; thiếu thời gian review và tài liệu |
| Rewrite tái tạo lỗi cũ dưới hình thức mới | Nếu nguyên nhân gốc là requirement thay đổi, coupling tổ chức hoặc thiếu test, viết lại code không tự loại bỏ các vấn đề đó | Trung bình–cao | Cao | Không có phân tích nguyên nhân; mục tiêu rewrite chỉ là “code cũ quá xấu” |
| Chi phí chìm làm mất khả năng dừng | Sau vài tuần, áp lực “đã đầu tư quá nhiều” có thể khiến dự án tiếp tục dù bằng chứng cho thấy không kịp hoặc không tạo đủ giá trị | Cao | Cao | Không có checkpoint go/no-go; tiến độ đo bằng lượng code thay vì luồng nghiệp vụ chạy được |
| Sự cố production ảnh hưởng cả hai luồng | Team đang bị phân tán nên một incident ở backend hiện tại có thể đồng thời làm trễ rewrite và feature | Trung bình–cao | Cao | Hệ thống hiện tại thiếu ổn định; không có capacity dự phòng |
| Kỳ vọng stakeholder bị sai lệch | “Rewrite trong 8 tuần” dễ được hiểu là hoàn thành production-ready, trong khi team có thể chỉ đạt prototype hoặc partial parity | Cao | Cao | Không định nghĩa rõ phạm vi, mức chất lượng, migration và giai đoạn ổn định hóa |

### Rủi ro của `Option 0`

| Rủi ro | Cơ chế | Khả năng / tác động |
|---|---|---|
| Nợ kỹ thuật tiếp tục tăng | Feature mới tiếp tục được xây trên kiến trúc hiện tại, có thể làm việc cải tiến sau này khó hơn | Khả năng cao nếu không dành capacity cải tiến; tác động tăng dần |
| Các điểm nghẽn hiện tại không được xử lý | Nếu backend đang gây sự cố, chậm delivery hoặc giới hạn scale, giữ nguyên trạng sẽ duy trì chi phí vận hành | Chưa xác định vì thiếu metrics; tác động có thể cao |
| Team mất niềm tin vào codebase | Việc liên tục vá lỗi mà không xử lý cấu trúc có thể giảm tinh thần và tăng thời gian onboarding | Khả năng trung bình; tác động trung bình–cao |
| Bỏ lỡ thời điểm migration thuận lợi | Khi số feature và dữ liệu tiếp tục tăng, lần thay đổi sau có thể tốn kém hơn | Khả năng trung bình–cao; tác động dài hạn cao |

### Điểm chưa đủ dữ liệu làm mức rủi ro chưa thể thu hẹp

- `[NEED-DATA: lập inventory theo module, endpoint, job, integration và bảng dữ liệu]` Chưa biết “toàn bộ backend” thực tế lớn đến đâu.
- `[NEED-DATA: chạy báo cáo test coverage và thống kê contract/integration/E2E test]` Chưa biết khả năng phát hiện regression.
- `[NEED-DATA: trích roadmap 8 tuần và ước lượng effort của từng feature đã cam kết]` Chưa biết bao nhiêu năng lực thực sự còn lại cho rewrite.
- `[NEED-DATA: phân tích incident, lead time, change-failure rate và thời gian sửa lỗi trong 3–6 tháng gần nhất]` Chưa chứng minh rewrite toàn bộ là cần thiết hơn cải tiến từng phần.
- `[NEED-DATA: dựng migration rehearsal trên bản sao dữ liệu production đã ẩn danh]` Chưa biết thời gian migration, tính toàn vẹn dữ liệu và khả năng rollback.
- `[NEED-DATA: lập dependency map và phỏng vấn người sở hữu từng integration]` Chưa xác định các contract ngầm.
- `[NEED-DATA: định nghĩa bằng văn bản “hoàn thành trong 8 tuần” gồm parity, tải, bảo mật, migration, observability và rollback]` Chưa có tiêu chí để phân biệt prototype với production-ready.

Mức rủi ro tổng thể hiện tại: **rất cao**, chủ yếu do xung đột năng lực, scope “toàn bộ”, phân kỳ giữa backend cũ và mới, và chưa thấy bằng chứng về cơ chế migration/rollback. Đây là đánh giá rủi ro, không phải quyết định go/no-go.
