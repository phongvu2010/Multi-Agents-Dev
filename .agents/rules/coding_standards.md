# TIÊU CHUẨN MÃ NGUỒN DỰ ÁN (CODING STANDARDS)

## 1. NGUYÊN TẮC CỐT LÕI
- **Ưu tiên Công nghệ Review-Friendly:** Khi bài toán phù hợp, ưu tiên xây dựng trên nền tảng **Python/FastAPI** cho Backend và **React Native / Node.js** cho Frontend/Mobile để hỗ trợ Tech Lead dễ dàng review thủ công.
- **Contract-First:** Không được viết code logic khi chưa có API Contract chuẩn (`openapi.yaml`) được ký duyệt tại Gate 2.
- **SOLID & Clean Architecture:** Tách biệt rõ ràng các tầng: Controller -> Service -> Repository / Data Access -> Models.
- **Strict Typing:**
  - Python: Sử dụng `typing`, `pydantic.BaseModel` chặt chẽ, không dùng `Any` bừa bãi.
  - TypeScript/JavaScript: Sử dụng TypeScript strict mode, định nghĩa interface/type đầy đủ.

## 2. QUY CHUẨN GIT VÀ FILE
- **Conventional Commits:** `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
- **Atomic Changes:** Mỗi commit/PR chỉ giải quyết một sub-task trong DAG.
- **Môi trường & Biến:** Tất cả bí mật và cấu hình môi trường phải nằm trong `.env`, luôn cung cấp `.env.example`.
