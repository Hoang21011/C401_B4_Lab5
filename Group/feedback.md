# Feedback — Demo round Day 6 
## Nhóm VinFast_C2 — AI tư vấn ưu đãi VinFast
| Tiêu chí | Điểm (1-5) |
|----------|-----------|
| Problem-solution fit | 4 |
| AI product thinking | 3 |
| Demo quality | 3 |

Điều làm tốt: UI đẹp, có ảnh demo, chất lượng demo tốt. Problem rõ - Thông tin ưu đãi khi mua xe phân tán trên nhiều nguồn, khiến người dùng khó xác định chính xác các ưu đãi mình được hưởng. Demo flow mượt, chatbot trả lời được câu hỏi thật.

Gợi ý cải thiện: Cần bổ sung fallback khi user feedback, cải thiện logic tính ưu đãi để tránh sai giá sau khuyến mãi, và thiết kế cơ chế thoát fallback loop khi người dùng chat nhiều vòng nhưng hệ thống vẫn chưa đưa ra được kết quả cụ thể.

---

## Nhóm VinFast_B3 — AI trợ lý bảo hành VinFast
| Tiêu chí | Điểm (1-5) |
|----------|-----------|
| Problem-solution fit | 3 |
| AI product thinking | 2 |
| Demo quality | 5 |

Điều làm tốt: Demo UI đẹp, trực quan. AI Agent trả lời tương đối đúng phạm vi, trình bày rõ.

Gợi ý cải thiện: Cần xử lý vấn đề review bias khi hiện tại, AI chủ yếu review, gợi ý về garage Ocean Park trong khi trong dữ liệu có garage khác gần và phù hợp hơn. Hiện tại còn sai tool và sai logic khi đặt lịch, Ví dụ: Xe này đang được đặt lịch hẹn rồi, nhưng khi người dùng yêu cầu đặt lại thì hệ thống vẫn tiếp nhận và tạo lịch mới -> cần đưa ra cảnh báo cho người dùng về việc xe đã được đặt lịch. Còn tồn tại lỗi sai khi đưa thông tin cho người dùng chọn, hệ thống hiển thị giờ trống nhưng khi người dùng chọn thì lại báo không có lịch trống.

---

## Nhóm VinFast_X4 — AI trợ lý bảo dưỡng, tư vấn và phân tích VinFast
| Tiêu chí | Điểm (1-5) |
|----------|-----------|
| Problem-solution fit | 3 |
| AI product thinking | 2 |
| Demo quality | 2 |

Điều làm tốt: UI đẹp, demo chạy được, có fallback.

Gợi ý cải thiện: Demo chạy được nhưng AI không thực sự được dùng, khi hỏi đáp về các tools, AI không trả lời mà chỉ đưa ra thông báo sẽ kết nối đến tư vấn viên. Do vậy không nhận xét được gì nhiều về logic các tools thông qua demo, cần vào file SPEC để xem và hiểu về logic hoạt động của các tools có trong bài. Cần cải thiện, xem lại phần gọi tools, trả lời câu hỏi trong demo.

---

## Nhóm VinFast_C1 — AI tư vấn mua xe VinFast
| Tiêu chí | Điểm (1-5) |
|----------|-----------|
| Problem-solution fit | 3 |
| AI product thinking | 3 |
| Demo quality | 4 |

Điều làm tốt: Xử lý tốt 2 vấn đề tư vấn và review, UI đẹp, demo khá tốt

Gợi ý cải thiện: Cần bổ sung fallback và cơ chế dừng vòng lặp hội thoại khi người dùng phản hồi rằng thông tin của bot không chính xác. Hiện tại bot đôi khi trả lời “không đủ ngữ cảnh” khiến người dùng mơ hồ và khi hỏi lại vẫn thiếu fallback để dẫn đến kết quả rõ ràng. Ngoài ra, logic so sánh giá vẫn chưa đúng: khi người dùng yêu cầu so sánh giá xe, bot lại so sánh giá pin thuê và mua thay vì giá xe. 


