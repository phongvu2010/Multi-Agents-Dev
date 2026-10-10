from collections import defaultdict, deque
from typing import List, Dict, Any, Set
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

console = Console()


class TaskNode(BaseModel):
    id: str
    team: str  # backend, frontend, devops
    title: str
    depends_on: List[str] = Field(default_factory=list)
    status: str = "pending"  # pending, running, completed, failed
    result: Dict[str, Any] = Field(default_factory=dict)


class DAGExecutionEngine:
    """Động cơ điều phối và thực thi công việc theo Đồ thị Có hướng Không chu trình (DAG)."""

    def __init__(self, raw_tasks: List[Dict[str, Any]]):
        self.tasks: Dict[str, TaskNode] = {t["id"]: TaskNode(**t) for t in raw_tasks}
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self._build_graph()

    def _build_graph(self):
        for task_id in self.tasks:
            self.in_degree[task_id] = 0

        for task_id, node in self.tasks.items():
            for dep in node.depends_on:
                if dep in self.tasks:
                    self.graph[dep].append(task_id)
                    self.in_degree[task_id] += 1
                else:
                    console.print(f"[bold yellow]Cảnh báo: Task {task_id} phụ thuộc {dep} không tồn tại.[/bold yellow]")

    def detect_cycle(self) -> bool:
        """Kiểm tra xem đồ thị có chu trình lặp vô tận (deadlock) hay không."""
        in_degrees = dict(self.in_degree)
        queue = deque([node for node, deg in in_degrees.items() if deg == 0])
        visited_count = 0

        while queue:
            current = queue.popleft()
            visited_count += 1
            for neighbor in self.graph[current]:
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count != len(self.tasks)

    def get_execution_waves(self) -> List[List[TaskNode]]:
        """Phân rã các task thành các Wave (Đợt thực thi song song)."""
        if self.detect_cycle():
            raise ValueError("Phát hiện chu trình phụ thuộc (Cycle/Deadlock) trong danh sách Task!")

        in_degrees = dict(self.in_degree)
        queue = deque([node for node, deg in in_degrees.items() if deg == 0])
        waves: List[List[TaskNode]] = []

        while queue:
            current_wave_ids = list(queue)
            current_wave_tasks = [self.tasks[tid] for tid in current_wave_ids]
            waves.append(current_wave_tasks)

            # Chuyển sang đợt tiếp theo
            next_queue = deque()
            for tid in current_wave_ids:
                for neighbor in self.graph[tid]:
                    in_degrees[neighbor] -= 1
                    if in_degrees[neighbor] == 0:
                        next_queue.append(neighbor)
            queue = next_queue

        return waves

    def display_execution_plan(self):
        """Hiển thị kế hoạch phân rã Task trực quan trên Terminal."""
        waves = self.get_execution_waves()
        table = Table(title="KẾ HOẠCH ĐIỀU PHỐI TASK THEO ĐỒ THỊ DAG", border_style="cyan")
        table.add_column("Wave (Đợt)", justify="center", style="cyan")
        table.add_column("Task ID", style="bold yellow")
        table.add_column("Sub-Team Phụ Trách", style="magenta")
        table.add_column("Tiêu Đề Công Việc", style="white")
        table.add_column("Phụ Thuộc Vào (Depends On)", style="green")

        for wave_idx, wave in enumerate(waves, 1):
            for task in wave:
                deps = ", ".join(task.depends_on) if task.depends_on else "[italic dim]None (Độc lập)[/italic dim]"
                table.add_row(f"Wave {wave_idx}", task.id, task.team.upper(), task.title, deps)

        console.print(table)
