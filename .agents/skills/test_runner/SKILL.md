---
name: test-runner
description: "Thực thi bộ kiểm thử tự động (Unit Tests & Integration Tests) bằng PyTest cho FastAPI và Jest cho React Native, tính toán tỷ lệ độ phủ (Code Coverage) và trích xuất lỗi stack trace."
---

# Test Runner Skill

## Mục đích
Hỗ trợ QA Automation Agent và Auto-Healing Coordinator thực thi kiểm thử tự động, phân tích kết quả và phát hiện lỗi hồi quy (regressions).

## Tiêu chí chất lượng:
1. **Độ phủ kiểm thử tối thiểu:** Tối thiểu **80% Code Coverage** trên toàn bộ Service Layer và API Routers.
2. **Kịch bản kiểm thử (BDD Mapping):** Mỗi User Story trong `user_stories.json` bắt buộc có ít nhất 1 test case tương ứng trong `tests/`.
3. **Phân loại kiểm thử:**
   - **Unit Tests:** Kiểm tra các hàm logic độc lập (Password hashing, token generation, slot availability calculation).
   - **Integration Tests:** Sử dụng `httpx.AsyncClient` giả lập HTTP Request đến FastAPI app, kiểm tra mã HTTP status (200, 201, 400, 401, 409, 422).
