## 🔵 Mũ xanh lam — Mở đầu

- **Quyết định:** Có nên mua SaaS monitoring giá **20 triệu đồng/tháng** thay cho việc tiếp tục tự vận hành Prometheus?
- **Phương án:**  
  - **Option 0:** Tiếp tục tự vận hành Prometheus.  
  - **Option 1:** Chuyển hoàn toàn sang SaaS.  
  - **Option 2:** Dùng SaaS có giới hạn hoặc chạy song song trong giai đoạn thử nghiệm.
- **Ràng buộc:** Team 3 người; phải quyết định trong tuần này. Tiêu chí chính: giảm công vận hành, độ tin cậy, khả năng xử lý sự cố và chi phí thực tế.
- **Chế độ:** `quick`; trình tự **Xanh lam → Trắng → Đỏ → Vàng → Đen → Xanh lá → Đỏ → Xanh lam**.

## ⚪ Mũ trắng — Dữ kiện

- [FACT: thông tin người dùng] SaaS có giá **20 triệu đồng/tháng**; team hiện có 3 người và đang tự vận hành Prometheus.
- [NEED-DATA: trích timesheet, ticket và lịch trực 3 tháng gần nhất] Prometheus đang tiêu tốn bao nhiêu giờ công mỗi tháng, bao gồm nâng cấp, lưu trữ, backup, alert và xử lý sự cố?
- [NEED-DATA: yêu cầu báo giá và chạy thử với dữ liệu thực tế] Giá 20 triệu đã bao gồm ingestion, retention, logs/traces, cảnh báo, support và thuế hay chưa? Cần kiểm tra thêm SLA, giới hạn dữ liệu và phí vượt ngưỡng.

## 🔴 Mũ đỏ — Cảm nhận ban đầu

Trực giác theo mẫu hình cho thấy SaaS đáng cân nhắc với team chỉ 3 người, nhưng chuyển toàn bộ ngay trong tuần này tạo cảm giác quá vội.

## 🟡 Mũ vàng — Giá trị

- **Ngắn hạn:** Giảm việc bảo trì, nâng cấp và trực hệ thống monitoring; team tập trung hơn vào sản phẩm.
- **Trung hạn:** Có thể cải thiện độ ổn định, hỗ trợ và thời gian phản ứng sự cố nếu SaaS có SLA và tính năng tốt hơn hệ thống hiện tại.
- **Dài hạn:** Giảm phụ thuộc vào một thành viên hiểu sâu Prometheus; chi phí vận hành dễ dự báo hơn nếu lượng dữ liệu ổn định.

## ⚫ Mũ đen — Rủi ro

- **Chi phí tăng ngoài dự kiến:** Giá thường phụ thuộc ingestion, cardinality hoặc retention; khả năng **trung bình**, tác động **cao** nếu dữ liệu tăng nhanh.
- **Vendor lock-in và mất quyền kiểm soát:** Dashboard, alert hoặc truy vấn độc quyền làm việc quay lại Prometheus khó hơn; khả năng **trung bình**, tác động **trung bình–cao**.
- **Rủi ro của Option 0:** Team nhỏ tiếp tục mất thời gian cho hạ tầng và có thể thiếu người xử lý khi Prometheus gặp sự cố; khả năng **trung bình**, tác động **cao** nếu monitoring là hệ thống trọng yếu.

## 🟢 Mũ xanh lá — Các phương án sáng tạo

- Chạy **pilot SaaS 30 ngày** với một môi trường hoặc một nhóm dịch vụ, chưa tắt Prometheus.
- Chỉ mua phần khó tự vận hành, chẳng hạn lưu trữ dài hạn hoặc cảnh báo, còn Prometheus tiếp tục thu thập metrics.
- Đàm phán gói giới hạn ngân sách, cảnh báo chi phí và điều khoản xuất dữ liệu; giữ dashboard/alert bằng chuẩn mở.
- Thử phương án “managed Prometheus” hoặc thuê hỗ trợ vận hành theo giờ thay vì thay toàn bộ nền tảng.

## 🔴 Mũ đỏ — Kiểm tra lại

Sau phân tích, trực giác nghiêng về **thử SaaS có kiểm soát**, không nghiêng về chuyển toàn bộ ngay lập tức.

## 🔵 Mũ xanh lam — Kết luận

### Khuyến nghị

**Chưa phê duyệt chuyển hoàn toàn sang SaaS.** Trong tuần này, nên phê duyệt **Option 2: pilot có giới hạn**, với ngân sách trần và Prometheus vẫn hoạt động làm phương án quay lui.

### Điều kiện đảo chiều

- **Chọn SaaS lâu dài** nếu chi phí dự kiến nằm trong ngân sách, giảm đáng kể công vận hành và đáp ứng SLA, khả năng xuất dữ liệu, bảo mật.
- **Giữ Prometheus** nếu công vận hành hiện tại thấp, SaaS có phí biến đổi khó kiểm soát hoặc không chứng minh được cải thiện về độ tin cậy.
- **Chuyển hoàn toàn ngay** chỉ khi Prometheus hiện có sự cố nghiêm trọng, thiếu người vận hành và nhà cung cấp đáp ứng đầy đủ yêu cầu kỹ thuật–thương mại.

### Kế hoạch hành động

| Bước | Chủ trì | Mốc / thời hạn | Tiêu chí hoàn thành |
|---|---|---|---|
| Đo chi phí và giờ công Prometheus trong 3 tháng gần nhất | Tech Lead | T+1 ngày | Có tổng giờ công, incident và chi phí hạ tầng |
| Xác minh báo giá, SLA, retention, giới hạn và phí vượt ngưỡng | Engineering Manager/Procurement | T+2 ngày | Có bảng tổng chi phí theo mức sử dụng thực tế |
| Demo hoặc pilot với dữ liệu đại diện | DevOps/SRE | T+3–4 ngày | Kiểm chứng ingestion, dashboard, alert, export và rollback |
| Ra quyết định tại cổng go/no-go | Người phụ trách ngân sách + Tech Lead | Cuối tuần | Chọn pilot, mua chính thức hoặc giữ Prometheus theo tiêu chí đã thống nhất |
