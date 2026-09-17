## Mũ xanh lam — đóng khung

**Chế độ: single — chỉ Mũ đen.** Đánh giá rủi ro của phương án **rewrite toàn bộ backend trong 8 tuần**, với **team 5 người vẫn phải phát triển feature mới**.

Giả định: backend đang chạy production; rewrite có thay đổi đáng kể về code/kiến trúc; 5 người bao gồm cả người xử lý feature, review, test và vận hành.

## Mũ đen — xem xét rủi ro

### Kết luận ngắn

**Đây là kế hoạch rủi ro rất cao và khó khả thi trong 8 tuần.** Hai mục tiêu “rewrite toàn bộ” và “không dừng feature” cạnh tranh trực tiếp về nhân lực, review, kiểm thử và sự tập trung. Nguy cơ lớn nhất không chỉ là trễ hạn mà là sau 8 tuần có **hai backend chưa ổn định**, trong khi feature mới bị chậm hoặc phải làm lại.

| Rủi ro | Cơ chế gây ra | Khả năng | Tác động |
|---|---|---:|---:|
| Phạm vi rewrite bị đánh giá thiếu | Backend hiện tại chứa nhiều business rule, edge case và hành vi ngầm chỉ lộ ra khi migrate | Rất cao | Rất cao |
| Năng lực team bị chia đôi | 5 người phải đồng thời rewrite, phát triển feature, review, sửa production và hỗ trợ release | Rất cao | Rất cao |
| Feature mới phải triển khai hai lần | Feature được thêm vào hệ thống cũ trong lúc hệ thống mới đang phát triển, sau đó phải port hoặc đồng bộ sang hệ thống mới | Cao | Cao |
| “Big-bang migration” thất bại | Toàn bộ hệ thống chỉ tạo giá trị khi rewrite gần hoàn thành; ít cơ hội kiểm chứng từng phần trên production | Cao | Rất cao |
| Không đủ thời gian kiểm thử hồi quy | Rewrite phải tái tạo cả hành vi mong muốn lẫn những hành vi mà client hiện đang phụ thuộc | Rất cao | Rất cao |
| Chất lượng kiến trúc mới suy giảm | Áp lực 8 tuần khiến team cắt test, observability, migration tooling, tài liệu và xử lý lỗi | Cao | Cao |
| Backend cũ tiếp tục thay đổi | Các feature và bug fix mới làm baseline liên tục dịch chuyển, khiến phạm vi rewrite không ổn định | Rất cao | Cao |
| Tắc nghẽn review và tích hợp | Với team nhỏ, cùng một số người thường vừa thiết kế, code, review và xử lý conflict | Cao | Cao |
| Phụ thuộc vào cá nhân | Kiến thức nghiệp vụ thường tập trung ở một vài thành viên; họ trở thành nút thắt cho cả rewrite lẫn feature | Trung bình–cao | Cao |
| Cutover và rollback không an toàn | Schema, dữ liệu, API compatibility và traffic migration có thể không đảo ngược đơn giản | Cao | Rất cao |
| Burnout và giảm năng suất | Deadline cố định cộng hai luồng công việc tạo context switching và làm thêm giờ | Cao | Cao |
| Mất niềm tin của stakeholder | Nếu vừa trễ rewrite vừa chậm feature, dự án bị nhìn nhận là tiêu tốn nguồn lực mà chưa tạo giá trị | Cao | Cao |

### Các điểm có thể làm kế hoạch vỡ sớm

1. **“Toàn bộ backend” chưa có ranh giới đóng**
   - Nếu chưa có inventory endpoint, worker, cron job, integration, schema, business rule và yêu cầu phi chức năng thì không thể bảo vệ deadline.
   - Một integration hoặc luồng dữ liệu ngầm bị bỏ sót có thể chặn cutover toàn hệ thống.

