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
   - **Cơ chế kiểm thử ba lớp (Triple Verification):** 
     - **Backend:** Chạy thực tế `pytest` qua subprocess (TestClient + Session testing).
     - **Database:** Thẩm định tính toàn vẹn của Alembic Migrations (`alembic.ini`, `env.py`, `versions/0001_initial_schema.py`).
     - **Frontend (Web/Mobile):** Kiểm tra cấu trúc đa màn hình / components, TypeScript AST & **thực thi bộ Jest Test Suite qua Node subprocess (`run_tests.cjs`)**.
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
- **Database Migrations:** `Alembic 1.13+` Version-Controlled Schema Migrations
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

### Cách 1: Chạy toàn trình qua Terminal tích hợp
```bash
# Chạy với file yêu cầu:
python -m orchestrator.runner --project "Ten_Du_An" --input-file "workspaces/sample_client_brief.md"

# Khôi phục từ checkpoint gián đoạn:
python -m orchestrator.runner --project "Ten_Du_An" --resume
```

### Cách 2: Triệu hồi Native Subagents qua Chat Canvas của Antigravity 2.0
Các Subagents đã được cấu hình native tại `.agents/subteams/`. Bạn có thể tương tác trực tiếp:
- **Sub-Team 1:** `@discovery_team: Phân tích file yêu cầu @sample_client_brief.md và xuất PRD chuẩn SMART`
- **Sub-Team 2:** `@architecture_team: Thiết kế OpenAPI và ERD theo tech stack của Tech Lead`
- **Sub-Team 3:** `@engineering_team: Sinh mã nguồn Clean Architecture và Frontend Mobile`
- **Sub-Team 4:** `@qa_team: Chạy PyTest, kiểm tra Jest frontend và scan bảo mật`
- **Sub-Team 5:** `@release_team: Đóng gói release zip và lập UAT Checklist`
- Kiểm tra các Artifacts trực quan trên **Auxiliary Pane** (bên phải giao diện Antigravity 2.0).
