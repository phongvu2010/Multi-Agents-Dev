import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory
from orchestrator.schemas import DiscoveryResult

console = Console()


async def run_discovery_phase(
    state: SDLCState,
    factory: AgentFactory,
    output_dir: Path,
    revision_feedback: str = ""
) -> SDLCState:
    """Thực thi chuyên sâu Sub-Team 1: Product Discovery sử dụng Structured Output."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY CHUYÊN SÂU SUB-TEAM 1: PRODUCT DISCOVERY & REQUIREMENTS[/bold cyan]")
    
    discovery_dir = output_dir / "01_discovery"
    discovery_dir.mkdir(parents=True, exist_ok=True)
    
    agent = factory.create_discovery_team(state.tech_lead_profile, response_schema=DiscoveryResult)

    target_platform = getattr(state, "platform", "auto")
    platform_hint = f"\nNền tảng mục tiêu yêu cầu: {target_platform.upper()} ({'Web Portal: React Vite / Next.js' if target_platform == 'web' else 'Mobile App: React Native'}). Hãy thiết kế luồng UI/UX và User Stories chuẩn xác cho nền tảng này." if target_platform in ("web", "mobile") else ""

    prompt_discovery = f"""
Hãy đóng vai trò trọn vẹn Sub-Team 1 (Client Liaison, BA/PO, UI/UX Concept Agent).
Dự án: {state.project_name}{platform_hint}
Yêu cầu thô từ khách hàng:
---
{state.raw_requirements}
---
{"PHẢN HỒI REVISION TỪ TECH LEAD: " + revision_feedback if revision_feedback else ""}

Nhiệm vụ:
1. Phân tích yêu cầu thô và xuất dữ liệu Structured Output tuân thủ nghiêm ngặt DiscoveryResult schema.
2. Trích xuất mục tiêu SMART, phân định In-Scope MVP vs Out-of-Scope.
3. Lập ma trận câu hỏi làm rõ (Clarification Q&A).
4. Viết User Stories chi tiết kèm Acceptance Criteria chuẩn cú pháp Gherkin.
5. Định nghĩa Business Rules (BR-01, BR-02...) và thiết kế luồng màn hình UI/UX.
"""
    model_tag = f"{getattr(agent, 'model', 'N/A')} [{getattr(agent, 'model_tier', 'flash').upper()}]"
    console.print(f"  [bold yellow]• Phân tích yêu cầu & Sinh Structured Output (Mô hình: {model_tag})...[/bold yellow]")
    async with agent:
        resp = await agent.chat(prompt_discovery)
        discovery_result: DiscoveryResult = await resp.structured_output()

    if not discovery_result:
        raise ValueError("Không thể sinh Structured Output cho Sub-Team 1 Discovery!")

    # =========================================================================
    # 1. XUẤT BIÊN BẢN LÀM RÕ YÊU CẦU (CLARIFICATION Q&A)
    # =========================================================================
    clarification_path = discovery_dir / "clarification_qna.md"
    qna_rows = []
    for q in discovery_result.clarifications:
        qna_rows.append(f"| **{q.q_id}** | {q.context} | {q.impact} | {q.proposed_solution} |")
    qna_table_str = "\n".join(qna_rows)

    clarification_content = f"""# BIÊN BẢN LÀM RÕ YÊU CẦU KHÁCH HÀNG (CLARIFICATION Q&A)
**Dự án:** {discovery_result.project_name}
**Ngày lập:** 2026-10-10
**Đơn vị thực hiện:** Sub-Team 1 (Client Liaison & BA Agent)

---

## 1. TẦM NHÌN SẢN PHẨM & MỤC TIÊU CỐT LÕI
{discovery_result.project_vision}

## 2. PHÂN ĐỊNH PHẠM VI (SCOPE BOUNDARIES)
### In-Scope (MVP v1.0.0):
{chr(10).join(f"- {item}" for item in discovery_result.in_scope_mvp)}

### Out-of-Scope (Dành cho v2.0):
{chr(10).join(f"- {item}" for item in discovery_result.out_of_scope)}

## 3. MA TRẬN CÂU HỎI LÀM RÕ (CLARIFICATION Q&A MATRIX)