2. **Không có capacity thực sự cho 5 người**
   - “Team 5 người” không đồng nghĩa có 5 người toàn thời gian cho rewrite.
   - Feature mới, incident, họp, review và vận hành đều lấy capacity từ cùng một nhóm.
   - Nếu không khóa tỷ lệ phân bổ nhân lực, rewrite sẽ luôn thua việc production khẩn cấp.

3. **Hai codebase tạo ra chi phí kép**
   - Mỗi thay đổi business rule phải quyết định: chỉ sửa hệ thống cũ, chỉ thêm vào hệ thống mới, hay làm cả hai.
   - Làm một bên tạo divergence; làm hai bên làm giảm gần một nửa tốc độ tại khu vực đó và tăng nguy cơ hành vi không nhất quán.

4. **Deadline khuyến khích “đạt demo”, không phải “sẵn sàng production”**
   - Có thể hoàn thành happy path trong 8 tuần nhưng thiếu migration dữ liệu, tải cao, bảo mật, audit, monitoring, runbook và rollback.
   - Vì vậy, “code complete” dễ bị báo cáo nhầm thành “rewrite hoàn tất”.

5. **Kiểm thử không chứng minh được tương đương hành vi**
   - Nếu hệ thống cũ thiếu test hoặc specification, team không có oracle đáng tin cậy để biết backend mới đúng hay sai.
   - Các client có thể đang phụ thuộc vào status code, thứ tự dữ liệu, timeout hoặc hành vi lỗi không được tài liệu hóa.

6. **Triển khai big-bang làm tăng bán kính sự cố**
   - Một lỗi chung trong authentication, transaction, cache hoặc data mapping có thể ảnh hưởng toàn bộ hệ thống.
   - Khi xảy ra lỗi, rollback có thể không phục hồi được dữ liệu đã ghi bằng schema hoặc semantics mới.

### Điều kiện làm rủi ro nghiêm trọng hơn

- Backend là monolith lớn hoặc có nhiều integration bên ngoài.
- Không có automated regression/contract test đủ tốt.
- Không có API và domain specification đáng tin cậy.
- Rewrite đồng thời đổi ngôn ngữ, framework, database hoặc kiến trúc.
- Feature roadmap trong 8 tuần chưa được đóng phạm vi.
- Team có nghĩa vụ on-call hoặc thường xuyên xử lý production incident.
- Không có staging gần giống production.
- Migration yêu cầu downtime rất thấp hoặc không được phép mất dữ liệu.
- Deadline 8 tuần là cam kết thương mại cứng.
- “Rewrite xong” chưa có tiêu chí nghiệm thu định lượng.
- Không có cơ chế chạy song song, shadow traffic hoặc rollback.

### Rủi ro của phương án không rewrite

Không rewrite cũng không an toàn nếu backend hiện tại:

- thường xuyên gây incident;
- không thể phát triển feature quan trọng;
- có lỗ hổng bảo mật hoặc dependency hết hỗ trợ;
- chi phí thay đổi tăng nhanh;
- kiến trúc hiện tại cản trở mục tiêu kinh doanh bắt buộc.

Tuy nhiên, những vấn đề này **không tự động chứng minh rằng rewrite toàn bộ trong 8 tuần là đúng**. Chúng chỉ chứng minh cần thay đổi; phương thức thay đổi vẫn có thể là thay thế từng phần.

### Phán quyết Mũ đen

**Không nên cam kết kế hoạch dưới dạng “rewrite toàn bộ backend và tiếp tục feature bình thường trong 8 tuần”.** Cấu trúc kế hoạch tạo ra quá nhiều rủi ro đồng thời: phạm vi mở, capacity cạnh tranh, hai codebase, kiểm thử hồi quy và cutover big-bang.

Chỉ nên coi kế hoạch khả thi nếu “rewrite toàn bộ” thực tế là một backend nhỏ, phạm vi đã được kiểm kê và đóng chặt, có test tốt, feature mới được giảm mạnh, và 8 tuần chỉ là mốc cho một lát cắt production có thể rollback — không phải thay thế toàn bộ hệ thống.
