import argparse
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
from orchestrator.persistence import StatePersistence
from orchestrator.workflows.discovery_phase import run_discovery_phase
from orchestrator.workflows.architecture_phase import run_architecture_phase
from orchestrator.workflows.engineering_phase import run_engineering_phase
from orchestrator.workflows.qa_phase import run_qa_phase
from orchestrator.workflows.release_phase import run_release_phase

console = Console()


class SDLCOrchestrator:
    """Bộ điều phối chu trình phần mềm toàn diện với Google Antigravity SDK & HITL."""

    def __init__(self, base_dir: Path, hitl_enabled: bool = True):
        self.base_dir = base_dir
        self.config_dir = base_dir / "config"
        self.artifacts_dir = base_dir / "workspaces" / "artifacts"
        self.output_project_dir = base_dir / "workspaces" / "output_project"
        self.checkpoints_dir = base_dir / "workspaces" / "checkpoints"
        
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.output_project_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

        # Đọc cấu hình
        self.tech_profile = self._load_yaml(self.config_dir / "tech_lead_profile.yaml")
        self.hitl_config = self._load_yaml(self.config_dir / "hitl_gates.yaml")
        
        env_hitl = os.getenv("HITL_ENABLED", "true").lower() in ("true", "1", "yes")
        final_hitl = hitl_enabled and env_hitl

        self.hitl_manager = HITLManager(self.hitl_config, enabled=final_hitl, artifacts_dir=self.artifacts_dir)
        self.persistence = StatePersistence(self.checkpoints_dir)
        self.factory = AgentFactory(self.base_dir)

    def _load_yaml(self, path: Path) -> dict:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    async def execute_lifecycle(
        self,
        project_name: str,
        raw_requirements: str,
        resume: bool = False,
        platform: str = "auto"
    ) -> SDLCState:
        platform_label = {
            "web": "Web Portal (React Vite / Next.js)",
            "mobile": "Mobile App (React Native)",
            "auto": "Tự động phát hiện qua Brief (Auto-detect)"
        }.get(platform.lower(), platform.upper())

        console.print(Panel(
            f"[bold green]KHỞI ĐỘNG HỆ THỐNG AI MULTI-AGENTS SDLC[/bold green]\n"
            f"[bold]Dự án:[/bold] {project_name}\n"
            f"[bold]Nền tảng Frontend:[/bold] {platform_label}\n"
            f"[bold]Tech Lead Stack:[/bold] Python/FastAPI + React Native / Node.js\n"
            f"[bold]Lộ trình:[/bold] 4 Giai đoạn phát triển hoàn chỉnh (DAG Engine, Auto-Healing, Release Bundler)\n"
            f"[bold]Chế độ:[/bold] {'Khôi phục phiên làm việc (Resume)' if resume else 'Khởi tạo mới'}",
            title="[bold cyan]Google Antigravity SDK Orchestrator[/bold cyan]",
            border_style="cyan"
        ))

        state: SDLCState
        if resume:
            loaded_state = self.persistence.load_checkpoint(project_name)
            if loaded_state:
                state = loaded_state
                if platform != "auto":
                    state.platform = platform
            else:
                console.print(f"[bold yellow]Không tìm thấy checkpoint cho '{project_name}'. Khởi tạo mới.[/bold yellow]")
                state = SDLCState(
                    project_name=project_name,
                    raw_requirements=raw_requirements,
                    tech_lead_profile=self.tech_profile,
                    platform=platform
                )
        else:
            state = SDLCState(
                project_name=project_name,
                raw_requirements=raw_requirements,
                tech_lead_profile=self.tech_profile,
                platform=platform
            )

        # =========================================================================
        # GIAI ĐOẠN 1: DISCOVERY & GATE 1 (PRD APPROVAL)
        # =========================================================================
        if state.current_phase in (SDLCPhase.INITIALIZATION, SDLCPhase.DISCOVERY, SDLCPhase.GATE_1_PRD):
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
                        state.artifacts["user_stories"],
                        state.artifacts.get("ui_ux_specs", "")
                    ],
                    state_summary=f"Dự án: {project_name} | Đã bóc tách yêu cầu, PRD chuẩn SMART, User Stories (Gherkin) và UI/UX Flow."
                )
                state.gate_decisions["gate_1_prd"] = gate_decision
                self.persistence.save_checkpoint(state)

                if gate_decision.status == GateDecisionStatus.APPROVED:
                    console.print("[bold green]✓ GATE 1 APPROVED: Chấp thuận PRD. Tiếp tục sang giai đoạn Kiến trúc.[/bold green]")
                    break
                elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                    console.print(f"[bold yellow]⟳ GATE 1 REVISION REQUESTED: {gate_decision.feedback}[/bold yellow]")
                    revision_feedback_gate1 = gate_decision.feedback or ""
                else:
                    console.print("[bold red]✗ GATE 1 REJECTED: Quy trình bị dừng theo yêu cầu của Reviewer.[/bold red]")
                    state.current_phase = SDLCPhase.FAILED
                    self.persistence.save_checkpoint(state)
                    return state

        # =========================================================================
        # GIAI ĐOẠN 2: ARCHITECTURE & GATE 2 (ARCHITECTURE & API SIGN-OFF)
        # =========================================================================
        if state.current_phase in (SDLCPhase.GATE_1_PRD, SDLCPhase.ARCHITECTURE, SDLCPhase.GATE_2_ARCHITECTURE):
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
                        state.artifacts.get("security_architecture", ""),
                        state.artifacts["tasks_dag"]
                    ],
                    state_summary=(
                        f"Tech Stack đề xuất: {state.selected_tech_stack.get('backend_framework')} & "
                        f"{state.selected_tech_stack.get('frontend_mobile')}\n"
                        f"Bảo mật: STRIDE Threat Model & Ma trận RBAC.\n"
                        f"Đã ưu tiên theo sở trường review của Tech Lead."
                    )
                )
                state.gate_decisions["gate_2_architecture"] = gate_decision
                self.persistence.save_checkpoint(state)

                if gate_decision.status == GateDecisionStatus.APPROVED:
                    console.print("[bold green]✓ GATE 2 APPROVED: Chấp thuận Kiến trúc & API Contract. Bắt đầu viết mã nguồn.[/bold green]")
                    break
                elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                    console.print(f"[bold yellow]⟳ GATE 2 REVISION REQUESTED: {gate_decision.feedback}[/bold yellow]")
                    revision_feedback_gate2 = gate_decision.feedback or ""
                else:
                    console.print("[bold red]✗ GATE 2 REJECTED: Dừng dự án ở khâu Kiến trúc.[/bold red]")
                    state.current_phase = SDLCPhase.FAILED
                    self.persistence.save_checkpoint(state)
                    return state

        # =========================================================================
        # GIAI ĐOẠN 3: CORE ENGINEERING & QA FEEDBACK (AUTO-HEALING LOOP)
        # =========================================================================
        if state.current_phase in (SDLCPhase.GATE_2_ARCHITECTURE, SDLCPhase.ENGINEERING, SDLCPhase.QA_VERIFICATION, SDLCPhase.GATE_3_DEPLOY):
            state = await run_engineering_phase(
                state=state,
                factory=self.factory,
                project_workspace=self.output_project_dir
            )
            self.persistence.save_checkpoint(state)

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
                self.persistence.save_checkpoint(state)

                if gate_decision.status == GateDecisionStatus.APPROVED:
                    console.print("[bold green]✓ GATE 3 APPROVED: Cấp phép triển khai & bàn giao chính thức cho khách hàng.[/bold green]")
                    break
                elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                    console.print(f"[bold yellow]⟳ GATE 3 REVISION REQUESTED (Auto-healing): {gate_decision.feedback}[/bold yellow]")
                    state = await run_engineering_phase(
                        state=state,
                        factory=self.factory,
                        project_workspace=self.output_project_dir,
                        review_feedback=gate_decision.feedback or ""
                    )
                else:
                    console.print("[bold red]✗ GATE 3 REJECTED: Từ chối deploy sản phẩm.[/bold red]")
                    state.current_phase = SDLCPhase.FAILED
                    self.persistence.save_checkpoint(state)
                    return state

        # =========================================================================
        # GIAI ĐOẠN 4: RELEASE, DOCUMENTATION & CLIENT HANDOVER AUTOMATION
        # =========================================================================
        state = await run_release_phase(
            state=state,
            factory=self.factory,
            output_dir=self.artifacts_dir,
            project_workspace=self.output_project_dir
        )
        self.persistence.save_checkpoint(state)

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
            "[bold green]✔ Dự án đã được chuyển giao thành công qua cả 4 Giai đoạn lộ trình![/bold green]\n"
            "• Gói phân phối ZIP: [bold]workspaces/artifacts/05_handover/[/bold]\n"
            "• Bảng nghiệm thu UAT: [bold]UAT_CHECKLIST.md[/bold]\n"
            "• Mã nguồn đã kiểm thử: [bold]workspaces/output_project/[/bold]",
            title="[bold yellow]Hoàn Thành Toàn Diện[/bold yellow]",
            border_style="green"
        ))


