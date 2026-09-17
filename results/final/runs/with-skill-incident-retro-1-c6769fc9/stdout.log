# Retrospective sự cố theo 6 chiếc mũ

## 🔵 Mũ xanh lam — Mở phiên

**Chế độ:** `retro`

**Vấn đề:** Dịch vụ xuất hiện error rate tăng sau một lần deploy; rollback đã được thực hiện và dịch vụ phục hồi, nhưng nguyên nhân gốc chưa được xác định.

**Mục tiêu phiên retro:**

1. Thiết lập timeline khách quan.
2. Không đồng nhất tương quan thời gian với quan hệ nhân quả.
3. Xác định dữ liệu còn thiếu để hoàn thành RCA.
4. Đưa ra hành động ngăn tái diễn mà không đổ lỗi cá nhân.

**Các lựa chọn hiện tại:**

- **Option 0 — Giữ nguyên trạng:** Không điều tra thêm vì dịch vụ đã phục hồi.
- **Option 1 — Kết luận deployment là nguyên nhân:** Sửa hoặc revert thay đổi vừa deploy.
- **Option 2 — Thực hiện RCA có kiểm chứng:** Bảo toàn dữ liệu, xây dựng và kiểm tra nhiều giả thuyết trước khi kết luận.
- **Option 3 — RCA kết hợp biện pháp phòng vệ tạm thời:** Điều tra nguyên nhân đồng thời siết rollout/monitoring cho các deployment tiếp theo.

**Ràng buộc:**

- `[FACT: người dùng cung cấp]` Chưa biết nguyên nhân gốc.
- `[NEED-DATA]` Chưa có thông tin về phiên bản, thay đổi mã nguồn/cấu hình, log, metrics, traces, hạ tầng và phạm vi người dùng bị ảnh hưởng.
- `[ASSUMPTION]` Chưa có bằng chứng về mất dữ liệu hoặc ảnh hưởng kéo dài sau 09:27.

**Tiêu chí thành công:**

- Có nguyên nhân gốc được hỗ trợ bởi bằng chứng.
- Phân biệt được nguyên nhân, yếu tố góp phần và triệu chứng.
- Có corrective actions với owner và tiêu chí hoàn thành.
- Có thể phát hiện, cô lập và phục hồi nhanh hơn nếu sự cố tương tự tái diễn.

**Trình tự:** Mũ xanh lam → Mũ trắng → Mũ đỏ → Mũ vàng → Mũ đen → Mũ xanh lá → Mũ xanh lam.

---

## ⚪ Mũ trắng — Facts, assumptions và dữ liệu còn thiếu

### 1. Timeline đã biết

| Thời điểm | Thông tin | Phân loại |
|---|---|---|
| 09:00 | Có hoạt động deploy | `[FACT: người dùng cung cấp]` |
| 09:12 | Error rate tăng | `[FACT: người dùng cung cấp]` |
| 09:18 | Rollback bắt đầu | `[FACT: người dùng cung cấp]` |
| 09:27 | Dịch vụ phục hồi | `[FACT: người dùng cung cấp]` |

### 2. Những điều chưa thể kết luận từ timeline

| Nhận định | Trạng thái |
|---|---|
| Deployment gây ra error rate tăng | `[ASSUMPTION]` Có tương quan thời gian nhưng chưa có bằng chứng nhân quả |
| Rollback trực tiếp làm dịch vụ phục hồi | `[ASSUMPTION]` Phục hồi xảy ra sau khi rollback bắt đầu, nhưng chưa loại trừ các nguyên nhân khác |
| Code mới có bug | `[ASSUMPTION]` Có thể là code, config, dependency, dữ liệu, hạ tầng hoặc tải |
| Hệ thống hoàn toàn ổn định sau 09:27 | `[ASSUMPTION]` “Phục hồi” chưa có định nghĩa hoặc observation window |
| Mọi instance đều chạy phiên bản cũ sau rollback | `[ASSUMPTION]` Chưa có deployment state hoặc version distribution |
| Sự cố chỉ ảnh hưởng một dịch vụ | `[ASSUMPTION]` Chưa có dependency map và blast-radius data |
| Không có mất hoặc sai lệch dữ liệu | `[ASSUMPTION]` Chưa có kiểm tra data integrity |
| Deploy là thay đổi duy nhất trong khoảng thời gian này | `[ASSUMPTION]` Chưa có change log tổng hợp |

### 3. Dữ liệu cần thu thập

