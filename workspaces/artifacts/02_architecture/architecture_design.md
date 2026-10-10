# TÀI LIỆU THIẾT KẾ KIẾN TRÚC HỆ THỐNG
**Dự án:** Test_Assessment
**Kiến trúc sư:** System Architect Agent & Tech Lead

## 1. TECH STACK LỰA CHỌN
- **Backend:** Python (FastAPI)
- **Frontend / Mobile:** React Native (TypeScript) / Node.js
- **Database:** PostgreSQL + SQLAlchemy ORM
- **Lý do lựa chọn:** Tối ưu hóa hiệu năng, tương thích hoàn hảo với khả năng review thủ công của Tech Lead.

## 2. KIẾN TRÚC PHÂN TẦNG (CLEAN ARCHITECTURE)
- **API Routers (FastAPI):** Tiếp nhận HTTP Request, xác thực token và validate schema Pydantic.
- **Service Layer:** Xử lý nghiệp vụ lõi độc lập với framework.
- **Data Access Layer (Repository):** Thao tác database qua SQLAlchemy ORM.

[Architecture Sub-Team] Đã xử lý prompt thành công.
