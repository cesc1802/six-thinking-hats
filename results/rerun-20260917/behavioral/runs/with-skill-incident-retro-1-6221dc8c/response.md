# Mũ xanh lam — Mở phiên retrospective

**Vấn đề:** Phân tích sự cố dịch vụ xảy ra sau đợt deploy lúc 09:00, tách biệt dữ kiện khỏi giả định và xác định kế hoạch điều tra nguyên nhân gốc.

- **Chế độ:** `retro`
- **Loại quyết định:** Retrospective sự cố và cải tiến quy trình vận hành.
- **Các phương án:**
  - **Option 0: Không hành động / giữ nguyên hiện trạng.**
  - **Phương án 1:** Chỉ điều tra nguyên nhân gốc.
  - **Phương án 2:** Điều tra nguyên nhân gốc đồng thời bổ sung biện pháp giảm thiểu và kiểm soát deploy.
- **Ràng buộc:**
  - Chưa biết nguyên nhân gốc.
  - Chưa có log, metric chi tiết, deployment diff hoặc dữ liệu cảnh báo.
  - Không được kết luận deploy gây ra lỗi chỉ dựa trên thứ tự thời gian.
- **Tiêu chí thành công:**
  1. Xác định được nguyên nhân gốc với bằng chứng tái kiểm chứng.
  2. Giải thích được vì sao error rate tăng.
  3. Xác định rõ rollback có thực sự giúp dịch vụ phục hồi hay không.
  4. Có biện pháp phát hiện sớm, rollback nhanh và ngăn tái diễn.
- **Trình tự:** Mũ xanh lam → Mũ trắng → Mũ đỏ → Mũ vàng → Mũ đen → Mũ xanh lá → Mũ xanh lam.

---

# Mũ trắng — Dữ kiện khách quan

## 1. Thông tin đã biết

| Thời điểm | Thông tin | Phân loại | Nguồn |
|---|---|---|---|
| 09:00 | Một hoạt động deploy đã diễn ra. | `[FACT: timeline do người dùng cung cấp]` | Mô tả sự cố |
| 09:12 | Error rate tăng. | `[FACT: timeline do người dùng cung cấp]` | Mô tả sự cố |
| 09:18 | Quá trình rollback bắt đầu. | `[FACT: timeline do người dùng cung cấp]` | Mô tả sự cố |
| 09:27 | Dịch vụ phục hồi. | `[FACT: timeline do người dùng cung cấp]` | Mô tả sự cố |
| Hiện tại | Nguyên nhân gốc chưa được xác định. | `[FACT: người dùng xác nhận]` | Mô tả sự cố |

## 2. Giả định cần giữ tách biệt

- `[ASSUMPTION]` Bản deploy lúc 09:00 có liên quan đến việc error rate tăng.
- `[ASSUMPTION]` Rollback là hành động làm dịch vụ phục hồi.
- `[ASSUMPTION]` Trạng thái rollback đã hoàn tất trước hoặc tại thời điểm 09:27.
- `[ASSUMPTION]` Error rate phản ánh lỗi mà người dùng thực sự gặp phải.
- `[ASSUMPTION]` Không có thay đổi hạ tầng, cấu hình, traffic hoặc dependency nào khác trong cùng khoảng thời gian.
- `[ASSUMPTION]` Tất cả timestamp sử dụng cùng timezone và đồng hồ đã được đồng bộ.
- `[ASSUMPTION]` “Dịch vụ phục hồi” đồng nghĩa với toàn bộ chỉ số kỹ thuật và trải nghiệm người dùng đã trở lại bình thường.

**Kết luận dữ kiện hiện tại:** Timeline cho thấy mối tương quan về thời gian giữa deploy, lỗi, rollback và phục hồi; nó chưa chứng minh quan hệ nhân quả.

## 3. Thông tin chưa biết

- Thành phần, phiên bản và phạm vi thay đổi của bản deploy.
- Endpoint, service, tenant hoặc khu vực bị ảnh hưởng.
- Mức error rate trước và sau sự cố.
- Loại lỗi: HTTP 5xx, timeout, application exception, database error hay dependency error.
- Số người dùng và giao dịch bị ảnh hưởng.
- Cảnh báo được kích hoạt lúc nào, bởi hệ thống hay con người.
- Ai phát hiện, ai quyết định rollback và thời điểm ra quyết định.
- Rollback hoàn tất lúc nào.
- Có thay đổi traffic, feature flag, cấu hình, schema hoặc dependency đồng thời hay không.
- Dịch vụ phục hồi do rollback, do dependency tự hồi phục hay do một hành động khác.
- Sau 09:27 còn lỗi tồn dư hoặc dữ liệu sai lệch hay không.

