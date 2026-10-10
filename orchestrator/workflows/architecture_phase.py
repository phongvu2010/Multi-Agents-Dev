import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory
from orchestrator.dag_engine import DAGExecutionEngine
from orchestrator.schemas import ArchitectureResult

console = Console()


async def run_architecture_phase(
    state: SDLCState,
    factory: AgentFactory,
    output_dir: Path,
    revision_feedback: str = ""
) -> SDLCState:
    """Thực thi chuyên sâu Sub-Team 2: Architecture, Security & Planning với Structured Output."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY CHUYÊN SÂU SUB-TEAM 2: ARCHITECTURE & TECHNICAL PLANNING[/bold cyan]")
    
    arch_dir = output_dir / "02_architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    
    agent = factory.create_architecture_team(state.tech_lead_profile, response_schema=ArchitectureResult)

    prompt = f"""
Hãy đóng vai Sub-Team 2: System Architect, Security Architect và Technical PM.
Dự án: {state.project_name}
Yêu cầu thô & Ngữ cảnh:
{state.raw_requirements}
{"PHẢN HỒI REVISION TỪ TECH LEAD: " + revision_feedback if revision_feedback else ""}

Nhiệm vụ:
1. Thiết kế kiến trúc phân tầng Clean Architecture, tuân thủ Tech Lead Profile (Python/FastAPI, React Native, PostgreSQL).
2. Viết tài liệu ADRs, định nghĩa các endpoints OpenAPI 3.0.3, bảng DB và quan hệ ERD.
3. Phân tích mô hình đe dọa STRIDE và ma trận phòng vệ.
4. Phân rã backlog thành danh sách Tasks có depends_on để đưa vào DAG Execution Engine.
Xuất dữ liệu đúng ArchitectureResult schema.
"""
    console.print("  [bold yellow]• Thiết kế Kiến trúc & Phân rã DAG Task (Structured Output)...[/bold yellow]")
    async with agent:
        resp = await agent.chat(prompt)
        arch_result: ArchitectureResult = await resp.structured_output()

    if not arch_result:
        raise ValueError("Không thể sinh Structured Output cho Sub-Team 2 Architecture!")

    # Cập nhật selected_tech_stack vào state
    state.selected_tech_stack = arch_result.tech_stack.model_dump()

    # 1. Ghi file architecture_design.md
    arch_doc_path = arch_dir / "architecture_design.md"
    adrs_md = "\n\n".join(f"### {a.id}: {a.title}\n- **Bối cảnh:** {a.context}\n- **Quyết định:** {a.decision}\n- **Lợi ích:** {a.consequences}" for a in arch_result.adrs)
    
    arch_content = f"""# TÀI LIỆU THIẾT KẾ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)
**Dự án:** {arch_result.project_name}
**Phiên bản:** 1.0.0 (Release Candidate)
**Trưởng ban Kiến trúc:** System Architect Agent & Tech Lead

---

## 1. QUYẾT ĐỊNH CÔNG NGHỆ (ARCHITECTURE DECISION RECORDS - ADR)
{adrs_md}

---

## 2. TECH STACK ĐÃ CHỌN (PHÙ HỢP TECH LEAD PROFILE)
- **Backend:** {arch_result.tech_stack.backend_framework}
- **ORM / Database Access:** {arch_result.tech_stack.backend_orm}
- **Data Validation:** {arch_result.tech_stack.data_validation}
- **Frontend / Mobile:** {arch_result.tech_stack.frontend_mobile}
- **Database:** {arch_result.tech_stack.database}
- **Caching:** {arch_result.tech_stack.caching_session}
- **Lý do lựa chọn:**
{arch_result.tech_stack.rationale}

---

## 3. MÔ HÌNH KIẾN TRÚC PHÂN TẦNG (CLEAN ARCHITECTURE)

```text
               [ Client App (React Native / Next.js) ]
                              │
                              ▼ (HTTPS RESTful)
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
   │  │ 3. Data Access / Repository Layer (Async ORM)     │  │
   │  └─────────────────────────┬─────────────────────────┘  │
   └────────────────────────────┼────────────────────────────┘
                                ▼
                     [ PostgreSQL 15+ ]
```
"""
    arch_doc_path.write_text(arch_content, encoding="utf-8")

    # 2. Ghi file openapi.yaml
    openapi_path = arch_dir / "openapi.yaml"
    openapi_path.write_text(arch_result.openapi_yaml, encoding="utf-8")

    # 3. Ghi file erd.mermaid
    erd_path = arch_dir / "erd.mermaid"
    erd_path.write_text(arch_result.erd_mermaid, encoding="utf-8")

    # 4. Ghi file security_architecture.md
    security_path = arch_dir / "security_architecture.md"
    stride_rows = "\n".join(f"| **{s.get('threat', '')}** | {s.get('mitigation', '')} |" for s in arch_result.security_stride_matrix)
    security_content = f"""# BẢO MẬT HỆ THỐNG & MÔ HÌNH STRIDE
**Dự án:** {arch_result.project_name}

## 1. MA TRẬN PHÒNG VỆ NGUY CƠ (STRIDE MATRIX)

| Mối Đe Dọa (STRIDE) | Biện Pháp Phòng Vệ Kỹ Thuật |
|---|---|
{stride_rows}
"""
    security_path.write_text(security_content, encoding="utf-8")

    # 5. Ghi file task_backlog_dag.json & Khởi tạo DAG Engine
    tasks_path = arch_dir / "task_backlog_dag.json"
    tasks_path.write_text(json.dumps(arch_result.tasks_backlog, indent=2, ensure_ascii=False), encoding="utf-8")

    # Khởi chạy và hiển thị Kế hoạch Wave qua DAG Engine
    dag_engine = DAGExecutionEngine(arch_result.tasks_backlog)
    dag_engine.display_execution_plan()

    # Cập nhật State
    state.artifacts["architecture_design"] = str(arch_doc_path)
    state.artifacts["openapi"] = str(openapi_path)
    state.artifacts["erd"] = str(erd_path)
    state.artifacts["security_architecture"] = str(security_path)
    state.artifacts["tasks_dag"] = str(tasks_path)
    state.current_phase = SDLCPhase.GATE_2_ARCHITECTURE

    console.print("  [bold green]✓ Sub-Team 2 hoàn tất Thiết kế Kiến trúc & Phân rã DAG Wave![/bold green]")
    return state
