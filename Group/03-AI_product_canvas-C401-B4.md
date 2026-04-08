# AI Product Canvas — template

Điền Canvas cho product AI của nhóm. Mỗi ô có câu hỏi guide — trả lời trực tiếp, xóa phần in nghiêng khi điền.

---

## Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi guide** | User nào? Pain gì? AI giải quyết gì mà cách hiện tại không giải được? | Khi AI sai thì user bị ảnh hưởng thế nào? User biết AI sai bằng cách nào? User sửa bằng cách nào? | Cost bao nhiêu/request? Latency bao lâu? Risk chính là gì? |
| **Trả lời** |User: Khách hàng cần tra cứu chuyến bay (chưa có mã đặt chỗ) |Recall cao: Ưu tiên đưa nhiều phương án  |Cost: ~$0.02/lượt GPT-4o |
||Pain: Bot không hiểu -> yêu cầu khách hàng nhập theo form cấp sẵn, nếu không tìm thấy lại yêu cầu khách hàng nhập lại -> mất 10-15', khách chờ lâu mà không có thông tin|Khi sai: Một số đề xuất có thể không khả dụng (hết chỗ/hết giờ) |Latency: < 5 giây |
||Aug: Chatbot sẽ đề xuất chuyến gần giờ / cùng ngày / đề xuất đổi ngày hoặc đề xuất solution khả thi |Recovery: Tiếp tục gợi ý phương án khác + fallback: "Xin quý khách vui lòng chờ, tư vấn viên sẽ hỗ trợ quý khách ngay: |Risk: Thông tin về chuyến bay bị cũ, không cập nhật real-time; dẫn đến trả lời sai thông tin |
||Value: Trả lời 24/7, đáp ứng nhu cầu khách, tăng khả năng  | |Dep: API Vietnam Airlines real-time |


---

## Automation hay augmentation?
☐ Automation — AI làm thay, user không can thiệp

[x] Augmentation — AI gợi ý, user quyết định cuối cùng

**Justify:** Vấn đề liên quan đến chuyến bay, quyết định đặt vé nằm ở user, chatbot chỉ có thể trả lời câu hỏi, gợi ý và hướng dẫn user.


---

## Learning signal

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | User correction đi vào đâu? |Log các hành vi: user sửa ngày bay, chọn chuyến khác, reject đề xuất → lưu vào hệ thống recommendation để cải thiện logic gợi ý (ranking chuyến bay) |
| 2 | Product thu signal gì để biết tốt lên hay tệ đi? | - Tỷ lệ user chọn chuyến được đề xuất (CTR) <br>- Tỷ lệ user phải nhập lại thông tin (re-entry rate)<br>- Tỷ lệ chuyển sang human (fallback rate)<br>- Tỷ lệ hoàn thành booking sau khi dùng chatbot|
| 3 | Data thuộc loại nào? | [x] User-specific · [x] Domain-specific · [x] Real-time · ☐ Human-judgment · ☐ Khác: ___ | |

**Có marginal value không?** (Model đã biết cái này chưa? Ai khác cũng thu được data này không?) <br> Có. Dữ liệu thu được mang marginal value cao vì phản ánh hành vi thực tế của người dùng trong quá trình tìm kiếm và lựa chọn chuyến bay (ví dụ: giờ bay, xu hướng reject/accept của các đề xuất). Những thông tin này không có sẵn trong model và cũng khó thu thập từ các nguồn công khai. Mặc dù các nền tảng khác có thể thu thập dữ liệu tương tự, nhưng giá trị nằm ở việc tích lũy dữ liệu theo ngữ cảnh và hệ thống riêng, từ đó giúp cải thiện khả năng gợi ý và duy trì flow người dùng hiệu quả hơn.
___