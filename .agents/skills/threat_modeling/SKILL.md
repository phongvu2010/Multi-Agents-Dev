---
name: threat-modeling
description: "Thực hiện phân tích mô hình mối đe dọa bảo mật theo chuẩn STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) và xây dựng ma trận phân quyền RBAC."
---

# Threat Modeling Skill

## Mục đích
Hỗ trợ Security & Compliance Architect Agent rà soát rủi ro an toàn thông tin ngay từ giai đoạn thiết kế kiến trúc trước khi viết code (Shift-Left Security).

## Khung phân tích STRIDE:
1. **S - Spoofing (Giả mạo danh tính):** Kẻ tấn công giả danh người dùng hoặc hệ thống khác (Khắc phục: JWT ký bằng RS256/HS256, HTTPS, Password hashing Bcrypt/Argon2id).
2. **T - Tampering (Can thiệp dữ liệu):** Sửa đổi dữ liệu trên đường truyền hoặc trong DB (Khắc phục: TLS 1.3, Data integrity hash, Parameterized queries).
3. **R - Repudiation (Chối bỏ hành vi):** Người dùng từ chối việc đã thực hiện một giao dịch (Khắc phục: Immutable Audit Logs, lưu IP, User ID, Timestamp).
4. **I - Information Disclosure (Rò rỉ thông tin):** Lộ thông tin nhạy cảm qua API responses hoặc log (Khắc phục: Không trả về password_hash/stack trace, mã hóa cột nhạy cảm trong DB).
5. **D - Denial of Service (Từ chối dịch vụ):** Làm nghẽn hệ thống (Khắc phục: Rate Limiting Redis token bucket, pagination max limit).
6. **E - Elevation of Privilege (Leo thang đặc quyền):** User thường truy cập tính năng Admin (Khắc phục: Strict RBAC middleware tại API layer, Ownership validation BOLA).

## Ma trận RBAC chuẩn:
```markdown
| Resource | Action | Role: Customer | Role: Technician | Role: Admin |
|---|---|---|---|---|
| Appointment | Create | ALLOW (Own) | DENY | ALLOW (Any) |
| Appointment | Read | ALLOW (Own) | ALLOW (Assigned) | ALLOW (Any) |
| SparePart | Update | DENY | DENY | ALLOW |
```
