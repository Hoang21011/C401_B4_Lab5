# SPEC — AI Product Hackathon

**Nhóm:** C401_B4

**Track:** [x] VinFast · [ ] Vinmec · [ ] VinUni-VinSchool · [ ] XanhSM · [ ] Open

**Problem statement (1 câu):** Người dùng mô tả lỗi mơ hồ: “xe rung”, “kêu lạ”, “hao xăng”, không biết cách liên hệ với thợ, cứu hộ trong trường hợp khẩn cấp, AI giúp người dùng liên hệ với các thợ sửa xe và cứu hộ available ở gần user nhất.

---

## 1. AI Product Canvas

|             | Value                                                                                   | Trust                                                                       | Feasibility                                                      |
| ----------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Câu hỏi** | User nào? Pain gì? AI giải gì?                                                          | Khi AI sai thì sao? User sửa bằng cách nào?                                 | Cost/latency bao nhiêu? Risk chính?                              |
| **Trả lời** | _Nhân viên văn phòng mất 30 phút/ngày phân loại email — AI gợi ý nhãn, giảm còn 5 phút_ | _AI gắn sai nhãn → user thấy ngay, sửa 1 click, hệ thống học từ correction_ | _~$0.01/email, latency <2s, risk: hallucinate nội dung nhạy cảm_ |

**Automation hay augmentation?** ☐ Automation · ☐ Augmentation
Justify: _Augmentation — user thấy gợi ý và chấp nhận/từ chối, cost of reject = 0_

**Learning signal:**

1. User correction đi vào đâu? \_\_\_
2. Product thu signal gì để biết tốt lên hay tệ đi? \_\_\_
3. Data thuộc loại nào? ☐ User-specific · ☐ Domain-specific · ☐ Real-time · ☐ Human-judgment · ☐ Khác: **_
   Có marginal value không? (Model đã biết cái này chưa?) _**

---

## 2. User Stories — 4 paths

### **Feature 1: Chẩn đoán lỗi qua âm thanh và mô tả**

**Trigger:** User nhập mô tả mơ hồ hoặc gửi đoạn ghi âm tiếng "kêu lạ" → AI phân tích và trả kết quả chẩn đoán sơ bộ.

| Path                               | Câu hỏi thiết kế                                           | Mô tả                                                                                                                                                                                      |
| ---------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Happy — AI đúng, tự tin**        | User thấy gì? Flow kết thúc ra sao?                        | Hiển thị 1 kết quả duy nhất kèm độ nguy hiểm (Ví dụ: "85% Lỏng dây curoa - Cần thay sớm"). User bấm "Đặt lịch" hoặc "Xem giá tham khảo".                                                   |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | Chatbot phản hồi: "Có 2 khả năng xảy ra: Lỗi A (60%) hoặc Lỗi B (40%)". AI yêu cầu user làm thêm 1 hành động để thu hẹp kết quả.                                                           |
| **Failure — AI sai**               | User biết AI sai bằng cách nào? Recover ra sao?            | User thấy chẩn đoán không khớp (Ví dụ: AI báo lỗi động cơ nhưng xe vẫn rung khi tắt máy). User bảo "Không phải lỗi này" → Hệ thống chuyển hướng sang bộ câu hỏi loại trừ hoặc kết nối thợ. |
| **Correction — user sửa**          | User sửa bằng cách nào? Data đó đi vào đâu?                | User chọn vùng lỗi đúng trên sơ đồ xe 3D hoặc nhập kết luận từ thợ sau khi đi sửa về → Lưu vào **Correction Log** kèm file âm thanh gốc để re-train model.                                 |

---

### **Feature 2: Tra cứu Benchmark giá sửa chữa**

**Trigger:** Sau khi xác định lỗi → AI truy xuất cơ sở dữ liệu thị trường → Đưa ra khoảng giá dự kiến.

| Path                               | Câu hỏi thiết kế                                           | Mô tả                                                                                                                                                         |
| ---------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Happy — AI đúng, tự tin**        | User thấy gì? Flow kết thúc ra sao?                        | Hiển thị bảng giá chi tiết (Phụ tùng + Công thợ) dựa trên khu vực của user. User thấy minh bạch, chọn "Ghé gara gần nhất".                                    |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI báo: "Giá phụ tùng này đang biến động". Hiển thị khoảng giá rộng (Ví dụ: 1.2tr - 2tr) kèm danh sách 3 gara có báo giá thực tế gần nhất để user tự so sánh. |
| **Failure — AI sai**               | User biết AI sai bằng cách nào? Recover ra sao?            | User ra gara và nhận báo giá lệch quá nhiều (>30%) so với AI → User chụp ảnh hóa đơn gửi vào chat để "khiếu nại" hoặc cập nhật thông tin.                     |
| **Correction — user sửa**          | User sửa bằng cách nào? Data đó đi vào đâu?                | User nhập số tiền thực tế đã chi trả → Dữ liệu đi vào **Market Price Database** để cập nhật benchmark real-time cho các user khác cùng khu vực.               |

