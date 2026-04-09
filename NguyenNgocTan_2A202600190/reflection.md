# Individual Reflection — Nguyễn Ngọc Tân (2A202600190)

## 1. Role  
**AI Engineer (Tool Designer)**  

Tôi chịu trách nhiệm thiết kế và xây dựng **tool layer** giúp AI agent có thể thực hiện các tác vụ chẩn đoán và tra cứu lỗi xe trong hệ thống chatbot. Vai trò này đóng vai trò cầu nối giữa **LLM reasoning** và **hệ thống dữ liệu có cấu trúc**, đảm bảo agent có thể xử lý bài toán một cách chính xác và có kiểm soát.

---

## 2. Đóng góp cụ thể  

### Tool `diagnose`  
- Cho phép AI agent chẩn đoán lỗi xe dựa trên mô tả ngôn ngữ tự nhiên của người dùng (ví dụ: “xe rung”, “có tiếng kêu lạ”).  
- Output bao gồm:
  - Danh sách các nguyên nhân khả dĩ (Top-k)  
  - Hướng xử lý đề xuất (tự kiểm tra / đi gara / gọi cứu hộ)  
- Tool được thiết kế theo hướng **augmentation**, chỉ gợi ý và hỗ trợ quyết định thay vì đưa ra kết luận tuyệt đối.

---

###  Tool `lookup_error_by_code`  
- Hỗ trợ tra cứu thông tin chi tiết về lỗi xe thông qua mã lỗi (error code).  
- Cung cấp:
  - Mô tả lỗi  
  - Nguyên nhân phổ biến  
  - Hướng xử lý tương ứng  
- Giúp người dùng và thợ sửa xe nhanh chóng xác định vấn đề mà không cần tra cứu thủ công.

---

## 3. Đánh giá SPEC  

###  Điểm mạnh  
Phần **AI Product Canvas** và **failure modes** được xây dựng rõ ràng và thực tế.  

Nhóm đã nhận diện tốt các rủi ro khi AI xử lý input mơ hồ từ người dùng, đồng thời đưa ra các hướng xử lý hợp lý như:
- Sử dụng câu hỏi follow-up để làm rõ thông tin  
- Trả về nhiều khả năng (Top-3) thay vì kết luận duy nhất  
- Chuyển hướng sang gara/cứu hộ khi độ tin cậy thấp  

###  Điểm yếu  
Phần dữ liệu và mô phỏng hệ thống chưa sát với thực tế.  

Cụ thể:
- Mock data về gara và thợ sửa chưa phản ánh được **trạng thái real-time**  
- Giá sửa chữa chưa thể hiện được sự biến động theo khu vực  
- Thiếu các yếu tố thực tế như lịch sử bảo dưỡng hoặc độ tuổi xe  

## 4. Đóng góp khác  
- Xây dựng file `requirements.txt` cho dự án, giúp đảm bảo môi trường cài đặt thống nhất giữa các thành viên trong nhóm.

---

## 5. Điều học được  

###  Cách làm việc nhóm  
Trước khi tham gia project, tôi nghĩ làm việc nhóm chỉ đơn giản là chia task rồi ghép lại.  

Tuy nhiên, trải nghiệm thực tế cho thấy điều quan trọng hơn là **sự phối hợp liên tục**. Khi các thành viên trao đổi thường xuyên và thống nhất hướng đi chung:
- Việc tích hợp code trở nên trơn tru hơn  
- Giảm xung đột (conflict)  
- Mọi người hiểu được bài toán tổng thể, không chỉ phần của mình  

### 🧠 LangGraph và quy trình gọi tool  
Thông qua việc thiết kế tool, tôi hiểu rõ hơn:
- Cách LangGraph điều phối luồng xử lý  
- Cách agent quyết định gọi tool nào  
- Cách dữ liệu được truyền giữa các bước  

### 📄 Tầm quan trọng của SPEC  
Việc viết spec trước khi code giúp:
- Định nghĩa rõ input/output  
- Tránh phải chỉnh sửa nhiều lần  
- Giảm thời gian debug và rework  

Một spec rõ ràng giúp toàn bộ team làm việc hiệu quả hơn.

---

## 6. Nếu làm lại  

- Tool `diagnose` hiện tại phụ thuộc nhiều vào keyword matching → dễ bỏ sót khi user diễn đạt khác.  
  → Nếu làm lại, tôi sẽ sử dụng **embedding-based retrieval** để hiểu ngữ nghĩa tốt hơn và cải thiện độ chính xác chẩn đoán.  

- Chủ động theo dõi tiến độ chung của nhóm thường xuyên hơn để kịp thời hỗ trợ khi cần, tránh phát sinh thiếu sót ở giai đoạn demo.

---

## 7. AI giúp gì / AI sai gì  
 
ChatGPT hỗ trợ:
- Sinh code theo đúng đặc tả  
- Thiết kế cấu trúc hàm  
- Xử lý input/output  
- Xây dựng logic tra cứu  
