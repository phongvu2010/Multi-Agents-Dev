import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from google.antigravity import Agent, LocalAgentConfig, types
    HAS_ANTIGRAVITY_SDK = True
except ImportError:
    HAS_ANTIGRAVITY_SDK = False
    Agent = None
    LocalAgentConfig = None
    types = None


class AgentFactory:
    """Factory khởi tạo các Agents và Sub-Teams sử dụng Google Antigravity SDK."""

    def __init__(self, base_dir: Path, api_key: Optional[str] = None):
        self.base_dir = base_dir
        self.skills_dir = base_dir / "skills"
        self.prompts_dir = base_dir / "config" / "prompts"
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    def _read_prompt(self, filename: str) -> str:
        prompt_path = self.prompts_dir / filename
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return ""

    def create_discovery_team(self, tech_lead_profile: Dict[str, Any]):
        """Khởi tạo Sub-Team 1: Product Discovery."""
        prompt = self._read_prompt("subteam_1_discovery.md")
        system_instruction = f"""
{prompt}

HỒ SƠ TECH LEAD & HỆ THỐNG:
- Tech Lead ưu tiên review: {tech_lead_profile.get('tech_lead', {}).get('familiar_stacks', {})}
- Mục tiêu: Chuyển đổi yêu cầu thô thành PRD.md, user_stories.json và luồng màn hình UI/UX.
"""
        if HAS_ANTIGRAVITY_SDK:
            config = LocalAgentConfig(
                api_key=self.api_key,
                skills_paths=[str(self.skills_dir)],
                system_instruction=system_instruction,
                capabilities=types.CapabilitiesConfig(
                    enable_subagents=True,
                    max_subagent_depth=2,
                )
            )
            return Agent(config)
        return MockAgent("Discovery Sub-Team", system_instruction)

    def create_architecture_team(self, tech_lead_profile: Dict[str, Any]):
        """Khởi tạo Sub-Team 2: Architecture & Planning."""
        prompt = self._read_prompt("subteam_2_architecture.md")
        profile_notes = tech_lead_profile.get("tech_lead", {}).get("architectural_preference", {}).get("explanation", "")
        system_instruction = f"""
{prompt}

ĐẶC BIỆT LƯU Ý VỀ TECH STACK THEO YÊU CẦU CỦA TECH LEAD:
{profile_notes}
Nếu yêu cầu bài toán phù hợp, HÃY ƯU TIÊN CHỌN:
- Backend: Python (FastAPI)
- Frontend / Mobile: React Native hoặc Node.js
- Database: PostgreSQL / MongoDB
"""
        if HAS_ANTIGRAVITY_SDK:
            config = LocalAgentConfig(
                api_key=self.api_key,
                skills_paths=[str(self.skills_dir)],
                system_instruction=system_instruction,
                capabilities=types.CapabilitiesConfig(
                    enable_subagents=True,
                    max_subagent_depth=2,
                )
            )
            return Agent(config)
        return MockAgent("Architecture Sub-Team", system_instruction)

    def create_engineering_team(self, tech_stack: Dict[str, Any]):
        """Khởi tạo Sub-Team 3: Core Engineering."""
        prompt = self._read_prompt("subteam_3_engineering.md")
        system_instruction = f"""
{prompt}

TECH STACK ĐÃ PHÊ DUYỆT BỞI TECH LEAD:
{tech_stack}
Hãy viết mã nguồn đầy đủ, chuẩn Clean Code, type annotations, và tương thích 100% với openapi.yaml.
"""
        if HAS_ANTIGRAVITY_SDK:
            config = LocalAgentConfig(
                api_key=self.api_key,
                skills_paths=[str(self.skills_dir)],
                system_instruction=system_instruction,
                capabilities=types.CapabilitiesConfig(
                    enable_subagents=True,
                    max_subagent_depth=3,
                )
            )
            return Agent(config)
        return MockAgent("Engineering Sub-Team", system_instruction)

    def create_qa_team(self):
        """Khởi tạo Sub-Team 4: Quality Assurance & Security."""
        prompt = self._read_prompt("subteam_4_qa.md")
        if HAS_ANTIGRAVITY_SDK:
            config = LocalAgentConfig(
                api_key=self.api_key,
                skills_paths=[str(self.skills_dir)],
                system_instruction=prompt,
                capabilities=types.CapabilitiesConfig(
                    enable_subagents=True,
                )
            )
            return Agent(config)
        return MockAgent("QA & Security Sub-Team", prompt)

    def create_release_team(self):
        """Khởi tạo Sub-Team 5: Release & Handover."""
        prompt = self._read_prompt("subteam_5_release.md")
        if HAS_ANTIGRAVITY_SDK:
            config = LocalAgentConfig(
                api_key=self.api_key,
                skills_paths=[str(self.skills_dir)],
                system_instruction=prompt,
                capabilities=types.CapabilitiesConfig(
                    enable_subagents=True,
                )
            )
            return Agent(config)
        return MockAgent("Release & Handover Sub-Team", prompt)


class MockAgentResponse:
    def __init__(self, text_content: str):
        self._text = text_content

    async def text(self) -> str:
        return self._text


class MockAgent:
    """Mock agent để kiểm thử khi chưa kết nối API key hoặc trong môi trường test."""
    def __init__(self, name: str, instruction: str):
        self.name = name
        self.instruction = instruction

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def chat(self, prompt: str) -> MockAgentResponse:
        return MockAgentResponse(f"[{self.name}] Đã xử lý prompt thành công.")
