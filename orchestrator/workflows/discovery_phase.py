from pathlib import Path
from rich.console import Console
from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory

console = Console()


async def run_discovery_phase(
    state: SDLCState,
    factory: AgentFactory,
    output_dir: Path,
    revision_feedback: str = ""
) -> SDLCState:
    """Thực thi Sub-Team 1: Discovery & Product Design."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY SUB-TEAM 1: PRODUCT DISCOVERY & REQUIREMENTS[/bold cyan]")
    
    discovery_dir = output_dir / "01_discovery"
    discovery_dir.mkdir(parents=True, exist_ok=True)
    
    agent = factory.create_discovery_team(state.tech_lead_profile)
    
    prompt = f"""
Hãy phân tích yêu cầu thô sau từ khách hàng cho dự án '{state.project_name}':
---
{state.raw_requirements}
---
{"YÊU CẦU SỬA ĐỔI TỪ TECH LEAD (REVISION): " + revision_feedback if revision_feedback else ""}

Nhiệm vụ:
1. Đóng vai trò Client Liaison: Phân tích các điểm mờ, tạo bộ Q&A làm rõ.
2. Đóng vai trò BA/PO: Viết PRD.md với các User Stories và Acceptance Criteria dạng Gherkin.
3. Đóng vai trò UI/UX Designer: Xác định luồng màn hình và UI specs.
"""
    
    console.print("  [dim]• Đang kích hoạt Client Liaison, BA/PO và UI/UX Agents...[/dim]")
    async with agent:
        response = await agent.chat(prompt)
        content = await response.text()
    
    # Tạo các artifact chuẩn hóa
    clarification_path = discovery_dir / "clarification_qna.md"
    prd_path = discovery_dir / "PRD.md"
    stories_path = discovery_dir / "user_stories.json"
    
    # Ghi nội dung artifact
    prd_content = f"""# PRODUCT REQUIREMENTS DOCUMENT (PRD)
**Dự án:** {state.project_name}
**Ngày tạo:** 2026-10-09
**Người phê duyệt yêu cầu:** Tech Lead / Product Owner

## 1. TỔNG QUAN & MỤC TIÊU
{state.raw_requirements}

## 2. PHẠM VI (SCOPE)
- **In-Scope:** Các tính năng cốt lõi được mô tả trong yêu cầu thô đã được chuẩn hóa.
- **Out-of-Scope:** Mở rộng bên ngoài chưa được khách hàng xác nhận.

## 3. USER STORIES & ACCEPTANCE CRITERIA (GHERKIN)
### US-01: Khởi tạo và Quản trị
- **Là một:** Người dùng hệ thống
- **Tôi muốn:** Đăng nhập an toàn và truy cập các tính năng chính
- **Để:** Sử dụng dịch vụ nhanh chóng và bảo mật

```gherkin
Scenario: Đăng nhập thành công
  Given người dùng đã có tài khoản hợp lệ
  When gửi thông tin xác thực đến hệ thống
  Then hệ thống trả về mã token JWT và thông tin tài khoản
```

{content}
"""
    prd_path.write_text(prd_content, encoding="utf-8")
    clarification_path.write_text(f"# CLARIFICATION Q&A\n\n{content}", encoding="utf-8")
    stories_path.write_text('{"stories": [{"id": "US-01", "title": "Core Service Access", "priority": "HIGH"}]}', encoding="utf-8")
    
    state.artifacts["PRD"] = str(prd_path)
    state.artifacts["clarification_qna"] = str(clarification_path)
    state.artifacts["user_stories"] = str(stories_path)
    state.current_phase = SDLCPhase.GATE_1_PRD
    
    console.print(f"  [bold green]✓ Hoàn thành Sub-Team 1. Đã tạo PRD tại:[/bold green] {prd_path}")
    return state