| Dữ liệu cần có | Mục đích |
|---|---|
| Error rate theo endpoint, status code, instance, zone và version | Xác định blast radius và failure pattern |
| Logs từ trước 09:00 đến sau 09:27 | Tìm exception, timeout và sự kiện chuyển trạng thái |
| Distributed traces hoặc request samples lỗi | Xác định component bắt đầu chuỗi lỗi |
| Diff của code, config, feature flag, schema và dependency | Liệt kê toàn bộ thay đổi của release |
| Deployment events và version distribution theo thời gian | Kiểm tra lỗi có bám theo phiên bản mới không |
| Rollback events và version distribution | Kiểm tra thời điểm rollback thực sự hoàn tất |
| CPU, memory, connection pool, queue depth, latency và saturation | Kiểm tra giới hạn tài nguyên |
| Database metrics, migration log và query latency | Kiểm tra tác động từ database |
| Dependency health và third-party status | Loại trừ nguyên nhân bên ngoài |
| Traffic volume và request mix | Kiểm tra tải hoặc loại request bất thường |
| Change calendar toàn hệ thống | Xác định thay đổi đồng thời ngoài deployment |
| Tỷ lệ lỗi sau 09:27 trong một observation window xác định | Xác nhận dịch vụ ổn định thực sự |
| Kiểm tra data integrity | Xác định có dữ liệu sai, thiếu hoặc xử lý trùng không |

### 4. Ý kiến có thể bị trình bày nhầm thành fact

- “Deploy chắc chắn gây ra sự cố” — `[OPINION/HYPOTHESIS]`
- “Rollback đã sửa lỗi” — `[OPINION/HYPOTHESIS]`
- “Đây chỉ là lỗi code” — `[OPINION/HYPOTHESIS]`
- “Dịch vụ phục hồi nên không còn rủi ro” — `[OPINION/HYPOTHESIS]`

### 5. Các câu hỏi `[NEED-DATA]` ưu tiên

1. Deploy 09:00 thay đổi những gì?
2. Error rate được ghi nhận lần đầu lúc 09:12 hay bắt đầu tăng từ trước đó?
3. Loại lỗi cụ thể là gì: 4xx, 5xx, timeout hay lỗi nghiệp vụ?
4. Phiên bản mới và cũ có chạy song song không?
5. Rollback hoàn tất lúc nào?
6. “Phục hồi” được xác nhận bằng metric nào?
7. Có thay đổi hạ tầng, dữ liệu, config hoặc dependency cùng thời điểm không?
8. Có mất dữ liệu, xử lý trùng hoặc side effect từ request thất bại không?

---

## 🔴 Mũ đỏ — Cảm nhận ban đầu

Trực giác cho thấy deployment là nghi phạm mạnh nhất, nhưng tôi chưa tin rằng chỉ riêng timeline đủ để kết luận nguyên nhân. Cảm giác tích cực là rollback path đã hoạt động, nhưng observability hoặc thông tin sự cố hiện chưa đủ sâu.

---

## 🟡 Mũ vàng — Những điểm đã làm tốt và giá trị có thể khai thác

| Trọng tâm | Ngắn hạn | Trung hạn | Dài hạn |
|---|---|---|---|
| **Lợi ích** | `[FACT]` Nhóm đã bắt đầu rollback và dịch vụ đã phục hồi trong cùng sự cố | Timeline cung cấp điểm khởi đầu rõ ràng cho RCA | Sự cố có thể trở thành test case thực tế cho quy trình release và incident response |
| **Giá trị** | Hạn chế thời gian dịch vụ tiếp tục ở trạng thái lỗi | Có thể cải thiện dashboard, runbook và rollback automation từ bằng chứng thực tế | Có thể xây dựng cơ chế progressive delivery và kiểm chứng release an toàn hơn |
| **Tính khả thi** | Có thể bảo toàn log, metric và artifact ngay lập tức | Có thể tái hiện bằng cùng artifact/config trong môi trường kiểm soát | Có thể bổ sung canary, automated rollback và release health gate |

**Điểm sáng cụ thể:**

- `[FACT: người dùng cung cấp]` Rollback đã được khởi động, tức là hệ thống hoặc đội vận hành có khả năng thực hiện rollback.
- `[FACT: người dùng cung cấp]` Dịch vụ đã phục hồi, nên giai đoạn mitigation đã đạt kết quả vận hành ban đầu.
- Timeline có các mốc quan trọng, thuận lợi để đối chiếu với logs, metrics và deployment events.

---

