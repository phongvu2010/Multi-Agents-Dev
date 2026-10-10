---
name: code-review-evaluator
description: "Chấm điểm mã nguồn dựa trên các tiêu chuẩn Clean Code, Security Guardrails, và kiểm tra tính tương thích với profile Tech Lead (Python/FastAPI, React Native/Node.js)."
---

# Code Review Evaluator Skill

## Mục đích
Hỗ trợ Code Reviewer Agent thực hiện phân tích tự động chất lượng mã nguồn trước khi chuyển sang bước chạy test.

## Quy trình đánh giá:
1. **Kiểm tra Secret Leakage:** Regex quét các chuỗi nghi ngờ là Private Keys, Tokens, Passwords.
2. **Kiểm tra Schema/Contract:** So sánh model trong code với schema trong `openapi.yaml`.
3. **Phát hiện Code Smells:** Hàm quá dài (> 50 dòng), lồng nhau quá sâu (> 3 cấp), thiếu xử lý ngoại lệ `try...except`.
4. **Đánh giá mức độ Review-Friendly:** Đảm bảo code được viết mạch lạc, có type annotations để Tech Lead dễ dàng kiểm tra thủ công.
