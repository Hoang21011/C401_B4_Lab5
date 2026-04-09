# Individual reflection — Nguyễn Thị Thùy Trang (2A202600214)

## 1. Role
Data Engineer + AI Engineer (Mock Data & Tooling). Phụ trách tạo dữ liệu giả lập và xây dựng công cụ truy vấn dữ liệu cho hệ thống chatbot.

## 2. Đóng góp cụ thể
- Thiết kế và tạo mock dataset cho hệ thống, bao gồm: thông tin garage, mechanic và car_data (chủ xe, xe, lịch sử bảo dưỡng, chi tiết bảo dưỡng).
- Phát triển tool search để AI agent có thể truy vấn thông tin gara và dữ liệu xe từ dataset.
- Tham gia xây dựng Spec (AI Product Canvas): mô tả dữ liệu, khả năng hệ thống và cách AI sử dụng dữ liệu để hỗ trợ người dùng.

## 3. SPEC mạnh/yếu
- Mạnh nhất: AI Product Canvas và failure modes — nhóm xác định rõ các rủi ro khi AI chẩn đoán lỗi từ mô tả mơ hồ của người dùng (ví dụ: “xe rung”, “kêu lạ”) và đưa ra mitigation cụ thể như hỏi thêm follow-up question, hiển thị nhiều khả năng (Top-3) thay vì một kết luận duy nhất, hoặc đề xuất liên hệ gara khi độ chắc chắn thấp.
- Yếu nhất: Phần dữ liệu và giả lập hệ thống — hiện tại nhóm mới sử dụng mock data cho gara, thợ sửa và lịch sử bảo dưỡng nên chưa phản ánh đầy đủ dữ liệu thực tế (ví dụ: trạng thái thợ real-time, giá sửa chữa thay đổi theo khu vực).

## 4. Đóng góp khác
- Hỗ trợ chỉnh sửa error_data (lỗi xe có thể gặp phải), viết thêm 3 lỗi, bổ sung thông tin về giá cho các lỗi đó.

## 5. Điều học được
- **Cách làm việc nhóm**: Trước khi làm project, tôi nghĩ làm việc nhóm chủ yếu là khi chia task cho từng người rồi ghép lại. Sau khi làm việc cùng team, tôi nhận ra việc phân chia role rõ ràng và trao đổi thường xuyên quan trọng hơn nhiều. Khi trao đổi rõ ràng với thành viên trong team, việc triển khai tool sẽ thống nhất, bài toán được clear hơn, các thành viên có thể hiểu rõ bài toán, không chỉ phần của riêng mình, cũng tránh được tình trạng conflic khi merge code. Vì vậy, teamwork trong AI Product cần trao đổi thường xuyên, thống nhất giữa các thành viên trong nhóm, không chỉ chia việc đơn thuần.
- **Quy trình build AI Product**: Trước đây tôi nghĩ xây dựng AI chủ yếu là train model và tối ưu thuật toán. Sau khi tham gia project, tôi hiểu rằng một AI product hoàn chỉnh cần nhiều bước hơn: <br> - Xác định problem (Spec), <br> - Thiết kế solution, <br> - Chuẩn bị dữ liệu, <br> - Xây tool, <br> - Test và demo. <br> Trong project này, việc tạo mock data, xây tool search và thiết kế AI Product Canvas giúp tôi hiểu rằng AI không chỉ là model, mà còn là hệ thống kết hợp dữ liệu, công cụ và trải nghiệm người dùng để giải quyết một bài toán cụ thể.

## 6. Nếu làm lại
- Nếu làm lại, tôi sẽ trao đổi nhiều hơn với các thành viên trong team để nắm được ai đang cần trợ giúp ở đâu, tránh để vấn đề thiếu demo như hôm nay.
- Nếu làm lại, tôi sẽ chuẩn bị sớm hơn, dành thêm thời gian chuẩn bị demo flow hoàn chỉnh, để khi trình bày có thể minh họa rõ cách AI sử dụng dữ liệu và tool để giải quyết bài toán.

## 7. AI giúp gì / AI sai gì
- **Giúp:** AI (ChatGPT) giúp tôi sinh dữ liệu (mock data) dựa trên các trường và theo cấu trúc tôi đã thiết kế.
- **Sai/mislead:** AI tự động sinh thêm các trường không cần thiết / lớn hơn mục tiêu của bài toán đề ra. Giả dụ như data về mechanics, bài toán của nhóm chỉ cần đến thông tin bao gồm Tên, id, nơi làm việc và trạng thái hiện tại của thợ; tuy nhiên, ChatGPT lại tự sinh thêm trường "specialties" (Lĩnh vực chuyên môn). Mặc dù trong tương lai của dự án, nhóm cũng có dự định sẽ thêm thông tin về lĩnh vực chuyên môn của thợ để tăng trải nghiệm người dùng, nhưng ở hiện tại thì việc thêm trường này vào database sẽ khiến nhóm bị rối, mất thêm thời gian để các thành viên clear được bài toán.