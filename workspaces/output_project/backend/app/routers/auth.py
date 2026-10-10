from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
_USERS_DB = {}

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: UserRegisterRequest):
    if req.phone_number in _USERS_DB:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Số điện thoại đã được đăng ký.")
    hashed_pwd = get_password_hash(req.password)
    _USERS_DB[req.phone_number] = {"full_name": req.full_name, "password": hashed_pwd, "role": "CUSTOMER"}
    token = create_access_token(subject=req.phone_number, role="CUSTOMER")
    return TokenResponse(access_token=token, role="CUSTOMER")

@router.post("/login", response_model=TokenResponse)
async def login(req: UserLoginRequest):
    user = _USERS_DB.get(req.phone_number)
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sai số điện thoại hoặc mật khẩu.")
    token = create_access_token(subject=req.phone_number, role=user["role"])
    return TokenResponse(access_token=token, role=user["role"])