def main():
    parser = argparse.ArgumentParser(description="Multi-Agents SDLC Orchestrator")
    parser.add_argument("--project", default="MotoCare_SmartApp", help="Tên dự án phần mềm")
    parser.add_argument("--input-file", help="Đường dẫn file chứa yêu cầu thô từ khách hàng (.txt hoặc .md)")
    parser.add_argument("--requirements", help="Chuỗi văn bản yêu cầu thô truyền trực tiếp qua dòng lệnh")
    parser.add_argument("--resume", action="store_true", help="Khôi phục phiên làm việc từ Checkpoint gần nhất")
    parser.add_argument("--no-hitl", action="store_true", help="Tự động bypass các cổng HITL (Dành cho CI/CD test)")
    parser.add_argument(
        "--platform",
        choices=["auto", "web", "mobile"],
        default="auto",
        help="Chỉ định nền tảng Frontend mục tiêu (auto: tự nhận diện qua Brief, web: React Vite/Next.js Web Portal, mobile: React Native Mobile App)"
    )
    args = parser.parse_args()

    orchestrator = SDLCOrchestrator(
        base_dir=Path(__file__).parent.parent,
        hitl_enabled=not args.no_hitl
    )

    raw_req = ""
    if args.input_file:
        input_path = Path(args.input_file)
        if input_path.exists():
            raw_req = input_path.read_text(encoding="utf-8")
            console.print(f"[bold cyan]Đã nạp yêu cầu thô từ file:[/bold cyan] {input_path}")
        else:
            console.print(f"[bold red]Lỗi: Không tìm thấy file {input_path}[/bold red]")
            sys.exit(1)
    elif args.requirements:
        raw_req = args.requirements
    else:
        raw_req = (
            "Chúng tôi muốn xây dựng ứng dụng di động cho phép khách hàng đặt lịch hẹn bảo dưỡng xe máy, "
            "nhận thông báo khi xe sửa xong, xem bảng giá phụ tùng minh bạch và thanh toán online hoặc tại quầy. "
            "Hệ thống cần có trang quản trị cho nhân viên tiếp nhận xe và quản lý kho linh kiện."
        )

    asyncio.run(orchestrator.execute_lifecycle(
        project_name=args.project,
        raw_requirements=raw_req,
        resume=args.resume,
        platform=args.platform
    ))


if __name__ == "__main__":
    main()
