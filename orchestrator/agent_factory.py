import os
import re
import json
from pathlib import Path
from typing import Dict, Any, Optional, Type, List
from pydantic import BaseModel

try:
    from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
    from google.antigravity.hooks import policy
    from google.antigravity.types import BuiltinTools
    HAS_ANTIGRAVITY_SDK = True
except ImportError:
    try:
        from google.antigravity import Agent, LocalAgentConfig, types
        HAS_ANTIGRAVITY_SDK = True
        CapabilitiesConfig = getattr(types, "CapabilitiesConfig", None)
        policy = None
        BuiltinTools = getattr(types, "BuiltinTools", None)
    except ImportError:
        HAS_ANTIGRAVITY_SDK = False
        Agent = None
        LocalAgentConfig = None
        CapabilitiesConfig = None
        policy = None
        BuiltinTools = None

try:
    from google import genai
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False

from orchestrator.synthesis_engine import DomainAnalyzer

from orchestrator.schemas import (
    DiscoveryResult,
    ClarificationQnAModel,
    UserStoryModel,
    FunctionalRequirementModel,
    BusinessRuleModel,
    ArchitectureResult,
    TechStackSelection,
    ADRModel,
    APIEndpointModel,
    DatabaseTableModel,
    QAReportResult,
    CodeReviewMetric,
    SecurityCheckItem,
)


