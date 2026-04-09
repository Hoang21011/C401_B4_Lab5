# Individual reflection — Trịnh Uyên Chi (2A202600435)
## 1. Role
UX designer + Prompt Engineer. Phụ trách User Stories, thiết kế System Prompt và slides demo.

## 2. Đóng góp cụ thể
- Thiết kế User Stories cho 2 feature chính của chatbot
- Thiết kế System Prompt
- Làm slides cho demo

## 3. SPEC mạnh/yếu
- Mạnh nhất: SPEC mạnh nhất ở phần eval Metrics + Threshold. Nhóm xác định đúng và đầy đủ các metrics cần thiết cho bài toán
- Yếu nhất: SPEC yếu nhất ở Top 3 Failure Mode. Nhóm chưa đưa ra được tình huống mà user không nhận ra được khi hệ thống đang sai. Các tình huống giả định ở Failure Mode này user đều có thể thấy và cảm nhận được.

## 4. Đóng góp khác
* Thiết kế sơ đồ Workflow của chatbot trong mục Mini AI Spec

## 5. Điều học được
Trước hackathon, em nghĩ rằng thiết kế system prompt cho AI khá đơn giản, chỉ cần những mục cần thiết như persona, rule, tools_instruction, response format và constraints.

Sau hackathon, em học được cách tinh chỉnh từ ngữ cho rules và constraints để không bị dài dòng lặp ý và cách thiết kế system prompt chi tiết hơn từ teammate với các mục như priority_safety_protocol, diagnostic_funnel, data_driven_logic để hoàn thiện và chuyên biệt AI cho một domain cụ thể hơn trước.

## 6. Nếu làm lại
Sẽ giao tiếp với teammate nhiều hơn và test prompt giúp teammate vì hôm nay nhóm gặp vấn đề về số lượng quota trong API key cũng như model bị high demand thành ra không kịp test agent đủ nhiều để sửa lỗi.

Nếu có giao tiếp rõ ràng, test sớm và kịp thời thì sẽ giúp nhóm detect lỗi nhiều hơn, giúp demo chạy mượt và đưa ra được metrics cuối cùng sau demo.

## 7. AI giúp gì / AI sai gì
- **Giúp:** Dùng Gemini để tinh chỉnh rules và constraints sau khi tự soạn một bản phác thảo System Prompt. Gemini giúp gợi thêm ý tưởng.
- **Sai:** Ý tưởng khá thô và sơ khai. Ví dụ: Gemini đề xuất luôn kèm theo giá cả khi trả lời người dùng, nhưng lại không xem xét đến mặt giá cả có thể varied tùy theo phụ tùng, công thợ sửa xe và thuế VAT. Ngoài ra, Gemini còn đề xuất khi người dùng khiếu nại thì phải lấy dữ liệu khiếu nại đó để học hỏi, nhưng gợi ý này khá tệ nếu như có người cố tình phá bot để làm nhiễu bộ dữ liệu của công ty.

**Bài học rút ra:** AI brainstorm tốt nhưng không biết tinh chỉnh phù hợp với ngữ cảnh.