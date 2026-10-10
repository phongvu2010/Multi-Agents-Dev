from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Core Service API",
    description="Hệ thống tự động sinh bởi AI Multi-Agent SDLC",
    version="1.0.0"
)

class HealthResponse(BaseModel):
    status: str
    version: str

@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Kiểm tra trạng thái sẵn sàng của dịch vụ."""
    return HealthResponse(status="healthy", version="1.0.0")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
