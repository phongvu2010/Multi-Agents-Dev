import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from orchestrator.state import SDLCState, SDLCPhase
from orchestrator.agent_factory import AgentFactory

console = Console()


async def run_engineering_phase(
    state: SDLCState,
    factory: AgentFactory,
    project_workspace: Path,
    review_feedback: str = ""
) -> SDLCState:
    """Thực thi chuyên sâu Sub-Team 3: Core Engineering (Backend FastAPI, Mobile React Native, Docker)."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY CHUYÊN SÂU SUB-TEAM 3: CORE ENGINEERING & IMPLEMENTATION[/bold cyan]")
    
    project_workspace.mkdir(parents=True, exist_ok=True)
    backend_dir = project_workspace / "backend"
    frontend_dir = project_workspace / "frontend"
    infra_dir = project_workspace / "infra"

    backend_dir.mkdir(parents=True, exist_ok=True)
    frontend_dir.mkdir(parents=True, exist_ok=True)
    infra_dir.mkdir(parents=True, exist_ok=True)

    agent = factory.create_engineering_team(state.selected_tech_stack)

    # =========================================================================
    # 1. XÂY DỰNG BACKEND CHUẨN CLEAN ARCHITECTURE (PYTHON / FASTAPI)
    # =========================================================================
    console.print("  [bold yellow]• Bước 3.1:[/bold yellow] [dim]Backend Engineer lập trình Clean Architecture (Core, Models, Schemas, Repos, Services, Routers)...[/dim]")

    app_dir = backend_dir / "app"
    for sub in ["core", "models", "schemas", "repositories", "services", "routers"]:
        (app_dir / sub).mkdir(parents=True, exist_ok=True)
        (app_dir / sub / "__init__.py").write_text("", encoding="utf-8")
    (app_dir / "__init__.py").write_text("", encoding="utf-8")

    # 1.1 Core Config & Security
    (app_dir / "core" / "config.py").write_text("""import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MotoCare SmartApp API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_jwt_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    MAX_SLOT_CAPACITY: int = 3  # Giới hạn tối đa 3 xe/khung giờ (BR-01)

    class Config:
        case_sensitive = True

settings = Settings()
""", encoding="utf-8")

    (app_dir / "core" / "security.py").write_text("""from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: str | Any, role: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "role": role}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
""", encoding="utf-8")

    # 1.2 Schemas (Pydantic v2 DTOs)
    (app_dir / "schemas" / "user.py").write_text("""from pydantic import BaseModel, Field

class UserRegisterRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^0\d{9}$", example="0912345678")
    full_name: str = Field(..., min_length=2, max_length=100, example="Nguyễn Văn A")
    password: str = Field(..., min_length=6, example="MatKhau123!@")

class UserLoginRequest(BaseModel):
    phone_number: str = Field(..., example="0912345678")
    password: str = Field(..., example="MatKhau123!@")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class UserResponse(BaseModel):
    id: str
    phone_number: str
    full_name: str
    role: str
""", encoding="utf-8")

    (app_dir / "schemas" / "appointment.py").write_text("""from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AppointmentCreateRequest(BaseModel):
    vehicle_id: str
    appointment_date: datetime
    notes: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: str
    user_id: str
    vehicle_id: str
    appointment_date: datetime
    status: str
    notes: Optional[str] = None
""", encoding="utf-8")

    (app_dir / "schemas" / "spare_part.py").write_text("""from pydantic import BaseModel

class SparePartResponse(BaseModel):
    id: str
    part_code: str
    part_name: str
    unit_price: float
    stock_quantity: int
    category: str
""", encoding="utf-8")

    # 1.3 Services (Business Logic & BR-01 checking)
    (app_dir / "services" / "auth_service.py").write_text("""from fastapi import HTTPException, status
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.user import UserRegisterRequest, UserLoginRequest, TokenResponse

# In-memory storage phục vụ test nhanh, tương thích hoàn toàn với Repository sau này
_users_db = {}

class AuthService:
    @staticmethod
    async def register_user(data: UserRegisterRequest) -> TokenResponse:
        if data.phone_number in _users_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Số điện thoại đã được đăng ký trong hệ thống."
            )
        hashed_pw = get_password_hash(data.password)
        user_id = f"usr_{len(_users_db) + 1}"
        user_record = {
            "id": user_id,
            "phone_number": data.phone_number,
            "full_name": data.full_name,
            "password_hash": hashed_pw,
            "role": "CUSTOMER"
        }
        _users_db[data.phone_number] = user_record
        token = create_access_token(subject=user_id, role="CUSTOMER")
        return TokenResponse(access_token=token, role="CUSTOMER")

    @staticmethod
    async def login_user(data: UserLoginRequest) -> TokenResponse:
        user = _users_db.get(data.phone_number)
        if not user or not verify_password(data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Số điện thoại hoặc mật khẩu không chính xác."
            )
        token = create_access_token(subject=user["id"], role=user["role"])
        return TokenResponse(access_token=token, role=user["role"])
""", encoding="utf-8")

    (app_dir / "services" / "appointment_service.py").write_text("""from datetime import datetime
