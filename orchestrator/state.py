from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import datetime


class SDLCPhase(str, Enum):
    INITIALIZATION = "initialization"
    DISCOVERY = "discovery"
    GATE_1_PRD = "gate_1_prd"
    ARCHITECTURE = "architecture"
    GATE_2_ARCHITECTURE = "gate_2_architecture"
    ENGINEERING = "engineering"
    QA_VERIFICATION = "qa_verification"
    GATE_3_DEPLOY = "gate_3_deploy"
    RELEASE_HANDOVER = "release_handover"
    COMPLETED = "completed"
    FAILED = "failed"


class GateDecisionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REVISION_REQUESTED = "revision_requested"
    REJECTED = "rejected"


class GateDecision(BaseModel):
    gate_id: str
    reviewer: str
    status: GateDecisionStatus = GateDecisionStatus.PENDING
    feedback: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())


class SDLCState(BaseModel):
    project_name: str
    raw_requirements: str
    current_phase: SDLCPhase = SDLCPhase.INITIALIZATION
    
    # Hồ sơ công nghệ của Tech Lead
    tech_lead_profile: Dict[str, Any] = Field(default_factory=dict)
    
    # Quyết định công nghệ do Architect lựa chọn
    selected_tech_stack: Dict[str, Any] = Field(default_factory=dict)
    
    # Danh sách đường dẫn các artifact đã tạo
    artifacts: Dict[str, str] = Field(default_factory=dict)
    
    # Các quyết định phê duyệt tại 3 Quality Gates
    gate_decisions: Dict[str, GateDecision] = Field(default_factory=dict)
    
    # Lịch sử phản hồi và vòng lặp sửa lỗi
    review_feedback_history: List[Dict[str, Any]] = Field(default_factory=list)
    qa_defect_count: int = 0
    current_iteration: int = 1
    max_iterations: int = 3
    
    # Trạng thái hoàn tất
    is_success: bool = False
    notes: Optional[str] = None

    # Nền tảng Frontend mục tiêu ('auto', 'web', 'mobile')
    platform: str = "auto"
