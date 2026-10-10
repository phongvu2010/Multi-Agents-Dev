from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

console = Console()


class DefectTicket(BaseModel):
    id: str
    target_team: str  # backend, frontend, devops
    file_path: str
    severity: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW
    issue_description: str
    suggested_fix: str
    resolved: bool = False


class QAEvaluationResult(BaseModel):
    passed: bool
    coverage_score: float
    total_defects: int
    defects: List[DefectTicket] = Field(default_factory=list)
    summary: str


class AutoHealingCoordinator:
    """Điều phối vòng lặp tự động sửa lỗi (Auto-Healing Loop) giữa Sub-Team 4 (QA) và Sub-Team 3 (Dev)."""

    def __init__(self, max_iterations: int = 3):
        self.max_iterations = max_iterations

    def format_fix_prompt_for_dev(self, defects: List[DefectTicket]) -> str:
        """Đóng gói danh sách lỗi thành prompt chỉ dẫn sửa lỗi cho Dev Agents."""
        lines = [
            "HỆ THỐNG QA VÀ CODE REVIEW ĐÃ PHÁT HIỆN CÁC LỖI CẦN SỬA ĐỔI (AUTO-HEALING REQUEST):",
            "Vui lòng đọc kỹ danh sách dưới đây và tiến hành sửa trực tiếp vào mã nguồn:\n"
        ]
        for idx, d in enumerate(defects, 1):
            lines.append(f"{idx}. [{d.severity}] Đội phụ trách: {d.target_team.upper()}")
            lines.append(f"   • File: {d.file_path}")
            lines.append(f"   • Lỗi: {d.issue_description}")
            lines.append(f"   • Hướng giải quyết đề xuất: {d.suggested_fix}\n")
        lines.append("Yêu cầu: Viết lại mã nguồn đã sửa hoàn chỉnh, đảm bảo không làm gãy các phần khác.")
        return "\n".join(lines)

    def log_iteration_status(self, iteration: int, qa_result: QAEvaluationResult):
        color = "green" if qa_result.passed else "yellow"
        console.print(Panel(
            f"[bold]Vòng lặp sửa lỗi (Iteration):[/bold] {iteration} / {self.max_iterations}\n"
            f"[bold]Kết quả QA:[/bold] {'[green]PASSED[/green]' if qa_result.passed else '[red]FAILED[/red]'}\n"
            f"[bold]Độ phủ kiểm thử (Coverage):[/bold] {qa_result.coverage_score}%\n"
            f"[bold]Số lỗi còn tồn đọng:[/bold] {qa_result.total_defects}\n"
            f"[italic]{qa_result.summary}[/italic]",
            title="[bold cyan]Cơ Chế Auto-Healing Loop[/bold cyan]",
            border_style=color
        ))
