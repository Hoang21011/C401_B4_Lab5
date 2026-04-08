# SPEC — AI Product Hackathon

**Nhóm:** C401_B4
**Track:** [x] VinFast · [ ] Vinmec · [ ] VinUni-VinSchool · [ ] XanhSM · [ ] Open
**Problem statement (1 câu):** Người dùng mô tả lỗi mơ hồ: “xe rung”, “kêu lạ”, “hao xăng”, không biết cách liên hệ với thợ, cứu hộ trong trường hợp khẩn cấp. Không có hệ thống theo dõi lịch bảo dưỡng, AI giúp người dùng liên hệ với các thợ sửa xe và cứu hộ available ở gần user nhất. 

---

## 1. AI Product Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi** | User nào? Pain gì? AI giải gì? | Khi AI sai thì sao? User sửa bằng cách nào? | Cost/latency bao nhiêu? Risk chính? |
| **Trả lời** | *Nhân viên văn phòng mất 30 phút/ngày phân loại email — AI gợi ý nhãn, giảm còn 5 phút* | *AI gắn sai nhãn → user thấy ngay, sửa 1 click, hệ thống học từ correction* | *~$0.01/email, latency <2s, risk: hallucinate nội dung nhạy cảm* |

**Automation hay augmentation?** ☐ Automation · ☐ Augmentation
Justify: *Augmentation — user thấy gợi ý và chấp nhận/từ chối, cost of reject = 0*

**Learning signal:**

1. User correction đi vào đâu? ___
2. Product thu signal gì để biết tốt lên hay tệ đi? ___
3. Data thuộc loại nào? ☐ User-specific · ☐ Domain-specific · ☐ Real-time · ☐ Human-judgment · ☐ Khác: ___
   Có marginal value không? (Model đã biết cái này chưa?) ___

---

## 2. User Stories — 4 paths

Mỗi feature chính = 1 bảng. AI trả lời xong → chuyện gì xảy ra?

### Feature: *tên feature*

### **Feature 1: Chẩn đoán lỗi qua âm thanh và mô tả**

**Trigger:** User nhập mô tả mơ hồ hoặc gửi đoạn ghi âm tiếng "kêu lạ" → AI phân tích và trả kết quả chẩn đoán sơ bộ.

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy — AI đúng, tự tin** | User thấy gì? Flow kết thúc ra sao? | Hiển thị 1 kết quả duy nhất kèm độ nguy hiểm (Ví dụ: "85% Lỏng dây curoa - Cần thay sớm"). User bấm "Đặt lịch" hoặc "Xem giá tham khảo". |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | Chatbot phản hồi: "Có 2 khả năng xảy ra: Lỗi A (60%) hoặc Lỗi B (40%)". AI yêu cầu user làm thêm 1 hành động để thu hẹp kết quả. |
| **Failure — AI sai** | User biết AI sai bằng cách nào? Recover ra sao? | User thấy chẩn đoán không khớp (Ví dụ: AI báo lỗi động cơ nhưng xe vẫn rung khi tắt máy). User bảo "Không phải lỗi này" → Hệ thống chuyển hướng sang bộ câu hỏi loại trừ hoặc kết nối thợ. |
| **Correction — user sửa** | User sửa bằng cách nào? Data đó đi vào đâu? | User chọn vùng lỗi đúng trên sơ đồ xe 3D hoặc nhập kết luận từ thợ sau khi đi sửa về → Lưu vào **Correction Log** kèm file âm thanh gốc để re-train model. |

---

### **Feature 2: Tra cứu Benchmark giá sửa chữa**

**Trigger:** Sau khi xác định lỗi → AI truy xuất cơ sở dữ liệu thị trường → Đưa ra khoảng giá dự kiến.

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy — AI đúng, tự tin** | User thấy gì? Flow kết thúc ra sao? | Hiển thị bảng giá chi tiết (Phụ tùng + Công thợ) dựa trên khu vực của user. User thấy minh bạch, chọn "Ghé gara gần nhất". |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI báo: "Giá phụ tùng này đang biến động". Hiển thị khoảng giá rộng (Ví dụ: 1.2tr - 2tr) kèm danh sách 3 gara có báo giá thực tế gần nhất để user tự so sánh. |
| **Failure — AI sai** | User biết AI sai bằng cách nào? Recover ra sao? | User ra gara và nhận báo giá lệch quá nhiều (>30%) so với AI → User chụp ảnh hóa đơn gửi vào chat để "khiếu nại" hoặc cập nhật thông tin. |
| **Correction — user sửa** | User sửa bằng cách nào? Data đó đi vào đâu? | User nhập số tiền thực tế đã chi trả → Dữ liệu đi vào **Market Price Database** để cập nhật benchmark real-time cho các user khác cùng khu vực. |

