# SPEC — AI Product Hackathon

**Nhóm:** C401_B4

**Track:** ☑ VinFast · ☐ Vinmec · ☐ VinUni-VinSchool · ☐ XanhSM · ☐ Open

**Problem statement (1 câu):** Người dùng mô tả lỗi mơ hồ: “xe rung”, “kêu lạ”, không biết cách liên hệ với thợ, cứu hộ trong trường hợp khẩn cấp, AI giúp người dùng liên hệ với các thợ sửa xe và cứu hộ available ở gần user nhất. 

---

## 1. AI Product Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi** | User nào? Pain gì? AI giải gì? | Khi AI sai thì sao? User sửa bằng cách nào? | Cost/latency bao nhiêu? Risk chính? |
| **Trả lời** |User: Chủ xe (xe máy/ô tô) - khách hàng của VinFast không có kiến thức kỹ thuật, về thông tin về bảo dưỡng và cần cứu hộ.|Recall cao: Ưu tiên đưa nhiều khả năng để không bỏ sót lỗi nghiêm trọng |Cost: ~0.01-0.03/lượt (LLM) + Chi phí API (nếu có - trong trường hợp cần liên hệ với thợ) |
||Pain: User không biết về kỹ thuật, mô tả lỗi mơ hồ, phải ra gara mới biết nguyên nhân, mất thời gian & chi phí, thiếu minh bạch về giá, lo bị "vẽ bệnh"|Khi sai: Có thể do đề xuất nguyên nhân chưa chính xác, hoặc cập nhật sai thời gian khả dụng của thợ sửa chữa/cứu hộ.|Latency: 2-5 giây|
||Aug: Nhận mô tả từ khách hàng -> hỏi follow up -> suy luận 3-5 nguyên nhân + hướng xử lý (tự check / check gara / cảnh báo cho khách) -> xử lý theo hướng phù hợp (giúp khách đặt lịch sửa chữa / cứu hộ với gara)|Recovery: Hiển thị nhiều phương án  + khuyến nghị kiểm tra lại + đề xuất liên hệ trực tiếp với gara. |Risk: Chuẩn đoán sai do input mơ hồ; estimate giá lệch; review gara bị bias|
||Value: Hỗ trợ 24/7, tiết kiệm thời gian, hỗ trợ khách hàng nhanh chóng||Dep: Database lỗi xe + thông tin gara/thợ + giá sửa chữa + API mapping gara|

**Automation hay augmentation?** ☐ Automation · ☑ Augmentation
<br>Justify: *Augmentation — AI chỉ gợi ý nguyên nhân, hướng xử lý và chi phí, hỗ trợ người dùng liên hệ / đặt lịch với gara nếu có nhu cầu; người dùng là người ra quyết định cuối cùng, đặc biệt trong các tình huống có rủi ro kỹ thuật cao*

**Learning signal:**

| # | Câu hỏi | Trả lời |
|---|---------|---------|
|1| User correction đi vào đâu?| Log các hành vi: user chọn nguyên nhân khác, bỏ qua đề xuất, thay đổi triệu chứng mô tả → đưa vào hệ thống để cải thiện thứ tự nguyên nhân và độ chính xác gợi ý|
|2| Product thu signal gì để biết tốt lên hay tệ đi?| - Tỷ lệ user chọn 1 trong các nguyên nhân đề xuất (accept rate) <br> - Tỷ lệ user phải hỏi lại / mô tả lại (re-query rate) <br> - Tỷ lệ chuyển sang gara (conversion to action) <br> - Tỷ lệ user abandon giữa chừng (drop-off rate) <br> - Feedback sau sửa chữa (đúng bệnh hay không) 
|3| Data thuộc loại nào?| ☑ User-specific · ☑ Domain-specific · ☑ Real-time · ☑ Human-judgment · ☑ Khác: Behavioral data|

