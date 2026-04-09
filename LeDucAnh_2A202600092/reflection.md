# Reflection Report

## 1. Role cụ thể trong nhóm
 - Backend developer + prompt engineer. Phụ trách thiết kế và triển khai hệ thống backend, bao gồm cả việc thiết kế các tool và prompt cho agent.

## 2. Phần phụ trách cụ thể
 - Lên ý tưởng và phản biện nhằm thống nhất solution chung của cả nhóm
 - Thiết kế tool mantain_schedule() 
 - Thiết kế agent sử dụng state machine để xử lý các tình huống khác nhau.

## 3. SPEC mạnh/yếu
 - **Mạnh nhất**: AI Product Canvas và failure modes — nhóm xác định rõ các rủi ro khi AI chẩn đoán lỗi từ mô tả mơ hồ của người dùng (ví dụ: “xe rung”, “kêu lạ”) và đưa ra mitigation cụ thể như hỏi thêm follow-up question, hiển thị nhiều khả năng (Top-3) thay vì một kết luận duy nhất, hoặc đề xuất liên hệ gara khi độ chắc chắn thấp.
- **Yếu nhất**: Phần dữ liệu và giả lập hệ thống — hiện tại nhóm mới sử dụng mock data cho gara, thợ sửa và lịch sử bảo dưỡng nên chưa phản ánh đầy đủ dữ liệu thực tế (ví dụ: trạng thái thợ real-time, giá sửa chữa thay đổi theo khu vực).

## 4. Đóng góp khác
 - Chỉnh sửa system prompt cùng Chi để tối ưu hóa hiệu năng của agent.
 
## 5. Điều học được
 - Sự quan trọng của thiết kế workflow cho agent, không chỉ cứ làm theo AI response, copy/paste lại lỗi lặp đi lặp lại. Điều này gây ảnh hướng lớn không chỉ đến cost mà còn ảnh hưởng lớn đến trải nghiệm của người dùng khi deploy trên hệ thống thật.
 - Các bài toán cần phải được define cực kỳ rõ ràng về scope, sau đó đến tools application, đánh giá xem tool có thực sự cần thiết hay không, có thể gộp hoặc loại bỏ tool không quan trọng hay không.

## 6. Nếu làm lại
 - tối ưu hóa các tool từ sớm hơn để đảm bảo tiến độ cho cả test và demo. Đồng thời cần một workflow kỹ và chi tiết hơn để agent không bị loop toàn bộ workflow với mỗi prompt của user gây ảnh hưởng đến latency do model phải xử lý quá nhiều thông tin gây ra 'high demand' cho model.

## 7. AI giúp gì / AI sai gì

- **Giúp**: dùng Gemini để brainstorm failure modes, tối ưu hóa system prompt. Gộp/ loại bỏ được tools không quan trọng.

- **Sai**: Gemeni gợi ý thêm features không cần thiết, làm tăng độ phức tạp của hệ thống.

