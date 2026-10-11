# 📘 DEVELOPER TEAM PLAYBOOK — HƯỚNG DẪN VẬN HÀNH MULTI-AGENTS SDLC
### Nền tảng: Google Antigravity 2.0 | Mô hình: Disciplined Vibe Coding

Chào mừng toàn thể các kỹ sư phần mềm, Tech Lead, Product Owner (PO), và QA gia nhập không gian làm việc **Multi-Agents-Dev**.

Tài liệu này là cẩm nang hướng dẫn thực chiến giúp toàn bộ đội ngũ phối hợp hiệu quả với **15 AI Agents** thuộc **5 Sub-Teams** theo chu trình SDLC khép kín.

---

## 🧭 1. TRIẾT LÝ "DISCIPLINED VIBE CODING"

**Vibe Coding** là phương thức phát triển phần mềm mà lập trình viên tương tác với AI bằng ngôn ngữ tự nhiên để hiện thực hóa ý tưởng với tốc độ tối đa.

Tuy nhiên, nếu không có kỷ luật, Vibe Coding sẽ tạo ra "mã nguồn rác" (unmaintainable code). Tại dự án của chúng ta:
1. **AI làm việc theo Phân vai & SDLC:** Không dùng 1 prompt dài để sinh toàn bộ dự án. Dự án được chia nhỏ qua 5 Sub-Teams chuyên biệt.
2. **Kiểm soát bằng 3 Chốt chặn Con người (HITL Quality Gates):** Con người giữ vai trò phê duyệt kiến trúc và cấp phép phát hành; AI tự chủ viết code và test.
3. **Mã nguồn chuẩn Clean Architecture:** Phân tầng triệt để, dễ đọc, dễ bảo trì cho Tech Lead.
4. **Kiểm thử thực tế (Zero Hallucination):** Toàn bộ test case phải chạy qua subprocess thật (`pytest` và `node run_tests.cjs`).

---

## 🏛️ 2. PHÂN VAI 5 SUB-TEAMS VÀ CÁCH TRIỆU HỒI TRONG ANTIGRAVITY 2.0

Bạn có thể triệu hồi trực tiếp các Sub-Teams qua **Chat Canvas** của Antigravity 2.0:

```text
[Khách hàng / PO: Brief yêu cầu]
         │
         ▼
1. @discovery_team     ➔ Bóc tách PRD, Gherkin Stories, UI/UX Specs
         ▼
   [GATE 1: Phê duyệt PRD trên review_gate_1_prd.md]
         │
         ▼
2. @architecture_team  ➔ Thiết kế OpenAPI, ERD, Threat Model, DAG Tasks
         ▼
   [GATE 2: Ký duyệt API & Kiến trúc trên review_gate_2_architecture.md]
         │
         ▼
3. @engineering_team   ➔ Sinh Backend Clean Architecture, Frontend Web/Mobile, Docker
         ▼
4. @qa_team            ➔ Chạy PyTest, Alembic check, Jest/Node runner, Auto-Healing
         ▼
   [GATE 3: Cấp phép Triển khai trên review_gate_3_deploy.md]
         │
         ▼
5. @release_team       ➔ Đóng gói Release ZIP, Manifest, UAT Checklist, Manual
```

### Cách gọi Native Sub-Teams & Kết hợp Slash Commands trong Chat Canvas:
- **Khởi tạo yêu cầu (@discovery_team):**
  - `@discovery_team: /grill-me Phỏng vấn tôi để làm rõ các điểm mâu thuẫn trong file @sample_client_brief.md.`
  - `@discovery_team: /plan Bóc tách phạm vi In-Scope MVP và tạo User Stories chuẩn Gherkin.`
- **Thiết kế kiến trúc (@architecture_team):**
  - `@architecture_team: /plan Thiết kế OpenAPI 3.0 và Mermaid ERD bám sát Tech Lead Profile.`
  - `@architecture_team: /boost Thực hiện phân tích mô hình bảo mật STRIDE và phân quyền RBAC.`