Có marginal value không? (Model đã biết cái này chưa?) <br> Có. Dữ liệu mang marginal value cao vì phản ánh hành vi thực tế của người dùng trong việc mô tả triệu chứng, lựa chọn nguyên nhân và kết quả sửa chữa. Đây là dữ liệu không có sẵn trong model và khó thu thập từ nguồn công khai, giúp cải thiện đáng kể khả năng chẩn đoán và ranking theo ngữ cảnh thực tế.

## 2. User Stories — 4 paths

### **Feature 1: Chẩn đoán lỗi qua mô tả**

**Trigger:** User nhập mô tả mơ hồ → AI phân tích và trả kết quả chẩn đoán sơ bộ.

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy — AI đúng, tự tin** | User thấy gì? Flow kết thúc ra sao? | Hiển thị 1 kết quả duy nhất kèm độ nguy hiểm (Ví dụ: "85% Lỏng dây curoa - Cần thay sớm"). User bấm "Đặt lịch" hoặc "Xem giá tham khảo". |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | Chatbot phản hồi: "Có 2 khả năng xảy ra: Lỗi A (60%) hoặc Lỗi B (40%)". AI yêu cầu user làm thêm 1 hành động để thu hẹp kết quả. |
| **Failure — AI sai** | User biết AI sai bằng cách nào? Recover ra sao? | User thấy chẩn đoán không khớp (Ví dụ: AI báo lỗi động cơ nhưng xe vẫn rung khi tắt máy). User bảo "Không phải lỗi này" → Hệ thống chuyển hướng sang bộ câu hỏi loại trừ hoặc kết nối thợ. |
| **Correction — user sửa** | User sửa bằng cách nào? Data đó đi vào đâu? | User chọn vùng lỗi đúng trên sơ đồ xe 3D hoặc nhập kết luận từ thợ sau khi đi sửa về → Lưu vào **Correction Log** kèm file âm thanh gốc để re-train model. |

---

### **Feature 2: Điều phối Cứu hộ & Kết nối thợ khẩn cấp (Emergency Assistance)**

**Trigger:** User gửi tin nhắn có từ khóa khẩn cấp ("xe chết máy giữa đường", "nổ lốp", "mất phanh") hoặc kết quả chẩn đoán ở Feature 1 xác định lỗi nguy hiểm không thể tiếp tục di chuyển.

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy — AI đúng, tự tin** | User thấy gì? Flow kết thúc ra sao? | AI xác định đúng loại hình cần thiết. Hiển thị danh sách thợ/cứu hộ gần nhất đang sẵn sàng. User bấm "Gọi ngay", dòng trạng thái cứu hộ hiện ra. |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI không rõ xe có thể nổ máy lại được không. AI hỏi: "Xe có lên điện/đèn không?". Nếu user trả lời "Không", AI tự động đề xuất Cứu hộ kéo xe thay vì chỉ thợ sửa lưu động. |
| **Failure — AI sai** | User biết AI sai bằng cách nào? Recover ra sao? | AI điều thợ sửa lốp nhưng thực tế xe bị hỏng thước lái (cần xe kéo). User thấy thợ đến nhưng không giải quyết được → User nhấn nút "Thay đổi phương án: Cần xe kéo" ngay trong giao diện đang theo dõi. |
| **Correction — user sửa** | User sửa bằng cách nào? Data đó đi vào đâu? | User chọn lý do hủy/đổi dịch vụ (VD: "Lỗi nặng hơn chẩn đoán ban đầu"). Data đi vào **Incident Log** và **Service Matching Model** để AI học cách phân loại mức độ nghiêm trọng chính xác hơn. |

---

## 3. Eval metrics + threshold

## Optimize precision hay recall?
☐ Precision · ☑ Recall  

**Tại sao?**  
Bài toán này ưu tiên **không bỏ sót các trường hợp cần xử lý (đặc biệt là lỗi nghiêm trọng)**. Nếu AI fail ở recall (không nhận ra lỗi cần sửa ngay), hậu quả trực tiếp là user **không hành động khi cần**, gây rủi ro cao hơn nhiều so với việc “báo động dư”.

