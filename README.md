# AI Multi-Agents SDLC System (Google Antigravity SDK)

Hệ thống AI Multi-Agents tự động hóa quy trình phát triển phần mềm (Software Development Life Cycle - SDLC) từ **Yêu cầu thô từ khách hàng (Raw Requirements)** đến **Thành phẩm bàn giao (Production-Ready Release)**.

Hệ thống được xây dựng trên nền tảng **Google Antigravity SDK**, hỗ trợ cơ chế **Sub-Teams**, **Skills**, **Rules** và **3 Chốt chặn Human-in-the-Loop (HITL Quality Gates)**.

---

## 🏛️ Kiến Trúc 5 Sub-Teams (15 Agents)

```text
[Khách hàng: Yêu cầu thô]
       │
       ▼
1. Sub-Team 1: Product Discovery (Client Liaison ➔ BA/PO ➔ UI/UX Concept)
       │  Artifacts: PRD.md, user_stories.json, clarification_qna.md
       ▼
   [GATE 1: Phê duyệt PRD & Scope (Tech Lead / PO Sign-off)]
       │
       ▼
2. Sub-Team 2: Architecture & Planning (System Architect ➔ Security Architect ➔ Technical PM)
       │  Artifacts: architecture_design.md, openapi.yaml, erd.mermaid, task_backlog_dag.json
       ▼
   [GATE 2: Phê duyệt Kiến trúc Kỹ thuật & API Contract (Tech Lead Sign-off)]
       │
       ▼
3. Sub-Team 3: Core Engineering (Backend Engineer ➔ Frontend Engineer ➔ DevOps Engineer)
       │  Artifacts: Mã nguồn Backend, Mobile/Frontend, Dockerfile, docker-compose
       ▼
4. Sub-Team 4: QA & Security (Code Reviewer ➔ QA Automation ➔ Security Auditor)
       │  Artifacts: code_review_report.md, test_summary.json, security_audit_report.md
       │  Feedback loop: Tự động yêu cầu sửa mã nguồn nếu fail test hoặc phát hiện lỗ hổng
       ▼
   [GATE 3: Cấp phép Triển khai & Nghiệm thu (Tech Lead / Release Manager Sign-off)]
       │
       ▼
5. Sub-Team 5: Release & Handover (Release Engineer ➔ Tech Writer ➔ Client Handover Lead)
       │  Artifacts: client_handover_package.md, UAT_CHECKLIST.md, USER_MANUAL.md
       ▼
[Thành phẩm hoàn chỉnh bàn giao cho Khách hàng]
```

---

## 👨‍💻 Hồ Sơ Công Nghệ Của Tech Lead (Manual Review Friendly)

Hệ thống tự chủ phân tích bài toán để chọn kiến trúc tối ưu. Tuy nhiên, theo cấu hình tại `config/tech_lead_profile.yaml`:
- **Backend:** Ưu tiên **Python (FastAPI)**
- **Frontend / Mobile:** Ưu tiên **React Native / Node.js**
- **Database:** Ưu tiên **PostgreSQL**

Mục đích: Giúp Tech Lead dễ dàng thực hiện kiểm tra mã nguồn thủ công, kiểm soát bảo mật và bảo trì dự án lâu dài mà không gặp rào cản về công nghệ.

---

## 🚦 3 Chốt Chặn Human-in-the-Loop (HITL Gates)

Hệ thống không chạy "mù quáng" mà dừng lại tại 3 trạm kiểm soát chất lượng quan trọng (được cấu hình tại `config/hitl_gates.yaml`):

1. **Gate 1 - PRD Approval:** Kiểm tra xem yêu cầu thô đã được hiểu đúng, phạm vi (Scope) và tiêu chí nghiệm thu (Gherkin format) đã đầy đủ chưa.
2. **Gate 2 - Architecture & API Sign-off:** Kiểm tra thiết kế kiến trúc, Tech Stack (xác nhận ưu tiên FastAPI + React Native) và chuẩn API Contract (`openapi.yaml`).
3. **Gate 3 - Production Deploy Sign-off:** Kiểm tra báo cáo Code Review, kết quả Unit/E2E test (phải đạt coverage >= 80%) và báo cáo quét lỗ hổng bảo mật trước khi bấm nút đóng gói bàn giao.

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
Multi-Agents-Dev/
├── README.md                          # Tài liệu hướng dẫn này
├── requirements.txt                   # Thư viện phụ thuộc (google-antigravity, rich...)
├── .env.example                       # Biến môi trường mẫu (GEMINI_API_KEY)
├── config/
│   ├── tech_lead_profile.yaml         # Hồ sơ năng lực review của Tech Lead
│   ├── hitl_gates.yaml                # Cấu hình 3 chốt chặn phê duyệt
│   └── prompts/                       # System prompts chi tiết cho 5 Sub-Teams
├── rules/                             # Bộ tiêu chuẩn và quy tắc phát triển
│   ├── coding_standards.md            # Chuẩn Clean Code, typing, naming
│   ├── security_guardrails.md         # Zero hardcoded secrets, OWASP Top 10
│   └── review_criteria.md             # Tiêu chí chấm điểm code review
├── skills/                            # Các kỹ năng Agent tuân thủ chuẩn SKILL.md
│   ├── requirement_parser/            # Kỹ năng bóc tách yêu cầu thô
│   ├── api_contract_validator/        # Kỹ năng thẩm định OpenAPI spec
│   ├── code_review_evaluator/         # Kỹ năng chấm điểm mã nguồn
│   └── uat_checklist_builder/         # Kỹ năng lập bảng kiểm nghiệm thu UAT
├── orchestrator/                      # Mã nguồn Python điều phối hệ thống
│   ├── state.py                       # Quản lý trạng thái SDLC State Machine
│   ├── hitl.py                        # Giao diện tương tác phê duyệt Console
│   ├── agent_factory.py               # Khởi tạo Agents với Google Antigravity SDK
│   ├── workflows/                     # Logic luồng làm việc của từng Sub-Team
│   └── runner.py                      # Điểm khởi chạy quy trình SDLC
└── workspaces/
    ├── artifacts/                     # Kho lưu trữ PRD, Architecture, Test Reports
    └── output_project/                # Thư mục chứa mã nguồn sản phẩm đích
```

---

## 🚀 Hướng Dẫn Vận Hành

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
cp .env.example .env
# Thêm GEMINI_API_KEY vào file .env
```

### 2. Khởi chạy chu trình phát triển
```bash
python -m orchestrator.runner
```

Hệ thống sẽ chạy qua từng Sub-Team và hiển thị bảng kiểm duyệt tương tác tại các Gate 1, Gate 2 và Gate 3 để bạn trực tiếp ra quyết định:
- Nhấn `1`: Phê duyệt (Approve) và tiếp tục.
- Nhấn `2`: Yêu cầu sửa đổi (Request Revision) và nhập ghi chú để AI làm lại.
- Nhấn `3`: Từ chối / Hủy (Reject).