## 4. Ý kiến đang bị trình bày như dữ kiện

Hiện chưa có ý kiến trực tiếp nào từ người dùng. Các phát biểu sau, nếu xuất hiện trong cuộc họp, phải được coi là giả thuyết cho đến khi có bằng chứng:

- “Deploy chắc chắn gây ra sự cố.”
- “Rollback đã sửa lỗi.”
- “Monitoring phát hiện quá chậm.”
- “Nếu rollback sớm hơn thì tác động sẽ nhỏ hơn.”
- “Dịch vụ phục hồi hoàn toàn lúc 09:27.”

## 5. Dữ liệu cần thu thập

- `[NEED-DATA: Đối chiếu deployment manifest, commit SHA và CI/CD audit log]` Xác định chính xác phiên bản, thành phần, cấu hình và feature flag được thay đổi lúc 09:00.
- `[NEED-DATA: Trích xuất dashboard và raw metrics trong cửa sổ trước, trong và sau sự cố]` Xác định baseline, đỉnh error rate, latency, throughput và phạm vi ảnh hưởng.
- `[NEED-DATA: Truy vấn log theo request ID, error signature và phiên bản ứng dụng]` Xác định lỗi nào tăng và code path liên quan.
- `[NEED-DATA: Kiểm tra rollback event, rollout status và trạng thái pod/instance]` Xác định rollback hoàn tất lúc nào và phiên bản nào đang chạy khi dịch vụ phục hồi.
- `[NEED-DATA: Đối chiếu audit log của hạ tầng, cấu hình, feature flag và database]` Tìm các thay đổi đồng thời ngoài bản deploy.
- `[NEED-DATA: Kiểm tra metric và incident log của các dependency]` Loại trừ database, cache, queue, DNS và dịch vụ bên thứ ba.
- `[NEED-DATA: Phỏng vấn incident commander và on-call dựa trên timestamp]` Khôi phục chuỗi phát hiện, đánh giá và quyết định rollback.
- `[NEED-DATA: Kiểm tra dữ liệu nghiệp vụ và reconciliation report]` Xác định có giao dịch mất, trùng hoặc sai dữ liệu hay không.
- `[NEED-DATA: So sánh timestamp từ CI/CD, observability và orchestration trên cùng timezone]` Xác nhận timeline không bị sai lệch do đồng hồ hoặc timezone.

---

# Mũ đỏ — Cảm nhận chủ quan

Trực giác theo mẫu sự cố cho thấy bản deploy đáng được ưu tiên điều tra, nhưng mức độ chắc chắn còn thấp vì chưa có bằng chứng nhân quả.

---

# Mũ vàng — Những điểm tích cực

| Trọng tâm | Ngắn hạn | Trung hạn | Dài hạn |
|---|---|---|---|
| **Lợi ích** | Đội ngũ đã nhận biết bất thường, bắt đầu rollback và đưa dịch vụ về trạng thái phục hồi. | Timeline hiện có tạo điểm xuất phát rõ ràng cho việc đối chiếu log và metric. | Sự cố có thể trở thành cơ sở cải thiện cơ chế deploy, quan sát và ứng phó. |
| **Giá trị** | Giới hạn được thời gian ảnh hưởng thay vì để lỗi tiếp tục mà không có phản ứng. | Có thể chuẩn hóa tiêu chí rollback và vai trò chỉ huy sự cố. | Có thể giảm blast radius và thời gian phục hồi cho các sự cố tương tự. |
| **Tính khả thi** | Việc thu thập artifact và bảo toàn log có thể bắt đầu ngay. | Có thể diễn tập rollback và bổ sung automated checks sau khi hiểu failure mode. | Có thể tiến tới progressive delivery, canary và automated rollback dựa trên SLO. |

---

# Mũ đen — Rủi ro và điểm yếu

