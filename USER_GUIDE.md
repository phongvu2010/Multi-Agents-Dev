# 📖 CẨM NANG HƯỚNG DẪN SỬ DỤNG TEMPLATE MULTI-AGENTS-DEV
### Nền tảng: Google Antigravity 2.0 | Mô hình: Disciplined Vibe Coding

Chào mừng bạn đến với **Multi-Agents-Dev** — hệ thống phát triển phần mềm tự động hóa toàn diện (Multi-Agents SDLC) chạy trên nền tảng **Google Antigravity 2.0**.

Tài liệu này hướng dẫn chi tiết từng bước từ khâu chuẩn bị ý tưởng, thiết lập dự án mới, phối hợp cùng 15 AI Agents thuộc 5 Sub-Teams, kiểm soát chất lượng qua 3 chốt chặn Human-in-the-Loop (HITL), cho đến khi bàn giao thành phẩm hoàn chỉnh.

---

## 🧭 1. TRIẾT LÝ "DISCIPLINED VIBE CODING"

**Vibe Coding** là phương thức phát triển phần mềm mà bạn giao tiếp với AI bằng ngôn ngữ tự nhiên để hiện thực hóa ý tưởng với tốc độ tối đa.

Tuy nhiên, nếu không có kỷ luật kỹ thuật, Vibe Coding sẽ tạo ra "mã nguồn rác" khó bảo trì. Hệ thống **Multi-Agents-Dev** khắc phục điều này bằng:
1. **Phân vai chuyên trách:** 15 AI Agents được chia thành 5 Sub-Teams theo chuẩn SDLC khép kín.
2. **Quyền kiểm soát tối cao của con người:** 3 Chốt chặn (HITL Quality Gates) đảm bảo Tech Lead / PO ký duyệt kiến trúc trước khi viết mã và cấp phép trước khi phát hành.
3. **Mã nguồn chuẩn Clean Architecture:** Phân tầng triệt để (`core/` ➔ `models/` ➔ `schemas/` ➔ `repositories/` ➔ `services/` ➔ `routers/`).
4. **Kiểm thử thực tế (Zero Hallucination):** Toàn bộ test case chạy qua subprocess thật (`pytest-cov` $\ge 80\%$, `alembic check` Zero Schema Drift, Jest unit test và E2E User Journeys).
5. **Định tuyến mô hình tối ưu chi phí (Model Routing):** Phân tầng Pro, Flash, Flash-Lite giúp tiết kiệm 60% – 75% chi phí token.

---

## 🏛️ 2. KIẾN TRÚC 5 SUB-TEAMS & 3 CHỐT CHẶN QUALITY GATES

```text
[Khách hàng / PO: Brief yêu cầu thô]
          │
          ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Sub-Team 1: Product Discovery (Tier: FLASH)                         │
│    • Thành viên: Client Liaison ➔ BA/PO ➔ UI/UX Concept Agent          │
│    • Đầu ra: PRD.md, user_stories.json, clarification_qna.md           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
       🚦 [GATE 1: Phê duyệt PRD trên review_gate_1_prd.md]
                                    │ (Approve)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. Sub-Team 2: Architecture & Planning (Tier: PRO)                     │
│    • Thành viên: System Architect ➔ Security Architect ➔ TPM           │
│    • Đầu ra: architecture_design.md, openapi.yaml, erd.mermaid, DAG    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
 🚦 [GATE 2: Ký duyệt Kiến trúc & API Contract trên review_gate_2.md]
                                    │ (Approve)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. Sub-Team 3: Core Engineering (Tier: PRO / FLASH Hybrid)             │
│    • Thành viên: Backend Engineer ➔ Frontend Engineer ➔ DevOps        │
│    • Đầu ra: Mã nguồn Clean Architecture (FastAPI, React/Mobile, Docker│
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. Sub-Team 4: QA & Security Audit (Tier: FLASH Runner / PRO Audit)   │
│    • Thành viên: QA Automation ➔ DB Auditor ➔ Security ➔ Code Reviewer │
│    • Thẩm định: PyTest (Coverage >= 80%), Alembic Check, Jest E2E      │
│    • Vòng lặp: Auto-Healing sửa lỗi mã nguồn tự động tối đa 3 lần      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
  🚦 [GATE 3: Cấp phép Triển khai trên review_gate_3_deploy.md]
                                    │ (Approve)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 5. Sub-Team 5: Release & Handover (Tier: FLASH-LITE)                   │
│    • Thành viên: Release Engineer ➔ Tech Writer ➔ Handover Lead       │
│    • Đầu ra: Gói ZIP phân phối, Checksum SHA-256, UAT_CHECKLIST, Manual│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 3. QUY TRÌNH TỪNG BƯỚC THIẾT LẬP DỰ ÁN MỚI

### BƯỚC 1: Chuẩn bị Bản Yêu Cầu (Client Brief)

Tạo một file Markdown mô tả yêu cầu trong thư mục `workspaces/`, ví dụ: `workspaces/cliniccare_brief.md`:

```markdown
# ĐẶT TẢ DỰ ÁN: CLINICCARE - ĐẶT KHÁM BỆNH TRỰC TUYẾN

