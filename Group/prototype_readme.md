# Prototype — AI kỹ thuật VinFast

## Mô tả
Chatbot thu thập thông số xe và dẫn dắt người dùng làm rõ các triệu chứng qua 3 câu hỏi tương tác. AI phân tích xác suất lỗi, đánh giá mức độ nguy hiểm và gợi ý khoảng giá benchmark minh bạch. Người dùng chọn đặt lịch tại xưởng gần nhất hoặc escalate tới chuyên viên cứu hộ 24/7 trong trường hợp khẩn cấp.

## Level: Mock prototype
- UI build bằng Streamlit.
- 1 flow chính chạy thật với Gemini API: nhập lỗi xe -> nhận gợi ý hành động tiếp theo (gọi cứu hộ, đặt lịch tại xưởng)

## Links
- Prototype: https://claude.site/artifacts/xxx
- Prompt test log: xem file `prototype/prompt-tests.md`
- Video demo (backup): https://drive.google.com/xxx

## Tools
- UI: Streamlit
- AI: Google Gemini 2.5 Flash (via Google AI Studio)
- Prompt: System prompt 

## Phân công
| Thành viên | Phần | Output |
|-----------|------|--------|
| Chi | User Stories 4 Paths + System Prompt + Slides Designer | system_prompt.txt, spec/spec_final.md phần 1, hình ảnh Mini AI Spec, demo/demo_slides.pdf |
| Trang | UX Designer + Mock Data + Define Tool | spec/spec_final.md phần 1, mock data: car_data.json, mock_garages.json, mock_mechanics.json; tool search_garages.json |
| Châu | Eval metrics + ROI + demo slides | spec/spec-final.md phần 3, 5, demo/slides.pdf |
| Dũng | UI prototype + demo script | prototype/, demo/demo-script.md |