| Rủi ro | Cơ chế và bằng chứng hiện có | Khả năng / tác động | Điều làm rủi ro nặng hơn |
|---|---|---|---|
| Kết luận nhầm rằng deploy là nguyên nhân | Deploy xảy ra trước khi error rate tăng, nhưng đây mới là tương quan thời gian. Chưa có log hoặc deployment diff. | Khả năng: chưa xác định. Tác động: cao nếu sửa sai chỗ và bỏ sót nguyên nhân thật. | Không kiểm tra thay đổi đồng thời hoặc dependency. |
| Kết luận nhầm rằng rollback đã khắc phục lỗi | Rollback bắt đầu trước khi dịch vụ phục hồi, nhưng chưa biết lúc rollback hoàn tất. | Khả năng: chưa xác định. Tác động: trung bình–cao. | Dependency tự phục hồi đúng lúc hoặc có thao tác khác không được ghi nhận. |
| Mất bằng chứng trước khi hoàn tất RCA | Log có thể hết retention; pod hoặc instance cũ có thể đã bị hủy khi rollback. | Khả năng: trung bình theo cơ chế vận hành thông thường, nhưng chưa có dữ liệu hệ thống. Tác động: cao. | Trì hoãn thu thập artifact hoặc tiếp tục redeploy nhiều lần. |
| Phục hồi kỹ thuật nhưng còn lỗi dữ liệu | Error rate giảm không chứng minh giao dịch không bị mất, trùng hoặc ghi sai. | Khả năng: chưa xác định. Tác động: có thể cao. | Thiếu idempotency, reconciliation hoặc audit trail nghiệp vụ. |
| Phạm vi ảnh hưởng chưa được đánh giá | Chưa có dữ liệu về người dùng, endpoint, khu vực và giao dịch bị ảnh hưởng. | Khả năng: chắc chắn đang thiếu thông tin. Tác động: cao đối với truyền thông và SLA. | Chỉ xem metric tổng hợp, không phân tách theo dimension. |
| Áp dụng biện pháp phòng ngừa sai failure mode | Automated rollback hoặc canary không giải quyết được mọi nguyên nhân, đặc biệt lỗi schema hay dependency. | Khả năng: trung bình nếu triển khai trước RCA. Tác động: trung bình–cao. | Chọn giải pháp theo trực giác thay vì thử nghiệm tái hiện. |
| **Rủi ro của Option 0** | Không điều tra khiến nguyên nhân chưa biết tiếp tục tồn tại; cùng điều kiện có thể tái xuất hiện. | Khả năng: chưa xác định. Tác động: cao nếu lỗi lặp lại ở quy mô lớn hơn. | Redeploy cùng thay đổi hoặc giữ nguyên quy trình phát hành. |

---

# Mũ xanh lá — Các ý tưởng cải tiến

Không xếp hạng ở bước này:

1. Tạm đóng băng việc redeploy cùng phiên bản cho đến khi artifact và bằng chứng được bảo toàn.
2. Dựng lại phiên bản trước và sau deploy trong môi trường staging, phát lại traffic hoặc test case đại diện.
3. Chia deployment diff thành các nhóm: code, dependency, cấu hình, schema, feature flag và hạ tầng; kiểm chứng từng nhóm.
4. Thực hiện canary theo tỷ lệ traffic nhỏ và so sánh error budget giữa phiên bản cũ/mới.
5. Thiết lập automated rollback dựa trên nhiều tín hiệu: error rate, latency, saturation và business KPI.
6. Tách thay đổi có rủi ro cao bằng feature flag để có thể vô hiệu hóa mà không cần rollback toàn bộ.
7. Lưu tự động “incident evidence bundle” khi cảnh báo nghiêm trọng xảy ra: manifest, commit, logs, metrics và audit events.
8. Bổ sung deployment marker thống nhất trên dashboard của ứng dụng, hạ tầng và dependency.
9. Chuẩn hóa runbook với điều kiện rollback, người có quyền quyết định và kênh phối hợp.
10. Thực hiện game day: mô phỏng error rate tăng sau deploy và đo toàn bộ quá trình phát hiện–quyết định–khôi phục.
11. **Ý tưởng phi truyền thống:** dùng “shadow deployment” để chạy phiên bản mới trên bản sao traffic thực mà không trả kết quả cho người dùng.
12. Nếu không thể tìm ra nguyên nhân xác định, lập fault tree và thiết kế biện pháp kiểm soát cho từng nhóm nguyên nhân có thể xảy ra.

---

# Mũ xanh lam — Kết luận và hành động

## Khuyến nghị

Chọn **Phương án 2: điều tra nguyên nhân gốc đồng thời triển khai biện pháp giảm thiểu có thể đảo ngược**.

Chưa đủ bằng chứng để kết luận deploy là nguyên nhân gốc hoặc rollback là nguyên nhân trực tiếp làm dịch vụ phục hồi. RCA phải được coi là **đang bị chặn bởi các mục `[NEED-DATA: …]` ở Mũ trắng**.

Không nên đóng sự cố chỉ với kết luận “rollback thành công”. Kết luận cuối cần phân biệt:

