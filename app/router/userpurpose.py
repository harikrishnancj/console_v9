from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user, get_tenant_id
from app.crud.crud4user import update_user as crud_update_user, get_user as crud_get_user
from app.crud.crud4user_apps import get_user_apps as crud_get_user_apps
from app.schemas.user import UserUpdate
from app.schemas.user_app_mapping import UserAppMappingResponse
from typing import List

router = APIRouter()

@router.get("/user-apps", response_model=List[UserAppMappingResponse])
def get_user_apps_endpoint(db: Session = Depends(get_db),user_id: int = Depends(get_current_user),tenant_id: int = Depends(get_tenant_id)):
    return crud_get_user_apps(db, user_id, tenant_id)

@router.put("/update-user")
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)):
    return crud_update_user(db, user_id, user, tenant_id)

@router.get("/get-user")
def get_user_endpoint(user_id: int, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)):
    return crud_get_user(db, user_id, tenant_id)

