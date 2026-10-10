from fastapi import APIRouter
from typing import List
from app.schemas.catalog import CatalogItemResponse

router = APIRouter(prefix="/catalog", tags=["Catalog"])

@router.get("", response_model=List[CatalogItemResponse])
async def get_catalog():
    return [
        CatalogItemResponse(id="cat_01", name="FlowerItem Premium", price=120000.0, stock_quantity=25, is_active=True),
        CatalogItemResponse(id="cat_02", name="FlowerItem Standard", price=80000.0, stock_quantity=50, is_active=True)
    ]
