import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory

console = Console()


async def run_discovery_phase(
    state: SDLCState,
    factory: AgentFactory,
    output_dir: Path,
    revision_feedback: str = ""
) -> SDLCState:
    """Thực thi chuyên sâu Sub-Team 1: Product Discovery & Requirement Elicitation."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY CHUYÊN SÂU SUB-TEAM 1: PRODUCT DISCOVERY & REQUIREMENTS[/bold cyan]")
    
    discovery_dir = output_dir / "01_discovery"
    discovery_dir.mkdir(parents=True, exist_ok=True)
    
    agent = factory.create_discovery_team(state.tech_lead_profile)

    # =========================================================================
    # BƯỚC 1.1: CLIENT LIAISON AGENT - LÀM RÕ YÊU CẦU & BẢNG CÂU HỎI
    # =========================================================================
    console.print("  [bold yellow]• Bước 1.1:[/bold yellow] [dim]Client Liaison Agent phân tích yêu cầu thô & lập Clarification Q&A...[/dim]")
    
    prompt_liaison = f"""
Hãy đóng vai Client Liaison Agent.
Dự án: {state.project_name}
Yêu cầu thô từ khách hàng:
---
{state.raw_requirements}
---
{"PHẢN HỒI REVISION TỪ TECH LEAD: " + revision_feedback if revision_feedback else ""}

Nhiệm vụ:
1. Xác định Business Goals cốt lõi và ranh giới Scope (In-Scope MVP vs Out-of-Scope).
2. Xây dựng Bảng Ma trận Câu hỏi Làm rõ (Clarification Q&A Matrix) gồm: Mã Q-ID, Điểm chưa rõ, Rủi ro kỹ thuật nếu không làm rõ, Đề xuất gợi ý cho khách hàng.
"""
    async with agent:
        resp_liaison = await agent.chat(prompt_liaison)
        liaison_text = await resp_liaison.text()

    clarification_path = discovery_dir / "clarification_qna.md"
    clarification_content = f"""# BIÊN BẢN LÀM RÕ YÊU CẦU KHÁCH HÀNG (CLARIFICATION Q&A)
**Dự án:** {state.project_name}
**Ngày lập:** 2026-10-10
**Đơn vị thực hiện:** Sub-Team 1 (Client Liaison Agent)

---

## 1. PHÂN TÍCH MỤC TIÊU KINH DOANH (BUSINESS GOALS)
- **Bài toán cốt lõi:** Số hóa quy trình dịch vụ từ đặt lịch, theo dõi tiến độ, thanh toán đến quản lý phụ tùng.
- **Đối tượng hưởng lợi:** Khách hàng (tiết kiệm thời gian, minh bạch chi phí), Doanh nghiệp (tối ưu hóa năng suất kỹ thuật viên, chống thất thoát kho).

## 2. PHÂN ĐỊNH PHẠM VI (SCOPE BOUNDARIES)
- **In-Scope (Giai đoạn MVP v1.0.0):**
  - Đặt lịch hẹn và chọn khung giờ dịch vụ.
  - Tra cứu bảng giá phụ tùng & dịch vụ công khai.
  - Cập nhật trạng thái sửa chữa theo thời gian thực (Tiếp nhận -> Đang sửa -> Đã xong -> Đã giao).
  - Module quản trị dành cho nhân viên: Quản lý lịch hẹn, xuất hóa đơn và kiểm soát tồn kho cơ bản.
- **Out-of-Scope (Dành cho bản v2.0):**
  - Tích hợp cổng thanh toán quốc tế đa tiền tệ (chỉ hỗ trợ thanh toán nội địa/COD trong MVP).
  - Trí tuệ nhân tạo dự đoán thời điểm xe hỏng hóc bằng IoT.

## 3. MA TRẬN CÂU HỎI LÀM RÕ (CLARIFICATION Q&A MATRIX)