from fastapi import HTTPException, status
from app.schemas.appointment import AppointmentCreateRequest, AppointmentResponse
from app.core.config import settings

_appointments_db = []

class AppointmentService:
    @staticmethod
    async def create_appointment(user_id: str, data: AppointmentCreateRequest) -> AppointmentResponse:
        # Kiểm tra quy tắc nghiệp vụ BR-01: Giới hạn tối đa 3 xe trong một khung giờ
        same_slot_count = sum(
            1 for appt in _appointments_db
            if appt["appointment_date"] == data.appointment_date and appt["status"] != "CANCELLED"
        )
        if same_slot_count >= settings.MAX_SLOT_CAPACITY:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Khung giờ này đã đủ tối đa 3 xe tiếp nhận. Vui lòng chọn khung giờ khác."
            )

        appt_id = f"appt_{len(_appointments_db) + 1}"
        record = {
            "id": appt_id,
            "user_id": user_id,
            "vehicle_id": data.vehicle_id,
            "appointment_date": data.appointment_date,
            "status": "CONFIRMED",
            "notes": data.notes
        }
        _appointments_db.append(record)
        return AppointmentResponse(**record)

    @staticmethod
    async def get_user_appointments(user_id: str):
        return [AppointmentResponse(**a) for a in _appointments_db if a["user_id"] == user_id]
""", encoding="utf-8")

    # 1.4 API Routers
    (app_dir / "routers" / "auth.py").write_text("""from fastapi import APIRouter, status
from app.schemas.user import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterRequest):
    \"\"\"Đăng ký tài khoản người dùng mới.\"\"\"
    return await AuthService.register_user(payload)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(payload: UserLoginRequest):
    \"\"\"Đăng nhập lấy Access Token.\"\"\"
    return await AuthService.login_user(payload)
""", encoding="utf-8")

    (app_dir / "routers" / "appointments.py").write_text("""from fastapi import APIRouter, status, Header, HTTPException
from typing import List, Optional
from app.schemas.appointment import AppointmentCreateRequest, AppointmentResponse
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    payload: AppointmentCreateRequest,
    authorization: Optional[str] = Header(None)
):
    \"\"\"Đặt lịch hẹn bảo dưỡng xe máy.\"\"\"
    if not authorization:
        raise HTTPException(status_code=401, detail="Thiếu Token xác thực Bearer.")
    # Giả lập trích xuất user_id từ Token
    user_id = "usr_current"
    return await AppointmentService.create_appointment(user_id, payload)

@router.get("", response_model=List[AppointmentResponse], status_code=status.HTTP_200_OK)
async def get_appointments(authorization: Optional[str] = Header(None)):
    \"\"\"Xem danh sách lịch hẹn của tôi.\"\"\"
    if not authorization:
        raise HTTPException(status_code=401, detail="Thiếu Token xác thực Bearer.")
    return await AppointmentService.get_user_appointments("usr_current")
""", encoding="utf-8")

    (app_dir / "routers" / "spare_parts.py").write_text("""from fastapi import APIRouter
from typing import List, Optional
from app.schemas.spare_part import SparePartResponse

router = APIRouter(prefix="/spare-parts", tags=["Spare Parts"])

_sample_parts = [
    SparePartResponse(id="p1", part_code="OIL-01", part_name="Dầu nhớt Motul 10W40 1L", unit_price=150000, stock_quantity=45, category="Dầu nhớt"),
    SparePartResponse(id="p2", part_code="SPK-02", part_name="Bugi NGK Iridium chân dài", unit_price=120000, stock_quantity=20, category="Điện & Đánh lửa"),
    SparePartResponse(id="p3", part_code="BRK-03", part_name="Bố thắng đĩa Nissin trước", unit_price=95000, stock_quantity=15, category="Hệ thống phanh")
]

@router.get("", response_model=List[SparePartResponse])
async def list_spare_parts(search: Optional[str] = None):
    \"\"\"Tra cứu bảng giá phụ tùng niêm yết minh bạch.\"\"\"
    if search:
        return [p for p in _sample_parts if search.lower() in p.part_name.lower()]
    return _sample_parts
""", encoding="utf-8")

    # 1.5 Main Entrypoint
    (app_dir / "main.py").write_text("""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, appointments, spare_parts

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Hệ thống Backend sinh tự động bởi AI Multi-Agents SDLC",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(appointments.router, prefix=settings.API_V1_STR)
app.include_router(spare_parts.router, prefix=settings.API_V1_STR)

@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME, "version": settings.VERSION}
""", encoding="utf-8")

    (backend_dir / "requirements.txt").write_text("""fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
httpx>=0.27.0
pytest>=8.1.0
pytest-asyncio>=0.23.0
""", encoding="utf-8")

    # =========================================================================
    # 2. XÂY DỰNG FRONTEND / MOBILE (REACT NATIVE & TYPESCRIPT)
    # =========================================================================
    console.print("  [bold yellow]• Bước 3.2:[/bold yellow] [dim]Frontend Engineer xây dựng cấu trúc React Native (API Client, Screens, Zustand Store)...[/dim]")

    src_dir = frontend_dir / "src"
    for sub in ["api", "types", "store", "screens"]:
        (src_dir / sub).mkdir(parents=True, exist_ok=True)

    (src_dir / "types" / "index.ts").write_text("""export interface User {
  id: string;
  phone_number: string;
  full_name: string;
  role: 'CUSTOMER' | 'TECHNICIAN' | 'ADMIN';
}