- **Phát triển tính năng (@engineering_team):**
  - `@engineering_team: /plan Lập trình phân tầng Clean Architecture cho tính năng đặt lịch.`
  - `@engineering_team: /goal Hoàn thiện toàn bộ mã nguồn Backend FastAPI và Frontend React Native kèm Jest tests.`
- **Kiểm định chất lượng (@qa_team):**
  - `@qa_team: Chạy PyTest kèm đo Code Coverage (pytest-cov), kiểm tra alembic check zero drift và scan Secret Leaks.`
  - `@qa_team: Tự động kích hoạt Auto-Healing vá lỗi nếu phát hiện test case thất bại.`
- **Bàn giao phát hành (@release_team):**
  - `@release_team: Đóng gói lại bản release v1.0.0 kèm UAT Checklist và RELEASE_MANIFEST.json.`

---

## ⚡ 3. BẢNG TRA CỨU LỆNH NHANH (DEVELOPER COMMAND CHEAT SHEET)

Tất cả các thao tác thường ngày đã được chuẩn hóa qua `Makefile`:

| Lệnh | Ý Nghĩa & Mục Đích |
| :--- | :--- |
| `make help` | Hiển thị menu hướng dẫn tất cả các lệnh khả dụng |
| `make venv` | **Khởi tạo môi trường ảo `.venv` cô lập và tự động cài đặt toàn bộ dependencies** |
| `make install` | Cài đặt/cập nhật thư viện Python (tự động ưu tiên môi trường ảo `.venv` nếu có) |
| `make dev [PROJECT=... FILE=... PLATFORM=web|mobile]` | Khởi chạy chu trình SDLC từ yêu cầu thô (có dừng HITL, hỗ trợ chỉ định nền tảng) |
| `make dev-quick [PROJECT=... PLATFORM=web|mobile]` | Chạy tự động không dừng (Bypass HITL - Dành cho kiểm thử CI/CD) |
| `make resume PROJECT="Tên"` | Khôi phục chu trình SDLC từ Checkpoint gián đoạn gần nhất |
| `make sync PROJECT="Tên"` | **Đồng bộ hóa mã nguồn thực tế ngược vào Checkpoint & State Machine** |
| `make status PROJECT="Tên"` | Kiểm tra đối chiếu trạng thái Gate, PyTest (Coverage), Alembic Drift, Frontend (Unit+E2E, Build) |
| `make backup [PROJECT="Tên"]` | **Sao lưu snapshot toàn bộ mã nguồn `output_project` & `artifacts` vào `workspaces/backups/`** |
| `make clean-project` | **Tự động sao lưu an toàn rồi dọn sạch mã nguồn & artifacts để sẵn sàng cho dự án mới** |
| `make models` | **Hiển thị Ma Trận Phân Bổ Mô Hình AI & Tối Ưu Chi Phí Token (Model Matrix)** |
| `make subteams` | Xem danh sách 5 Native Sub-Teams & Kỹ năng |
| `make test-examples` | **Chạy bộ kiểm thử của Dự án Mẫu Tham Khảo (examples/motocare_reference)** |
| `make test-all` | Thực thi kiểm thử toàn diện Backend (PyTest Coverage), DB check & Frontend (Unit, E2E, Build) |
| `make test-backend` | Chạy bộ kiểm thử PyTest Backend FastAPI kèm đo độ phủ Code Coverage |
| `make cov-html` | Xuất báo cáo trực quan Code Coverage dạng HTML (`htmlcov/index.html`) |
| `make check-db` | **Thẩm định Schema Drift Database (Zero Drift Policy) qua `alembic check`** |
| `make test-frontend` | Chạy toàn bộ kiểm thử Frontend qua Node runner (Unit Tests, E2E Journeys, Build Check) |
| `make test-frontend-unit` | Chạy riêng bộ kiểm thử Unit Tests Frontend (`run_tests.cjs`) |
| `make test-frontend-e2e` | **Chạy bộ kiểm thử Frontend End-to-End thực tế (`run_e2e_tests.cjs`)** |
| `make check-frontend-build` | **Thẩm định tính sẵn sàng Production Build của Frontend (`package.json`, `tsconfig.json`)** |
| `make run-backend` | Khởi chạy FastAPI Uvicorn Server tại `http://localhost:8000` |
| `make run-frontend` | Khởi chạy Frontend Dev Server (Expo Mobile hoặc Vite Web) |
| `make docker-build [PROJECT=...]` | **Đóng gói Docker Image độc lập cho Backend** |
| `make docker-up` | **Khởi chạy hệ thống multi-container bằng Docker Compose (FastAPI + PostgreSQL)** |
| `make docker-down` | **Dừng và gỡ bỏ toàn bộ Docker Compose containers** |
| `make docker-logs` | **Theo dõi log thời gian thực của Docker Compose** |
| `make clean` | Dọn dẹp cache `__pycache__`, `.pytest_cache`, `.pyc`, coverage, database |

