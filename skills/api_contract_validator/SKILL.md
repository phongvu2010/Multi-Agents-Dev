---
name: api-contract-validator
description: "Thẩm định cú pháp, tính đầy đủ và tính nhất quán của đặc tả OpenAPI (YAML/JSON) trước khi ký duyệt Gate 2."
---

# API Contract Validator Skill

## Mục đích
Đảm bảo bản hợp đồng giao tiếp giữa Frontend và Backend (`openapi.yaml`) không có lỗi logic, đầy đủ mã phản hồi HTTP và schema kiểu dữ liệu.

## Kiểm tra:
1. **Chuẩn cú pháp OpenAPI 3.0+:** `paths`, `components/schemas`, `responses`.
2. **RESTful Naming Conventions:** Đường dẫn danh từ số nhiều (vd: `/api/v1/users` thay vì `/api/v1/getUsers`).
3. **Mã lỗi chuẩn:** Có định nghĩa đầy đủ 200/201, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Error.
4. **Bảo mật:** Tất cả các endpoint yêu cầu xác thực phải có khai báo `security: - bearerAuth: []`.