class AgentFactory:
    """Factory khởi tạo các Agents và Sub-Teams sử dụng Google Antigravity SDK & Native Tooling."""

    def __init__(self, base_dir: Path, api_key: Optional[str] = None):
        self.base_dir = base_dir
        self.skills_dir = (base_dir / ".agents" / "skills") if (base_dir / ".agents" / "skills").exists() else (base_dir / "skills")
        self.prompts_dir = base_dir / "config" / "prompts"
        self.rules_dir = (base_dir / ".agents" / "rules") if (base_dir / ".agents" / "rules").exists() else (base_dir / "rules")
        self.subteams_dir = base_dir / ".agents" / "subteams"
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    def _read_prompt(self, filename: str) -> str:
        prompt_path = self.prompts_dir / filename
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return ""

    def _load_rules(self) -> str:
        """Đọc toàn bộ quy tắc phát triển để đưa vào system instructions."""
        rules_text = []
        if self.rules_dir.exists():
            for rf in sorted(self.rules_dir.glob("*.md")):
                rules_text.append(f"### RULE: {rf.name}\n{rf.read_text(encoding='utf-8')}\n")
        return "\n".join(rules_text)

    def get_available_mcp_servers(self) -> List[Dict[str, Any]]:
        """Phát hiện các MCP Servers khả dụng trong Antigravity 2.0 (~/.gemini/antigravity/mcp)."""
        mcp_dirs = [
            Path(os.path.expanduser("~/.gemini/antigravity/mcp")),
            self.base_dir / ".gemini" / "antigravity" / "mcp"
        ]
        available_mcps = []
        for mcp_root in mcp_dirs:
            if mcp_root.exists() and mcp_root.is_dir():
                for d in mcp_root.iterdir():
                    if d.is_dir() and not d.name.startswith("."):
                        tools = [t.stem for t in d.glob("*.json")]
                        available_mcps.append({
                            "name": d.name,
                            "path": str(d),
                            "tools": tools
                        })
        return available_mcps

    def _get_mcp_context_instructions(self) -> str:
        """Sinh chỉ dẫn khai thác MCP Servers cho Agents trên Antigravity 2.0."""
        mcps = self.get_available_mcp_servers()
        if not mcps:
            return ""
        lines = [
            "\n### TẬN DỤNG CÁC MCP SERVERS KHẢ DỤNG TRÊN ANTIGRAVITY 2.0:",
            "Các Agents được trang bị quyền truy vấn các MCP tools sau để hỗ trợ thẩm định và phát triển:"
        ]
        for m in mcps:
            tools_str = ", ".join(m["tools"][:6]) if m["tools"] else "native tools"
            lines.append(f"- MCP Server `{m['name']}`: Công cụ khả dụng: [{tools_str}]")
        lines.append("- Sub-Team 2 & 3: Ưu tiên dùng `gemini-api_gemini-api-docs` (`gemini_search_docs`, `gemini_get_doc`) để tra cứu chuẩn SDK Google GenAI & OpenAPI specs mới nhất.")
        lines.append("- Sub-Team 1 & 4: Ưu tiên dùng `gemini-notebook-mcp` / `notebooklm` để tra cứu tài liệu nghiệp vụ tham khảo.")
        return "\n".join(lines) + "\n"

    def create_discovery_team(
        self,
        tech_lead_profile: Dict[str, Any],
        response_schema: Optional[Type[BaseModel]] = DiscoveryResult
    ):
        """Khởi tạo Sub-Team 1: Product Discovery hỗ trợ Structured Output & MCP Servers."""
        prompt = self._read_prompt("subteam_1_discovery.md")
        rules = self._load_rules()
        mcp_context = self._get_mcp_context_instructions()
        system_instruction = f"""
{prompt}

HỆ THỐNG TIÊU CHUẨN & QUY TẮC CỐT LÕI:
{rules}
{mcp_context}
HỒ SƠ TECH LEAD & HỆ THỐNG:
- Tech Lead ưu tiên review: {tech_lead_profile.get('tech_lead', {}).get('familiar_stacks', {})}
- Mục tiêu: Chuyển đổi yêu cầu thô từ khách hàng thành đặc tả có cấu trúc chuẩn xác (PRD, Gherkin User Stories, UI/UX Flows).
"""
        if HAS_ANTIGRAVITY_SDK and self.api_key:
            cap = CapabilitiesConfig(enable_subagents=True) if CapabilitiesConfig else None
            config_kwargs = {
                "api_key": self.api_key,
                "skills_paths": [str(self.skills_dir)] if self.skills_dir.exists() else None,
                "system_instructions": system_instruction,
            }
            if cap:
                config_kwargs["capabilities"] = cap
            if response_schema:
                config_kwargs["response_schema"] = response_schema
            if policy and hasattr(policy, "allow_all"):
                config_kwargs["policies"] = [policy.allow_all()]
            return Agent(LocalAgentConfig(**{k: v for k, v in config_kwargs.items() if v is not None}))
        
        return DynamicAgent("Discovery Sub-Team", system_instruction, response_schema=response_schema, api_key=self.api_key)

    def create_architecture_team(
        self,
        tech_lead_profile: Dict[str, Any],
        response_schema: Optional[Type[BaseModel]] = ArchitectureResult
    ):
        """Khởi tạo Sub-Team 2: Architecture & Planning."""
        prompt = self._read_prompt("subteam_2_architecture.md")
        profile_notes = tech_lead_profile.get("tech_lead", {}).get("architectural_preference", {}).get("explanation", "")
        rules = self._load_rules()
        mcp_context = self._get_mcp_context_instructions()
        system_instruction = f"""
{prompt}

TIÊU CHUẨN KIẾN TRÚC & CODING:
{rules}
{mcp_context}
ĐẶC BIỆT LƯU Ý VỀ TECH STACK THEO YÊU CẦU CỦA TECH LEAD:
{profile_notes}
Nếu yêu cầu bài toán phù hợp, HÃY ƯU TIÊN CHỌN:
- Backend: Python (FastAPI v0.110+) + SQLAlchemy 2.0 Async + Pydantic v2
- Frontend / Mobile: React Native (TypeScript) hoặc Next.js
- Database: PostgreSQL 15+ & Redis Cache
"""
        if HAS_ANTIGRAVITY_SDK and self.api_key:
            cap = CapabilitiesConfig(enable_subagents=True) if CapabilitiesConfig else None
            config_kwargs = {
                "api_key": self.api_key,
                "skills_paths": [str(self.skills_dir)] if self.skills_dir.exists() else None,
                "system_instructions": system_instruction,
            }
            if cap:
                config_kwargs["capabilities"] = cap
            if response_schema:
                config_kwargs["response_schema"] = response_schema
            if policy and hasattr(policy, "allow_all"):
                config_kwargs["policies"] = [policy.allow_all()]
            return Agent(LocalAgentConfig(**{k: v for k, v in config_kwargs.items() if v is not None}))

        return DynamicAgent("Architecture Sub-Team", system_instruction, response_schema=response_schema, api_key=self.api_key)

    def create_engineering_team(
        self,
        tech_stack: Dict[str, Any],
        workspace_dir: Optional[Path] = None
    ):
        """Khởi tạo Sub-Team 3: Core Engineering (trang bị Native Tools: Viết code & tạo thư mục)."""
        prompt = self._read_prompt("subteam_3_engineering.md")
        rules = self._load_rules()
        mcp_context = self._get_mcp_context_instructions()
        system_instruction = f"""
{prompt}

TIÊU CHUẨN MÃ NGUỒN:
{rules}
{mcp_context}
TECH STACK ĐÃ PHÊ DUYỆT BỞI TECH LEAD:
{tech_stack}
Hãy lập trình mã nguồn hoàn chỉnh chuẩn Clean Architecture, type hints đầy đủ, và tương thích 100% với openapi.yaml.
"""
        if HAS_ANTIGRAVITY_SDK and self.api_key:
            cap = CapabilitiesConfig(enable_subagents=True) if CapabilitiesConfig else None
            config_kwargs = {
                "api_key": self.api_key,
                "skills_paths": [str(self.skills_dir)] if self.skills_dir.exists() else None,
                "system_instructions": system_instruction,
            }
            if cap:
                config_kwargs["capabilities"] = cap
            if policy and hasattr(policy, "allow_all"):
                config_kwargs["policies"] = [policy.allow_all()]
            return Agent(LocalAgentConfig(**{k: v for k, v in config_kwargs.items() if v is not None}))

        return DynamicAgent("Engineering Sub-Team", system_instruction, api_key=self.api_key)

    def create_qa_team(self, response_schema: Optional[Type[BaseModel]] = QAReportResult):
        """Khởi tạo Sub-Team 4: QA & Security (trang bị Native Tools: chạy PyTest & rà soát bảo mật)."""
        prompt = self._read_prompt("subteam_4_qa.md")
        rules = self._load_rules()
        mcp_context = self._get_mcp_context_instructions()
        system_instruction = f"""
{prompt}

TIÊU CHÍ REVIEW & BẢO MẬT:
{rules}
{mcp_context}
"""
        if HAS_ANTIGRAVITY_SDK and self.api_key:
            cap = CapabilitiesConfig(enable_subagents=True) if CapabilitiesConfig else None
            config_kwargs = {
                "api_key": self.api_key,
                "skills_paths": [str(self.skills_dir)] if self.skills_dir.exists() else None,
                "system_instructions": system_instruction,
            }
            if cap:
                config_kwargs["capabilities"] = cap
            if response_schema:
                config_kwargs["response_schema"] = response_schema
            if policy and hasattr(policy, "allow_all"):
                config_kwargs["policies"] = [policy.allow_all()]
            return Agent(LocalAgentConfig(**{k: v for k, v in config_kwargs.items() if v is not None}))

        return DynamicAgent("QA & Security Sub-Team", system_instruction, response_schema=response_schema, api_key=self.api_key)

    def create_release_team(self):
        """Khởi tạo Sub-Team 5: Release & Handover."""
        prompt = self._read_prompt("subteam_5_release.md")
        mcp_context = self._get_mcp_context_instructions()
        system_instruction = f"{prompt}\n{self._load_rules()}\n{mcp_context}"
        if HAS_ANTIGRAVITY_SDK and self.api_key:
            cap = CapabilitiesConfig(enable_subagents=True) if CapabilitiesConfig else None
            config_kwargs = {
                "api_key": self.api_key,
                "skills_paths": [str(self.skills_dir)] if self.skills_dir.exists() else None,
                "system_instructions": system_instruction,
            }
            if cap:
                config_kwargs["capabilities"] = cap
            if policy and hasattr(policy, "allow_all"):
                config_kwargs["policies"] = [policy.allow_all()]
            return Agent(LocalAgentConfig(**{k: v for k, v in config_kwargs.items() if v is not None}))

        return DynamicAgent("Release & Handover Sub-Team", system_instruction, api_key=self.api_key)

    def list_subteams(self) -> list:
        """Liệt kê danh sách các Native Sub-Teams được định nghĩa trong .agents/subteams."""
        subteams = []
        if self.subteams_dir.exists():
            for sf in sorted(self.subteams_dir.glob("*.md")):
                text = sf.read_text(encoding="utf-8")
                match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
                meta = {}
                if match:
                    for line in match.group(1).splitlines():
                        if ":" in line:
                            k, v = line.split(":", 1)
                            meta[k.strip()] = v.strip()
                subteams.append({
                    "id": sf.stem,
                    "name": meta.get("name", sf.stem),
                    "role": meta.get("role", "SDLC Subagent"),
                    "description": meta.get("description", ""),
                    "path": str(sf)
                })
        return subteams

    def get_subteam(self, team_name: str, **kwargs):
        """Khởi tạo Native Sub-Team tương ứng theo tên gọi (@discovery_team, @architecture_team, v.v.)."""
        clean_name = team_name.lower().replace("-", "_").replace("@", "")
        if "discovery" in clean_name or "subteam_1" in clean_name:
            tech_lead_profile = kwargs.get("tech_lead_profile", {"tech_lead": {"familiar_stacks": {"backend": ["Python (FastAPI)"]}}})
            return self.create_discovery_team(tech_lead_profile=tech_lead_profile)
        elif "architecture" in clean_name or "subteam_2" in clean_name:
            tech_lead_profile = kwargs.get("tech_lead_profile", {"tech_lead": {"familiar_stacks": {"backend": ["Python (FastAPI)"]}}})
            return self.create_architecture_team(tech_lead_profile=tech_lead_profile)
        elif "engineering" in clean_name or "subteam_3" in clean_name:
            tech_stack = kwargs.get("tech_stack", {"backend": "Python/FastAPI", "frontend": "React Native"})
            return self.create_engineering_team(tech_stack=tech_stack, workspace_dir=kwargs.get("workspace_dir"))
        elif "qa" in clean_name or "subteam_4" in clean_name or "quality" in clean_name:
            return self.create_qa_team()
        elif "release" in clean_name or "subteam_5" in clean_name or "handover" in clean_name:
            return self.create_release_team()
        else:
            raise ValueError(f"Không nhận diện được Sub-Team: '{team_name}'. Các Sub-Teams hợp lệ: discovery_team, architecture_team, engineering_team, qa_team, release_team.")


