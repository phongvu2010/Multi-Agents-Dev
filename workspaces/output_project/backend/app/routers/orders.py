from fastapi import APIRouter, HTTPException, status, Header
from typing import List, Optional
from app.schemas.order import OrderCreateRequest, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(req: OrderCreateRequest, authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization Header")
    order = await OrderService.create_order(req.item_id, req.scheduled_time, req.notes)
    return OrderResponse(**order)

@router.get("", response_model=List[OrderResponse])
async def list_orders():
    orders = await OrderService.get_all_orders()
    return [OrderResponse(**o) for o in orders]