## 1. Mục tiêu sản phẩm
Số hóa quy trình đặt lịch khám cho chuỗi phòng khám y tế ClinicCare.

## 2. Đối tượng người dùng
- Bệnh nhân (Customer)
- Bác sĩ & Lễ tân phòng khám (Staff / Admin)

## 3. Các tính năng cốt lõi MVP (In-Scope)
- Đăng ký và đăng nhập bảo mật bằng số điện thoại (JWT Bearer Token).
- Xem danh mục chuyên khoa khám và bảng giá niêm yết minh bạch.
- Chọn bác sĩ và đặt lịch hẹn theo khung giờ (Slot Booking).
- Quy tắc vận hành (BR-01): Mỗi khung giờ 30 phút chỉ tiếp nhận tối đa 2 bệnh nhân. Nếu quá tải, hệ thống phải từ chối lịch hẹn và gợi ý khung giờ khác.
- Lịch sử đặt khám và tra cứu trạng thái đơn (CONFIRMED, CANCELLED, COMPLETED).
- Thanh toán chuyển khoản qua mã QR động (VietQR).

## 4. Tính năng dành cho tương lai (Out-of-Scope v2.0)
- Tích hợp cổng thanh toán quốc tế Stripe.
- Khám bệnh từ xa qua video call (Telemedicine).
```

---

### BƯỚC 2: Khởi chạy Dự án mới (Khuyên dùng Makefile CLI)

Mở terminal trong thư mục workspace và chạy lệnh:

```bash
# Khởi chạy ứng dụng Web Portal (React Vite / Next.js):
make dev PROJECT="ClinicCare" FILE="workspaces/cliniccare_brief.md" PLATFORM="web"