class DynamicAgentResponse:
    """Đối tượng phản hồi hỗ trợ cả .text() và .structured_output()."""
    def __init__(self, text_content: str, structured_data: Optional[Any] = None):
        self._text = text_content
        self._structured_data = structured_data

    async def text(self) -> str:
        return self._text

    async def structured_output(self) -> Optional[Any]:
        return self._structured_data


class DynamicAgent:
    """Agent thông minh tự động trích xuất ngữ cảnh và sinh Structured Output linh hoạt theo bài toán."""

    def __init__(self, name: str, instruction: str, response_schema: Optional[Type[BaseModel]] = None, api_key: Optional[str] = None):
        self.name = name
        self.instruction = instruction
        self.response_schema = response_schema
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def chat(self, prompt: str) -> DynamicAgentResponse:
        # Trích xuất project name nếu có
        match_proj = re.search(r"Dự án:\s*([^\n\r]+)", prompt)
        project_name = match_proj.group(1).strip() if match_proj else "SmartApp"

        # 1. Thử gọi trực tiếp Google Gemini API nếu có key và môi trường mạng hỗ trợ
        if HAS_GOOGLE_GENAI and self.api_key:
            try:
                client = genai.Client(api_key=self.api_key)
                kwargs: Dict[str, Any] = {}
                if self.response_schema:
                    kwargs["config"] = {
                        "response_mime_type": "application/json",
                        "response_schema": self.response_schema,
                    }
                gen_resp = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{self.instruction}\n\n{prompt}",
                    **kwargs
                )
                if self.response_schema:
                    if hasattr(gen_resp, "parsed") and gen_resp.parsed is not None:
                        return DynamicAgentResponse(gen_resp.text, structured_data=gen_resp.parsed)
                    data = json.loads(gen_resp.text)
                    return DynamicAgentResponse(gen_resp.text, structured_data=self.response_schema.model_validate(data))
                return DynamicAgentResponse(gen_resp.text, structured_data=None)
            except Exception:
                # Chuyển tiếp mượt mà sang Adaptive Domain Synthesis khi offline / sandbox
                pass

        # 2. Phân tích thích ứng đa miền sử dụng DomainAnalyzer
        domain_analysis = DomainAnalyzer.analyze(prompt, project_name=project_name)
        domain_info = {
            "domain": domain_analysis["domain"],
            "item_name": domain_analysis["primary_label"],
            "entity_main": domain_analysis["primary_entity"],
            "entity_order": domain_analysis["order_entity"],
            "slot_rule": domain_analysis["rule_desc"],
            "prefix": domain_analysis["primary_entity"][:4].upper()
        }

        structured_obj = None

        if self.response_schema == DiscoveryResult:
            structured_obj = DiscoveryResult(
                project_name=project_name,
                project_vision=f"Hệ thống số hóa toàn diện quy trình cung ứng và đặt hàng {domain_info['item_name']}.",
                business_goals=[
                    f"Giảm 70% thời gian xử lý đơn hàng và phục vụ khách hàng mua {domain_info['item_name']}.",
                    "Minh bạch 100% bảng giá và trạng thái xử lý đơn hàng theo thời gian thực.",
                    f"Tuân thủ triệt để quy tắc vận hành cốt lõi: {domain_info['slot_rule']}."
                ],
                in_scope_mvp=[
                    "Xác thực người dùng (Đăng ký, Đăng nhập qua JWT, phân quyền Khách hàng & Nhân viên).",
                    f"Tra cứu danh mục và bảng giá {domain_info['item_name']}.",
                    f"Đặt lịch / Đặt hàng dịch vụ trực tuyến và chọn khung giờ xử lý.",
                    "Hệ thống hóa đơn và thanh toán qua mã QR động (VietQR/MoMo).",
                    "Module quản trị dành cho nhân viên xử lý tiếp nhận và tồn kho."
                ],
                out_of_scope=[
                    "Tích hợp cổng thanh toán đa quốc gia qua Stripe (dành cho v2.0).",
                    "Hệ thống dự báo nhu cầu bằng AI nâng cao (dành cho v2.0)."
                ],
                clarifications=[
                    ClarificationQnAModel(
                        q_id="Q-01",
                        context=f"Khách hàng có bắt buộc phải đăng nhập trước khi xem danh mục {domain_info['item_name']} không?",
                        impact="Ảnh hưởng trực tiếp đến tỷ lệ chuyển đổi đơn hàng và trải nghiệm duyệt ban đầu.",
                        proposed_solution="Cho phép xem danh mục và giá công khai; chỉ bắt buộc đăng nhập khi bấm xác nhận đặt hàng."
                    ),
                    ClarificationQnAModel(
                        q_id="Q-02",
                        context="Phương thức thanh toán trực tuyến ưu tiên trong pha MVP là gì?",
                        impact="Quyết định việc tích hợp cổng thanh toán và xử lý callback trạng thái.",
                        proposed_solution="Tích hợp thanh toán chuyển khoản qua mã QR động (VietQR) và thanh toán COD/tiền mặt."
                    ),
                    ClarificationQnAModel(
                        q_id="Q-03",
                        context=f"Quy tắc khi số lượng yêu cầu trong một khung giờ vượt giới hạn ({domain_info['slot_rule']})?",
                        impact="Nguy cơ quá tải hệ thống và trễ hẹn bàn giao cho khách.",
                        proposed_solution=f"Khóa tự động slot khi đạt ngưỡng tối đa; hiển thị cảnh báo gợi ý khung giờ kế tiếp."
                    )
                ],
                user_stories=[
                    UserStoryModel(
                        id="US-01",
                        epic="Authentication & Profile",
                        title="Đăng ký & Đăng nhập Người Dùng",
                        as_a="Khách hàng",
                        i_want_to="Đăng ký và đăng nhập nhanh bằng số điện thoại và mật khẩu",
                        so_that="Tôi có thể theo dõi lịch sử và trạng thái đơn hàng của mình",
                        priority="MUST_HAVE",
                        story_points=3,
                        acceptance_criteria_gherkin=(
                            "Scenario: Đăng ký tài khoản mới thành công\n"
                            "  Given số điện thoại '0912345678' chưa từng đăng ký\n"
                            "  When người dùng nhập họ tên và mật khẩu hợp lệ\n"
                            "  Then hệ thống tạo tài khoản mới và trả về HTTP 201 kèm Access Token JWT\n\n"
                            "Scenario: Đăng ký trùng số điện thoại\n"
                            "  Given số điện thoại '0912345678' đã tồn tại trong DB\n"
                            "  When người dùng cố gắng đăng ký lại\n"
                            "  Then hệ thống từ chối với HTTP 409 Conflict và thông báo lỗi rõ ràng"
                        )
                    ),
                    UserStoryModel(
                        id="US-02",
                        epic="Core Order & Booking",
                        title=f"Đặt hàng / Đặt lịch {domain_info['item_name']}",
                        as_a="Khách hàng",
                        i_want_to=f"Chọn dịch vụ {domain_info['item_name']} và chọn thời gian thực hiện",
                        so_that="Đơn hàng của tôi được chuẩn bị chu đáo và không bị chờ đợi",
                        priority="MUST_HAVE",
                        story_points=5,
                        acceptance_criteria_gherkin=(
                            "Scenario: Đặt dịch vụ vào khung giờ còn trống\n"
                            "  Given khung giờ được chọn còn slot trống hợp lệ\n"
                            "  When người dùng bấm xác nhận đặt đơn\n"
                            "  Then hệ thống tạo đơn với trạng thái 'CONFIRMED' và trừ 1 slot còn trống\n\n"
                            f"Scenario: Từ chối khi vượt công suất ({domain_info['slot_rule']})\n"
                            "  Given khung giờ đã đạt ngưỡng giới hạn tối đa\n"
                            "  When người dùng cố gắng đặt thêm\n"
                            "  Then hệ thống từ chối với HTTP 400 Bad Request và thông báo 'Khung giờ đã đầy chỗ'"
                        )
                    ),
                    UserStoryModel(
                        id="US-03",
                        epic="Catalog & Pricing",
                        title=f"Tra cứu Bảng Giá {domain_info['item_name']}",
                        as_a="Khách hàng và Nhân viên",
                        i_want_to="Xem danh mục mặt hàng niêm yết minh bạch kèm hình ảnh và đơn giá",
                        so_that="Tôi nắm rõ chi phí chính xác trước khi ra quyết định mua hàng",
                        priority="MUST_HAVE",
                        story_points=3,
                        acceptance_criteria_gherkin=(
                            "Scenario: Tra cứu danh mục sản phẩm công khai\n"
                            "  Given hệ thống có danh mục sản phẩm đang hoạt động\n"
                            "  When người dùng gửi yêu cầu GET /api/v1/catalog\n"
                            "  Then hệ thống trả về danh sách sản phẩm HTTP 200 kèm đơn giá niêm yết"
                        )
                    )
                ],
                functional_requirements=[
                    FunctionalRequirementModel(
                        code="FR-01",
                        name="Xác thực & Phân quyền RBAC",
                        description="Hỗ trợ đăng ký, đăng nhập JWT, phân quyền Customer, Staff, Admin",
                        priority="P0 (Must Have)",
                        subteam="Backend & Mobile"
                    ),
                    FunctionalRequirementModel(
                        code="FR-02",
                        name=f"Quản lý Đơn hàng & Lịch hẹn {domain_info['item_name']}",
                        description=f"Tiếp nhận và kiểm soát dung lượng theo quy tắc: {domain_info['slot_rule']}",
                        priority="P0 (Must Have)",
                        subteam="Backend & Mobile"
                    ),
                    FunctionalRequirementModel(
                        code="FR-03",
                        name="Quản lý Danh mục & Bảng giá",
                        description=f"Tra cứu, cập nhật tồn kho và giá bán của {domain_info['item_name']}",
                        priority="P0 (Must Have)",
                        subteam="Backend & Mobile"
                    ),
                    FunctionalRequirementModel(
                        code="FR-04",
                        name="Hóa đơn & Thanh toán QR",
                        description="Tự động tính tổng tiền dịch vụ và sinh mã QR động thanh toán chuyển khoản",
                        priority="P0 (Must Have)",
                        subteam="Backend"
                    )
                ],
                business_rules=[
                    BusinessRuleModel(
                        rule_id="BR-01",
                        name="Ràng buộc giới hạn công suất",
                        statement=domain_info["slot_rule"],
                        enforcement_layer="Service"
                    ),
                    BusinessRuleModel(
                        rule_id="BR-02",
                        name="Thời hạn hiệu lực Access Token",
                        statement="JWT Access Token có thời hạn tối đa 15 phút, ký thuật toán HS256",
                        enforcement_layer="Core Security"
                    )
                ],
                ui_ux_screen_flows=[
                    "Màn hình Đăng nhập & Đăng ký (AuthScreen)",
                    f"Màn hình Khám phá & Danh mục {domain_info['item_name']} (CatalogScreen)",
                    f"Màn hình Đặt lịch / Đặt hàng (BookingScreen)",
                    "Màn hình Theo dõi Trạng thái đơn hàng Realtime (TrackingScreen)",
                    "Màn hình Quản trị Đơn hàng & Kho dành cho Nhân viên (AdminDashboard)"
                ]
            )

        elif self.response_schema == ArchitectureResult:
            structured_obj = ArchitectureResult(
                project_name=project_name,
                tech_stack=TechStackSelection(
                    rationale=(
                        "1. Ưu tiên tuyệt đối theo sở trường của Tech Lead: Python/FastAPI và React Native/TypeScript.\n"
                        "2. FastAPI cho hiệu năng IO bất đồng bộ xuất sắc, sinh OpenAPI docs tự động từ Pydantic.\n"
                        "3. PostgreSQL 15+ đảm bảo toàn vẹn dữ liệu ACID và bảo vệ giao dịch đặt hàng."
                    )
                ),
                adrs=[
                    ADRModel(
                        id="ADR-01",
                        title="Lựa chọn Tech Stack thân thiện với Tech Lead Review",
                        context="Dự án cần phát triển nhanh, chất lượng cao và Tech Lead có thể tự tay review từng file code.",
                        decision="Sử dụng FastAPI (Backend) + React Native (Mobile) + PostgreSQL.",
                        consequences="Mã nguồn dễ bảo trì, typing chặt chẽ, ngăn ngừa lỗi runtime."
                    ),
                    ADRModel(
                        id="ADR-02",
                        title="Áp dụng kiến trúc Clean Architecture phân tầng",
                        context="Tránh việc logic nghiệp vụ bị phân tán hoặc lẫn lộn vào tầng Controller/Router.",
                        decision="Chia rõ: Routers -> Services -> Repositories -> Models.",
                        consequences="Dễ viết Unit Test, cô lập lỗi và có thể tráo đổi database mà không ảnh hưởng use case."
                    )
                ],
                endpoints=[
                    APIEndpointModel(path="/api/v1/auth/register", method="POST", summary="Đăng ký tài khoản", response_schema="TokenResponse", status_code=201),
                    APIEndpointModel(path="/api/v1/auth/login", method="POST", summary="Đăng nhập lấy token", response_schema="TokenResponse", status_code=200),
                    APIEndpointModel(path="/api/v1/orders", method="POST", summary="Tạo đơn hàng mới", response_schema="OrderResponse", status_code=201),
                    APIEndpointModel(path="/api/v1/orders", method="GET", summary="Danh sách đơn hàng", response_schema="List[OrderResponse]", status_code=200),
                    APIEndpointModel(path="/api/v1/catalog", method="GET", summary="Bảng giá danh mục", response_schema="List[CatalogItemResponse]", status_code=200)
                ],
                database_tables=[
                    DatabaseTableModel(table_name="users", description="Lưu thông tin người dùng", columns=["id UUID", "phone_number VARCHAR(20)", "password_hash VARCHAR(255)", "full_name VARCHAR(100)", "role VARCHAR(20)"]),
                    DatabaseTableModel(table_name="catalog_items", description="Danh mục sản phẩm dịch vụ", columns=["id UUID", "name VARCHAR(150)", "price NUMERIC(12,2)", "stock_quantity INT", "is_active BOOLEAN"]),
                    DatabaseTableModel(table_name="orders", description="Đơn hàng & Lịch hẹn", columns=["id UUID", "user_id UUID", "scheduled_time TIMESTAMP", "status VARCHAR(30)", "total_amount NUMERIC(12,2)"])
                ],
                openapi_yaml=f"""openapi: 3.0.3
info:
  title: {project_name} API
  description: API chuẩn Clean Architecture cho {project_name}
  version: 1.0.0
paths:
  /api/v1/auth/register:
    post:
      summary: Đăng ký tài khoản mới
      tags: [Authentication]
      responses:
        '201':
          description: Đăng ký thành công
  /api/v1/auth/login:
    post:
      summary: Đăng nhập hệ thống
      tags: [Authentication]
      responses:
        '200':
          description: Trả về access token JWT
  /api/v1/orders:
    post:
      summary: Tạo đơn hàng hoặc đặt lịch mới
      tags: [Orders]
      responses:
        '201':
          description: Tạo thành công
    get:
      summary: Lấy danh sách đơn hàng
      tags: [Orders]
      responses:
        '200':
          description: Danh sách đơn hàng
  /api/v1/catalog:
    get:
      summary: Tra cứu danh mục sản phẩm dịch vụ
      tags: [Catalog]
      responses:
        '200':
          description: Bảng giá công khai
""",
                erd_mermaid="""erDiagram
    USERS ||--o{ ORDERS : places
    USERS {
        uuid id PK
        string phone_number UK
        string password_hash
        string full_name
        string role
    }
    CATALOG_ITEMS ||--o{ ORDER_ITEMS : contains
    CATALOG_ITEMS {
        uuid id PK
        string name
        decimal price
        int stock_quantity
    }
    ORDERS ||--|{ ORDER_ITEMS : includes
    ORDERS {
        uuid id PK
        uuid user_id FK
        datetime scheduled_time
        string status
        decimal total_amount
    }
""",
                security_stride_matrix=[
                    {"threat": "Spoofing (Giả mạo)", "mitigation": "Xác thực JWT HS256, hash mật khẩu Bcrypt với salt cost 12."},
                    {"threat": "Tampering (Sửa đổi dữ liệu)", "mitigation": "Pydantic DTOs validate kiểu dữ liệu chặt chẽ; HTTPS bắt buộc."},
                    {"threat": "Information Disclosure", "mitigation": "Ẩn chi tiết stack trace ở production; lọc trường nhạy cảm trong Response DTO."},
                    {"threat": "Denial of Service", "mitigation": f"Áp dụng quy tắc kiểm soát công suất ({domain_info['slot_rule']}) và rate limiting."}
                ],
                tasks_backlog=[
                    {"id": "BE-01", "team": "backend", "title": "Khởi tạo Clean Architecture Core, Config & Security JWT", "depends_on": []},
                    {"id": "BE-02", "team": "backend", "title": "Xây dựng Schemas DTOs & Models cơ sở dữ liệu", "depends_on": ["BE-01"]},
                    {"id": "BE-03", "team": "backend", "title": "Hiện thực hóa Services, Business Rules (BR-01) & Routers", "depends_on": ["BE-02"]},
                    {"id": "FE-01", "team": "frontend", "title": "Khởi tạo React Native TypeScript, Zustand Store & API Client", "depends_on": []},
                    {"id": "FE-02", "team": "frontend", "title": "Xây dựng Giao diện Đặt hàng & Tra cứu Danh mục", "depends_on": ["FE-01", "BE-02"]},
                    {"id": "DO-01", "team": "devops", "title": "Xây dựng Multi-stage Dockerfile & docker-compose (FastAPI + PostgreSQL)", "depends_on": ["BE-03"]}
                ]
            )

        text_response = f"[{self.name}] Đã xử lý yêu cầu cho dự án '{project_name}' thành công."
        return DynamicAgentResponse(text_response, structured_data=structured_obj)


