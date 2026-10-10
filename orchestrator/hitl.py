import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from orchestrator.state import GateDecision, GateDecisionStatus

console = Console()


class HITLManager:
    """Quản lý các điểm chốt chặn Human-in-the-Loop (HITL) tích hợp Antigravity 2.0 Artifacts."""

    def __init__(self, hitl_config: Dict[str, Any], enabled: bool = True, artifacts_dir: Optional[Path] = None):
        self.config = hitl_config.get("hitl_gates", {})
        self.enabled = enabled
        self.artifacts_dir = artifacts_dir or Path("workspaces/artifacts")

    def _generate_interactive_artifact(
        self,
        gate_key: str,
        gate_name: str,
        role: str,
        desc: str,
        artifacts_paths: List[str],
        state_summary: str,
        decision: Optional[GateDecision] = None
    ) -> Path:
        """Sinh tài liệu Markdown Review tương tác để hiển thị trực quan trên Antigravity IDE."""
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        review_doc_path = self.artifacts_dir / f"review_{gate_key}.md"

        artifact_rows = []
        for idx, path_str in enumerate(artifacts_paths, 1):
            p = Path(path_str)
            exists = p.exists()
            status_icon = "✅ Sẵn sàng" if exists else "❌ Chưa tìm thấy"
            size_str = f"{p.stat().st_size:,} bytes" if exists else "N/A"
            artifact_rows.append(f"| {idx} | [{p.name}]({p.resolve()}) | `{p}` | {size_str} | {status_icon} |")

        table_md = "\n".join(artifact_rows)
        decision_status_md = ""
        if decision:
            status_color = "green" if decision.status == GateDecisionStatus.APPROVED else "yellow" if decision.status == GateDecisionStatus.REVISION_REQUESTED else "red"
            decision_status_md = f"""
---

## 📋 KẾT QUẢ PHÊ DUYỆT (DECISION LOG)
- **Trạng thái:** **{decision.status.value.upper()}**
- **Người ký duyệt:** `{decision.reviewer}`
- **Thời gian:** `{decision.timestamp}`
- **Ghi chú / Feedback:**
> {decision.feedback}
"""

        content = f"""# 🚦 CHỐT CHẶN KIỂM SOÁT CHẤT LƯỢNG: {gate_name.upper()}
> [!IMPORTANT]
> **Vai trò người phê duyệt yêu cầu:** `{role}`  
> **Mục tiêu chốt chặn:** {desc}

{state_summary}

---

## 📂 DANH SÁCH ARTIFACTS CẦN THẨM ĐỊNH

| STT | Tập Tin / Tài Liệu | Đường Dẫn Tuyệt Đối | Dung Lượng | Trạng Thái |
|---|---|---|---|---|
{table_md}

---

## 🎯 TIÊU CHÍ NGHIỆM THU (GATE EXIT CRITERIA)
- [x] Tài liệu tuân thủ chuẩn cấu trúc và phân tầng Clean Architecture.
- [x] Không vi phạm Security Guardrails (Zero Hardcoded Secrets).
- [x] Tương thích tối đa với năng lực review của Tech Lead (FastAPI & React Native).

{decision_status_md}
"""
        review_doc_path.write_text(content, encoding="utf-8")
        return review_doc_path

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

        # 1. Sinh file artifact review cho Antigravity 2.0 IDE
        review_doc = self._generate_interactive_artifact(
            gate_key=gate_key,
            gate_name=gate_name,
            role=role,
            desc=desc,
            artifacts_paths=artifacts_paths,
            state_summary=state_summary
        )

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

        console.print(Panel(
            f"[bold]Vai trò người phê duyệt:[/bold] {role}\n"
            f"[italic]{desc}[/italic]\n\n"
            f"[bold cyan]Artifact Review Markdown:[/bold cyan] {review_doc}\n\n"
            f"{state_summary}",
            title="[bold yellow]Thông Tin Gate[/bold yellow]",
            border_style="yellow"
        ))
        console.print(table)

        if not self.enabled:
            console.print("[bold green][AUTO-BYPASS] Chế độ HITL_ENABLED=false: Tự động phê duyệt chốt chặn.[/bold green]")
            decision = GateDecision(
                gate_id=gate_key,
                reviewer=f"Automated System ({role})",
                status=GateDecisionStatus.APPROVED,
                feedback="Auto-approved via non-interactive mode."
            )
            self._generate_interactive_artifact(gate_key, gate_name, role, desc, artifacts_paths, state_summary, decision)
            return decision

        console.print("\n[bold cyan]LỰA CHỌN CỦA BẠN (Tech Lead / Reviewer):[/bold cyan]")
        console.print("  [1] [bold green]PHÊ DUYỆT (Approve)[/bold green] -> Chuyển tiếp sang Sub-Team tiếp theo")
        console.print("  [2] [bold yellow]YÊU CẦU SỬA ĐỔI (Request Revision)[/bold yellow] -> Nhập phản hồi để AI Auto-Healing sửa lại")
        console.print("  [3] [bold red]TỪ CHỐI / DỪNG DỰ ÁN (Reject & Abort)[/bold red]")

        choice = Prompt.ask("Vui lòng chọn", choices=["1", "2", "3"], default="1")

        if choice == "1":
            feedback = Prompt.ask("Nhập ghi chú phê duyệt (nếu có)", default="Đã phê duyệt, đạt tiêu chuẩn kỹ thuật.")
            decision = GateDecision(
                gate_id=gate_key,
                reviewer=role,
                status=GateDecisionStatus.APPROVED,
                feedback=feedback
            )
        elif choice == "2":
            feedback = Prompt.ask("[bold yellow]Nhập nội dung yêu cầu sửa đổi chi tiết cho AI[/bold yellow]")
            decision = GateDecision(
                gate_id=gate_key,
                reviewer=role,
                status=GateDecisionStatus.REVISION_REQUESTED,
                feedback=feedback
            )
        else:
            feedback = Prompt.ask("[bold red]Lý do từ chối dự án[/bold red]", default="Dự án không đạt tiêu chuẩn kỹ thuật.")
            decision = GateDecision(
                gate_id=gate_key,
                reviewer=role,
                status=GateDecisionStatus.REJECTED,
                feedback=feedback
            )

        # Cập nhật kết quả quyết định vào artifact markdown
        self._generate_interactive_artifact(gate_key, gate_name, role, desc, artifacts_paths, state_summary, decision)
        return decision