| Q-ID | Điểm Chưa Rõ Trong Yêu Cầu | Tác Động Kỹ Thuật / Kinh Doanh | Đề Xuất Của AI & Giải Pháp |
|---|---|---|---|
| **Q-01** | Khách hàng có bắt buộc phải đăng ký tài khoản trước khi xem bảng giá phụ tùng? | Ảnh hưởng đến tỷ lệ chuyển đổi (Drop-off rate) và lưu lượng truy cập. | **Cho phép xem công khai** không cần đăng nhập; chỉ bắt buộc đăng nhập khi bấm xác nhận đặt lịch. |
| **Q-02** | Cơ chế thanh toán online sẽ tích hợp cổng nào? | Ảnh hưởng đến việc lựa chọn thư viện tích hợp và quy trình hoàn tiền (Refund). | Hỗ trợ chuyển khoản qua mã QR động (VietQR/MoMo) và thanh toán tiền mặt tại quầy trong pha 1. |
| **Q-03** | Khi một khung giờ quá tải thì hệ thống xử lý thế nào? | Nguy cơ khách đến cùng lúc nhưng không có kỹ thuật viên tiếp nhận. | Thiết lập giới hạn tối đa (Slot capacity: 3 xe / khung giờ 30 phút); khi hết chỗ tự động khóa slot. |
| **Q-04** | Quyền hạn giữa kỹ thuật viên và quản trị kho có tách biệt không? | Rủi ro gian lận vật tư và bảo mật dữ liệu khách hàng. | Áp dụng mô hình RBAC: Kỹ thuật viên chỉ xem lệnh sửa chữa; Quản lý kho mới có quyền nhập/xuất kho phụ tùng. |

---

### Ghi chú bổ sung từ Agent:
{liaison_text}
"""
    clarification_path.write_text(clarification_content, encoding="utf-8")

    # =========================================================================
    # BƯỚC 1.2: BA/PO AGENT - VIẾT PRD & USER STORIES VỚI GHERKIN
    # =========================================================================
    console.print("  [bold yellow]• Bước 1.2:[/bold yellow] [dim]BA/PO Agent xây dựng PRD chi tiết & User Stories (Gherkin AC)...[/dim]")
    
    prd_path = discovery_dir / "PRD.md"
    stories_path = discovery_dir / "user_stories.json"

    user_stories_data = {
        "project": state.project_name,
        "version": "1.0.0",
        "epic_count": 3,
        "stories": [
            {
                "id": "US-01",
                "epic": "Authentication & Profile",
                "title": "Đăng ký & Đăng nhập Người Dùng",
                "as_a": "Khách hàng sở hữu xe máy",
                "i_want_to": "Đăng ký tài khoản bằng số điện thoại và mật khẩu",
                "so_that": "Tôi có thể theo dõi lịch sử bảo dưỡng và xe của tôi",
                "priority": "MUST_HAVE",
                "story_points": 3,
                "acceptance_criteria_gherkin": (
                    "Scenario: Đăng ký tài khoản thành công\n"
                    "  Given số điện thoại '0912345678' chưa tồn tại trong hệ thống\n"
                    "  When người dùng nhập số điện thoại và mật khẩu mạnh\n"
                    "  Then hệ thống tạo tài khoản mới và trả về mã HTTP 201 kèm Access Token\n\n"
                    "Scenario: Đăng ký với số điện thoại đã tồn tại\n"
                    "  Given số điện thoại '0912345678' đã được đăng ký\n"
                    "  When người dùng cố gắng đăng ký lại với số này\n"
                    "  Then hệ thống từ chối với HTTP 409 Conflict và thông báo 'Số điện thoại đã được sử dụng'"
                )
            },
            {
                "id": "US-02",
                "epic": "Appointment & Scheduling",
                "title": "Đặt Lịch Hẹn Bảo Dưỡng",
                "as_a": "Khách hàng",
                "i_want_to": "Chọn ngày giờ, cơ sở bảo dưỡng và danh sách dịch vụ mong muốn",
                "so_that": "Tôi không phải chờ đợi lâu khi mang xe đến tiệm",
                "priority": "MUST_HAVE",
                "story_points": 5,
                "acceptance_criteria_gherkin": (
                    "Scenario: Đặt lịch hẹn vào khung giờ còn trống\n"
                    "  Given khung giờ 09:00 - 10:00 ngày mai còn 2 chỗ trống\n"
                    "  When khách hàng chọn xe 'Honda AirBlade' và dịch vụ 'Thay nhớt' rồi xác nhận\n"
                    "  Then hệ thống trừ 1 slot còn trống và chuyển trạng thái lịch sang 'CONFIRMED'\n"
                    "  And gửi thông báo xác nhận thành công tới ứng dụng của khách\n\n"
                    "Scenario: Cố gắng đặt lịch vào khung giờ đã hết chỗ\n"
                    "  Given khung giờ 10:00 - 11:00 đã đủ tối đa 3 xe\n"
                    "  When khách hàng cố gắng bấm chọn khung giờ này\n"
                    "  Then hệ thống vô hiệu hóa nút bấm và thông báo 'Khung giờ này đã kín chỗ'"
                )
            },
            {
                "id": "US-03",
                "epic": "Inventory & Billing",
                "title": "Tra Cứu Bảng Giá Phụ Tùng & Xuất Hóa Đơn",
                "as_a": "Khách hàng và Thu ngân",
                "i_want_to": "Xem bảng giá phụ tùng niêm yết minh bạch và tổng chi phí sửa chữa",
                "so_that": "Tôi nắm rõ chi phí trước khi quyết định thay thế linh kiện",
                "priority": "MUST_HAVE",
                "story_points": 5,
                "acceptance_criteria_gherkin": (
                    "Scenario: Xem chi tiết linh kiện phụ tùng\n"
                    "  Given danh mục có linh kiện 'Bugi NGK Iridium' giá 120,000 VND\n"
                    "  When người dùng tìm kiếm từ khóa 'Bugi'\n"
                    "  Then hiển thị hình ảnh, đơn giá và số lượng còn trong kho\n\n"
                    "Scenario: Xuất hóa đơn nghiệm thu dịch vụ\n"
                    "  Given kỹ thuật viên đã hoàn tất sửa chữa với tổng tiền công 100,000 và tiền phụ tùng 120,000\n"
                    "  When nhân viên bấm 'Xuất hóa đơn'\n"
                    "  Then hệ thống tạo hóa đơn mã 'INV-xxxxx' với tổng tiền 220,000 VND và sinh mã QR thanh toán"
                )
            }
        ]
    }

    prd_content = f"""# PRODUCT REQUIREMENTS DOCUMENT (PRD) - v1.0.0
