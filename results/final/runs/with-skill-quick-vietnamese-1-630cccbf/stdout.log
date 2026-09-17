## Mũ xanh lam — Mở đầu

**Chế độ:** nhanh  
**Quyết định:** Có nên mua SaaS monitoring giá **20 triệu đồng/tháng** thay cho việc tiếp tục tự vận hành Prometheus?

**Các phương án:**
- **Option 0:** Tiếp tục tự vận hành Prometheus.
- **Option 1:** Chuyển hoàn toàn sang SaaS.
- **Option 2:** Phê duyệt có điều kiện: chạy thử SaaS song song rồi mới chuyển.

**Ràng buộc:** Team 3 người; phải ra quyết định trong tuần này.  
**Tiêu chí thành công:** giảm công vận hành và rủi ro sự cố mà không làm chi phí, bảo mật hoặc phụ thuộc nhà cung cấp vượt ngưỡng chấp nhận.

## Mũ trắng — Dữ kiện

- `[FACT: người dùng]` SaaS có giá **20 triệu đồng/tháng**.
- `[FACT: người dùng]` Team hiện có **3 người** và đang tự vận hành Prometheus.
- `[NEED-DATA]` Số giờ/tháng team dùng cho nâng cấp, storage, backup, dashboard, alert và xử lý sự cố Prometheus.
- `[NEED-DATA]` SaaS đã bao gồm logs, traces, retention, on-call, SSO và support hay chỉ metrics.
- `[NEED-DATA]` Chi phí phát sinh theo ingestion/cardinality, yêu cầu bảo mật, vị trí lưu dữ liệu và chi phí thoát khỏi nhà cung cấp.

**Công thức cần so sánh:**

`TCO Prometheus = hạ tầng + giờ kỹ sư vận hành + tổn thất do sự cố monitoring`

Không nên chỉ so **hóa đơn hạ tầng Prometheus** với **giá SaaS**.

## Mũ đỏ — Cảm nhận ban đầu

Trực giác cho thấy team 3 người không nên dành nhiều năng lực cho việc nuôi một hệ thống monitoring, trừ khi Prometheus hiện rất ổn định và gần như không tốn công.

## Mũ vàng — Lợi ích của SaaS

| Thời hạn | Lợi ích |
|---|---|
| Ngắn hạn | Giảm việc nâng cấp, backup, storage, HA và xử lý lỗi hệ thống monitoring |
| Trung hạn | Team tập trung hơn vào sản phẩm; onboarding dashboard và alert có thể nhanh hơn |
| Dài hạn | Có support, SLA và khả năng mở rộng mà không cần tự xây thêm platform team |

SaaS đặc biệt đáng giá nếu Prometheus đang phụ thuộc vào một người hoặc từng mất dữ liệu/không phát cảnh báo khi có sự cố.

## Mũ đen — Rủi ro

| Rủi ro | Cơ chế | Khả năng / tác động |
|---|---|---|
| Chi phí tăng ngoài dự kiến | Giá có thể phụ thuộc ingestion, cardinality hoặc retention | Trung bình / Cao |
| Vendor lock-in | Dashboard, alert và query dùng tính năng riêng của nhà cung cấp | Trung bình / Trung bình-Cao |
| Chưa chắc giảm đủ công việc | Team vẫn phải thiết kế instrumentation, dashboard và alert | Cao / Trung bình |
| Rủi ro dữ liệu | Metrics/logs có thể chứa metadata nhạy cảm | Tùy hệ thống / Cao |
| Chuyển đổi gây gián đoạn | Alert thiếu hoặc sai trong quá trình migration | Trung bình / Cao |

**Rủi ro của Option 0:** tiếp tục mất thời gian của team nhỏ, tích lũy nợ nâng cấp và có nguy cơ monitoring hỏng đúng lúc production gặp sự cố.

## Mũ xanh lá — Các phương án cải tiến

- Chạy SaaS song song trong 30 ngày, chỉ gửi metrics của một dịch vụ quan trọng.
- Giữ Prometheus/OpenTelemetry làm lớp thu thập chuẩn, dùng SaaS cho storage, dashboard và alert để giảm lock-in.
- Đàm phán gói giới hạn chi phí, có cảnh báo quota và cam kết không vượt ngân sách.
- Dùng managed Prometheus thay vì một nền tảng observability đầy đủ.
- Thuê ngoài phần nâng cấp/HA định kỳ nhưng vẫn giữ hệ thống hiện tại.
- Giảm cardinality và retention trước, rồi đo lại xem Prometheus còn thực sự tốn công không.

## Mũ đỏ — Kiểm tra lại

Sau phân tích, trực giác chuyển từ “nên mua SaaS” sang **“nên thử có điều kiện, không nên chuyển toàn bộ ngay”**.

## Mũ xanh lam — Kết luận và hành động

### Khuyến nghị

**Chọn Option 2: phê duyệt pilot SaaS trong tuần này, chưa cam kết chuyển hoàn toàn.**

Chỉ mua dài hạn nếu pilot chứng minh được cả ba điều:

1. **Chi phí thực tế có trần rõ ràng**, bao gồm ingestion, retention, support và thuế.
2. **Giảm đáng kể giờ vận hành monitoring** hoặc giảm một rủi ro sự cố quan trọng.
3. **Có đường thoát:** tiếp tục dùng PromQL/OpenTelemetry, xuất được dữ liệu và không phụ thuộc quá nhiều vào dashboard/alert độc quyền.

### Điều kiện làm quyết định đảo chiều

- **Chuyển sang SaaS:** Prometheus tiêu tốn nhiều công sức, thường xuyên có sự cố, phụ thuộc một người, hoặc SaaS thay thế được nhiều công cụ khác.
- **Giữ Prometheus:** hệ thống đang ổn định, chỉ tốn rất ít giờ mỗi tháng, yêu cầu dữ liệu nghiêm ngặt, hoặc báo giá SaaS không có trần.
- **Không nên ký hợp đồng dài hạn** nếu chưa biết chi phí theo cardinality/ingestion.

### Kế hoạch trong tuần

| Thời điểm | Việc cần làm | Chủ trì | Tiêu chí hoàn thành |
|---|---|---|---|
| Ngày 1 | Đo công vận hành Prometheus trong 3 tháng gần nhất | Tech lead | Có số giờ, chi phí hạ tầng và danh sách sự cố |
| Ngày 2 | Yêu cầu báo giá đầy đủ và điều khoản dữ liệu | Người phụ trách vendor | Có trần chi phí và danh sách phần đã bao gồm |
| Ngày 3 | Kiểm tra security, retention, export và lock-in | Kỹ sư phụ trách platform | Không còn rủi ro nghiêm trọng chưa xử lý |
| Ngày 4 | Thiết kế pilot song song | Team | Có phạm vi, KPI và rollback |
| Ngày 5 | Quyết định | Cả team/người giữ ngân sách | Go pilot hoặc tiếp tục Prometheus |

**Kết luận ngắn:** Với team chỉ 3 người, SaaS có khả năng đáng tiền, nhưng **20 triệu/tháng chưa đủ cơ sở để chuyển ngay**. Quyết định hợp lý trong tuần này là **duyệt pilot có giới hạn chi phí và giữ Prometheus làm phương án dự phòng**.
