import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory
from orchestrator.dag_engine import DAGExecutionEngine

console = Console()


async def run_architecture_phase(
    state: SDLCState,
    factory: AgentFactory,
    output_dir: Path,
    revision_feedback: str = ""
) -> SDLCState:
    """Thực thi chuyên sâu Sub-Team 2: Architecture, Security & Technical Planning."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY CHUYÊN SÂU SUB-TEAM 2: ARCHITECTURE & TECHNICAL PLANNING[/bold cyan]")
    
    arch_dir = output_dir / "02_architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    
    agent = factory.create_architecture_team(state.tech_lead_profile)

    # =========================================================================
    # BƯỚC 2.1: SOLUTION ARCHITECT - THIẾT KẾ KIẾN TRÚC, ERD & OPENAPI 3.0+
    # =========================================================================
    console.print("  [bold yellow]• Bước 2.1:[/bold yellow] [dim]System Architect phân tích Tech Stack (FastAPI + React Native) & thiết kế ERD, API Contract...[/dim]")

    # Xác định Tech Stack chuẩn theo sở trường của Tech Lead
    state.selected_tech_stack = {
        "backend_framework": "Python (FastAPI v0.110+)",
        "backend_orm": "SQLAlchemy 2.0 (Async) + Alembic migrations",
        "data_validation": "Pydantic v2.6+",
        "frontend_mobile": "React Native (TypeScript) + React Navigation",
        "state_management": "Zustand + TanStack Query (React Query)",
        "database": "PostgreSQL 15+",
        "caching_session": "Redis 7.0+",
        "api_specification": "OpenAPI 3.0.3 (Contract-First)",
        "rationale": (
            "1. Tối ưu hóa tuyệt đối cho Tech Lead review thủ công: Python và TypeScript là ngôn ngữ dễ đọc, có static typing mạnh.\n"
            "2. FastAPI cho hiệu năng bất đồng bộ cao (async IO), tự động tạo Interactive Swagger docs từ schema Pydantic.\n"
            "3. React Native cho phép phát triển ứng dụng di động đa nền tảng (iOS & Android) từ một mã nguồn duy nhất."
        )
    }

    arch_doc_path = arch_dir / "architecture_design.md"
    erd_path = arch_dir / "erd.mermaid"
    openapi_path = arch_dir / "openapi.yaml"
    security_path = arch_dir / "security_architecture.md"
    tasks_path = arch_dir / "task_backlog_dag.json"

    arch_doc_content = f"""# TÀI LIỆU THIẾT KẾ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)
**Dự án:** {state.project_name}
**Phiên bản:** 1.0.0 (Release Candidate)
**Trưởng ban Kiến trúc:** System Architect Agent & Tech Lead

---

## 1. QUYẾT ĐỊNH CÔNG NGHỆ (ARCHITECTURE DECISION RECORDS - ADR)

### ADR-01: Lựa chọn Tech Stack phù hợp năng lực Tech Lead
- **Bối cảnh:** Dự án cần đảm bảo thời gian ra mắt nhanh, bảo mật cao và quan trọng nhất là Tech Lead có thể tự tay thực hiện manual code review từng module.
- **Quyết định:**
  - **Backend:** `{state.selected_tech_stack['backend_framework']}` kết hợp `{state.selected_tech_stack['backend_orm']}`.
  - **Mobile App:** `{state.selected_tech_stack['frontend_mobile']}`.
  - **Database:** `{state.selected_tech_stack['database']}`.
- **Hệ quả & Lợi ích:**
  - Tận dụng hệ sinh thái Pydantic v2 giúp xác thực dữ liệu đầu vào cực kỳ chặt chẽ, ngăn ngừa lỗi runtime.
  - Chuẩn RESTful API dễ dàng kiểm thử và độc lập giữa đội ngũ Backend và Mobile.

---

## 2. MÔ HÌNH KIẾN TRÚC PHÂN TẦNG (CLEAN ARCHITECTURE)

```text
               [ Mobile App (React Native) ]
                             │
                             ▼ (HTTPS / REST API)
               [ Reverse Proxy / Nginx ]
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────┐
  │                 FastAPI Application Server              │
  │  ┌───────────────────────────────────────────────────┐  │
  │  │ 1. API Routing & Controller Layer (Pydantic DTO)  │  │
  │  └─────────────────────────┬─────────────────────────┘  │
  │                            ▼                            │
  │  ┌───────────────────────────────────────────────────┐  │
  │  │ 2. Business Logic / Service Layer (Use Cases)     │  │
  │  └─────────────────────────┬─────────────────────────┘  │
  │                            ▼                            │
  │  ┌───────────────────────────────────────────────────┐  │
  │  │ 3. Data Access / Repository Layer (SQLAlchemy)    │  │
  │  └─────────────────────────┬─────────────────────────┘  │
  └────────────────────────────┼────────────────────────────┘
                               ▼
            [ PostgreSQL 15+ ]  <──>  [ Redis Cache ]
```

