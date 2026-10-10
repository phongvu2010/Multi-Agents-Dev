from typing import List, Dict, Any
from fastapi import HTTPException, status
from app.core.config import settings

# In-memory store cho môi trường kiểm thử
_ORDERS_DB: List[Dict[str, Any]] = []

class OrderService:
    @staticmethod
    async def create_order(item_id: str, scheduled_time: str, notes: str | None = None) -> Dict[str, Any]:
        # Kiểm tra Business Rule công suất tối đa
        slot_count = sum(1 for o in _ORDERS_DB if o.get("scheduled_time") == scheduled_time)
        if slot_count >= settings.MAX_SLOT_CAPACITY:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Khung giờ {scheduled_time} đã đạt giới hạn tối đa {settings.MAX_SLOT_CAPACITY} yêu cầu. Vui lòng chọn khung giờ khác!"
            )
        
        new_order = {
            "id": f"ORD_{len(_ORDERS_DB) + 1:04d}",
            "item_id": item_id,
            "scheduled_time": scheduled_time,
            "status": "CONFIRMED",
            "total_amount": 150000.0,
            "notes": notes
        }
        _ORDERS_DB.append(new_order)
        return new_order

    @staticmethod
    async def get_all_orders() -> List[Dict[str, Any]]:
        return _ORDERS_DB
