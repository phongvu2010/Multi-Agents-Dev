import sys
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from orchestrator.state import GateDecision, GateDecisionStatus

console = Console()


class HITLManager:
    """Quản lý các điểm chốt chặn Human-in-the-Loop (HITL)."""

    def __init__(self, hitl_config: Dict[str, Any], enabled: bool = True):
        self.config = hitl_config.get("hitl_gates", {})
        self.enabled = enabled

    def conduct_gate_review(
        self,
        gate_key: str,
        artifacts_paths: List[str],
        state_summary: str = ""
    ) -> GateDecision:
        gate_info = self.config.get(gate_key, {
            "name": gate_key,
            "role_required": "Tech Lead / Human Reviewer",
            "description": "Review artifacts before proceeding."
        })

        gate_name = gate_info.get("name", gate_key)
        role = gate_info.get("role_required", "Tech Lead")
        desc = gate_info.get("description", "")

        console.print()
        console.rule(f"[bold yellow]HUMAN-IN-THE-LOOP QUALITY GATE: {gate_name}[/bold yellow]")

        table = Table(title="Danh sách Artifacts cần Phê duyệt", border_style="cyan")
        table.add_column("STT", justify="center", style="cyan")
        table.add_column("Loại Tài Liệu / File", style="white")
        table.add_column("Đường Dẫn Thực Tế", style="green")
        table.add_column("Trạng Thái Tồn Tại", justify="center")

        for idx, path_str in enumerate(artifacts_paths, 1):
            p = Path(path_str)
            exists = "[bold green]✓ Sẵn sàng[/bold green]" if p.exists() else "[bold red]✗ Chưa thấy[/bold red]"
            table.add_row(str(idx), p.name, str(p), exists)

        console.print(Panel(f"[bold]Vai trò người phê duyệt:[/bold] {role}\n[italic]{desc}[/italic]\n\n{state_summary}",
                            title="[bold yellow]Thông Tin Gate[/bold yellow]", border_style="yellow"))
        console.print(table)

        if not self.enabled:
            console.print("[bold green][AUTO-BYPASS] Chế độ HITL_ENABLED=false: Tự động phê duyệt chốt chặn.[/bold green]")
            return GateDecision(
                gate_id=gate_key,
                reviewer=f"Automated System ({role})",
                status=GateDecisionStatus.APPROVED,
                feedback="Auto-approved via non-interactive mode."
            )

        console.print("\n[bold cyan]LỰA CHỌN CỦA BẠN (Tech Lead / Reviewer):[/bold cyan]")
        console.print("  [1] [bold green]PHÊ DUYỆT (Approve)[/bold green] -> Chuyển tiếp sang Sub-Team tiếp theo")
        console.print("  [2] [bold yellow]YÊU CẦU SỬA ĐỔI (Request Revision)[/bold yellow] -> Nhập phản hồi để Agent làm lại")
        console.print("  [3] [bold red]TỪ CHỐI / DỪNG DỰ ÁN (Reject & Abort)[/bold red]")

        choice = Prompt.ask("Vui lòng chọn", choices=["1", "2", "3"], default="1")

        if choice == "1":
            feedback = Prompt.ask("Nhập ghi chú phê duyệt (nếu có)", default="Đã phê duyệt, đạt tiêu chuẩn.")
            return GateDecision(
                gate_id=gate_key,
                reviewer=role,
                status=GateDecisionStatus.APPROVED,
                feedback=feedback
            )
        elif choice == "2":
            feedback = Prompt.ask("[bold yellow]Nhập nội dung yêu cầu sửa đổi chi tiết cho AI[/bold yellow]")
            return GateDecision(
                gate_id=gate_key,
                reviewer=role,
                status=GateDecisionStatus.REVISION_REQUESTED,
                feedback=feedback
            )
        else:
            feedback = Prompt.ask("[bold red]Lý do từ chối dự án[/bold red]", default="Dự án không đạt tiêu chuẩn kỹ thuật.")
            return GateDecision(
                gate_id=gate_key,
                reviewer=role,
                status=GateDecisionStatus.REJECTED,
                feedback=feedback
            )
