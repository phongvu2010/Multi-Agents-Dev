# AGENTS.md — HƯỚNG DẪN HỆ THỐNG MULTI-AGENTS SDLC (ANTIGRAVITY 2.0)

Chào mừng bạn đến với Không gian làm việc **Multi-Agents-Dev** chạy trên nền tảng **Google Antigravity 2.0**.

Tài liệu này được tự động nạp bởi Antigravity 2.0 IDE để định hình hành vi, phân quyền và tiêu chuẩn kỹ thuật cho toàn bộ các tác tử AI khi tham gia phát triển dự án.

---

## 🏛️ 1. CƠ CẤU 5 SUB-TEAMS (15 AGENTS)

Khi nhận yêu cầu phần mềm từ người dùng hoặc khách hàng, hệ thống hoạt động theo 5 Sub-Teams chuyên biệt (được định nghĩa native tại `.agents/subteams/`):

1. **Sub-Team 1: Product Discovery & Requirements (`.agents/subteams/subteam_1_discovery.md`)**
   - **Thành viên:** Client Liaison Agent, BA/PO Agent, UI/UX Concept Agent.
   - **Kỹ năng sử dụng:** `requirement-parser`, `gherkin-generator`.
   - **Đầu ra (Artifacts):** `PRD.md`, `user_stories.json`, `clarification_qna.md`, `ui_ux_specifications.md`.
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 1 (PRD Approval)** chờ Tech Lead / PO ký duyệt tại file interactive `review_gate_1_prd.md`.

2. **Sub-Team 2: Architecture & Technical Planning (`.agents/subteams/subteam_2_architecture.md`)**
   - **Thành viên:** System Architect Agent, Security Architect Agent, Technical PM Agent.
   - **Kỹ năng sử dụng:** `api-contract-validator`, `threat-modeling`.
   - **Đầu ra (Artifacts):** `architecture_design.md`, `openapi.yaml`, `erd.mermaid`, `security_architecture.md`, `task_backlog_dag.json`.
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 2 (Architecture & API Sign-off)** chờ Tech Lead duyệt tại `review_gate_2_architecture.md`.

3. **Sub-Team 3: Core Engineering & Implementation (`.agents/subteams/subteam_3_engineering.md`)**
   - **Thành viên:** Backend Engineer Agent, Frontend/Mobile Engineer Agent, DevOps Engineer Agent.
   - **Động cơ điều phối:** **DAG Execution Engine** phân rã các đợt thực thi song song (Execution Waves) kết hợp **Hybrid Synthesis Engine** (Cân bằng Heuristic Context + Deep LLM Dynamic Code Synthesis).
   - **Chuẩn mã nguồn Backend:** Clean Architecture 5 tầng (`core/` -> `models/` -> `schemas/` -> `repositories/` -> `services/` -> `routers/`) tích hợp **SQLAlchemy 2.0 ORM**, Pydantic v2 và **Alembic Database Migrations**.
   - **Chuẩn mã nguồn Frontend (Linh hoạt Web & Mobile):**
     - **Web Portal:** **React Vite / Next.js (TypeScript)** với responsive components (`Navbar`, `CatalogView`, `BookingForm`, `OrderTracker`), REST API Client, Store và Jest test suite.
     - **Mobile App:** **React Native (TypeScript)** đa màn hình (`AuthScreen`, `CatalogScreen`, `BookingScreen`, `TrackingScreen`), Navigation và Jest test suite.
   - **Đầu ra:** Mã nguồn hoàn chỉnh tại `workspaces/output_project/` (Backend FastAPI, Frontend Web/Mobile TypeScript, Docker).

