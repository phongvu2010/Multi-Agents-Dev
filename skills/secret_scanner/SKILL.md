---
name: secret-scanner
description: "Quét tĩnh mã nguồn để phát hiện rò rỉ khóa bí mật, API Keys, mật khẩu cơ sở dữ liệu, private keys và tokens thông qua entropy analysis và regex patterns."
---

# Secret Scanner Skill

## Mục đích
Hỗ trợ Security Auditor Agent phát hiện các vi phạm quy chuẩn Zero-Hardcoded Secrets trước khi đưa mã nguồn vào khâu kiểm thử và đóng gói.

## Các mẫu nhận diện rủi ro cao:
1. **API Keys / JWT Secrets:** `SECRET_KEY = "..."`, `api_key = "..."`, `jwt_secret = "..."`.
2. **Database Credentials:** `postgres://user:password@host/db` nằm trực tiếp trong file code thay vì đọc từ `os.getenv()`.
3. **Private Keys:** Chuỗi bắt đầu bằng `-----BEGIN RSA PRIVATE KEY-----`.

## Hành động bắt buộc khi phát hiện vi phạm:
- Ngay lập tức đánh dấu trạng thái `REJECT` trong `security_audit_report.md`.
- Tạo một `DefectTicket(severity="CRITICAL")` chuyển cho Auto-Healing Coordinator để Dev Agent đưa các biến nhạy cảm vào `.env`.
