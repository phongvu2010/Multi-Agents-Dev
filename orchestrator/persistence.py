import json
from pathlib import Path
from typing import Optional
from rich.console import Console

from orchestrator.state import SDLCState

console = Console()


class StatePersistence:
    """Quản lý lưu trữ và khôi phục trạng thái (Checkpoints) cho chu trình SDLC."""

    def __init__(self, checkpoints_dir: Path):
        self.checkpoints_dir = checkpoints_dir
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

    def _get_checkpoint_path(self, project_name: str) -> Path:
        safe_name = project_name.lower().replace(" ", "_")
        return self.checkpoints_dir / f"{safe_name}_checkpoint.json"

    def save_checkpoint(self, state: SDLCState) -> Path:
        """Lưu snapshot hiện tại của dự án vào đĩa."""
        path = self._get_checkpoint_path(state.project_name)
        data = state.model_dump(mode="json")
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"  [dim]💾 Đã lưu checkpoint tại Phase [{state.current_phase.value}]: {path.name}[/dim]")
        return path

    def load_checkpoint(self, project_name: str) -> Optional[SDLCState]:
        """Khôi phục trạng thái dự án từ checkpoint đã lưu."""
        path = self._get_checkpoint_path(project_name)
        if not path.exists():
            return None
        try:
            content = path.read_text(encoding="utf-8")
            data = json.loads(content)
            state = SDLCState.model_validate(data)
            console.print(f"[bold green]✓ Khôi phục thành công checkpoint dự án '{project_name}' tại Phase [{state.current_phase.value}][/bold green]")
            return state
        except Exception as e:
            console.print(f"[bold red]✗ Không thể đọc checkpoint: {e}[/bold red]")
            return None