4. **Sub-Team 4: Quality Assurance & Security Audit (`.agents/subteams/subteam_4_qa.md`)**
   - **Thành viên:** QA Automation Agent, Code Reviewer Agent, Security Auditor Agent, Database Auditor Agent.
   - **Kỹ năng sử dụng:** `test-runner`, `code-review-evaluator`, `secret-scanner`.
   - **Cơ chế kiểm thử ba lớp nâng cao (Triple Verification & Quality Metrics):** 
     - **Backend:** Chạy thực tế `pytest` qua subprocess tích hợp **Code Coverage tự động (`pytest-cov`)**, bắt buộc đạt tối thiểu **>= 80% coverage**.
     - **Database:** Thẩm định tính toàn vẹn của Alembic Migrations và **kiểm soát Schema Drift bằng `alembic check` (Zero Drift Policy)**.
     - **Frontend (Web/Mobile):** Kiểm tra cấu trúc đa màn hình / components, TypeScript AST, **Jest Unit Test Suite (`run_tests.cjs`)**, và **Kiểm thử End-to-End User Journeys qua Subprocess (`run_e2e_tests.cjs`)**.
     - **Security:** Quét tĩnh Secret Leaks & kiểm toán OWASP API Security Top 10.
   - ⟳ **Auto-Healing Loop:** Nếu phát hiện lỗi (Defect Ticket), tự động trích xuất traceback, áp bản vá trực tiếp vào mã nguồn tối đa 3 lần.
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 3 (Production Deploy Sign-off)** tại `review_gate_3_deploy.md`.

5. **Sub-Team 5: Release & Client Handover (`.agents/subteams/subteam_5_release.md`)**
   - **Thành viên:** Release Engineer Agent, Tech Writer Agent, Client Handover Lead Agent.
   - **Kỹ năng sử dụng:** `uat-checklist-builder`.
   - **Đầu ra:** Gói phân phối nén `.zip` trong `workspaces/artifacts/05_handover/`, `UAT_CHECKLIST.md`, `USER_MANUAL.md`, `RELEASE_MANIFEST.json`.

---

## 👨‍💻 2. HỒ SƠ TECH LEAD & TIÊU CHUẨN CÔNG NGHỆ (TECH LEAD PROFILE)

Hệ thống được thiết kế tối ưu cho việc **Manual Review của Tech Lead**. Toàn bộ các Subagents PHẢI ưu tiên lựa chọn:

- **Backend Framework:** `Python (FastAPI v0.110+)`
- **ORM / Database Access:** `SQLAlchemy 2.0` Declarative Mapped Models + Repositories Pattern
- **Database Migrations:** `Alembic 1.13+` Version-Controlled Schema Migrations kèm `alembic check`
- **Testing & Coverage:** `PyTest 8.0+` kèm `pytest-cov` (Ngưỡng >= 80% Coverage) + `Jest`
- **Frontend / Web & Mobile:** `React Native (TypeScript)` (Mobile) hoặc `Next.js / React Vite (TypeScript)` (Web) + `Jest`
- **Database:** `PostgreSQL 15+` (production) & `SQLite` (local/testing)
- **Kiến trúc mã nguồn:** Phân tầng triệt để Clean Architecture (`core/` -> `models/` -> `schemas/` -> `repositories/` -> `services/` -> `routers/`).
- **Tích hợp MCP Servers:** Khai thác `gemini-api_gemini-api-docs` cho API specs và `gemini-notebook-mcp` cho domain research.

---

## 🚦 3. QUY TRÌNH DUYỆT HUMAN-IN-THE-LOOP (HITL) TRONG ANTIGRAVITY 2.0

Khi chạy trong IDE hoặc qua CLI Runner, hệ thống tự động sinh tài liệu đánh giá tương tác:
- **Gate 1:** Kiểm tra `workspaces/artifacts/review_gate_1_prd.md` và `PRD.md` trên tab Artifacts.
- **Gate 2:** Kiểm tra `workspaces/artifacts/review_gate_2_architecture.md`, `openapi.yaml` và `erd.mermaid`.
- **Gate 3:** Kiểm tra `workspaces/artifacts/review_gate_3_deploy.md`, `test_summary.json` và `security_audit_report.md`.

