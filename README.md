# AI Multi-Agents SDLC System (Google Antigravity SDK & Antigravity 2.0)

Hệ thống AI Multi-Agents tự động hóa toàn diện quy trình phát triển phần mềm (Software Development Life Cycle - SDLC) từ **Yêu cầu thô từ khách hàng (Raw Requirements)** đến **Thành phẩm bàn giao (Production-Ready Release)**.

Hệ thống được xây dựng tối ưu cho nền tảng **Google Antigravity 2.0**, trang bị cơ chế **Sub-Teams**, **Skills**, **Rules**, **DAG Wave Execution Engine**, **Auto-Healing Loop**, và **3 Chốt chặn Human-in-the-Loop (HITL Quality Gates)**.

---

## 🏛️ Kiến Trúc 5 Sub-Teams (15 Agents)

```text
[Khách hàng: Yêu cầu thô]
       │
       ▼
1. Sub-Team 1: Product Discovery (Client Liaison ➔ BA/PO ➔ UI/UX Concept)
       │  Artifacts: PRD.md, user_stories.json, clarification_qna.md, ui_ux_specifications.md
       ▼
   [GATE 1: Phê duyệt PRD & Scope (review_gate_1_prd.md)]
       │
       ▼
2. Sub-Team 2: Architecture & Planning (System Architect ➔ Security Architect ➔ Technical PM)
       │  Artifacts: architecture_design.md, openapi.yaml, erd.mermaid, task_backlog_dag.json
       ▼
   [GATE 2: Phê duyệt Kiến trúc Kỹ thuật & API Contract (review_gate_2_architecture.md)]
       │
       ▼
3. Sub-Team 3: Core Engineering (Backend Engineer ➔ Frontend Engineer ➔ DevOps Engineer)
       │  Engine: AdaptiveCodeSynthesizer (SQLAlchemy 2.0 + Pydantic v2 + React Native TypeScript)
       │  Artifacts: Mã nguồn Backend Clean Architecture, Mobile App, Dockerfile, docker-compose
       ▼
4. Sub-Team 4: QA & Security (Code Reviewer ➔ QA Automation ➔ Security Auditor)
       │  Verification: PyTest thực tế (FastAPI) + React Native TypeScript Linter + OWASP Audit
       │  Feedback loop: Tự động áp bản vá (Auto-Healing Patch) nếu fail test hoặc phát hiện lỗi
       ▼
   [GATE 3: Cấp phép Triển khai & Nghiệm thu (review_gate_3_deploy.md)]
       │
       ▼
5. Sub-Team 5: Release & Handover (Release Engineer ➔ Tech Writer ➔ Client Handover Lead)
       │  Artifacts: Release Package (.zip), RELEASE_MANIFEST.json, UAT_CHECKLIST.md, USER_MANUAL.md
       ▼
[Thành phẩm hoàn chỉnh bàn giao cho Khách hàng]
```

---

## 👨‍💻 Hồ Sơ Công Nghệ Của Tech Lead (Manual Review Friendly)

Hệ thống định hướng công nghệ phục vụ cho việc **Manual Review của Tech Lead**:
- **Backend:** **Python (FastAPI v0.110+)**
- **ORM / Database Access:** **SQLAlchemy 2.0 (Declarative Mapped)** + **Pydantic v2**
- **Frontend / Mobile:** **React Native (TypeScript)**
- **Database:** **PostgreSQL 15+** (production) & **SQLite** (local testing)
- **Kiến trúc mã nguồn:** Phân tầng triệt để Clean Architecture (`core/` -> `models/` -> `schemas/` -> `repositories/` -> `services/` -> `routers/`).

---

## 🚦 3 Chốt Chặn Human-in-the-Loop (HITL Gates) & Interactive Review

