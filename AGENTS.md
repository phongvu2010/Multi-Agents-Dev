# AGENTS.md — HƯỚNG DẪN HỆ THỐNG MULTI-AGENTS SDLC (ANTIGRAVITY 2.0)

Chào mừng bạn đến với Không gian làm việc **Multi-Agents-Dev** chạy trên nền tảng **Google Antigravity 2.0**.

Tài liệu này được tự động nạp bởi Antigravity 2.0 IDE để định hình hành vi, phân quyền và tiêu chuẩn kỹ thuật cho toàn bộ các tác tử AI khi tham gia phát triển dự án.

---

## 🏛️ 1. CƠ CẤU 5 SUB-TEAMS (15 AGENTS)

Khi nhận yêu cầu phần mềm từ người dùng hoặc khách hàng, hệ thống hoạt động theo 5 Sub-Teams chuyên biệt:

1. **Sub-Team 1: Product Discovery & Requirements**
   - **Thành viên:** Client Liaison Agent, BA/PO Agent, UI/UX Concept Agent.
   - **Kỹ năng sử dụng:** `requirement-parser`, `gherkin-generator`.
   - **Đầu ra (Artifacts):** `PRD.md`, `user_stories.json`, `clarification_qna.md`, `ui_ux_specifications.md`.
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 1 (PRD Approval)** chờ Tech Lead / PO ký duyệt tại file interactive `review_gate_1_prd.md`.

2. **Sub-Team 2: Architecture & Technical Planning**
   - **Thành viên:** System Architect Agent, Security Architect Agent, Technical PM Agent.
   - **Kỹ năng sử dụng:** `api-contract-validator`, `threat-modeling`.
   - **Đầu ra (Artifacts):** `architecture_design.md`, `openapi.yaml`, `erd.mermaid`, `security_architecture.md`, `task_backlog_dag.json`.
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 2 (Architecture & API Sign-off)** chờ Tech Lead duyệt tại `review_gate_2_architecture.md`.

3. **Sub-Team 3: Core Engineering & Implementation**
   - **Thành viên:** Backend Engineer Agent, Frontend/Mobile Engineer Agent, DevOps Engineer Agent.
   - **Động cơ điều phối:** **DAG Execution Engine** phân rã các đợt thực thi song song (Execution Waves) kết hợp **AdaptiveCodeSynthesizer** & Live Gemini LLM (`google.genai`).
   - **Chuẩn mã nguồn:** Clean Architecture 5 tầng (`core/` -> `models/` -> `schemas/` -> `repositories/` -> `services/` -> `routers/`) tích hợp **SQLAlchemy 2.0 ORM** và Pydantic v2.
   - **Đầu ra:** Mã nguồn hoàn chỉnh tại `workspaces/output_project/` (Backend FastAPI, Mobile React Native TypeScript, Docker).

4. **Sub-Team 4: Quality Assurance & Security Audit**
   - **Thành viên:** QA Automation Agent, Code Reviewer Agent, Security Auditor Agent.
   - **Kỹ năng sử dụng:** `test-runner`, `code-review-evaluator`, `secret-scanner`.
   - **Cơ chế kiểm thử kép:** 
     - **Backend:** Chạy thực tế `pytest` (TestClient + Session testing).
     - **Frontend/Mobile:** Kiểm tra cấu trúc Component React Native & kiểm toán Type Safety TypeScript.
     - **Security:** Quét tĩnh Secret Leaks & kiểm toán OWASP API Security Top 10.
   - ⟳ **Auto-Healing Loop:** Nếu phát hiện lỗi (Defect Ticket), tự động áp bản vá trực tiếp vào mã nguồn tối đa 3 lần.
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 3 (Production Deploy Sign-off)** tại `review_gate_3_deploy.md`.

5. **Sub-Team 5: Release & Client Handover**
   - **Thành viên:** Release Engineer Agent, Tech Writer Agent, Client Handover Lead Agent.
   - **Kỹ năng sử dụng:** `uat-checklist-builder`.
   - **Đầu ra:** Gói phân phối nén `.zip` trong `workspaces/artifacts/05_handover/`, `UAT_CHECKLIST.md`, `USER_MANUAL.md`, `RELEASE_MANIFEST.json`.

---

## 👨‍💻 2. HỒ SƠ TECH LEAD & TIÊU CHUẨN CÔNG NGHỆ (TECH LEAD PROFILE)

Hệ thống được thiết kế tối ưu cho việc **Manual Review của Tech Lead**. Toàn bộ các Subagents PHẢI ưu tiên lựa chọn:

- **Backend Framework:** `Python (FastAPI v0.110+)`
- **ORM / Database Access:** `SQLAlchemy 2.0` Declarative Mapped Models + Repositories Pattern
- **Frontend / Mobile:** `React Native (TypeScript)`
- **Database:** `PostgreSQL 15+` (production) & `SQLite` (local/testing)
- **Kiến trúc mã nguồn:** Phân tầng triệt để Clean Architecture (`core/` -> `models/` -> `schemas/` -> `repositories/` -> `services/` -> `routers/`).

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

### Cách 2: Tương tác qua Chat Canvas của Antigravity 2.0
- Sử dụng `@` để tag tài liệu: `@workspaces/sample_client_brief.md`
- Yêu cầu tác tử: *"Hãy đóng vai Sub-Team 1 phân tích yêu cầu này và xuất PRD theo chuẩn AGENTS.md"*
- Kiểm tra các Artifacts trực quan trên **Auxiliary Pane** (bên phải giao diện Antigravity 2.0).