---

## 🛠️ 4. CÁCH THỰC THI TRONG ANTIGRAVITY 2.0 IDE

### Cách 1: Triệu hồi Native Subagents qua Chat Canvas của Antigravity 2.0
Các Subagents đã được cấu hình native tại `.agents/subteams/`. Bạn có thể tương tác trực tiếp bằng cách gõ `@<tên_subteam>` kết hợp cùng các Slash Commands:

- **Sub-Team 1 (Discovery):**
  - `@discovery_team: /grill-me Phỏng vấn tôi để làm rõ các yêu cầu nghiệp vụ còn mâu thuẫn trong file @sample_client_brief.md`
  - `@discovery_team: /plan Bóc tách phạm vi In-scope MVP và xuất bộ User Stories chuẩn Gherkin.`
- **Sub-Team 2 (Architecture):**
  - `@architecture_team: /plan Thiết kế API OpenAPI 3.0 và Mermaid ERD theo sở trường Tech Lead (FastAPI + React Native).`
  - `@architecture_team: /boost Phân tích mô hình đe dọa STRIDE và thiết lập ma trận phân quyền RBAC.`
- **Sub-Team 3 (Engineering):**
  - `@engineering_team: /plan Lập trình tính năng đặt lịch theo Clean Architecture 5 tầng.`
  - `@engineering_team: /goal Hoàn thiện toàn bộ mã nguồn Backend FastAPI và Frontend React Native kèm Jest tests.`
- **Sub-Team 4 (QA & Audit):**
  - `@qa_team: Chạy PyTest đo Code Coverage (pytest-cov), kiểm tra alembic check zero drift và scan Secret Leaks.`
  - `@qa_team: Tự động kích hoạt Auto-Healing vá lỗi nếu phát hiện test case thất bại.`
- **Sub-Team 5 (Release):**
  - `@release_team: Đóng gói gói phát hành ZIP, tính checksum SHA-256 và lập bảng nghiệm thu UAT_CHECKLIST.md.`
- **Quan sát tương tác:** Xem tài liệu review tương tác và biểu đồ hiển thị thời gian thực trên **Auxiliary Pane** (bên phải giao diện Antigravity 2.0).

### Cách 2: Triệu hồi Native Subagent qua Terminal Dispatcher
```bash
# Xem danh sách tất cả Sub-Teams:
python -m orchestrator.agent_factory --list

# Triệu hồi trực tiếp 1 Sub-Team bằng CLI:
python -m orchestrator.agent_factory --subteam discovery_team --prompt "Phân tích brief @sample_client_brief.md" --project "MotoCare"
```

### Cách 3: Sử dụng Makefile & State Synchronizer (Khuyên dùng cho Dev)
```bash
# Xem toàn bộ lệnh:
make help

# Chạy chu trình SDLC (hỗ trợ chỉ định nền tảng PLATFORM=web hoặc PLATFORM=mobile):
make dev PROJECT="Ten_Du_An" PLATFORM="web"

# Chạy test toàn diện Backend (kèm đo độ phủ pytest-cov), Alembic check, và Frontend (Unit + E2E):
make test-all

# Chạy riêng bộ kiểm thử Frontend E2E:
make test-frontend-e2e

# Thẩm định riêng Schema Drift Database:
make check-db

# Xuất báo cáo HTML Coverage:
make cov-html

# Đồng bộ mã nguồn đã chỉnh sửa ngược vào SDLC Checkpoint:
make sync PROJECT="Ten_Du_An"

# Khởi chạy server:
make run-backend    # FastAPI :8000
make run-frontend   # Expo Mobile / Vite Web
```

> Chi tiết cẩm nang vận hành dành cho đội ngũ: Xem tại [TEAM_PLAYBOOK.md](./TEAM_PLAYBOOK.md).