Tại mỗi chốt chặn, hệ thống tự động sinh tài liệu Markdown tương tác hiển thị trực quan trên **Auxiliary Pane / Artifacts tab** của Antigravity 2.0:
1. **Gate 1 - PRD Approval (`review_gate_1_prd.md`):** Kiểm tra Scope, mục tiêu SMART, User Stories (Gherkin format) và luồng UI/UX.
2. **Gate 2 - Architecture & API Sign-off (`review_gate_2_architecture.md`):** Kiểm tra thiết kế kiến trúc, API Contract (`openapi.yaml`), sơ đồ ERD và ma trận đe dọa STRIDE.
3. **Gate 3 - Production Deploy Sign-off (`review_gate_3_deploy.md`):** Kiểm tra báo cáo Code Review, kết quả kiểm thử PyTest Backend + TypeScript Frontend (Coverage $\ge 80\%$) và báo cáo kiểm toán bảo mật.

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
Multi-Agents-Dev/
├── README.md                          # Tài liệu hướng dẫn hệ thống
├── AGENTS.md                          # Quy chuẩn nạp tự động cho Antigravity 2.0 IDE
├── requirements.txt                   # Thư viện phụ thuộc (google-genai, sqlalchemy, rich...)
├── .env.example                       # Biến môi trường mẫu
├── config/
│   ├── tech_lead_profile.yaml         # Hồ sơ năng lực review của Tech Lead
│   ├── hitl_gates.yaml                # Cấu hình 3 chốt chặn phê duyệt
│   └── prompts/                       # System prompts chuyên sâu cho 5 Sub-Teams
├── rules/                             # Tiêu chuẩn mã nguồn và bảo mật
│   ├── coding_standards.md            # Chuẩn Clean Code, typing, naming
│   ├── security_guardrails.md         # Zero hardcoded secrets, OWASP Top 10
│   └── review_criteria.md             # Tiêu chí chấm điểm code review
├── skills/                            # Các kỹ năng chuẩn Antigravity SKILL.md
│   ├── requirement_parser/            # Bóc tách yêu cầu thô
│   ├── api_contract_validator/        # Thẩm định OpenAPI spec
│   ├── code_review_evaluator/         # Chấm điểm mã nguồn
│   └── uat_checklist_builder/         # Bảng kiểm nghiệm thu UAT
├── orchestrator/                      # Mã nguồn Python điều phối SDLC
│   ├── state.py                       # Quản lý trạng thái SDLC State Machine
│   ├── hitl.py                        # HITL Manager & Interactive Review Generator
│   ├── synthesis_engine.py            # Adaptive Code Synthesizer & Auto-Healing Patcher
│   ├── agent_factory.py               # Khởi tạo Agents kết nối google.genai & Antigravity SDK
│   ├── dag_engine.py                  # Động cơ DAG điều phối Wave execution
│   ├── auto_healing.py                # Điều phối vòng lặp tự động sửa lỗi
│   ├── release_bundler.py             # Đóng gói zip, manifest & tài liệu
│   └── runner.py                      # Điểm khởi chạy CLI
└── workspaces/
    ├── artifacts/                     # Kho lưu trữ PRD, Architecture, Review Docs, Handover
    ├── output_project/                # Mã nguồn sản phẩm đích (backend, frontend, infra)
    └── checkpoints/                   # Checkpoints phục vụ khôi phục phiên làm việc
```

---

## 🌟 Các Nâng Cấp Nổi Bật Vừa Hoàn Thiện

1. **Giai đoạn 1: Live LLM & Adaptive Code Synthesis Engine (`synthesis_engine.py`)**
   - Hỗ trợ gọi trực tiếp Google Gemini 2.5 Flash (`google.genai`).
   - Tự động phân tích ngữ cảnh mọi domain bài toán (`DomainAnalyzer`) và chuyển tiếp mượt mà khi chạy offline/sandbox.
   - Hỗ trợ cơ chế **Auto-Healing Patch** tự động vá lỗi code theo feedback của Tech Lead hoặc QA.

2. **Giai đoạn 2: Chuẩn hóa Tầng Dữ liệu & Kiểm thử Toàn diện**
   - Backend phân tầng Clean Architecture đầy đủ với **SQLAlchemy 2.0 Mapped Declarative Models**, **Repositories Pattern** và **Database Session Management**.
   - Kiểm thử tự động kép: **PyTest thực tế** cho Backend và **TypeScript AST/Syntax Validator** cho Mobile App React Native.

3. **Giai đoạn 3: Tích hợp Sâu Antigravity 2.0 & Interactive Review Artifacts**
   - Sinh tự động các tài liệu `review_gate_1_prd.md`, `review_gate_2_architecture.md`, `review_gate_3_deploy.md` với GitHub Alerts (`> [!IMPORTANT]`), đường dẫn file clickable, trạng thái file và Decision Log minh bạch.

4. **Giai đoạn 4: Bộ Tinh Chỉnh Nâng Cao (Vibe Code & Subagents)**
   - **Cân bằng Hybrid Code Synthesis:** Kết hợp Heuristic Domain Context với Deep LLM Dynamic Generation để làm giàu logic nghiệp vụ chuyên sâu.
   - **Frontend React Native Đa Màn Hình:** Xây dựng đầy đủ 4 màn hình (`AuthScreen`, `CatalogScreen`, `BookingScreen`, `TrackingScreen`), REST API Client, State Store và bộ kiểm thử **Jest Unit Test Suite**.
   - **Alembic Database Migrations:** Tự động tạo `alembic.ini`, `env.py`, version `0001_initial_schema.py` và module `migration_manager.py` cho PostgreSQL & SQLite.
   - **Native Antigravity Subagents:** Thiết lập đầy đủ 5 Sub-Teams chuyên biệt tại `.agents/subteams/` để lập trình viên có thể tương tác trực tiếp qua Chat Canvas.

---

## 🚀 Hướng Dẫn Vận Hành

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
cp .env.example .env
# Thêm GEMINI_API_KEY vào file .env
```

### 2. Các chế độ khởi chạy

- **Chạy với file yêu cầu thô từ khách hàng (Khuyên dùng):**
  ```bash
  python -m orchestrator.runner --project "Ten_Du_An" --input-file "workspaces/sample_client_brief.md"
  ```

- **Chạy truyền trực tiếp yêu cầu qua dòng lệnh:**
  ```bash
  python -m orchestrator.runner --project "EduMaster_App" --requirements "Làm app học trực tuyến..."
  ```

- **Khôi phục phiên làm việc bị gián đoạn (Resume từ Checkpoint):**
  ```bash
  python -m orchestrator.runner --project "EduMaster_App" --resume
  ```

- **Chạy tự động không dừng (Dành cho CI/CD test):**
  ```bash
  python -m orchestrator.runner --project "EduMaster_App" --no-hitl
  ```