## ⚫ Mũ đen — Rủi ro và điểm yếu

| Rủi ro | Cơ chế | Bằng chứng hiện có | Khả năng / Tác động | Yếu tố làm rủi ro tăng |
|---|---|---|---|---|
| Kết luận sai rằng deployment là nguyên nhân | Tương quan thời gian bị diễn giải thành nhân quả | Chỉ có timeline | Khả năng: chưa xác định; tác động: cao | Không kiểm tra thay đổi đồng thời và dependency |
| Sự cố tái diễn | Nguyên nhân gốc và yếu tố góp phần chưa được loại bỏ | `[FACT]` Chưa biết root cause | Khả năng: chưa xác định; tác động: cao | Deploy lại cùng thay đổi hoặc gặp cùng điều kiện |
| Bằng chứng bị mất | Logs hoặc traces bị rotate; trạng thái runtime bị thay đổi sau rollback | Chưa có thông tin về retention | Khả năng: chưa xác định; tác động: cao đối với RCA | Trì hoãn snapshot và thu thập artifact |
| Phục hồi chưa hoàn toàn | Error rate tổng thể có thể trở lại bình thường trong khi một số endpoint/tenant vẫn lỗi | Chưa có dữ liệu phân đoạn | Khả năng: chưa xác định; tác động: trung bình–cao | Chỉ theo dõi aggregate metric |
| Có hậu quả dữ liệu tiềm ẩn | Request lỗi có thể đã ghi một phần, retry hoặc tạo xử lý trùng | Chưa có integrity check | Khả năng: chưa xác định; tác động: có thể cao | Non-idempotent operations hoặc transaction không nguyên tử |
| Rollback không loại bỏ toàn bộ thay đổi | Migration, config, cache hoặc external state có thể không rollback cùng code | Chưa có release diff | Khả năng: chưa xác định; tác động: cao | Release chứa thay đổi không backward-compatible |
| Option 0 tạo “false closure” | Dịch vụ phục hồi bị coi là sự cố đã kết thúc | Root cause vẫn chưa biết | Khả năng: cao nếu không mở RCA; tác động: cao | Không có owner và deadline điều tra |
| RCA biến thành đổ lỗi | Tập trung vào người deploy thay vì điều kiện hệ thống | Chưa có dữ liệu về quy trình | Khả năng: chưa xác định; tác động: trung bình–cao | Thiếu nguyên tắc blameless và audit trail khách quan |

---

## 🟢 Mũ xanh lá — Các phương án cải tiến và giả thuyết kiểm tra

Không xếp hạng các ý tưởng trong phần này.

### Các hướng điều tra

1. So sánh error rate giữa instance chạy phiên bản cũ và phiên bản mới.
2. Overlay trên cùng timeline:
   - deploy events;
   - version distribution;
   - error rate;
   - latency;
   - resource saturation;
   - dependency health;
   - rollback progression.
3. Lập “change inventory” bao gồm code, config, feature flags, schema, secrets, infrastructure và dependency.
4. Lấy request lỗi đại diện và lần theo distributed trace.
5. Tái hiện release bằng production artifact trong môi trường staging với traffic replay đã loại dữ liệu nhạy cảm.
6. Thực hiện fault isolation: bật riêng từng thay đổi hoặc chia đôi tập thay đổi để thu hẹp nghi phạm.
7. Kiểm tra giả thuyết không liên quan deployment: traffic spike, dependency degradation, database contention, certificate/DNS/network event.

### Các cải tiến phòng vệ

8. Canary deployment với health gate theo error rate và latency.
9. Automated rollback khi metric vượt ngưỡng trong một cửa sổ xác định.
10. Gắn `release_id`, `commit_sha`, `config_version` vào logs, metrics và traces.
11. Dashboard so sánh old-version/new-version theo thời gian thực.
12. Pre-deploy snapshot và post-deploy verification checklist.
13. Feature flag cho thay đổi rủi ro cao để tắt chức năng mà không rollback toàn bộ.
14. Shadow traffic hoặc traffic replay trước khi rollout rộng.
15. Synthetic transaction kiểm tra các luồng nghiệp vụ trọng yếu sau deploy.
16. Thiết lập change freeze tạm thời chỉ cho component liên quan, với ngoại lệ cho bản vá khẩn cấp.
17. Ý tưởng phi truyền thống: chạy “dark canary” thường trực nhận bản sao traffic nhưng không tạo side effect, nhằm phát hiện sai lệch trước khi phục vụ người dùng thật.

---

