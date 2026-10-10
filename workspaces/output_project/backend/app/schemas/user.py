from pydantic import BaseModel, Field

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
    role: str = "CUSTOMER"
