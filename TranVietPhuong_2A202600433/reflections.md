# Individual reflection — Trần Việt Phương (2A202600433)

## 1. Role
AI Agent Engineer / Backend Developer. 
Phụ trách kiến trúc hệ thống Chatbot, kết nối LLM (Gemini 2.5 Flash) bằng framework LangChain và LangGraph, lập trình file thực thi chính (`agent.py` và `main.py`), đồng thời rà soát (revise) và tích hợp các công cụ (tools) do các thành viên khác viết.

## 2. Đóng góp cụ thể
- Lập trình hệ thống Agent cốt lõi (`agent.py`) bằng `StateGraph` của LangGraph, thiết lập các node `agent` và `execute_tools` thủ công thay vì dùng prebuilt để kiểm soát chặt chẽ input/output của tools.
- Viết file khởi chạy chương trình bằng giao diện dòng lệnh (`main.py`), có tính năng stream thời gian thực (CLI streaming) và in chi tiết các lần Agent gọi công cụ (*Tool Called, Parameters, Tool Output*) để phục vụ debug và demo.
- Rà soát toàn bộ source code của nhóm, sửa các lỗi đường dẫn tương đối (relative paths) dễ gây crash hệ thống trong các file `search_garages.py`, `search_mechanic.py`.
- Thiết kế một cấu trúc `diagnose.py` hoàn chỉnh hơn: tạo wrapper nhận đúng `(description, car_history)` như System Prompt yêu cầu, thay cho hàm `search_error_by_symptom` ban đầu.
- Tạo dữ liệu mock `car_history.json` và thiết lập luồng nhúng ("inject") dữ liệu xe của người dùng vào context background trước khi chat.

## 3. SPEC mạnh/yếu
- **Mạnh nhất:** Cơ chế *Safety Protocol* & *Emergency Trigger*. Đội đã thiết kế rất tốt việc khi có mô tả "cháy, mất phanh, bốc khói", AI ngay lập tức không chẩn đoán vòng vo mà kích hoạt khẩn cấp công cụ `maintain_schedule` với cờ `is_emergency=True`.
- **Yếu nhất:** Xung đột logic giữa System Prompt và Tools Code. Trong bản Spec/Prompt yêu cầu công cụ tên là `error_predict` (kèm tham số `car_history`), nhưng code tool nhóm viết lại tên là `search_error_by_symptom` (trong `diagnose.py`) và thiếu logic nhận `car_history`. Việc này đòi hỏi kỹ thuật phải can thiệp tạo wrapper tốn thời gian. Nên chuẩn hóa hợp đồng API (API contract) giữa Prompt và Code ngay từ đầu.

## 4. Đóng góp khác
- Cải tiến và fix bug định dạng output: Xử lý thành công lỗi LLM trả về cấu trúc mảng JSON thô (`metadata, type, signature`) của LangChain thay vì phản hồi chữ, giúp giao diện Terminal trở nên gọn gàng.
- Xây dựng file `requirements.txt` gom lại tất cả các packages cần thiết (`langgraph`, `langchain-google-genai`, `python-dotenv`) để chạy dự án hoàn chỉnh.

## 5. Điều học được
Qua việc thiết lập LangGraph bằng code tùy biến, tôi mới hiểu rõ bản chất vấn đề *State & Memory* khi làm Agentic AI. Ban đầu, tôi quản lý lịch sử hội thoại bằng một List Array đơn giản (`user -> assistant -> user`), dẫn đến việc lỡ xóa mất lịch sử `ToolCalls` và `ToolOutputs`. Hệ quả là LLM bị mất bối cảnh (hallucinate) và in ra các chuỗi JSON rỗng tuếch do không nhớ công cụ mình vừa gọi. 
Sau khi học cách bật `MemorySaver` của LangGraph và thiết lập `thread_id` để "ủy quyền" quản lý State cho framework, AI lập tức vận hành liên tục qua nhiều turn, đọc tool output chính xác 100%.

## 6. Nếu làm lại
- Sẽ thống nhất kỹ với đội viết System Prompt và đội Data về **tên hàm** và **tham số truyền vào** ngay từ đầu. Chữa cháy mismatch giữa code và prompt tốn thời gian hơn mong đợi.
- Nếu có thời gian, tôi sẽ chuyển hẳn hệ thống từ Command Line Interface (CLI) sang ứng dụng Web (Streamlit/Gradio) để giao diện hackathon mang tính thẩm mỹ và dễ trình bày (demo) cho ban giám khảo hơn dựa trên thư mục `Sketch - Prototype.png` nhóm đã vẽ.

## 7. AI giúp gì / AI sai gì
- **Giúp:** Trợ lý AI coding (Antigravity/Gemini) giúp đọc và rà soát bug hệ thống toàn diện của cả một tệp code phức tạp (tìm ra ngay lỗi lệch đường dẫn path cwd và lỗi Pydantic liên quan đến Python 3.14). AI cũng viết Custom Node cho StateGraph cực kì nhanh giúp bỏ qua được `create_react_agent` bị gãy.
- **Sai/mislead:** Ban đầu AI đã xây dựng vòng lặp quản lý lịch sử tin nhắn (messages log) trong `main.py` sai cách, khiến luồng chẩn đoán bị đánh mất ToolMessages làm phản hồi của LLM trả về rác. Phải trải qua quá trình tự phân tích log lỗi in ra mới nhận diện được lỗ hổng state memory và buộc AI phải sửa lại luồng chạy sử dụng `MemorySaver(checkpointer=...)`.
