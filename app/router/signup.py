from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.tenant import TenantCreate, TenantInDBBase, TenantValidate
from app.schemas.otp import OTPRequest, OTPVerify
from app.api.dependencies import get_current_user
from app.schemas.auth import RefreshTokenSchema, PasswordResetRequest, PasswordResetConfirm
from app.service import otp as otp_service
from app.service import tenant as tenant_service
from app.service import auth as auth_service
from app.service import password_reset as password_reset_service

router = APIRouter()

@router.post("/request-otp")
async def request_otp(data: OTPRequest):
    return await otp_service.request_otp_service(data.email)

@router.post("/verify-otp")
def verify_otp(data: OTPVerify):
    return otp_service.verify_otp_service(data.email, data.otp)

@router.post("/signup", response_model=TenantInDBBase)
def signup(tenant: TenantCreate, db: Session = Depends(get_db)):
    return tenant_service.signup_tenant_service(db, tenant)

@router.post("/login")
def login(login_data: TenantValidate, db: Session = Depends(get_db)):
    return auth_service.login_service(db, login_data)

@router.post("/logout")
def logout(request: Request):
    # Extract token from header for logout
    auth_header = request.headers.get("Authorization")
    token = ""
    if auth_header and len(auth_header.split(" ")) == 2:
        token = auth_header.split(" ")[1]
    
    return auth_service.logout_service(token)

@router.post("/refresh-token")
def refresh_token(request: Request):
    auth_header = request.headers.get("Authorization")
    token = ""
    if auth_header and len(auth_header.split(" ")) == 2:
        token = auth_header.split(" ")[1]
        
    return auth_service.refresh_token_service(token)

@router.post("/forgot-password-request")
async def forgot_password_request(data: PasswordResetRequest, db: Session = Depends(get_db)):
    return await password_reset_service.request_password_reset_service(db, data.email)

@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    return password_reset_service.reset_password_service(db, data.email, data.otp, data.new_password)