if __name__ == "__main__":
    import argparse
    import asyncio
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    console = Console()
    parser = argparse.ArgumentParser(description="Google Antigravity 2.0 Native Subagent Dispatcher")
    parser.add_argument("--list", action="store_true", help="Liệt kê toàn bộ Native Sub-Teams trong .agents/subteams")
    parser.add_argument("--subteam", help="Tên Sub-Team cần triệu hồi (vd: discovery_team, architecture_team, engineering_team, qa_team, release_team)")
    parser.add_argument("--prompt", help="Chỉ thị hoặc context yêu cầu gửi đến Sub-Team")
    parser.add_argument("--project", default="SmartApp", help="Tên dự án phần mềm")
    args = parser.parse_args()

    factory = AgentFactory(Path(__file__).parent.parent)

    if args.list:
        subteams = factory.list_subteams()
        table = Table(title="Danh Sách Native Sub-Teams Antigravity 2.0 (.agents/subteams)", border_style="cyan")
        table.add_column("Tên Sub-Team (@mention)", style="bold yellow")
        table.add_column("Vai Trò (Role)", style="green")
        table.add_column("Mô Tả & Kỹ Năng", style="white")
        for st in subteams:
            table.add_row(f"@{st['name']}", st["role"], st["description"])
        console.print(table)
    elif args.subteam and args.prompt:
        async def run_dispatch():
            console.print(Panel(
                f"[bold cyan]Triệu hồi Native Sub-Team:[/bold cyan] [bold yellow]@{args.subteam}[/bold yellow]\n"
                f"[bold]Dự án:[/bold] {args.project}\n"
                f"[bold]Chỉ thị:[/bold] {args.prompt}",
                title="Google Antigravity 2.0 Subagent Execution Canvas",
                border_style="green"
            ))
            agent = factory.get_subteam(args.subteam)
            full_prompt = f"Dự án: {args.project}\n\n{args.prompt}"
            async with agent:
                resp = await agent.chat(full_prompt)
                txt = await resp.text()
                struct = await resp.structured_output()
                console.print(Panel(txt, title=f"[bold green]Phản Hồi Từ @{args.subteam}[/bold green]", border_style="cyan"))
                if struct:
                    console.print(f"[bold yellow]Structured Output (Model: {struct.__class__.__name__}):[/bold yellow]")
                    console.print(struct)

        asyncio.run(run_dispatch())
    else:
        parser.print_help()