**Nếu chọn ngược lại (precision cao, recall thấp):**  
→ Hệ thống chỉ trả lời khi rất chắc chắn  
→ Bỏ sót nhiều case thực tế  
→ User bị “false safe” (tưởng không sao nhưng thực ra có vấn đề)  
→ Mất trust nhanh chóng, đặc biệt với lỗi nghiêm trọng  

---

## Core Metrics

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| Diagnosis Recall (Top-3) | ≥ 80% | < 65% trong 1 tuần |
| Urgency Classification Recall (Critical cases) | ≥ 90% | < 75% |
| Time to First Action (reduction) | ≥ 50% | < 25% |
| Cost Estimation Error | ≤ 25% | > 40% |
| Contact Success Rate (Emergency) | ≥ 90% | < 70% |

---

## 4. Top 3 failure modes

Liệt kê các cách product có thể fail — tập trung vào những lỗi nguy hiểm, đặc biệt là khi **user không nhận ra hệ thống đang sai**.

| #   | Trigger                                                                                                                        | Hậu quả                                                                                                               | Mitigation                                                                                                                         |
| --- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1   |  AI tự động gọi cứu hộ (automation) nhưng user không thực sự cần hoặc nhập sai vị trí | Gọi nhầm cứu hộ, sai địa điểm → delay xử lý thật, user không nhận ra lỗi ngay | Xác nhận lại trước khi call ("Bạn có chắc cần cứu hộ khẩn cấp không?") + hiển thị location + nút cancel/undo      |
| 2   | Data trạng thái thợ không real-time (thợ đã bận nhưng hệ thống vẫn hiển thị available) | AI điều phối thợ không đến → user bị bỏ rơi, đặc biệt nguy hiểm trong tình huống khẩn cấp                        | Sync trạng thái real-time (WebSocket/Firebase), TTL cho availability, fallback gọi nhiều thợ cùng lúc          |
| 3   | AI bỏ sót lỗi critical (false negative), phân loại nhầm thành “low”                                                          | User tiếp tục sử dụng xe → có thể gây hỏng nghiêm trọng hoặc mất an toàn                                              | Rule-based safety layer (hard constraints); nếu có pattern nguy hiểm → auto escalate “Critical”; luôn khuyến nghị kiểm tra thực tế |

---

## 5. ROI 3 kịch bản

|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | *100 user/ngày, 50% sử dụng feature chẩn đoán* | *500 user/ngày, 70% sử dụng, retention tăng nhẹ* | *2000 user/ngày, 85% sử dụng, retention cao* |
| **Cost** | *$40/ngày (LLM + inference + server)* | *$150/ngày* | *$400/ngày* |
| **Benefit** | *Giảm 1–2h support thủ công/ngày, user tiết kiệm thời gian đi gara (~$200 value/ngày)* | *Giảm 6–8h support/ngày, tăng conversion dịch vụ sửa chữa (~$800 value/ngày)* | *Giảm 20h support, tăng mạnh booking dịch vụ + retention (~$3000 value/ngày)* |
| **Net** | *+$160/ngày* | *+$650/ngày* | *+$2600/ngày* |

**Kill criteria:**  
*Dừng nếu cost > benefit trong 2 tháng liên tục hoặc accuracy chẩn đoán <70% gây mất trust user*

---

## 6. Mini AI spec (1 trang)

**Product này giải gì, cho ai?**
Đây là một AI assistant dành cho **chủ xe (xe máy/ô tô, đặc biệt là user VinFast)** không có kiến thức kỹ thuật. Vấn đề chính là user mô tả lỗi mơ hồ (“xe rung”, “kêu lạ”), không biết mức độ nghiêm trọng, không biết giá sửa chữa hợp lý, và gặp khó khăn khi cần liên hệ thợ/cứu hộ. Product giúp **rút ngắn thời gian từ “có vấn đề” → “hành động đúng”**.


---

<img width="981" height="801" alt="image" src="https://github.com/user-attachments/assets/c55493e8-d808-4465-ad2d-08f4700b33a1" />



**AI làm gì (automation vs augmentation)?**
Hệ thống theo hướng **augmentation**:

* Nhận input: text mô tả
* Hỏi follow-up để làm rõ triệu chứng
* Suy luận:

  * Top 3–5 nguyên nhân có khả năng nhất
  * Mức độ nguy hiểm (critical / non-critical)
  * Hướng xử lý (tự check / đi gara / gọi cứu hộ)
* Truy xuất:

  * Giá sửa chữa tham khảo theo khu vực
  * Danh sách gara/thợ gần nhất (real-time availability)
* Hỗ trợ hành động:

  * Đặt lịch sửa chữa
  * Gọi cứu hộ

AI **không tự quyết định thay user**, mà đóng vai trò “copilot” giúp user ra quyết định nhanh và đúng hơn.

---

**Quality: tối ưu precision hay recall?**
Hệ thống tối ưu **recall**, đặc biệt với lỗi nghiêm trọng:

* Luôn đưa ra nhiều khả năng thay vì 1 kết luận duy nhất nếu chưa chắc chắn
* Ưu tiên **không bỏ sót lỗi nguy hiểm (false negative)** hơn là tránh cảnh báo dư
* Có lớp **rule-based safety** để override model khi phát hiện pattern nguy hiểm

Target:

* Diagnosis Recall (Top-3): ≥ 80%
* Urgency Recall (Critical): ≥ 90%

---

**System flow (end-to-end)**

1. User nhập mô tả
2. LLM:
   
   * Parse intent
   * Detect symptom entities
4. Clarification loop (nếu cần)
5. Diagnosis engine:

   * Hybrid: LLM reasoning + rule-based + knowledge base
6. Output:

   * Nguyên nhân (ranked)
   * Mức độ nguy hiểm
   * Hành động đề xuất
7. Retrieval:

   * Giá sửa chữa (market DB)
   * Gara/thợ (geo + availability API)
8. Action layer:

   * Booking / emergency dispatch

---

**Risk chính & cách giảm thiểu**

1. **Chẩn đoán sai do input mơ hồ**

   * Mitigation: hỏi follow-up có cấu trúc + hiển thị nhiều khả năng + confidence score

2. **Bỏ sót lỗi nguy hiểm (critical false negative)**

   * Mitigation: safety rules + keyword trigger (“mất phanh”, “xe chết máy giữa đường”) → auto escalate

3. **Sai lệch giá sửa chữa → mất trust**

   * Mitigation: hiển thị price range + confidence + nguồn data + user feedback loop

4. **Matching thợ/cứu hộ không chính xác**

   * Mitigation: real-time availability + fallback option + cho phép đổi phương án ngay trong flow

---

**Data & flywheel (lõi cải thiện theo thời gian)**

Hệ thống tạo **data flywheel mạnh** từ hành vi thực tế:

* Input data:

  * Mô tả lỗi (text)
  * Context (loại xe, khu vực, thời gian)

* Behavioral signals:

  * User chọn nguyên nhân nào
  * User có hỏi lại / bỏ qua không
  * Có chuyển sang gara/cứu hộ không

* Ground truth:

  * Kết luận từ thợ
  * Chi phí thực tế
  * Feedback sau sửa chữa

→ Loop:

* Update ranking model (nguyên nhân nào đúng hơn theo context)
* Update cost database (giá thị trường real-time)
* Improve urgency classifier
* Improve service matching

=> Theo thời gian, system chuyển từ “generic reasoning” → “context-aware + market-aware AI”

---

**Why this wins**

* Dữ liệu hành vi + kết quả sửa chữa thực tế (khó crawl/public)
* Kết hợp **diagnosis + pricing + action** (end-to-end, không chỉ chatbot)
* Real-time layer (gara/thợ availability)
* Safety-aware AI (quan trọng trong domain physical risk)

---


Phân công:
* Nguyen Thi Thuy Trang: Part 1. 
* Trinh Uyen Chi: Part 2. 
* Tran Viet Phuong: Part 3.
* Pham Nguyen Tien Manh: Part 4. 
* Nguyen Hoang Nghia: Part 5. 
* Nguyen Ngoc Tan: Part 6. 
* Le Duc Anh: Part 6. 