---

## 🔄 4. QUY TRÌNH LÀM VIỆC HÀNG NGÀY CỦA DEVELOPER (DAILY WORKFLOWS)

### 📌 Luồng 1: Khởi tạo dự án mới từ Client Brief
1. Khách hàng hoặc PO chuẩn bị file yêu cầu (ví dụ: `workspaces/sample_client_brief.md`).
2. Khởi chạy dự án (có thể chỉ định rõ nền tảng `PLATFORM="web"` hoặc `PLATFORM="mobile"`):
   ```bash
   make dev PROJECT="EduMaster_App" FILE="workspaces/sample_client_brief.md" PLATFORM="web"
   ```
3. Khi đến từng Gate, kiểm tra tài liệu tương tác trên **Auxiliary Pane** (bên phải giao diện Antigravity 2.0):
   - **Gate 1:** Mở `workspaces/artifacts/review_gate_1_prd.md`
   - **Gate 2:** Mở `workspaces/artifacts/review_gate_2_architecture.md`
   - **Gate 3:** Mở `workspaces/artifacts/review_gate_3_deploy.md`
4. Lựa chọn:
   - `[1] Approve:` Tiếp tục sang Sub-Team kế tiếp.
   - `[2] Request Revision:` Nhập phản hồi cụ thể để AI tự kích hoạt Auto-Healing vá lỗi.

---

### 📌 Luồng 2: Tinh chỉnh cục bộ mã nguồn & Đồng bộ Checkpoint (`make sync`)
Khi bạn muốn can thiệp code trực tiếp hoặc dùng Chat Canvas của Antigravity (`@engineering_team`):
1. Bạn chỉnh sửa file trong `workspaces/output_project/backend/` hoặc `frontend/`.
2. **QUAN TRỌNG:** Sau khi sửa xong, luôn chạy lệnh:
   ```bash
   make sync PROJECT="EduMaster_App"
   ```
   *Lệnh này sẽ tự động:*
   - Quét lại toàn bộ cây thư mục mã nguồn và artifacts.
   - Chạy PyTest backend và kiểm tra tính toàn vẹn của Alembic migrations.
   - Chạy Frontend test runner và quét Secret leaks.
   - Cập nhật `test_summary.json` và ghi đè trạng thái chính xác vào file Checkpoint `workspaces/checkpoints/edumaster_app_checkpoint.json`.
3. Nhờ đó, nếu người khác chạy `make resume`, hệ thống sẽ tiếp tục từ đúng trạng thái bạn vừa sửa!

---

### 📌 Luồng 3: Chạy và debug cục bộ (Local Debugging)
- **Backend (FastAPI Swagger UI):**
  ```bash
  make run-backend
  # Truy cập Swagger UI tại: http://localhost:8000/docs
  # Health check: http://localhost:8000/api/v1/health
  ```
- **Frontend (Web hoặc Mobile):**
  ```bash
  make run-frontend
  # Nếu là Web Portal: Mở trình duyệt tại http://localhost:5173
  # Nếu là Mobile App: Quét mã QR bằng ứng dụng Expo Go trên điện thoại
  ```

---

