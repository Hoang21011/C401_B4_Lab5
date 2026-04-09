# Individual reflection — Phạm Nguyễn Tiến Mạnh (2A202600418)

## 1. Role

AI Engineer (Tool Designer). Phụ trách thiết kế và xây dựng các tool để AI agent có thể thực hiện chẩn đoán và tra cứu lỗi xe trong hệ thống chatbot.

## 2. Đóng góp cụ thể

- Thiết kế tool `diagnose`: cho phép AI agent chẩn đoán lỗi xe dựa trên mô tả bằng ngôn ngữ tự nhiên của người dùng (ví dụ: "xe rung", "có tiếng kêu lạ"), từ đó gợi ý các nguyên nhân và hướng xử lý phù hợp.
- Thiết kế tool `lookup_error_by_code`: hỗ trợ tra cứu thông tin chi tiết về lỗi xe thông qua mã lỗi (error code) cụ thể, giúp người dùng hoặc thợ sửa xe nhanh chóng xác định vấn đề.

## 3. SPEC mạnh/yếu

- **Mạnh nhất:** Phần AI Product Canvas và failure modes được nhóm đầu tư rõ ràng — các rủi ro khi AI tiếp nhận mô tả mơ hồ từ người dùng đã được nhận diện cụ thể, kèm theo các hướng xử lý như đặt câu hỏi follow-up, trình bày Top-3 khả năng thay vì chốt một kết luận duy nhất, hoặc chuyển hướng người dùng liên hệ gara khi độ tin cậy chẩn đoán còn thấp.
- **Yếu nhất:** Phần mô phỏng dữ liệu và hệ thống chưa đủ sát với thực tế — mock data hiện tại về gara, thợ sửa và lịch sử bảo dưỡng chưa phản ánh được các yếu tố động như trạng thái thợ theo thời gian thực hay mức giá sửa chữa biến động theo từng khu vực.

## 4. Đóng góp khác

- Xây dựng file `requirements.txt` cho dự án, đảm bảo môi trường cài đặt thống nhất giữa các thành viên trong nhóm.

## 5. Điều học được

- **Cách làm việc nhóm:** Trước khi tham gia project, tôi hiểu làm việc nhóm đơn giản là mỗi người làm phần của mình rồi ghép lại. Thực tế cho thấy điều quan trọng hơn là sự phối hợp liên tục — khi các thành viên trao đổi thường xuyên và thống nhất hướng đi chung, việc tích hợp code trở nên trơn tru hơn, tránh được conflict và mọi người đều hiểu rõ bài toán tổng thể, không chỉ phần mình đảm nhận.
- **LangGraph và quy trình gọi tool:** Thông qua việc thiết kế tool trong dự án, tôi hiểu rõ hơn cách LangGraph điều phối luồng xử lý, cách agent quyết định gọi tool nào và truyền dữ liệu giữa các bước ra sao. Đây là kiến thức thực tế mà tôi khó nắm được nếu chỉ đọc tài liệu.
- **Tầm quan trọng của Spec:** Lần đầu tiên tôi trải nghiệm việc viết spec trước khi bắt tay code, và nhận ra rằng một spec rõ ràng giúp tiết kiệm rất nhiều thời gian chỉnh sửa về sau — định nghĩa đúng input/output của tool ngay từ đầu giúp tránh phải làm lại nhiều lần.

## 6. Nếu làm lại

- Tool `diagnose` hiện tại phụ thuộc khá nhiều vào keyword matching với dữ liệu trong database — cách tiếp cận này dễ bỏ sót khi người dùng diễn đạt theo cách khác. Nếu làm lại, tôi sẽ áp dụng embedding để agent có thể hiểu ngữ nghĩa câu mô tả thay vì chỉ khớp từ khóa, từ đó nâng cao độ chính xác của kết quả chẩn đoán.
- Ngoài ra, tôi sẽ chủ động theo dõi tiến độ chung của nhóm thường xuyên hơn để kịp thời hỗ trợ khi có thành viên gặp khó khăn, tránh để phát sinh thiếu sót ở khâu demo như lần này.

## 7. AI giúp gì / AI sai gì

- **Giúp:** ChatGPT hỗ trợ tôi hiện thực hóa các tool theo đúng đặc tả đã thiết kế — từ cấu trúc hàm, xử lý input/output cho đến logic tra cứu dữ liệu — giúp rút ngắn đáng kể thời gian viết code.
- **Sai/mislead:** AI tự ý sinh thêm một số tool ngoài phạm vi yêu cầu, khiến tôi mất thêm thời gian để lọc lại và xác định đâu là thứ thực sự cần thiết cho bài toán. Đây là lời nhắc nhở rằng output của AI luôn cần được review kỹ trước khi tích hợp vào dự án.