---

### **Feature 3: Điều phối Cứu hộ & Kết nối thợ khẩn cấp (Emergency Assistance)**

**Trigger:** User gửi tin nhắn có từ khóa khẩn cấp ("xe chết máy giữa đường", "nổ lốp", "mất phanh") hoặc kết quả chẩn đoán ở Feature 1 xác định lỗi nguy hiểm không thể tiếp tục di chuyển.

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy — AI đúng, tự tin** | User thấy gì? Flow kết thúc ra sao? | AI xác định đúng loại hình cần thiết. Hiển thị danh sách thợ/cứu hộ gần nhất đang sẵn sàng. User bấm "Gọi ngay", dòng trạng thái cứu hộ hiện ra. |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI không rõ xe có thể nổ máy lại được không. AI hỏi: "Xe có lên điện/đèn không?". Nếu user trả lời "Không", AI tự động đề xuất Cứu hộ kéo xe thay vì chỉ thợ sửa lưu động. |
| **Failure — AI sai** | User biết AI sai bằng cách nào? Recover ra sao? | AI điều thợ sửa lốp nhưng thực tế xe bị hỏng thước lái (cần xe kéo). User thấy thợ đến nhưng không giải quyết được → User nhấn nút "Thay đổi phương án: Cần xe kéo" ngay trong giao diện đang theo dõi. |
| **Correction — user sửa** | User sửa bằng cách nào? Data đó đi vào đâu? | User chọn lý do hủy/đổi dịch vụ (VD: "Lỗi nặng hơn chẩn đoán ban đầu"). Data đi vào **Incident Log** và **Service Matching Model** để AI học cách phân loại mức độ nghiêm trọng chính xác hơn. |

---

## 3. Eval metrics + threshold

**Optimize precision hay recall?** ☐ Precision · ☐ Recall
Tại sao? ___
Nếu sai ngược lại thì chuyện gì xảy ra? *VD: Nếu chọn precision nhưng low recall → user không tìm thấy kết quả cần → bỏ dùng*

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| *VD: Accuracy phân loại đúng* | *≥85%* | *<70% trong 1 tuần* |
|   |   |   |
|   |   |   |

---

## 4. Top 3 failure modes

*Liệt kê cách product có thể fail — không phải list features.*
*"Failure mode nào user KHÔNG BIẾT bị sai? Đó là cái nguy hiểm nhất."*

| # | Trigger | Hậu quả | Mitigation |
|---|---------|---------|------------|
| 1 | *VD: Email chứa thuật ngữ ngoài domain* | *AI gắn nhãn sai, tự tin cao* | *Detect low-confidence → hỏi user xác nhận* |
| 2 |   |   |   |
| 3 |   |   |   |

---

## 5. ROI 3 kịch bản

|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | *100 user/ngày, 60% hài lòng* | *500 user/ngày, 80% hài lòng* | *2000 user/ngày, 90% hài lòng* |
| **Cost** | *$50/ngày inference* | *$200/ngày* | *$500/ngày* |
| **Benefit** | *Giảm 2h support/ngày* | *Giảm 8h/ngày* | *Giảm 20h, tăng retention 5%* |
| **Net** |   |   |   |

**Kill criteria:** *Khi nào nên dừng? VD: cost > benefit 2 tháng liên tục*

---

## 6. Mini AI spec (1 trang)

*Tóm tắt tự do — viết bằng ngôn ngữ tự nhiên, không format bắt buộc.*
*Gom lại: product giải gì, cho ai, AI làm gì (auto/aug), quality thế nào (precision/recall), risk chính, data flywheel ra sao.*
