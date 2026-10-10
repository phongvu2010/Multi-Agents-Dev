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
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 1 (PRD Approval)** chờ Tech Lead / PO ký duyệt.

2. **Sub-Team 2: Architecture & Technical Planning**
   - **Thành viên:** System Architect Agent, Security Architect Agent, Technical PM Agent.
   - **Kỹ năng sử dụng:** `api-contract-validator`, `threat-modeling`.
   - **Đầu ra (Artifacts):** `architecture_design.md`, `openapi.yaml`, `erd.mermaid`, `security_architecture.md`, `task_backlog_dag.json`.
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 2 (Architecture & API Sign-off)** chờ Tech Lead duyệt.

3. **Sub-Team 3: Core Engineering & Implementation**
   - **Thành viên:** Backend Engineer Agent, Frontend/Mobile Engineer Agent, DevOps Engineer Agent.
   - **Động cơ điều phối:** Phân rã theo **DAG Execution Waves** (Wave 1: Core/Models -> Wave 2: Services -> Wave 3: Routers/UI -> Wave 4: Infra).
   - **Đầu ra:** Mã nguồn hoàn chỉnh tại `workspaces/output_project/` (Backend FastAPI, Mobile React Native, Docker).

4. **Sub-Team 4: Quality Assurance & Security Audit**
   - **Thành viên:** QA Automation Agent, Code Reviewer Agent, Security Auditor Agent.
   - **Kỹ năng sử dụng:** `test-runner`, `code-review-evaluator`, `secret-scanner`.
   - **Cơ chế:** Chạy thực tế `pytest`, quét tĩnh lỗ hổng OWASP API Top 10 và Secret Leaks.
   - ⟳ **Auto-Healing Loop:** Nếu phát hiện lỗi (Defect Ticket), tự động yêu cầu Sub-Team 3 sửa đổi tối đa 3 lần.
   - 🚦 **Chốt chặn:** Dừng lại tại **Gate 3 (Production Deploy Sign-off)**.

5. **Sub-Team 5: Release & Client Handover**
   - **Thành viên:** Release Engineer Agent, Tech Writer Agent, Client Handover Lead Agent.
   - **Kỹ năng sử dụng:** `uat-checklist-builder`.
   - **Đầu ra:** Gói phân phối `.zip` trong `workspaces/artifacts/05_handover/`, `UAT_CHECKLIST.md`, `USER_MANUAL.md`, `RELEASE_MANIFEST.json`.

---

## 👨‍💻 2. HỒ SƠ TECH LEAD & TIÊU CHUẨN CÔNG NGHỆ (TECH LEAD PROFILE)

Hệ thống được thiết kế tối ưu cho việc **Manual Review của Tech Lead**. Trừ khi có yêu cầu đặc thù bất khả kháng, toàn bộ các Subagents PHẢI ưu tiên lựa chọn:

- **Backend Framework:** `Python (FastAPI v0.110+)`
- **ORM / Database Access:** `SQLAlchemy 2.0 (Async)` + `Pydantic v2` DTOs
- **Frontend / Mobile:** `React Native (TypeScript)` hoặc `Next.js`
- **Database:** `PostgreSQL 15+` & `Redis 7+`
- **Kiến trúc mã nguồn:** Phân tầng triệt để Clean Architecture (`core/` -> `models/` -> `schemas/` -> `services/` -> `routers/`).

---

## 🚦 3. QUY TRÌNH DUYỆT HUMAN-IN-THE-LOOP (HITL) TRONG ANTIGRAVITY 2.0

Khi chạy trong IDE hoặc qua CLI Runner:
- **Gate 1:** Tech Lead kiểm tra file `workspaces/artifacts/01_discovery/PRD.md` trên tab Artifacts.
- **Gate 2:** Tech Lead kiểm tra file `openapi.yaml` và `erd.mermaid` tại `workspaces/artifacts/02_architecture/`.
- **Gate 3:** Tech Lead kiểm tra kết quả `code_review_report.md` và `test_summary.json` trước khi bấm nút đóng gói.

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
