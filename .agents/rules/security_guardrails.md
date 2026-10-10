# QUY CHUẨN BẢO MẬT (SECURITY GUARDRAILS)

## 1. BẢO VỆ DỮ LIỆU VÀ BÍ MẬT
- **Zero Hardcoded Credentials:** Nghiêm cấm đặt API Keys, JWT Secrets, Database Passwords trực tiếp trong source code. Vi phạm này tự động dẫn đến REJECT ở bước Code Review.
- **Secure Password Hashing:** Luôn sử dụng bcrypt hoặc argon2 để hash mật khẩu. Không bao giờ lưu trữ mật khẩu dạng plain text hoặc MD5/SHA1.

## 2. PHÒNG CHỐNG OWASP TOP 10
- **SQL Injection:** Luôn sử dụng ORM (SQLAlchemy, Prisma...) hoặc Parameterized Queries. Tuyệt đối không nối chuỗi (string concatenation) trong câu lệnh SQL.
- **Cross-Site Scripting (XSS):** Làm sạch (sanitize) mọi input từ người dùng trước khi hiển thị.
- **Access Control (Broken Object Level Authorization - BOLA):** Mỗi endpoint truy vấn tài nguyên phải kiểm tra xem user hiện tại có quyền sở hữu (ownership) tài nguyên đó hay không.
- **Rate Limiting:** Bắt buộc có cơ chế giới hạn tần suất yêu cầu trên các endpoint xác thực (`/login`, `/register`, `/forgot-password`).