# Hoặc khởi chạy ứng dụng Mobile App (React Native):
make dev PROJECT="ClinicCare" FILE="workspaces/cliniccare_brief.md" PLATFORM="mobile"
```

> **Giải thích tham số:**
> - `PROJECT="Tên_Dự_Án"`: Tên dự án (dùng để định danh package, DB, models).
> - `FILE="đường_dẫn_brief"`: File Markdown yêu cầu bạn vừa tạo ở Bước 1.
> - `PLATFORM="web" | "mobile"`: Chỉ định rõ nền tảng giao diện frontend mong muốn.

*(Nếu muốn chạy tự động không dừng để kiểm thử CI/CD, dùng: `make dev-quick PROJECT="ClinicCare" PLATFORM="web"`)*

---

### BƯỚC 3: Phê duyệt tại 3 Chốt chặn Human-in-the-Loop (HITL)

Trong quá trình thực thi, hệ thống sẽ dừng lại tại 3 chốt chặn để bạn kiểm tra:

#### 🚦 Chốt chặn 1: Gate 1 (PRD & Scope Approval)
1. Sub-Team 1 hoàn thành bóc tách yêu cầu.
2. Mở file `workspaces/artifacts/review_gate_1_prd.md` trên tab **Artifacts / Auxiliary Pane** (bên phải Antigravity 2.0).
3. Đọc đối chiếu:
   - Mục tiêu SMART và phạm vi In-Scope vs Out-of-Scope.
   - User Stories chuẩn định dạng Gherkin (`Given - When - Then`).
   - Sơ đồ luồng màn hình UI/UX.
4. Trên Terminal, chọn:
   - `[1] Approve:` Tiếp tục chuyển sang Sub-Team 2 thiết kế kiến trúc.
   - `[2] Request Revision:` Nhập phản hồi cụ thể (ví dụ: *"Bổ sung thêm yêu cầu xác thực OTP"*), AI sẽ cập nhật lại.

#### 🚦 Chốt chặn 2: Gate 2 (Architecture & API Sign-off)
1. Sub-Team 2 hoàn thành thiết kế kỹ thuật.
2. Mở file `workspaces/artifacts/review_gate_2_architecture.md`.
3. Kiểm tra:
   - Tech Stack: Xác nhận đúng chuẩn Tech Lead (FastAPI + SQLAlchemy 2.0 + React/React Native).
   - Đặc tả API: Kiểm tra file `workspaces/artifacts/02_architecture/openapi.yaml`.
   - Cơ sở dữ liệu: Kiểm tra sơ đồ quan hệ `erd.mermaid`.
   - Phân tích đe dọa STRIDE và ma trận phân quyền RBAC.
4. Chọn `[1] Approve` để cấp phép cho các Dev Agents bắt đầu viết mã.

#### 🚦 Chốt chặn 3: Gate 3 (Production Deploy Sign-off)
1. Sub-Team 3 viết code và Sub-Team 4 chạy kiểm thử tự động.
2. Mở file `workspaces/artifacts/review_gate_3_deploy.md`.
3. Đối chiếu các chỉ số chất lượng:
   - **Backend PyTest Coverage:** Phải đạt $\ge 80\%$ (ví dụ: $90\%$).
   - **Database Schema Drift:** Báo cáo `Zero Drift` (Models khớp 100% với DB qua `alembic check`).
   - **Frontend Tests:** Unit Test và E2E User Journeys đều báo `PASSED`.
   - **Security Audit:** 0 rò rỉ hardcoded secrets; đạt chuẩn OWASP API Security Top 10.
4. Chọn `[1] Approve` để cấp phép cho Sub-Team 5 đóng gói sản phẩm phát hành.

---

### BƯỚC 4: Vận hành và Kiểm thử Cục bộ (Local Verification)

Sau khi hoàn tất, toàn bộ mã nguồn của dự án nằm tại `workspaces/output_project/`:

```text
workspaces/output_project/
├── backend/            # FastAPI, SQLAlchemy 2.0 models, Alembic migrations, PyTest
├── frontend/           # React Native Mobile hoặc React Vite Web, Jest test suite
└── infra/              # Dockerfile, docker-compose.yml, .env.example
```

#### 1. Chạy toàn bộ kiểm thử tự động:
```bash
make test-all
```
*Lệnh này sẽ chạy: PyTest Backend kèm đo Code Coverage, kiểm tra Schema Drift Database (`alembic check`), và chạy toàn bộ Frontend Unit & E2E Tests.*

#### 2. Khởi chạy Backend FastAPI:
```bash
make run-backend
```
- Mở Swagger UI tương tác tại: [http://localhost:8000/docs](http://localhost:8000/docs)
- Kiểm tra Health check API tại: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

#### 3. Khởi chạy Frontend:
```bash
make run-frontend
```
- **Web Portal:** Truy cập trình duyệt tại `http://localhost:5173`.
- **Mobile App:** Quét mã QR hiển thị bằng ứng dụng Expo Go trên điện thoại.

#### 4. Khởi chạy hệ thống hoàn chỉnh bằng Docker:
```bash
make docker-build          # Đóng gói toàn bộ Multi-Stage Images (Frontend Nginx + Backend FastAPI)
make docker-build-frontend # Đóng gói riêng Frontend Multi-Stage Image (Node.js -> Nginx)
make docker-build-backend  # Đóng gói riêng Backend Image (Python 3.12 / FastAPI)
make docker-up             # Khởi động cụm Multi-container (Web :80 + FastAPI :8000 + PostgreSQL :5432)
make docker-logs           # Theo dõi nhật ký logs thời gian thực
make docker-down           # Dừng và gỡ bỏ containers khi xong việc
```

---

### BƯỚC 5: Tinh chỉnh Mã nguồn & Đồng bộ Checkpoint (`make sync`)

Nếu bạn muốn trực tiếp can thiệp chỉnh sửa mã nguồn hoặc dùng Chat Canvas của Antigravity để code cùng AI:

1. Chỉnh sửa file bất kỳ trong `workspaces/output_project/backend/` hoặc `frontend/`.
2. **Luôn chạy lệnh đồng bộ sau khi sửa:**
   ```bash
   make sync PROJECT="ClinicCare"
   ```
