# PRODUCT REQUIREMENTS DOCUMENT (PRD)
**Dự án:** Test_Assessment
**Ngày tạo:** 2026-10-09
**Người phê duyệt yêu cầu:** Tech Lead / Product Owner

## 1. TỔNG QUAN & MỤC TIÊU
Chúng tôi muốn xây dựng ứng dụng di động cho phép khách hàng đặt lịch hẹn bảo dưỡng xe máy, nhận thông báo khi xe sửa xong, xem bảng giá phụ tùng minh bạch và thanh toán online hoặc tại quầy. Hệ thống cần có trang quản trị cho nhân viên tiếp nhận xe và quản lý kho linh kiện.

## 2. PHẠM VI (SCOPE)
- **In-Scope:** Các tính năng cốt lõi được mô tả trong yêu cầu thô đã được chuẩn hóa.
- **Out-of-Scope:** Mở rộng bên ngoài chưa được khách hàng xác nhận.

## 3. USER STORIES & ACCEPTANCE CRITERIA (GHERKIN)
### US-01: Khởi tạo và Quản trị
- **Là một:** Người dùng hệ thống
- **Tôi muốn:** Đăng nhập an toàn và truy cập các tính năng chính
- **Để:** Sử dụng dịch vụ nhanh chóng và bảo mật

```gherkin
Scenario: Đăng nhập thành công
  Given người dùng đã có tài khoản hợp lệ
  When gửi thông tin xác thực đến hệ thống
  Then hệ thống trả về mã token JWT và thông tin tài khoản
```

[Discovery Sub-Team] Đã xử lý prompt thành công.