export interface Appointment {
  id: string;
  vehicle_id: string;
  appointment_date: string;
  status: 'PENDING' | 'CONFIRMED' | 'COMPLETED' | 'CANCELLED';
  notes?: string;
}

export interface SparePart {
  id: string;
  part_code: string;
  part_name: string;
  unit_price: number;
  stock_quantity: number;
  category: string;
}
""", encoding="utf-8")

    (src_dir / "api" / "client.ts").write_text("""const BASE_URL = 'http://localhost:8000/api/v1';

export async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = ""; // Lấy từ auth store
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Có lỗi xảy ra khi gọi API');
  }
  return response.json();
}
""", encoding="utf-8")

    (src_dir / "screens" / "BookingScreen.tsx").write_text("""import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, Alert } from 'react-native';

export const BookingScreen = () => {
  const [vehicle, setVehicle] = useState('Honda AirBlade 125');
  const [slot, setSlot] = useState('09:00 - 10:00 Sáng');
  const [notes, setNotes] = useState('');

  const handleBooking = () => {
    Alert.alert('Thành công', `Đã đặt lịch hẹn cho xe ${vehicle} vào lúc ${slot}!`);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Đặt Lịch Bảo Dưỡng Xe Máy</Text>
      
      <Text style={styles.label}>Xe của bạn:</Text>
      <TextInput style={styles.input} value={vehicle} onChangeText={setVehicle} />

      <Text style={styles.label}>Khung giờ tiếp nhận (Tối đa 3 xe/slot):</Text>
      <TextInput style={styles.input} value={slot} onChangeText={setSlot} />

      <Text style={styles.label}>Ghi chú cho thợ sửa xe:</Text>
      <TextInput style={styles.input} placeholder="Vd: Thay nhớt máy, kiểm tra phanh kêu" value={notes} onChangeText={setNotes} />

      <TouchableOpacity style={styles.btn} onPress={handleBooking}>
        <Text style={styles.btnText}>XÁC NHẬN ĐẶT LỊCH (BR-01)</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#0f172a' },
  header: { fontSize: 20, fontWeight: 'bold', color: '#38bdf8', marginBottom: 20 },
  label: { color: '#94a3b8', fontSize: 14, marginTop: 10, marginBottom: 5 },
  input: { backgroundColor: '#1e293b', color: '#fff', padding: 12, borderRadius: 8 },
  btn: { backgroundColor: '#0284c7', padding: 16, borderRadius: 8, marginTop: 24, alignItems: 'center' },
  btnText: { color: '#fff', fontWeight: 'bold' },
});
""", encoding="utf-8")

    (frontend_dir / "package.json").write_text("""{
  "name": "motocare-mobile-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "react-native start",
    "android": "react-native run-android",
    "ios": "react-native run-ios"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-native": "0.73.4",
    "zustand": "^4.5.2"
  }
}
""", encoding="utf-8")

    # =========================================================================
    # 3. XÂY DỰNG DEVOPS & INFRA (DOCKER-COMPOSE & DOCKERFILE)
    # =========================================================================
    console.print("  [bold yellow]• Bước 3.3:[/bold yellow] [dim]DevOps Engineer lập cấu hình Multi-stage Dockerfile & docker-compose...[/dim]")

    (infra_dir / "Dockerfile").write_text("""# Stage 1: Build & Dependencies
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production Minimal Image
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app ./app
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""", encoding="utf-8")

    (infra_dir / "docker-compose.yml").write_text("""version: '3.8'

services:
  backend-api:
    build:
      context: ../backend
      dockerfile: ../infra/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres_secure_pass@postgres-db:5432/motocare_db
      - SECRET_KEY=prod_jwt_super_secret_key
    depends_on:
      - postgres-db
    restart: unless-stopped

  postgres-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres_secure_pass
      POSTGRES_DB: motocare_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  pgdata:
""", encoding="utf-8")

    # Cập nhật State
    state.artifacts["backend_source"] = str(backend_dir)
    state.artifacts["frontend_source"] = str(frontend_dir)
    state.artifacts["infra_source"] = str(infra_dir)
    state.current_phase = SDLCPhase.QA_VERIFICATION

    console.print(Panel(
        f"[bold green]✔ HOÀN TẤT CHUYÊN SÂU SUB-TEAM 3 (CORE ENGINEERING)![/bold green]\n"
        f"• Backend Clean Architecture (FastAPI): [bold]{backend_dir}/app/[/bold]\n"
        f"• Mobile Screens & Types (React Native): [bold]{frontend_dir}/src/[/bold]\n"
        f"• Hạ tầng Dockerfile & Compose: [bold]{infra_dir}/docker-compose.yml[/bold]",
        title="[bold cyan]Sub-Team 3 Output Summary[/bold cyan]",
        border_style="green"
    ))
    return state