| Q-ID | Điểm Chưa Rõ Trong Yêu Cầu | Tác Động Kỹ Thuật / Kinh Doanh | Đề Xuất Của AI & Giải Pháp |
|---|---|---|---|
{qna_table_str}
"""
    clarification_path.write_text(clarification_content, encoding="utf-8")

    # =========================================================================
    # 2. XUẤT USER STORIES (JSON VỚI GHERKIN AC)
    # =========================================================================
    stories_path = discovery_dir / "user_stories.json"
    user_stories_dict = {
        "project": discovery_result.project_name,
        "version": "1.0.0",
        "epic_count": len(set(s.epic for s in discovery_result.user_stories)),
        "stories": [s.model_dump() for s in discovery_result.user_stories]
    }
    stories_path.write_text(json.dumps(user_stories_dict, indent=2, ensure_ascii=False), encoding="utf-8")

    # =========================================================================
    # 3. XUẤT PRODUCT REQUIREMENTS DOCUMENT (PRD.md)
    # =========================================================================
    prd_path = discovery_dir / "PRD.md"
    
    fr_rows = []
    for fr in discovery_result.functional_requirements:
        fr_rows.append(f"| **{fr.code}** | {fr.name} | {fr.description} | {fr.priority} | {fr.subteam} |")
    fr_table_str = "\n".join(fr_rows)

    br_rows = []
    for br in discovery_result.business_rules:
        br_rows.append(f"| **{br.rule_id}** | {br.name} | {br.statement} | {br.enforcement_layer} |")
    br_table_str = "\n".join(br_rows)

    stories_markdown = []
    for s in discovery_result.user_stories:
        stories_markdown.append(f"""### {s.id}: {s.title} ({s.priority} - {s.story_points} pts)
- **As a:** {s.as_a}
- **I want to:** {s.i_want_to}
- **So that:** {s.so_that}
- **Acceptance Criteria (Gherkin):**
```gherkin
{s.acceptance_criteria_gherkin}
```
""")
    stories_md_str = "\n".join(stories_markdown)

    prd_content = f"""# PRODUCT REQUIREMENTS DOCUMENT (PRD) - v1.0.0
**Dự án:** {discovery_result.project_name}
**Tác giả:** Business Analyst Agent & Tech Lead
**Ngày ban hành:** 2026-10-10
**Trạng thái:** DRAFT HOÀN CHỈNH (Chờ phê duyệt tại Gate 1)

---

## 1. TỔNG QUAN & MỤC TIÊU ĐỊNH LƯỢNG (SMART GOALS)
- **Tầm nhìn sản phẩm:** {discovery_result.project_vision}
- **Mục tiêu SMART:**
{chr(10).join(f"  - {g}" for g in discovery_result.business_goals)}

---

## 2. MA TRẬN TÍNH NĂNG CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

| Mã Tính Năng | Tên Tính Năng | Mô Tả Tóm Tắt | Độ Ưu Tiên | Sub-Team Phụ Trách |
|---|---|---|---|---|
{fr_table_str}

---

## 3. DANH MỤC QUY TẮC NGHIỆP VỤ (BUSINESS RULES)

| Mã Quy Tắc | Tên Quy Tắc | Nội Dung Ràng Buộc | Tầng Xử Lý |
|---|---|---|---|
{br_table_str}

---

## 4. DANH SÁCH USER STORIES (VỚI TIÊU CHÍ GHERKIN)
{stories_md_str}
"""
    prd_path.write_text(prd_content, encoding="utf-8")

    # =========================================================================
    # 4. XUẤT ĐẶC TẢ UI/UX (UI_UX_SPECIFICATIONS.MD)
    # =========================================================================
    ui_ux_path = discovery_dir / "ui_ux_specifications.md"
    mermaid_flow = "\n".join(f"    S{idx} --> S{idx+1}" for idx in range(1, len(discovery_result.ui_ux_screen_flows)))
    flow_nodes = "\n".join(f"    S{idx}[\"{name}\"]" for idx, name in enumerate(discovery_result.ui_ux_screen_flows, 1))

    ui_ux_content = f"""# ĐẶC TẢ TRẢI NGHIỆM GIAO DIỆN (UI/UX SPECIFICATIONS)
**Dự án:** {discovery_result.project_name}

## 1. SƠ ĐỒ ĐIỀU HƯỚNG MÀN HÌNH (NAVIGATION FLOW)

```mermaid
graph TD
{flow_nodes}
{mermaid_flow}
```

## 2. DANH SÁCH MÀN HÌNH
{chr(10).join(f"- **{name}**" for name in discovery_result.ui_ux_screen_flows)}
"""
    ui_ux_path.write_text(ui_ux_content, encoding="utf-8")

    # Cập nhật State
    state.artifacts["PRD"] = str(prd_path)
    state.artifacts["user_stories"] = str(stories_path)
    state.artifacts["clarification_qna"] = str(clarification_path)
    state.artifacts["ui_ux_specs"] = str(ui_ux_path)
    state.current_phase = SDLCPhase.GATE_1_PRD

    console.print("  [bold green]✓ Sub-Team 1 hoàn tất toàn bộ Artifacts dạng Structured Output![/bold green]")
    return state
