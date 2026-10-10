---
name: requirement-parser
description: "Phân tích yêu cầu thô của khách hàng, trích xuất thực thể, hành động, và phát hiện các điểm thiếu sót, mâu thuẫn để tạo bộ câu hỏi làm rõ (Clarification Q&A)."
---

# Requirement Parser Skill

## Mục đích
Giúp Client Liaison Agent và Business Analyst Agent bóc tách các văn bản phi cấu trúc (email, đoạn chat, biên bản họp) thành danh sách yêu cầu có cấu trúc.

## Các bước thực hiện:
1. **Trích xuất Mục tiêu Dự án (Project Objective):** Xác định bài toán cốt lõi mà khách hàng muốn giải quyết.
2. **Liệt kê Tác nhân (Actors / Personas):** Ai là người sử dụng hệ thống (Admin, User, Khách vãng lai...).
3. **Phát hiện Vùng mờ (Ambiguity Detection):**
   - Thiếu luồng xử lý lỗi (vd: Khi thanh toán thất bại thì làm gì?).
   - Thiếu tiêu chí phi chức năng (vd: Số lượng người dùng đồng thời, thời gian phản hồi kỳ vọng).
   - Mâu thuẫn logic giữa các yêu cầu.
4. **Sinh bảng câu hỏi làm rõ (Clarification Questions):**
   - Định dạng: Bảng gồm ID câu hỏi, Yêu cầu gốc, Điểm chưa rõ, Đề xuất gợi ý cho khách hàng lựa chọn.
