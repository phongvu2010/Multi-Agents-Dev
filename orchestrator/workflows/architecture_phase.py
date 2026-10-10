from pathlib import Path
from rich.console import Console
from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory

console = Console()


async def run_architecture_phase(
    state: SDLCState,
    factory: AgentFactory,
    output_dir: Path,
    revision_feedback: str = ""
) -> SDLCState:
    """Thực thi Sub-Team 2: Architecture & Planning."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY SUB-TEAM 2: ARCHITECTURE & TECHNICAL PLANNING[/bold cyan]")
    
    arch_dir = output_dir / "02_architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    
    agent = factory.create_architecture_team(state.tech_lead_profile)
    
    prompt = f"""
Hãy thiết kế kiến trúc kỹ thuật dựa trên PRD đã được phê duyệt tại Gate 1:
Dự án: {state.project_name}

LƯU Ý CỰC KỲ QUAN TRỌNG TỪ TECH LEAD:
Tech Lead muốn dễ dàng review thủ công. Vì vậy, HÃY ƯU TIÊN:
- Backend: Python (FastAPI)
- Frontend / Mobile: React Native hoặc Node.js
- Database: PostgreSQL

{"YÊU CẦU SỬA ĐỔI TỪ TECH LEAD (REVISION): " + revision_feedback if revision_feedback else ""}

Nhiệm vụ:
1. Quyết định Tech Stack chi tiết và lý giải tính phù hợp.
2. Thiết kế API Contract chuẩn OpenAPI 3.0+ (openapi.yaml).
3. Thiết kế sơ đồ quan hệ cơ sở dữ liệu ERD (erd.mermaid).
4. Phân rã DAG các công việc cần thực thi (task_backlog_dag.json).
"""
    
    console.print("  [dim]• Đang kích hoạt System Architect, Security Architect và TPM Agents...[/dim]")
    async with agent:
        response = await agent.chat(prompt)
        content = await response.text()
    
    # Ghi nhận Tech Stack ưu tiên
    state.selected_tech_stack = {
        "backend": "Python (FastAPI)",
        "frontend_mobile": "React Native (TypeScript) / Node.js",
        "database": "PostgreSQL + SQLAlchemy ORM",
        "api_spec": "OpenAPI 3.0.3",
        "rationale": "Tối ưu hóa hiệu năng, tương thích hoàn hảo với khả năng review thủ công của Tech Lead."
    }
    
    arch_doc_path = arch_dir / "architecture_design.md"
    openapi_path = arch_dir / "openapi.yaml"
    erd_path = arch_dir / "erd.mermaid"
    tasks_path = arch_dir / "task_backlog_dag.json"
    
    arch_doc_content = f"""# TÀI LIỆU THIẾT KẾ KIẾN TRÚC HỆ THỐNG
**Dự án:** {state.project_name}
**Kiến trúc sư:** System Architect Agent & Tech Lead

## 1. TECH STACK LỰA CHỌN
- **Backend:** {state.selected_tech_stack['backend']}
- **Frontend / Mobile:** {state.selected_tech_stack['frontend_mobile']}
- **Database:** {state.selected_tech_stack['database']}
- **Lý do lựa chọn:** {state.selected_tech_stack['rationale']}

## 2. KIẾN TRÚC PHÂN TẦNG (CLEAN ARCHITECTURE)
- **API Routers (FastAPI):** Tiếp nhận HTTP Request, xác thực token và validate schema Pydantic.
- **Service Layer:** Xử lý nghiệp vụ lõi độc lập với framework.
- **Data Access Layer (Repository):** Thao tác database qua SQLAlchemy ORM.

{content}
"""
    
    openapi_sample = """openapi: 3.0.3
info:
  title: API Specification
  version: 1.0.0
  description: API Contracts chuẩn hóa sinh ra bởi System Architect Agent.
paths:
  /api/v1/health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "healthy"
"""
    
    erd_sample = """erDiagram
    USER ||--o{ REQ_LOG : creates
    USER {
        uuid id PK
        string email UK
        string password_hash
        datetime created_at
    }
    REQ_LOG {
        uuid id PK
        uuid user_id FK
        string action
        datetime timestamp
    }
"""
    
    tasks_sample = """{
  "tasks": [
    {"id": "TASK-BE-01", "team": "backend", "title": "Setup FastAPI scaffold & database models", "depends_on": []},
    {"id": "TASK-FE-01", "team": "frontend", "title": "Setup React Native navigation & API client", "depends_on": []},
    {"id": "TASK-DEVOPS-01", "team": "devops", "title": "Docker-compose for PostgreSQL & App", "depends_on": []}
  ]
}"""

    arch_doc_path.write_text(arch_doc_content, encoding="utf-8")
    openapi_path.write_text(openapi_sample, encoding="utf-8")
    erd_path.write_text(erd_sample, encoding="utf-8")
    tasks_path.write_text(tasks_sample, encoding="utf-8")
    
    state.artifacts["architecture_design"] = str(arch_doc_path)
    state.artifacts["openapi"] = str(openapi_path)
    state.artifacts["erd"] = str(erd_path)
    state.artifacts["tasks_dag"] = str(tasks_path)
    state.current_phase = SDLCPhase.GATE_2_ARCHITECTURE
    
    console.print(f"  [bold green]✓ Hoàn thành Sub-Team 2. Đã thiết kế kiến trúc và API Contract tại:[/bold green] {arch_doc_path}")
    return state