---

### **Feature 3: Điều phối Cứu hộ & Kết nối thợ khẩn cấp (Emergency Assistance)**

**Trigger:** User gửi tin nhắn có từ khóa khẩn cấp ("xe chết máy giữa đường", "nổ lốp", "mất phanh") hoặc kết quả chẩn đoán ở Feature 1 xác định lỗi nguy hiểm không thể tiếp tục di chuyển.

| Path                               | Câu hỏi thiết kế                                           | Mô tả                                                                                                                                                                                                   |
| ---------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Happy — AI đúng, tự tin**        | User thấy gì? Flow kết thúc ra sao?                        | AI xác định đúng loại hình cần thiết. Hiển thị danh sách thợ/cứu hộ gần nhất đang sẵn sàng. User bấm "Gọi ngay", dòng trạng thái cứu hộ hiện ra.                                                        |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI không rõ xe có thể nổ máy lại được không. AI hỏi: "Xe có lên điện/đèn không?". Nếu user trả lời "Không", AI tự động đề xuất Cứu hộ kéo xe thay vì chỉ thợ sửa lưu động.                              |
| **Failure — AI sai**               | User biết AI sai bằng cách nào? Recover ra sao?            | AI điều thợ sửa lốp nhưng thực tế xe bị hỏng thước lái (cần xe kéo). User thấy thợ đến nhưng không giải quyết được → User nhấn nút "Thay đổi phương án: Cần xe kéo" ngay trong giao diện đang theo dõi. |
| **Correction — user sửa**          | User sửa bằng cách nào? Data đó đi vào đâu?                | User chọn lý do hủy/đổi dịch vụ (VD: "Lỗi nặng hơn chẩn đoán ban đầu"). Data đi vào **Incident Log** và **Service Matching Model** để AI học cách phân loại mức độ nghiêm trọng chính xác hơn.          |

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

| Metric                                         | Threshold | Red flag (dừng khi) |
| ---------------------------------------------- | --------- | ------------------- |
| Diagnosis Recall (Top-3)                       | ≥ 80%     | < 65% trong 1 tuần  |
| Urgency Classification Recall (Critical cases) | ≥ 90%     | < 75%               |
| Time to First Action (reduction)               | ≥ 50%     | < 25%               |
| Cost Estimation Error                          | ≤ 25%     | > 40%               |
| Contact Success Rate (Emergency)               | ≥ 90%     | < 70%               |

---

## 4. Top 3 failure modes

| #   | Trigger                                                                                                                        | Hậu quả                                                                                                               | Mitigation                                                                                                                         |
| --- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AI hiểu sai ngữ cảnh do ngôn ngữ tự nhiên (vd: user nói “hao xăng” nhưng thực ra do thói quen lái xe, không phải lỗi kỹ thuật) | AI vẫn đưa ra chẩn đoán “có vẻ hợp lý” → user tin nhưng thực tế không có lỗi → sửa chữa không cần thiết (waste money) | Clarify intent bằng câu hỏi phân biệt (behavior vs mechanical); dùng decision tree để tách “usage issue” vs “technical issue”      |
| 2   | Data cost estimation không đủ hoặc bias theo khu vực/loại xe                                                                   | AI đưa ra giá sai lệch lớn → user mất trust hoặc nghĩ gara “vẽ bệnh”                                                  | Trả về **price range + confidence level**; show nguồn dữ liệu; cho phép feedback loop từ user                                      |
| 3   | AI bỏ sót lỗi critical (false negative), phân loại nhầm thành “minor”                                                          | User tiếp tục sử dụng xe → có thể gây hỏng nghiêm trọng hoặc mất an toàn                                              | Rule-based safety layer (hard constraints); nếu có pattern nguy hiểm → auto escalate “Critical”; luôn khuyến nghị kiểm tra thực tế |

---

## 5. ROI 3 kịch bản

|                | Conservative                  | Realistic                     | Optimistic                     |
| -------------- | ----------------------------- | ----------------------------- | ------------------------------ |
| **Assumption** | _100 user/ngày, 60% hài lòng_ | _500 user/ngày, 80% hài lòng_ | _2000 user/ngày, 90% hài lòng_ |
| **Cost**       | _$50/ngày inference_          | _$200/ngày_                   | _$500/ngày_                    |
| **Benefit**    | _Giảm 2h support/ngày_        | _Giảm 8h/ngày_                | _Giảm 20h, tăng retention 5%_  |
| **Net**        |                               |                               |                                |

**Kill criteria:** _Khi nào nên dừng? VD: cost > benefit 2 tháng liên tục_

---

## 6. Mini AI spec (1 trang)

_Tóm tắt tự do — viết bằng ngôn ngữ tự nhiên, không format bắt buộc._
_Gom lại: product giải gì, cho ai, AI làm gì (auto/aug), quality thế nào (precision/recall), risk chính, data flywheel ra sao._
