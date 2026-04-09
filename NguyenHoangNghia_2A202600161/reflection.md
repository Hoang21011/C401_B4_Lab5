# Individual reflection — Nguyễn Hoàng Nghĩa (2A202600161)

## 1. Role
Developer, Phụ trách thiết kế tool cho chatbot và viết/hoàn thiện SPEC.

## 2. Đóng góp cụ thể
- Thiết kế và implement tool search_mechanic (tìm thợ/cứu hộ available)
- Viết và double-check file `spec_final`, đảm bảo logic giữa các phần consistent
- Review các module trong chatbot (flow + tool integration)
- Chủ động tìm bugs trong flow và spec 

## 3. SPEC mạnh/yếu
- **Mạnh nhất:** Flow end-to-end rõ ràng (diagnosis → decision → action), đặc biệt phần emergency có thể chuyển thành hành động thật (gọi thợ/cứu hộ), không chỉ dừng ở suggestion  
- **Yếu nhất:** Data dependency — spec phụ thuộc nhiều vào dữ liệu real-time (trạng thái thợ, location), nhưng chưa define rõ cách đảm bảo data luôn đúng và cập nhật

## 4. Đóng góp khác
- Đóng góp ý kiến để refine các module chatbot (đặc biệt phần tool calling và decision logic)
- Hỗ trợ debug các vấn đề liên quan đến logic matching

## 5. Điều học được
Trước hackathon nghĩ việc viết spec chỉ là mô tả ý tưởng. Sau khi làm mới thấy:  
spec tốt phải cover cả failure modes, data flow, và real-world constraints.  
- Tool design quan trọng không kém model (LLM chỉ là 1 phần)
- Product tốt là sự kết hợp giữa AI + system + data, không chỉ prompt

## 6. Nếu làm lại
- Sẽ define rõ data layer và API contract sớm hơn (mechanic availability, pricing, location).  
- Hiện tại phần này được làm sau nên phải sửa lại nhiều chỗ trong flow và spec.  
- Thực thi nhiều test cases hơn.

## 7. AI giúp gì / AI sai gì
- **Giúp:** dùng AI để draft spec nhanh, generate edge cases và hỗ trợ rà soát logic (đặc biệt ở failure modes và user flows)  
- **Sai/mislead:** AI đôi khi đề xuất giải pháp quá “ideal” (giả định data luôn đúng, system luôn available), không phản ánh đúng constraint thực tế. Các đóng góp của AI đôi khi không sát với dữ liệu và bài toán của nhóm

→ Bài học: AI hữu ích cho ideation và speed, nhưng cần con người để validate về feasibility và system design**