## 🔵 Mũ xanh lam — Kết luận và hành động

### Kết luận

**Chưa đủ bằng chứng để xác định root cause.**

Khuyến nghị chọn **Option 3: RCA có kiểm chứng kết hợp biện pháp phòng vệ tạm thời**.

Các kết luận được phép đưa ra lúc này:

- `[FACT]` Có deploy lúc 09:00.
- `[FACT]` Error rate tăng lúc 09:12.
- `[FACT]` Rollback bắt đầu lúc 09:18.
- `[FACT]` Dịch vụ phục hồi lúc 09:27.
- `[ASSUMPTION]` Deployment có liên quan đến sự cố.
- `[ASSUMPTION]` Rollback là nguyên nhân làm dịch vụ phục hồi.
- `[UNKNOWN]` Root cause, trigger, contributing factors, blast radius và data impact.

Không nên đóng incident chỉ với nhãn “bad deployment” nếu chưa có bằng chứng kỹ thuật.

### Kế hoạch hành động

| Bước | Owner đề xuất | Mốc | Exit criterion |
|---|---|---|---|
| 1. Bảo toàn logs, metrics, traces, deployment events và release artifacts | Incident Commander + SRE | Ngay lập tức | Dữ liệu từ trước deploy đến sau phục hồi được lưu và truy cập được |
| 2. Xác nhận trạng thái ổn định và blast radius | SRE/Operations | Trong ngày | Error rate/latency bình thường theo endpoint, tenant, zone và version trong observation window đã thống nhất |
| 3. Kiểm tra tính toàn vẹn dữ liệu | Backend + Data/DB owner | Trong ngày | Không có sai lệch, hoặc có danh sách record cần khắc phục |
| 4. Lập inventory toàn bộ thay đổi | Release owner | Trong ngày | Có danh sách code, config, schema, flag, infra và dependency changes |
| 5. Dựng timeline kỹ thuật chi tiết | Incident Commander | T+1 ngày làm việc | Mỗi mốc có metric, event hoặc log làm bằng chứng |
| 6. Xây dựng và kiểm tra các giả thuyết | Backend + SRE + QA | T+1 đến T+2 | Mỗi giả thuyết có bằng chứng ủng hộ, phản bác và kết quả kiểm tra |
| 7. Xác định root cause và contributing factors | Nhóm RCA | T+2 | Nguyên nhân giải thích được cả sự xuất hiện lỗi và quá trình phục hồi |
| 8. Tạo corrective actions | Tech Lead + Product/Operations | Sau RCA | Mỗi action có owner, deadline, priority và verification test |
| 9. Kiểm chứng trước khi deploy lại | Release owner + QA/SRE | Trước lần phát hành kế tiếp | Reproduction test hoặc regression test thất bại trước fix và thành công sau fix |
| 10. Review hiệu quả hành động | Engineering Manager/SRE Lead | Sau một chu kỳ release | Action được xác minh bằng bằng chứng, không chỉ đánh dấu hoàn thành |

### Điều kiện để quyết định thay đổi

- Nếu lỗi chỉ xuất hiện trên phiên bản mới và tái hiện được với cùng thay đổi, deployment trở thành nguyên nhân có bằng chứng mạnh.
- Nếu lỗi xuất hiện đồng thời trên cả phiên bản cũ, phải mở rộng điều tra sang dependency, hạ tầng, dữ liệu và traffic.
- Nếu phát hiện nguy cơ mất/sai dữ liệu, ưu tiên reconciliation và thông báo stakeholder trước việc deploy lại.
- Nếu không còn đủ telemetry để chứng minh root cause, kết luận phải ghi rõ **“probable cause”**, mức độ tin cậy và bằng chứng còn thiếu.

### Câu hỏi còn mở

1. Deployment chứa những thay đổi nào?
2. Error rate tăng trên phiên bản nào và loại request nào?
3. Rollback hoàn tất chính xác khi nào?
4. Metric nào xác nhận “dịch vụ phục hồi”?
5. Có thay đổi đồng thời ngoài deployment không?
6. Có data corruption, partial write hoặc duplicate processing không?
7. Sự cố có thể tái hiện không?
8. Vì sao hệ thống không phát hiện hoặc ngăn chặn sớm hơn?
9. Canary, health gate hoặc automated rollback hiện có hay chưa?

**Trạng thái retrospective:** Mitigation đã hoàn thành; RCA vẫn mở. Không gán root cause cho deployment cho đến khi có bằng chứng kiểm chứng được.