- **Trigger:** sự kiện kích hoạt lỗi.
- **Root cause:** cơ chế kỹ thuật tạo ra lỗi.
- **Contributing factors:** yếu tố làm tăng phạm vi hoặc kéo dài ảnh hưởng.
- **Detection gap:** vì sao lỗi không được phát hiện sớm hơn.
- **Recovery mechanism:** hành động nào thực sự dẫn đến phục hồi.

## Điều kiện đảo chiều

Khuyến nghị sẽ thay đổi nếu:

- Bằng chứng cho thấy deploy không liên quan; trọng tâm RCA chuyển sang dependency, traffic, hạ tầng hoặc cấu hình.
- Không còn đủ log/artifact để xác định nguyên nhân; chuyển từ RCA xác định sang fault-tree analysis và phòng ngừa theo nhóm failure mode.
- Kiểm tra cho thấy có lỗi toàn vẹn dữ liệu; ưu tiên reconciliation và khắc phục dữ liệu trước cải tiến quy trình deploy.
- Cùng failure mode có thể tái diễn ngay; ưu tiên vô hiệu hóa tính năng hoặc khóa phát hành trước khi hoàn tất báo cáo RCA.

## Kế hoạch hành động

| Bước | Hành động | Chủ trì | Mốc / thời hạn | Tiêu chí hoàn thành |
|---|---|---|---|---|
| 1 | Bảo toàn log, metric, deployment manifest, commit SHA, audit log và incident chat. | Incident Commander + SRE | Ngay sau retrospective | Evidence bundle được lưu ở nơi dùng chung, có timestamp và quyền truy cập phù hợp. |
| 2 | Xác nhận timeline trên cùng timezone, gồm lúc deploy hoàn tất, alert kích hoạt, rollback được quyết định, rollback hoàn tất và phục hồi. | SRE | Trong 1 ngày làm việc | Timeline có nguồn chứng minh cho từng mốc; assumptions được đánh dấu riêng. |
| 3 | Đo phạm vi ảnh hưởng kỹ thuật và nghiệp vụ. | SRE + Product/Business Ops | Trong 1 ngày làm việc | Có số liệu theo service/endpoint/tenant và kết quả kiểm tra dữ liệu nghiệp vụ. |
| 4 | Phân tích deployment diff và các thay đổi đồng thời. | Tech Lead + Release Engineer | Trong 2 ngày làm việc | Có danh sách giả thuyết, bằng chứng ủng hộ/phản bác và owner kiểm chứng từng giả thuyết. |
| 5 | Tái hiện hoặc kiểm chứng failure mechanism trong môi trường an toàn. | Nhóm phát triển + QA/SRE | Trong 3 ngày làm việc | Ít nhất một giả thuyết được tái hiện; nếu không, có fault tree và lý do loại trừ từng nhánh. |
| 6 | Xác định root cause và contributing factors. | Incident Commander + Tech Lead | Sau khi hoàn tất bước 5 | Kết luận giải thích đầy đủ trigger → lỗi → tác động → phục hồi và liên kết tới bằng chứng. |
| 7 | Triển khai biện pháp khắc phục và phòng ngừa. | Engineering Owner + SRE | Theo RCA, có lịch riêng | Có test, monitoring, runbook và phương án rollback cho từng thay đổi. |
| 8 | Kiểm chứng bằng game day hoặc canary có kiểm soát. | SRE + Release Engineering | Trước lần phát hành lại | Hệ thống phát hiện đúng tín hiệu, quy trình rollback chạy được và không gây lỗi dữ liệu. |
| 9 | Đóng incident review. | Incident Commander | Sau bước 8 | Mọi action item có owner, deadline; bằng chứng và quyết định được ghi trong postmortem không đổ lỗi. |

## Câu hỏi còn mở

1. Bản deploy thay đổi chính xác những gì?
2. Error rate tăng ở loại lỗi và thành phần nào?
3. Alert xuất hiện lúc nào, và tại sao phản ứng bắt đầu ở thời điểm đó?
4. Rollback hoàn tất lúc nào?
5. Tín hiệu nào xác nhận dịch vụ đã phục hồi?
6. Có thay đổi hoặc sự cố dependency nào xảy ra đồng thời không?
7. Có ảnh hưởng đến dữ liệu nghiệp vụ hay không?
8. Có thể tái hiện lỗi bằng phiên bản đã deploy không?
9. Guardrail nào có thể phát hiện hoặc giới hạn cùng failure mode trong lần phát hành tiếp theo?
