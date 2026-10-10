import os
import json
import re
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory
from orchestrator.dag_engine import DAGExecutionEngine
from orchestrator.synthesis_engine import DomainAnalyzer, AdaptiveCodeSynthesizer

console = Console()


async def run_engineering_phase(
    state: SDLCState,
    factory: AgentFactory,
    project_workspace: Path,
    review_feedback: str = ""
) -> SDLCState:
    """Thực thi chuyên sâu Sub-Team 3: Core Engineering kết nối với DAG Execution Engine & SQLAlchemy 2.0."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY CHUYÊN SÂU SUB-TEAM 3: CORE ENGINEERING & IMPLEMENTATION[/bold cyan]")

    project_workspace.mkdir(parents=True, exist_ok=True)
    backend_dir = project_workspace / "backend"
    frontend_dir = project_workspace / "frontend"
    infra_dir = project_workspace / "infra"

    backend_dir.mkdir(parents=True, exist_ok=True)
    frontend_dir.mkdir(parents=True, exist_ok=True)
    infra_dir.mkdir(parents=True, exist_ok=True)

    synthesizer = AdaptiveCodeSynthesizer(project_workspace)

    # 1. Xử lý phản hồi Auto-Healing nếu có feedback từ Reviewer / QA
    if review_feedback:
        console.print(Panel(
            f"[bold yellow]⟳ ĐANG KÍCH HOẠT AUTO-HEALING SỬA ĐỔI MÃ NGUỒN THEO PHẢN HỒI:[/bold yellow]\n{review_feedback}",
            title="[bold red]Auto-Healing Loop In Progress[/bold red]",
            border_style="yellow"
        ))
        from orchestrator.auto_healing import AutoHealingCoordinator, DefectTicket
        target_heal_file = "backend/app/routers/orders.py" if ("order" in review_feedback.lower() or "slot" in review_feedback.lower() or "capacity" in review_feedback.lower()) else "backend/app/core/config.py"
        feedback_defect = DefectTicket(
            id="DEF-HITL-REVISION",
            target_team="backend",
            file_path=target_heal_file,
            severity="HIGH",
            issue_description=review_feedback,
            suggested_fix=f"Cập nhật mã nguồn theo yêu cầu của Reviewer: {review_feedback}"
        )
        coordinator = AutoHealingCoordinator(max_iterations=1)
        await coordinator.execute_healing(feedback_defect, factory, project_workspace)

    # 2. Phân tích DAG Tasks
    tasks_dag_path = Path(state.artifacts.get("tasks_dag", ""))
    tasks_data = []
    if tasks_dag_path.exists():
        try:
            tasks_data = json.loads(tasks_dag_path.read_text(encoding="utf-8"))
        except Exception:
            tasks_data = []

    if tasks_data:
        dag_engine = DAGExecutionEngine(tasks_data)
        waves = dag_engine.get_execution_waves()
        console.print(f"  [bold yellow]• Động cơ DAG phát hiện {len(waves)} Execution Waves cần thực thi.[/bold yellow]")
    else:
        waves = []

    # 3. Phân tích ngữ cảnh domain thích ứng
    domain_info = DomainAnalyzer.analyze(state.raw_requirements, project_name=state.project_name)

    # =========================================================================
    # WAVE 1 & 2: CORE CONFIG, DATABASE, REPOSITORIES & SERVICES
    # =========================================================================
    console.print(f"  [bold cyan]► Wave 1: Khởi tạo Clean Architecture, SQLAlchemy 2.0 Engine & Models ({domain_info['primary_label']})...[/bold cyan]")
    console.print(f"  [bold cyan]► Wave 2: Hiện thực hóa Services, Repositories & Quy tắc ({domain_info['rule_desc']})...[/bold cyan]")
    synthesizer.synthesize_backend(domain_info)

    # =========================================================================
    # WAVE 3: ROUTERS & MOBILE FRONTEND (REACT NATIVE TYPESCRIPT)
    # =========================================================================
    console.print("  [bold cyan]► Wave 3: Thiết lập Routers API & Giao diện Mobile App React Native...[/bold cyan]")
    synthesizer.synthesize_frontend(domain_info)

    # =========================================================================
    # WAVE 4: DEVOPS INFRASTRUCTURE (DOCKERFILE & DOCKER-COMPOSE)
    # =========================================================================
    console.print("  [bold cyan]► Wave 4: Thiết lập Hạ tầng DevOps Docker & Compose (FastAPI + PostgreSQL)...[/bold cyan]")
    synthesizer.synthesize_infra(state.project_name)

    # Lưu artifacts
    state.artifacts["backend_source"] = str(backend_dir)
    state.artifacts["frontend_source"] = str(frontend_dir)
    state.artifacts["infra_source"] = str(infra_dir)
    state.current_phase = SDLCPhase.ENGINEERING

    console.print("  [bold green]✓ Sub-Team 3 hoàn thành toàn bộ mã nguồn Clean Architecture theo DAG Waves![/bold green]")
    return state