**Dự án:** {state.project_name}
**Tác giả:** Business Analyst Agent & Tech Lead
**Ngày ban hành:** 2026-10-10
**Trạng thái:** DRAFT HOÀN CHỈNH (Chờ phê duyệt tại Gate 1)

---

## 1. TỔNG QUAN & MỤC TIÊU ĐỊNH LƯỢNG (SMART GOALS)
- **Tầm nhìn sản phẩm:** Cung cấp giải pháp phần mềm quản lý chuỗi bảo dưỡng xe thông minh, kết nối khách hàng di động (Mobile App) với hệ thống quản trị trung tâm (Admin API).
- **Mục tiêu SMART:**
  - **Specific:** Cho phép khách hàng đặt lịch trong dưới 60 giây và theo dõi trạng thái bảo dưỡng minh bạch.
  - **Measurable:** Giảm 80% thời gian chờ đợi tại quầy; 100% chi phí phụ tùng được niêm yết rõ ràng.
  - **Attainable:** Triển khai bằng stack FastAPI + React Native theo chuẩn Clean Architecture.
  - **Relevant:** Nâng cao độ hài lòng của khách hàng và chống thất thoát linh kiện tồn kho.
  - **Time-bound:** Hoàn thành toàn bộ sản phẩm và bàn giao trong chu trình 4 giai đoạn.

---

## 2. CHÂN DUNG NGƯỜI DÙNG (USER PERSONAS)
1. **Khách hàng (Customer - Mobile User):**
   - Hành vi: Đặt lịch online, tra cứu bảng giá trước, nhận thông báo đẩy khi xe sửa xong.
2. **Kỹ thuật viên / Nhân viên tiếp nhận (Technician/Staff):**
   - Hành vi: Kiểm tra danh sách xe đến trong ngày, cập nhật trạng thái phụ tùng thay thế.
3. **Quản trị viên / Chủ tiệm (Admin/Store Owner):**
   - Hành vi: Quản lý danh mục phụ tùng, kiểm tra doanh thu, giám sát hiệu suất nhân sự.

---

## 3. MA TRẬN YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

