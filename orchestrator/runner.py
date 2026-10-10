import asyncio
import os
import sys
from pathlib import Path
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from orchestrator.state import SDLCState, SDLCPhase, GateDecisionStatus
from orchestrator.hitl import HITLManager
from orchestrator.agent_factory import AgentFactory
from orchestrator.workflows.discovery_phase import run_discovery_phase
from orchestrator.workflows.architecture_phase import run_architecture_phase
from orchestrator.workflows.engineering_phase import run_engineering_phase
from orchestrator.workflows.qa_phase import run_qa_phase
from orchestrator.workflows.release_phase import run_release_phase

console = Console()


class SDLCOrchestrator:
    """Bộ điều phối chu trình phần mềm toàn diện với Google Antigravity SDK & HITL."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.config_dir = base_dir / "config"
        self.artifacts_dir = base_dir / "workspaces" / "artifacts"
        self.output_project_dir = base_dir / "workspaces" / "output_project"
        
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.output_project_dir.mkdir(parents=True, exist_ok=True)

        # Đọc cấu hình
        self.tech_profile = self._load_yaml(self.config_dir / "tech_lead_profile.yaml")
        self.hitl_config = self._load_yaml(self.config_dir / "hitl_gates.yaml")
        
        hitl_enabled = os.getenv("HITL_ENABLED", "true").lower() in ("true", "1", "yes")
        self.hitl_manager = HITLManager(self.hitl_config, enabled=hitl_enabled)
        self.factory = AgentFactory(self.base_dir)

    def _load_yaml(self, path: Path) -> dict:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    async def execute_lifecycle(self, project_name: str, raw_requirements: str) -> SDLCState:
        console.print(Panel(
            f"[bold green]KHỞI ĐỘNG HỆ THỐNG AI MULTI-AGENTS SDLC[/bold green]\n"
            f"[bold]Dự án:[/bold] {project_name}\n"
            f"[bold]Tech Lead Stack:[/bold] Python/FastAPI + React Native / Node.js\n"
            f"[bold]Mô hình:[/bold] 5 Sub-Teams (15 Agents) với 3 Chốt chặn Human-in-the-Loop",
            title="[bold cyan]Google Antigravity SDK Orchestrator[/bold cyan]",
            border_style="cyan"
        ))

        state = SDLCState(
            project_name=project_name,
            raw_requirements=raw_requirements,
            tech_lead_profile=self.tech_profile
        )

        # =========================================================================
        # 1. SUB-TEAM 1: DISCOVERY & GATE 1 (PRD APPROVAL)
        # =========================================================================
        revision_feedback_gate1 = ""
        while True:
            state = await run_discovery_phase(
                state=state,
                factory=self.factory,
                output_dir=self.artifacts_dir,
                revision_feedback=revision_feedback_gate1
            )

            gate_decision = self.hitl_manager.conduct_gate_review(
                gate_key="gate_1_prd",
                artifacts_paths=[
                    state.artifacts["PRD"],
                    state.artifacts["clarification_qna"],
                    state.artifacts["user_stories"]
                ],
                state_summary=f"Dự án: {project_name} | Đã phân rã yêu cầu thô thành PRD và User Stories."
            )
            state.gate_decisions["gate_1_prd"] = gate_decision

            if gate_decision.status == GateDecisionStatus.APPROVED:
                console.print("[bold green]✓ GATE 1 APPROVED: Chấp thuận PRD. Tiếp tục sang giai đoạn Kiến trúc.[/bold green]")
                break
            elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                console.print(f"[bold yellow]⟳ GATE 1 REVISION REQUESTED: {gate_decision.feedback}[/bold yellow]")
                revision_feedback_gate1 = gate_decision.feedback or ""
            else:
                console.print("[bold red]✗ GATE 1 REJECTED: Quy trình bị dừng theo yêu cầu của Reviewer.[/bold red]")
                state.current_phase = SDLCPhase.FAILED
                return state

        # =========================================================================
        # 2. SUB-TEAM 2: ARCHITECTURE & GATE 2 (ARCHITECTURE & API SIGN-OFF)
        # =========================================================================
        revision_feedback_gate2 = ""
        while True:
            state = await run_architecture_phase(
                state=state,
                factory=self.factory,
                output_dir=self.artifacts_dir,
                revision_feedback=revision_feedback_gate2
            )

            gate_decision = self.hitl_manager.conduct_gate_review(
                gate_key="gate_2_architecture",
                artifacts_paths=[
                    state.artifacts["architecture_design"],
                    state.artifacts["openapi"],
                    state.artifacts["erd"],
                    state.artifacts["tasks_dag"]
                ],
                state_summary=(
                    f"Tech Stack đề xuất: {state.selected_tech_stack.get('backend')} & "
                    f"{state.selected_tech_stack.get('frontend_mobile')}\n"
                    f"Đã ưu tiên theo sở trường review của Tech Lead."
                )
            )
            state.gate_decisions["gate_2_architecture"] = gate_decision

            if gate_decision.status == GateDecisionStatus.APPROVED:
                console.print("[bold green]✓ GATE 2 APPROVED: Chấp thuận Kiến trúc & API Contract. Bắt đầu viết mã nguồn.[/bold green]")
                break
            elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                console.print(f"[bold yellow]⟳ GATE 2 REVISION REQUESTED: {gate_decision.feedback}[/bold yellow]")
                revision_feedback_gate2 = gate_decision.feedback or ""
            else:
                console.print("[bold red]✗ GATE 2 REJECTED: Dừng dự án ở khâu Kiến trúc.[/bold red]")
                state.current_phase = SDLCPhase.FAILED
                return state

        # =========================================================================
        # 3. SUB-TEAM 3: CORE ENGINEERING (IMPLEMENTATION)
        # =========================================================================
        state = await run_engineering_phase(
            state=state,
            factory=self.factory,
            project_workspace=self.output_project_dir
        )

        # =========================================================================
        # 4. SUB-TEAM 4: QUALITY ASSURANCE, CODE REVIEW & GATE 3 (DEPLOY APPROVAL)
        # =========================================================================
        while True:
            state = await run_qa_phase(
                state=state,
                factory=self.factory,
                output_dir=self.artifacts_dir
            )

            gate_decision = self.hitl_manager.conduct_gate_review(
                gate_key="gate_3_deploy",
                artifacts_paths=[
                    state.artifacts["code_review_report"],
                    state.artifacts["test_summary"],
                    state.artifacts["security_audit_report"]
                ],
                state_summary="Tất cả test suite và kiểm tra an toàn bảo mật đã hoàn tất. Yêu cầu cấp phép Deploy & Bàn giao."
            )
            state.gate_decisions["gate_3_deploy"] = gate_decision

            if gate_decision.status == GateDecisionStatus.APPROVED:
                console.print("[bold green]✓ GATE 3 APPROVED: Cấp phép triển khai & bàn giao chính thức cho khách hàng.[/bold green]")
                break
            elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                console.print(f"[bold yellow]⟳ GATE 3 REVISION REQUESTED: Sửa lỗi mã nguồn theo phản hồi: {gate_decision.feedback}[/bold yellow]")
                state = await run_engineering_phase(
                    state=state,
                    factory=self.factory,
                    project_workspace=self.output_project_dir,
                    review_feedback=gate_decision.feedback or ""
                )
            else:
                console.print("[bold red]✗ GATE 3 REJECTED: Từ chối deploy sản phẩm.[/bold red]")
                state.current_phase = SDLCPhase.FAILED
                return state

        # =========================================================================
        # 5. SUB-TEAM 5: RELEASE, DOCUMENTATION & CLIENT HANDOVER
        # =========================================================================
        state = await run_release_phase(
            state=state,
            factory=self.factory,
            output_dir=self.artifacts_dir,
            project_workspace=self.output_project_dir
        )

        # Hoàn tất
        self._print_final_summary(state)
        return state

    def _print_final_summary(self, state: SDLCState):
        console.print()
        console.rule("[bold green]TỔNG KẾT BÀN GIAO THÀNH PHẨM (SDLC COMPLETED)[/bold green]")

        table = Table(title="Danh Sách Sản Phẩm Đã Bàn Giao", border_style="green")
        table.add_column("Hạng Mục", style="cyan")
        table.add_column("Vị Trí File / Thư Mục", style="white")

        for key, path in state.artifacts.items():
            table.add_row(key, path)

        console.print(table)
        console.print(Panel(
            "[bold green]✔ Dự án đã được chuyển giao thành công từ Yêu cầu thô đến Thành phẩm sẵn sàng chạy![/bold green]\n"
            "• Khách hàng có thể tiến hành nghiệm thu qua: [bold]UAT_CHECKLIST.md[/bold]\n"
            "• Tech Lead có thể kiểm tra mã nguồn tại: [bold]workspaces/output_project/[/bold]",
            title="[bold yellow]Chúc Mừng![/bold yellow]",
            border_style="green"
        ))


if __name__ == "__main__":
    orchestrator = SDLCOrchestrator(base_dir=Path(__file__).parent.parent)
    sample_requirements = (
        "Chúng tôi muốn xây dựng ứng dụng di động cho phép khách hàng đặt lịch hẹn bảo dưỡng xe máy, "
        "nhận thông báo khi xe sửa xong, xem bảng giá phụ tùng minh bạch và thanh toán online hoặc tại quầy. "
        "Hệ thống cần có trang quản trị cho nhân viên tiếp nhận xe và quản lý kho linh kiện."
    )
    asyncio.run(orchestrator.execute_lifecycle(
        project_name="MotoCare_SmartApp",
        raw_requirements=sample_requirements
    ))
