---
name: test-runner
description: "Thực thi bộ kiểm thử tự động (Unit Tests & Integration Tests) bằng PyTest cho FastAPI và Jest cho React Native, tính toán tỷ lệ độ phủ (Code Coverage) và trích xuất lỗi stack trace."
---

# Test Runner Skill

## Mục đích
Hỗ trợ QA Automation Agent và Auto-Healing Coordinator thực thi kiểm thử tự động, phân tích kết quả và phát hiện lỗi hồi quy (regressions).

## Tiêu chí chất lượng & Bộ công cụ:
1. **Đo độ phủ kiểm thử tự động (Automated Code Coverage):**
   - Sử dụng `pytest-cov` với cờ: `--cov=app --cov-report=term-missing --cov-report=json:coverage.json`
   - Ngưỡng tối thiểu bắt buộc: **>= 80% Code Coverage** trên toàn bộ Service Layer, API Routers và Repositories.
   - Trích xuất tự động `coverage_percentage` lưu vào `test_summary.json` và bảng scorecard `code_review_report.md`.

2. **Thẩm định Schema Drift Database (Zero Drift Policy):**
   - Sử dụng lệnh `alembic check` trong thư mục backend để thẩm định trạng thái đồng bộ giữa SQLAlchemy 2.0 Declarative Models và cơ sở dữ liệu.
   - Tiêu chí Pass: Zero Drift (`No new upgrade operations detected`).
   - Nếu phát hiện drift, sinh `DefectTicket(id="DEF-DB-DRIFT")` yêu cầu sinh file migration mới qua `alembic revision --autogenerate`.

3. **Kịch bản kiểm thử (BDD Mapping):**
   - Mỗi User Story trong `user_stories.json` bắt buộc có ít nhất 1 test case tương ứng trong `tests/`.
   - Kết hợp kiểm thử Happy Path, Edge Path (Capacity full, duplicate phone) và Error Path (Auth 401).

4. **Frontend Subprocess Runner:**
   - Thực thi bộ test qua Node runner `run_tests.cjs` hoặc Jest CLI, kiểm tra rendering và quy tắc nghiệp vụ màn hình.