3. **Cơ chế hoạt động:**
   - Bộ **State Synchronizer** sẽ quét lại toàn bộ cây thư mục mã nguồn và artifacts.
   - Tự động chạy lại `pytest` và `alembic check` để đảm bảo code bạn sửa không làm hỏng tính toàn vẹn hệ thống.
   - Cập nhật file Checkpoint tại `workspaces/checkpoints/cliniccare_checkpoint.json`.
   - Nhờ đó, nếu bạn hoặc đồng đội muốn khôi phục chu trình sau này, chỉ cần chạy `make resume PROJECT="ClinicCare"`.

---

### BƯỚC 6: Nghiệm thu & Bàn giao Sản phẩm

Mở thư mục `workspaces/artifacts/05_handover/` để nhận toàn bộ gói phát hành:
- **File nén `.zip`**: Chứa toàn bộ mã nguồn sạch, cấu hình hạ tầng và tài liệu bàn giao.
- **`RELEASE_MANIFEST.json`**: Ghi nhận phiên bản, danh mục file, và mã băm SHA-256 xác thực toàn vẹn.
- **`UAT_CHECKLIST.md`**: Bảng kiểm nghiệm thu tính năng người dùng cuối (dành cho PO và Khách hàng).
- **`USER_MANUAL.md`**: Hướng dẫn cài đặt, cấu hình biến môi trường và vận hành hệ thống.

---

## 💬 4. PHƯƠNG THỨC THAY THẾ: TRIỆU HỒI NATIVE AGENTS QUA CHAT CANVAS

Trong quá trình phát triển, bạn có thể gọi trực tiếp các Sub-Teams bằng cú pháp `@<tên_subteam>` kết hợp cùng các Slash Commands trong khung chat của Antigravity 2.0:

| Sub-Team | Ví Dụ Câu Lệnh Tương Tác |
| :--- | :--- |
| **@discovery_team** | `@discovery_team: /grill-me Hãy phỏng vấn tôi để làm rõ các điểm mâu thuẫn trong file @workspaces/cliniccare_brief.md` |
| **@discovery_team** | `@discovery_team: /plan Bóc tách phạm vi In-Scope MVP và tạo User Stories chuẩn Gherkin.` |
| **@architecture_team** | `@architecture_team: /plan Thiết kế OpenAPI 3.0 và sơ đồ Mermaid ERD chuẩn theo Tech Lead Profile.` |
| **@architecture_team** | `@architecture_team: /boost Thực hiện phân tích mô hình đe dọa bảo mật STRIDE và phân quyền RBAC.` |
| **@engineering_team** | `@engineering_team: /plan Lập trình tính năng đặt lịch khám phân tầng Clean Architecture 5 tầng.` |
| **@engineering_team** | `@engineering_team: /goal Hoàn thiện mã nguồn Backend FastAPI và Frontend TypeScript kèm Jest tests.` |
| **@qa_team** | `@qa_team: Chạy PyTest đo độ phủ Code Coverage, kiểm tra alembic check zero drift và scan Secret Leaks.` |
| **@qa_team** | `@qa_team: Tự động kích hoạt Auto-Healing vá lỗi nếu phát hiện test case thất bại.` |
| **@release_team** | `@release_team: Đóng gói bản phát hành ZIP, tính checksum SHA-256 và lập bảng nghiệm thu UAT_CHECKLIST.md.` |

---

## ⚡ 5. BẢNG TRA CỨU LỆNH NHANH (DEVELOPER CHEAT SHEET)