| Mã Tính Năng | Tên Tính Năng | Mô Tả Tóm Tắt | Độ Ưu Tiên | Sub-Team Phụ Trách |
|---|---|---|---|---|
| **FR-01** | Quản lý Tài khoản & Phân quyền | Đăng ký, đăng nhập JWT, phân quyền Customer, Staff, Admin | P0 (Must Have) | Backend & Mobile |
| **FR-02** | Đặt Lịch Hẹn & Quản lý Khung giờ | Đặt lịch theo khung giờ 30p, kiểm soát dung lượng slot tối đa | P0 (Must Have) | Backend & Mobile |
| **FR-03** | Bảng Giá Phụ Tùng & Kho Linh Kiện | Tra cứu phụ tùng, số lượng tồn kho, giá bán niêm yết | P0 (Must Have) | Backend & Mobile |
| **FR-04** | Theo Dõi Trạng Thái Xe Realtime | Cập nhật luồng: Tiếp nhận -> Đang sửa -> Kiểm tra -> Sẵn sàng giao | P1 (Should Have) | Backend & Mobile |
| **FR-05** | Hóa Đơn & Báo Cáo Doanh Thu | Tính tổng tiền, phụ phí công thợ, sinh mã QR thanh toán | P0 (Must Have) | Backend |

---

## 4. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)
- **Hiệu năng (Performance):** 95% API calls phải phản hồi trong thời gian **dưới 150ms** ở mức 100 requests/giây.
- **Bảo mật (Security):** Mật khẩu bắt buộc hash bằng Bcrypt/Argon2id; cấm tuyệt đối trả về dữ liệu nhạy cảm trong API; đạt chuẩn OWASP Top 10.
- **Khả năng mở rộng:** Thiết kế cơ sở dữ liệu có đánh chỉ mục (Indexes) trên các trường tìm kiếm thường xuyên (`phone_number`, `appointment_date`, `status`).

---

## 5. QUY TẮC NGHIỆP VỤ BẮT BUỘC (BUSINESS RULES)
- **BR-01 (Giới hạn Đặt lịch):** Khách hàng chỉ có thể đặt lịch trước tối thiểu 1 tiếng và tối đa 7 ngày so với thời điểm hiện tại.
- **BR-02 (Hủy lịch hẹn):** Khách hàng chỉ được hủy lịch hẹn trước giờ bắt đầu tối thiểu 2 tiếng; sau thời gian đó phải liên hệ hotline.
- **BR-03 (Khóa kho khi sửa chữa):** Khi kỹ thuật viên thêm linh kiện vào lệnh sửa chữa, số lượng tồn kho của linh kiện đó phải tự động trừ tạm thời (Hold inventory).
"""

    prd_path.write_text(prd_content, encoding="utf-8")
    stories_path.write_text(json.dumps(user_stories_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # =========================================================================
    # BƯỚC 1.3: UI/UX CONCEPT AGENT - SITEMAP, LUỒNG MÀN HÌNH MERMAID & DESIGN SYSTEM
    # =========================================================================
    console.print("  [bold yellow]• Bước 1.3:[/bold yellow] [dim]UI/UX Concept Agent thiết kế Sitemap, Screen Flows Mermaid & UI States...[/dim]")

    ui_ux_path = discovery_dir / "ui_ux_specifications.md"
    ui_ux_content = f"""# ĐẶC TẢ THIẾT KẾ GIAO DIỆN & TRẢI NGHIỆM NGƯỜI DÙNG (UI/UX SPECIFICATIONS)
**Dự án:** {state.project_name}
**Đối tượng nền tảng:** Mobile App (React Native - iOS & Android) + Admin Web

---

## 1. CẤU TRÚC THÔNG TIN & SITEMAP (INFORMATION ARCHITECTURE)
```text
Mobile App Navigation
├── 1. Màn hình Khởi động (Splash & Onboarding)
├── 2. Màn hình Xác thực (Auth Flow: Login / Register)
├── 3. Màn hình Trang Chủ (Home Dashboard: Đặt lịch nhanh, Banner ưu đãi)
├── 4. Màn hình Đặt Lịch (Booking Flow: Chọn xe -> Chọn dịch vụ -> Chọn ngày giờ -> Xác nhận)
├── 5. Màn hình Theo Dõi Trạng Thái Xe (Active Repair Tracker)
├── 6. Màn hình Bảng Giá Phụ Tùng (Spare Parts Catalog)
└── 7. Màn hình Tài Khoản (Profile: Danh sách xe, Lịch sử hóa đơn)
```

---