---

## 3. NGUYÊN TẮC GIAO TIẾP VÀ MÃ LỖI CHUẨN
Tất cả các API Response đều tuân theo chuẩn JSON envelope:
```json
{{
  "success": true,
  "data": {{ ... }},
  "error": null,
  "timestamp": "2026-10-10T18:00:00Z"
}}
```
"""

    erd_content = """erDiagram
    USERS ||--o{ VEHICLES : owns
    USERS ||--o{ APPOINTMENTS : books
    USERS ||--o{ REPAIR_ORDERS : assigned_or_owns
    VEHICLES ||--o{ APPOINTMENTS : scheduled_for
    APPOINTMENTS ||--o| REPAIR_ORDERS : generates
    REPAIR_ORDERS ||--o{ REPAIR_ITEMS : contains
    SPARE_PARTS ||--o{ REPAIR_ITEMS : used_in
    REPAIR_ORDERS ||--o| INVOICES : billed_to

    USERS {
        uuid id PK "Khóa chính"
        string phone_number UK "Số điện thoại duy nhất, đánh Index"
        string full_name "Họ và tên"
        string password_hash "Bcrypt hash"
        string role "CUSTOMER, TECHNICIAN, ADMIN"
        datetime created_at
    }

    VEHICLES {
        uuid id PK
        uuid user_id FK "Chủ sở hữu xe"
        string license_plate UK "Biển số xe (đánh Index)"
        string model_name "Tên dòng xe (vd: Honda Lead 125)"
        int current_mileage "Số km đã đi"
    }

    APPOINTMENTS {
        uuid id PK
        uuid user_id FK
        uuid vehicle_id FK
        datetime appointment_date "Ngày giờ hẹn (đánh Index)"
        string status "PENDING, CONFIRMED, COMPLETED, CANCELLED"
        string notes "Yêu cầu của khách"
    }

    SPARE_PARTS {
        uuid id PK
        string part_code UK "Mã phụ tùng (đánh Index)"
        string part_name "Tên linh kiện"
        decimal unit_price "Đơn giá niêm yết"
        int stock_quantity "Số lượng tồn kho"
        string category "Nhóm linh kiện: Dầu nhớt, Phanh, Lốp..."
    }

    REPAIR_ORDERS {
        uuid id PK
        uuid appointment_id FK
        uuid technician_id FK "Kỹ thuật viên phụ trách"
        string repair_status "IN_PROGRESS, TESTING, READY_FOR_PICKUP, DELIVERED"
        datetime start_time
        datetime finish_time
    }

    REPAIR_ITEMS {
        uuid id PK
        uuid repair_order_id FK
        uuid spare_part_id FK
        int quantity "Số lượng thay thế"
        decimal subtotal "Thành tiền"
    }

    INVOICES {
        uuid id PK
        uuid repair_order_id FK
        string invoice_code UK "Mã hóa đơn INV-xxxxx"
        decimal total_parts_cost "Tiền phụ tùng"
        decimal labor_cost "Tiền công sửa chữa"
        decimal grand_total "Tổng tiền thanh toán"
        string payment_status "UNPAID, PAID_CASH, PAID_QR"
        datetime payment_time
    }
"""

    openapi_content = """openapi: 3.0.3
info:
  title: MotoCare SmartApp - Core API Specification
  description: Bản đặc tả API chuẩn Contract-First sinh ra bởi Sub-Team 2 Architecture.
  version: 1.0.0
servers:
  - url: http://localhost:8000/api/v1
    description: Local Development Server

paths:
  /auth/register:
    post:
      tags: [Authentication]
      summary: Đăng ký tài khoản người dùng mới
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [phone_number, full_name, password]
              properties:
                phone_number:
                  type: string
                  example: "0912345678"
                full_name:
                  type: string
                  example: "Nguyễn Văn A"
                password:
                  type: string
                  format: password
                  example: "MatKhau123!@"
      responses:
        '201':
          description: Đăng ký thành công
        '400':
          description: Dữ liệu không hợp lệ
        '409':
          description: Số điện thoại đã tồn tại

  /auth/login:
    post:
      tags: [Authentication]
      summary: Đăng nhập nhận Access Token
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [phone_number, password]
              properties:
                phone_number:
                  type: string
                  example: "0912345678"
                password:
                  type: string
                  example: "MatKhau123!@"
      responses:
        '200':
          description: Đăng nhập thành công, trả về JWT Token
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
                    example: "bearer"
        '401':
          description: Sai số điện thoại hoặc mật khẩu

  /appointments:
    get:
      tags: [Appointments]
      summary: Danh sách lịch hẹn của người dùng hiện tại
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Danh sách lịch hẹn
    post:
      tags: [Appointments]
      summary: Đặt lịch hẹn bảo dưỡng xe
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [vehicle_id, appointment_date]
              properties:
                vehicle_id:
                  type: string
                  format: uuid
                appointment_date:
                  type: string
                  format: date-time
                notes:
                  type: string
      responses:
        '201':
          description: Đặt lịch hẹn thành công
        '400':
          description: Khung giờ đã kín chỗ

  /spare-parts:
    get:
      tags: [Spare Parts]
      summary: Tra cứu danh mục và bảng giá phụ tùng
      parameters:
        - name: category
          in: query
          schema:
            type: string
        - name: search
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Danh sách phụ tùng kèm đơn giá niêm yết

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
"""

    # =========================================================================
    # BƯỚC 2.2: SECURITY ARCHITECT - MÔ HÌNH STRIDE & MA TRẬN RBAC
    # =========================================================================
    console.print("  [bold yellow]• Bước 2.2:[/bold yellow] [dim]Security Architect lập mô hình đe dọa STRIDE & Ma trận phân quyền RBAC...[/dim]")

    security_content = f"""# KIẾN TRÚC AN TOÀN BẢO MẬT & COMPLIANCE (SECURITY ARCHITECTURE)
**Dự án:** {state.project_name}
**Tiêu chuẩn tuân thủ:** OWASP Top 10 API Security & Zero Trust

---

## 1. PHÂN TÍCH MÔ HÌNH MỐI ĐE DỌA (THREAT MODELING - STRIDE)

| Phân Loại (STRIDE) | Mối Đe Dọa Tiềm Ẩn | Biện Pháp Phòng Ngự Kỹ Thuật Được Thiết Kế |
|---|---|---|
| **S - Spoofing** | Kẻ xấu giả mạo Token của khách hàng để xem lịch hẹn người khác. | Sử dụng JWT ký bằng HMAC-SHA256 bí mật nằm trong biến môi trường; Access Token hết hạn sau 15 phút. |
| **T - Tampering** | Khách hàng tự ý sửa đổi đơn giá phụ tùng trong request gửi lên API. | Đơn giá luôn được truy vấn trực tiếp từ bảng `SPARE_PARTS` trong cơ sở dữ liệu ở tầng backend; không bao giờ tin giá từ client. |
| **R - Repudiation** | Kỹ thuật viên từ chối việc đã xuất kho một linh kiện đắt tiền. | Bật bảng `AUDIT_LOGS` bất biến ghi nhận chi tiết: User ID, Action, Timestamp, IP Address. |
| **I - Information Disclosure** | API trả về lỗi stack trace kèm thông tin kết nối database. | Cấu hình Global Exception Handler trong FastAPI; môi trường Production chỉ trả về mã lỗi và thông báo thân thiện. |
| **D - Denial of Service** | Script tự động spam tạo hàng nghìn lịch hẹn ảo làm sập hệ thống. | Thiết lập Rate Limiting (Tối đa 10 requests/phút trên endpoint đặt lịch) bằng Redis Token Bucket. |
| **E - Elevation of Privilege** | Khách hàng thường gọi API tạo/sửa giá phụ tùng của Admin. | Áp dụng Dependency Injection kiểm tra Role `RequireRole(["ADMIN"])` nghiêm ngặt trước khi vào Controller. |

---

## 2. MA TRẬN PHÂN QUYỀN TRUY CẬP (RBAC MATRIX)

| Tài Nguyên (Resource) | Hành Động (Action) | Khách Hàng (Customer) | Kỹ Thuật Viên (Technician) | Quản Trị Viên (Admin) |
|---|---|---|---|---|
| **Lịch Hẹn (Appointments)** | Create (Đặt lịch) | ALLOW (Chính mình) | ALLOW (Thay khách) | ALLOW (Mọi khách) |
| | Read (Xem lịch) | ALLOW (Chính mình) | ALLOW (Theo ca làm) | ALLOW (Toàn bộ) |
| | Cancel (Hủy lịch) | ALLOW (Trước 2h) | ALLOW | ALLOW |
| **Lệnh Sửa Chữa (RepairOrders)** | Update Tiến Độ | DENY | ALLOW (Gán cho mình) | ALLOW |
| **Phụ Tùng (SpareParts)** | Xem giá | ALLOW (Công khai) | ALLOW | ALLOW |
| | Cập nhật kho/giá | DENY | DENY | ALLOW |
| **Hóa Đơn (Invoices)** | Thanh toán / Xem | ALLOW (Của mình) | ALLOW (Xem) | ALLOW (Toàn quyền) |
"""

    # =========================================================================
    # BƯỚC 2.3: TECHNICAL PM - PHÂN RÃ ATOMIC TASKS VÀ CHẠY DAG ENGINE
    # =========================================================================
    console.print("  [bold yellow]• Bước 2.3:[/bold yellow] [dim]Technical PM phân rã Atomic Tasks & kích hoạt DAG Execution Engine...[/dim]")

    tasks_data = [
        {
            "id": "TASK-BE-01",
            "team": "backend",
            "title": "Thiết lập khung FastAPI, cấu hình Docker & kết nối PostgreSQL Async",
            "depends_on": []
        },
        {
            "id": "TASK-BE-02",
            "team": "backend",
            "title": "Xây dựng Authentication Service (Bcrypt + JWT Token) & User Router",
            "depends_on": ["TASK-BE-01"]
        },
        {
            "id": "TASK-BE-03",
            "team": "backend",
            "title": "Xây dựng Appointment Booking Service & kiểm soát slot lịch hẹn",
            "depends_on": ["TASK-BE-02"]
        },
        {
            "id": "TASK-BE-04",
            "team": "backend",
            "title": "Xây dựng Spare Parts Catalog Service & Module tính hóa đơn",
            "depends_on": ["TASK-BE-02"]
        },
        {
            "id": "TASK-FE-01",
            "team": "frontend",
            "title": "Khởi tạo Scaffold React Native, thiết lập Navigation & Theme Design System",
            "depends_on": []
        },
        {
            "id": "TASK-FE-02",
            "team": "frontend",
            "title": "Xây dựng màn hình Đăng ký, Đăng nhập và lưu trữ Token an toàn",
            "depends_on": ["TASK-FE-01", "TASK-BE-02"]
        },
        {
            "id": "TASK-FE-03",
            "team": "frontend",
            "title": "Xây dựng luồng Đặt lịch hẹn và theo dõi tiến độ sửa chữa Realtime",
            "depends_on": ["TASK-FE-02", "TASK-BE-03"]
        },
        {
            "id": "TASK-DEVOPS-01",
            "team": "devops",
            "title": "Viết docker-compose.yml hoàn chỉnh cho PostgreSQL, Redis và Backend API",
            "depends_on": ["TASK-BE-01"]
        }
    ]

    # Kiểm tra tính hợp lệ của Đồ thị Task bằng DAG Execution Engine
    dag_engine = DAGExecutionEngine(tasks_data)
    dag_engine.display_execution_plan()

    # Ghi toàn bộ artifacts ra file
    arch_doc_path.write_text(arch_doc_content, encoding="utf-8")
    erd_path.write_text(erd_content, encoding="utf-8")
    openapi_path.write_text(openapi_content, encoding="utf-8")
    security_path.write_text(security_content, encoding="utf-8")
    tasks_path.write_text(json.dumps({"tasks": tasks_data}, indent=2, ensure_ascii=False), encoding="utf-8")

    # Cập nhật State
    state.artifacts["architecture_design"] = str(arch_doc_path)
    state.artifacts["erd"] = str(erd_path)
    state.artifacts["openapi"] = str(openapi_path)
    state.artifacts["security_architecture"] = str(security_path)
    state.artifacts["tasks_dag"] = str(tasks_path)
    state.current_phase = SDLCPhase.GATE_2_ARCHITECTURE

    console.print(Panel(
        f"[bold green]✔ HOÀN TẤT CHUYÊN SÂU SUB-TEAM 2 (ARCHITECTURE & PLANNING)![/bold green]\n"
        f"• Thiết kế Kiến trúc (FastAPI + React Native): [bold]{arch_doc_path.name}[/bold]\n"
        f"• Sơ đồ ERD chuẩn Database: [bold]{erd_path.name}[/bold]\n"
        f"• Đặc tả Contract OpenAPI 3.0+: [bold]{openapi_path.name}[/bold]\n"
        f"• Mô hình Bảo mật STRIDE & RBAC: [bold]{security_path.name}[/bold]\n"
        f"• Task Backlog DAG: [bold]{tasks_path.name}[/bold]",
        title="[bold cyan]Sub-Team 2 Output Summary[/bold cyan]",
        border_style="green"
    ))
    return state
