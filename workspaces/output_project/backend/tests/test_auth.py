import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login_flow():
    # 1. Đăng ký thành công (US-01 Happy Path)
    reg_payload = {
        "phone_number": "0987654321",
        "full_name": "Trần Thị B",
        "password": "SecurePassword123!"
    }
    resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert data["role"] == "CUSTOMER"

    # 2. Đăng ký trùng số điện thoại (US-01 Edge Path: 409 Conflict)
    resp_dup = client.post("/api/v1/auth/register", json=reg_payload)
    assert resp_dup.status_code == 409

    # 3. Đăng nhập sai mật khẩu (US-01 Error Path: 401 Unauthorized)
    login_fail = {"phone_number": "0987654321", "password": "WrongPassword"}
    resp_fail = client.post("/api/v1/auth/login", json=login_fail)
    assert resp_fail.status_code == 401

    # 4. Đăng nhập đúng (200 OK)
    login_ok = {"phone_number": "0987654321", "password": "SecurePassword123!"}
    resp_ok = client.post("/api/v1/auth/login", json=login_ok)
    assert resp_ok.status_code == 200
    assert "access_token" in resp_ok.json()