## 📐 5. TIÊU CHUẨN MÃ NGUỒN CLEAN ARCHITECTURE (TECH LEAD STANDARD)

Tất cả mã nguồn sinh ra bởi AI hoặc do kỹ sư viết thêm PHẢI tuân thủ các quy tắc sau:

### 1. Phân tầng Backend (Python / FastAPI):
- `app/core/`: Chứa cấu hình (`config.py` đọc qua Pydantic `SettingsConfigDict`), kết nối DB (`database.py`), bảo mật JWT (`security.py`), và quản lý migration (`migration_manager.py`).
- `app/models/`: Chứa các SQLAlchemy 2.0 Declarative Mapped Models (`class Item(Base): ...`). **Tuyệt đối không viết raw SQL trong router.**
- `app/schemas/`: Chứa Pydantic v2 DTOs (Request / Response validation).
- `app/repositories/`: Chứa tầng tương tác dữ liệu (CRUD operations với DB Session).
- `app/services/`: Chứa nghiệp vụ kinh doanh cốt lõi (Business Logic & Rule validations).
- `app/routers/`: Chứa API endpoints mỏng (chỉ nhận request, gọi service, trả response status).
- `alembic/`: Chứa `env.py`, `alembic.ini` và các file `versions/*.py`. Khi sửa model, luôn tạo script migration mới.

### 2. Cấu trúc Frontend (React Native Mobile hoặc React Vite Web):
- `src/api/client.ts`: Sử dụng Axios client có cấu hình timeout và baseURL từ biến môi trường.
- `src/store/appStore.ts`: Quản lý client state tập trung.
- `src/screens/` hoặc `src/components/`: Tách biệt UI hiển thị và business logic.
- `__tests__/App.test.tsx`: Bộ test Jest kiểm tra component rendering và quy tắc nghiệp vụ.

---

## 🛠️ 6. CẨM NANG XỬ LÝ SỰ CỐ (TROUBLESHOOTING & FAQS)

### Q1: PyTest báo lỗi khi chạy kiểm thử?
- **Nguyên nhân:** Có thể thiếu module path hoặc dữ liệu test bị trùng lặp.
- **Cách xử lý:** 
  1. Chạy `make test-backend` để xem chi tiết stack trace.
  2. Kiểm tra xem database SQLite test có bị khóa không: chạy `make clean`.
  3. Yêu cầu Sub-Team 4 tự sửa: `@qa_team: PyTest bị fail tại test_orders.py, hãy phân tích stack trace và áp bản vá Auto-Healing.`

### Q2: Checkpoint bị lệch trạng thái so với code trên đĩa?
- **Cách xử lý:** Chạy ngay `make sync PROJECT="Tên_Du_An"`. Bộ State Synchronizer sẽ tự động tái thẩm định toàn bộ hệ thống và ghi đè checkpoint đồng bộ 100%.

### Q3: Làm sao để chuyển từ SQLite sang PostgreSQL trên Production?
- Trong file `workspaces/output_project/backend/.env` (hoặc biến môi trường), cập nhật:
  ```env
  DATABASE_URL=postgresql+asyncpg://postgres:matkhau@localhost:5432/ten_database
  ```
  Hệ thống tự động sử dụng driver PostgreSQL và chạy Alembic migrations tương ứng.

---

## 🎯 7. CHECKLIST HOÀN THÀNH MỖI DỰ ÁN (DEFINITION OF DONE - DOD)
Trước khi bàn giao bản release cho khách hàng, đảm bảo:
- [ ] Cả 3 Quality Gates đã được ký duyệt (`APPROVED`).
- [ ] `make test-all` vượt qua 100% test cases (Zero failures).
- [ ] Không có hardcoded secrets trong mã nguồn (`make status` báo Security Scan PASSED).
- [ ] Gói `.zip` phát hành và `RELEASE_MANIFEST.json` đã sẵn sàng trong `workspaces/artifacts/05_handover/`.
- [ ] Bảng kiểm `UAT_CHECKLIST.md` đã được đối chiếu đầy đủ với yêu cầu ban đầu.