| Lệnh | Ý Nghĩa & Công Dụng |
| :--- | :--- |
| `make help` | Hiển thị menu hướng dẫn toàn bộ lệnh |
| `make venv` | **Khởi tạo môi trường ảo `.venv` cô lập và tự động cài đặt toàn bộ dependencies** |
| `make install` | Cài đặt/cập nhật thư viện Python (tự động ưu tiên môi trường ảo `.venv` nếu có) |
| `make dev PROJECT=.. FILE=.. PLATFORM=..` | Khởi chạy chu trình SDLC mới từ Brief (có dừng HITL) |
| `make dev-quick PROJECT=.. PLATFORM=..` | Chạy tự động không dừng HITL (Dành cho CI/CD) |
| `make resume PROJECT="Tên"` | Khôi phục chu trình từ Checkpoint gần nhất |
| `make sync PROJECT="Tên"` | **Đồng bộ mã nguồn thực tế ngược vào Checkpoint & State Machine** |
| `make status PROJECT="Tên"` | Báo cáo kiểm tra đối chiếu trạng thái Gates, PyTest, Alembic, Frontend (Unit, E2E, Build) |
| `make backup [PROJECT="Tên"]` | **Sao lưu snapshot toàn bộ mã nguồn `output_project` & `artifacts` vào `workspaces/backups/`** |
| `make clean-project` | **Tự động sao lưu an toàn rồi dọn sạch mã nguồn & artifacts để sẵn sàng cho dự án mới** |
| `make models` | Hiển thị Ma Trận Phân Bổ Mô Hình AI & Tối Ưu Chi Phí Token |
| `make subteams` | Xem danh sách 5 Native Sub-Teams & Kỹ năng |
| `make test-examples` | Chạy bộ kiểm thử của Dự án Mẫu Tham Khảo (`examples/motocare_reference`) |
| `make test-all` | Chạy kiểm thử toàn diện: PyTest Backend, Alembic Drift, Frontend (Unit, E2E & Build) |
| `make test-backend` | Chạy PyTest Backend kèm đo độ phủ Code Coverage (`pytest-cov`) |
| `make cov-html` | Xuất báo cáo HTML trực quan về Code Coverage (`htmlcov/index.html`) |
| `make check-db` | Thẩm định Schema Drift Database (Zero Drift Policy) qua `alembic check` |
| `make test-frontend` | Chạy toàn bộ kiểm thử Frontend (cả Unit Tests, E2E Journeys & Build Check) |
| `make check-frontend-build` | **Thẩm định tính sẵn sàng Production Build của Frontend (`package.json`, `tsconfig.json`)** |
| `make run-backend` | Khởi chạy FastAPI Server tại `http://localhost:8000` |
| `make docker-build [PROJECT=...]` | **Đóng gói toàn bộ Docker Images (Frontend Multi-Stage + Backend)** |
| `make docker-build-frontend` | **Đóng gói riêng Frontend Multi-Stage Image (Node.js -> Nginx SPA)** |
| `make docker-build-backend` | **Đóng gói riêng Backend Image (Python 3.12 / FastAPI)** |
| `make docker-up` | Khởi chạy hệ thống Multi-container bằng Docker Compose (Web:80, API:8000, DB:5432) |
| `make docker-down` | Dừng và gỡ bỏ Docker Compose containers |
| `make docker-logs` | Theo dõi log thời gian thực của Docker Compose |
| `make clean` | Dọn dẹp cache `__pycache__`, `.pytest_cache`, `.db` tạm |

---

## ❓ 6. CẨM NANG XỬ LÝ SỰ CỐ THƯỜNG GẶP (FAQS)

### Q1: Làm thế nào để thay đổi mô hình AI sang Gemini 3.8 Series?
Trong file `.env`, bạn chỉ cần khai báo các biến môi trường:
```env
GEMINI_PRO_MODEL=gemini-3.8-pro
GEMINI_FLASH_MODEL=gemini-3.8-flash
GEMINI_FLASH_LITE_MODEL=gemini-3.8-flash-lite
```
Hệ thống sẽ tự động định tuyến toàn bộ Sub-Teams sang thế hệ mô hình mới nhất.

### Q2: Tôi muốn cấu hình sử dụng PostgreSQL thật thay vì SQLite cho Backend?
Trong file `workspaces/output_project/backend/.env`, chỉnh sửa:
```env
DATABASE_URL=postgresql+asyncpg://postgres:matkhau@localhost:5432/ten_database
```
Hệ thống đã có sẵn `alembic` migrations tương thích 100% với cả SQLite và PostgreSQL.

### Q3: Nếu test bị fail khi chạy `make test-all`, tôi nên làm gì?
1. Đọc stack trace lỗi trực tiếp trên terminal.
2. Bạn có thể sửa trực tiếp trong file mã nguồn rồi chạy `make sync PROJECT="Tên_Dự_Án"`.
3. Hoặc yêu cầu Sub-Team 4 tự động sửa:
   `@qa_team: Test case bị fail tại test_orders.py, hãy phân tích stack trace và kích hoạt Auto-Healing để vá mã nguồn.`

---

> 📘 **Tài liệu tham khảo chuyên sâu:**
> - Cẩm nang nội bộ Tech Lead: [TEAM_PLAYBOOK.md](./TEAM_PLAYBOOK.md)
> - Quy chuẩn nạp Antigravity IDE: [AGENTS.md](./AGENTS.md)
> - Dự án mẫu tham khảo hoàn chỉnh: [examples/motocare_reference/](./examples/motocare_reference/)