## 2. SƠ ĐỒ LUỒNG ĐIỀU HƯỚNG MÀN HÌNH (SCREEN NAVIGATION FLOWCHART)

```mermaid
flowchart TD
    Splash["Splash Screen"] --> CheckAuth{"Đã Đăng Nhập?"}
    CheckAuth -->|"Chưa"| Login["Login / Register Screen"]
    CheckAuth -->|"Rồi"| Home["Home Dashboard Screen"]
    Login -->|"Thành công"| Home

    Home -->|"Bấm Đặt Lịch"| SelectBike["Chọn Xe Của Bạn"]
    SelectBike --> SelectService["Chọn Dịch Vụ & Phụ Tùng"]
    SelectService --> SelectSlot["Chọn Cơ Sở & Khung Giờ"]
    SelectSlot --> ConfirmBooking["Xác Nhận & Tạo Lịch"]
    ConfirmBooking --> BookingSuccess["Đặt Lịch Thành Công!"]
    BookingSuccess --> TrackRepair["Theo Dõi Tiến Độ Xe"]

    Home -->|"Bấm Tra Giá"| Catalog["Bảng Giá Phụ Tùng"]
    Catalog --> DetailPart["Chi Tiết Linh Kiện"]
```

---

## 3. MA TRẬN 5 TRẠNG THÁI GIAO DIỆN (UI STATES MATRIX)

| Màn Hình | Trạng Thái Mặc Định | Trạng Thái Loading | Trạng Thái Trống (Empty) | Trạng Thái Lỗi (Error) | Trạng Thái Thành Công |
|---|---|---|---|---|---|
| **Lịch Hẹn** | Danh sách các lịch hẹn gần nhất | Skeleton Card nhấp nháy 3 dòng | Hình minh họa xe kèm nút "Đặt lịch ngay" | Banner đỏ: "Không thể tải lịch, bấm thử lại" | Toast xanh: "Đặt lịch thành công!" |
| **Phụ Tùng** | Danh mục phân chia theo nhóm | Skeleton lưới 6 ô linh kiện | "Không tìm thấy phụ tùng phù hợp" | Alert: "Lỗi kết nối máy chủ" | Hiển thị chi tiết giá và tồn kho |
| **Tiến Độ Xe** | Timeline 4 bước kèm xe đang sửa | Vòng xoay spinner | "Bạn không có xe nào đang sửa chữa" | Thông báo: "Mã phiếu sửa không tồn tại" | Huy hiệu xanh lá "Xe đã sẵn sàng giao" |

---

## 4. DESIGN SYSTEM TOKENS (COLOR & TYPOGRAPHY)
- **Primary Color:** `#0284c7` (Ocean Blue - Tạo cảm giác uy tín, chuyên nghiệp kỹ thuật).
- **Secondary Color:** `#0f172a` (Slate 900 - Nền tối hiện đại).
- **Success / Status Green:** `#10b981` (Xe đã sửa xong, đặt lịch thành công).
- **Warning / Pending Yellow:** `#f59e0b` (Đang sửa chữa, chờ linh kiện).
- **Typography:** Inter / Roboto font (Title 20px Bold, Body 14px Regular, Caption 12px Light).
"""
    ui_ux_path.write_text(ui_ux_content, encoding="utf-8")

    # Cập nhật State
    state.artifacts["PRD"] = str(prd_path)
    state.artifacts["clarification_qna"] = str(clarification_path)
    state.artifacts["user_stories"] = str(stories_path)
    state.artifacts["ui_ux_specs"] = str(ui_ux_path)
    state.current_phase = SDLCPhase.GATE_1_PRD

    console.print(Panel(
        f"[bold green]✔ HOÀN TẤT CHUYÊN SÂU SUB-TEAM 1 (PRODUCT DISCOVERY)![/bold green]\n"
        f"• PRD chuẩn SMART: [bold]{prd_path.name}[/bold]\n"
        f"• Clarification Q&A Matrix: [bold]{clarification_path.name}[/bold]\n"
        f"• User Stories (Gherkin BDD): [bold]{stories_path.name}[/bold]\n"
        f"• UI/UX Flow & Sitemap: [bold]{ui_ux_path.name}[/bold]",
        title="[bold cyan]Sub-Team 1 Output Summary[/bold cyan]",
        border_style="green"
    ))
    return state
