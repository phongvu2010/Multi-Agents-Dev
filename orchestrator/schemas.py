"""Pydantic Schemas for Structured Output across all SDLC Sub-Teams.
Enables reliable, machine-validated, and dynamic generation without hardcoded templates.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# =============================================================================
# SUB-TEAM 1: PRODUCT DISCOVERY SCHEMAS
# =============================================================================

class ClarificationQnAModel(BaseModel):
    q_id: str = Field(description="Mã câu hỏi (vd: Q-01)")
    context: str = Field(description="Điểm mơ hồ trong yêu cầu ban đầu")
    impact: str = Field(description="Tác động kỹ thuật hoặc rủi ro kinh doanh")
    proposed_solution: str = Field(description="Đề xuất gợi ý cho khách hàng lựa chọn")


class UserStoryModel(BaseModel):
    id: str = Field(description="Mã Story (vd: US-01)")
    epic: str = Field(description="Tên Epic hoặc Module lớn")
    title: str = Field(description="Tiêu đề User Story")
    as_a: str = Field(description="Vai trò người dùng (As a...)")
    i_want_to: str = Field(description="Hành động mong muốn (I want to...)")
    so_that: str = Field(description="Mục đích / Giá trị đạt được (So that...)")
    priority: str = Field(default="MUST_HAVE", description="Độ ưu tiên: MUST_HAVE, SHOULD_HAVE, COULD_HAVE")
    story_points: int = Field(default=3, description="Ước lượng độ phức tạp (Fibonacci: 1, 2, 3, 5, 8)")
    acceptance_criteria_gherkin: str = Field(
        description="Tiêu chí nghiệm thu chuẩn cú pháp Gherkin (Scenario, Given, When, Then)"
    )


class FunctionalRequirementModel(BaseModel):
    code: str = Field(description="Mã yêu cầu (vd: FR-01)")
    name: str = Field(description="Tên tính năng chức năng")
    description: str = Field(description="Mô tả tóm tắt tính năng")
    priority: str = Field(default="P0 (Must Have)", description="Độ ưu tiên: P0, P1, P2")
    subteam: str = Field(default="Backend & Mobile", description="Đội ngũ phụ trách")


class BusinessRuleModel(BaseModel):
    rule_id: str = Field(description="Mã quy tắc nghiệp vụ (vd: BR-01)")
    name: str = Field(description="Tên quy tắc")
    statement: str = Field(description="Nội dung ràng buộc nghiệp vụ")
    enforcement_layer: str = Field(default="Service", description="Tầng xử lý: Service, DB, Router")


class DiscoveryResult(BaseModel):
    """Kết quả hoàn chỉnh từ Sub-Team 1 (Product Discovery)."""
    project_name: str = Field(description="Tên dự án chuẩn hóa")
    project_vision: str = Field(description="Tầm nhìn sản phẩm và mục tiêu cốt lõi")
    business_goals: List[str] = Field(description="Danh sách mục tiêu kinh doanh định lượng")
    in_scope_mvp: List[str] = Field(description="Các tính năng nằm trong phạm vi MVP v1.0")
    out_of_scope: List[str] = Field(description="Các tính năng để dành cho giai đoạn sau")
    clarifications: List[ClarificationQnAModel] = Field(default_factory=list)
    user_stories: List[UserStoryModel] = Field(default_factory=list)
    functional_requirements: List[FunctionalRequirementModel] = Field(default_factory=list)
    business_rules: List[BusinessRuleModel] = Field(default_factory=list)
    ui_ux_screen_flows: List[str] = Field(
        default_factory=list,
        description="Danh sách các màn hình chính và luồng điều hướng"
    )


# =============================================================================
# SUB-TEAM 2: ARCHITECTURE & PLANNING SCHEMAS
# =============================================================================

class TechStackSelection(BaseModel):
    backend_framework: str = Field(default="Python (FastAPI v0.110+)")
    backend_orm: str = Field(default="SQLAlchemy 2.0 (Async) + Alembic")
    data_validation: str = Field(default="Pydantic v2.6+")
    frontend_mobile: str = Field(default="React Native (TypeScript) + React Navigation")
    state_management: str = Field(default="Zustand + TanStack Query")
    database: str = Field(default="PostgreSQL 15+")
    caching_session: str = Field(default="Redis 7.0+")
    api_specification: str = Field(default="OpenAPI 3.0.3 (Contract-First)")
    rationale: str = Field(description="Lý do lựa chọn phù hợp Tech Lead Profile")


class ADRModel(BaseModel):
    id: str = Field(description="Mã ADR (vd: ADR-01)")
    title: str = Field(description="Tiêu đề quyết định kiến trúc")
    context: str = Field(description="Bối cảnh kỹ thuật")
    decision: str = Field(description="Quyết định lựa chọn")
    consequences: str = Field(description="Hệ quả và lợi ích mang lại")


class APIEndpointModel(BaseModel):
    path: str = Field(description="Đường dẫn endpoint (vd: /api/v1/users)")
    method: str = Field(description="Phương thức HTTP: GET, POST, PUT, DELETE")
    summary: str = Field(description="Tóm tắt chức năng")
    tags: List[str] = Field(default_factory=list)
    request_body_schema: Optional[str] = None
    response_schema: str = Field(description="Tên schema trả về")
    status_code: int = Field(default=200)


class DatabaseTableModel(BaseModel):
    table_name: str
    description: str
    columns: List[str]
    relationships: List[str] = Field(default_factory=list)


class ArchitectureResult(BaseModel):
    """Kết quả hoàn chỉnh từ Sub-Team 2 (Architecture & Planning)."""
    project_name: str
    tech_stack: TechStackSelection
    adrs: List[ADRModel] = Field(default_factory=list)
    endpoints: List[APIEndpointModel] = Field(default_factory=list)
    database_tables: List[DatabaseTableModel] = Field(default_factory=list)
    openapi_yaml: str = Field(description="Toàn bộ nội dung file OpenAPI 3.0.3 YAML")
    erd_mermaid: str = Field(description="Mã nguồn sơ đồ ERD dạng Mermaid syntax")
    security_stride_matrix: List[Dict[str, str]] = Field(default_factory=list)
    tasks_backlog: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Danh sách task phân rã có depends_on để đưa vào DAG Execution Engine"
    )


# =============================================================================
# SUB-TEAM 4: QUALITY & SECURITY SCHEMAS
# =============================================================================

class CodeReviewMetric(BaseModel):
    category: str = Field(description="Tên hạng mục đánh giá")
    score: float = Field(description="Điểm số (thang 10)")
    standard: str = Field(description="Tiêu chuẩn so sánh")
    comment: str = Field(description="Nhận xét chi tiết")


class SecurityCheckItem(BaseModel):
    code: str = Field(description="Mã rủi ro (vd: API1:2023 BOLA)")
    name: str = Field(description="Tên lỗ hổng OWASP")
    status: str = Field(description="PASSED hoặc FAILED")
    details: str = Field(description="Chi tiết kiểm tra")


class QAReportResult(BaseModel):
    """Kết quả tổng hợp từ Sub-Team 4 (QA & Security)."""
    clean_architecture_score: float = 9.5
    typing_score: float = 10.0
    tech_lead_friendly_score: float = 10.0
    overall_score: float = 9.8
    scorecard: List[CodeReviewMetric] = Field(default_factory=list)
    secret_leaks_found: List[str] = Field(default_factory=list)
    owasp_checks: List[SecurityCheckItem] = Field(default_factory=list)
    test_metrics: Dict[str, Any] = Field(default_factory=dict)
