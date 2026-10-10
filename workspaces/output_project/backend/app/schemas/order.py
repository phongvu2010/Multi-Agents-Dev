from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class OrderCreateRequest(BaseModel):
    item_id: str = Field(..., example="item_uuid_123")
    scheduled_time: str = Field(..., example="2026-10-15T09:00:00Z")
    notes: Optional[str] = Field(None, example="Ghi chú yêu cầu phục vụ")

class OrderResponse(BaseModel):
    id: str
    item_id: str
    scheduled_time: str
    status: str
    total_amount: float
