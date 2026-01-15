from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.user import UserUpdate, UserInDBBase
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, user_update: UserUpdate, tenant_id: int):
    """Update user with tenant isolation for security."""
    db_user = db.query(User).filter(User.user_id == user_id, User.tenant_id == tenant_id).first()
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Map schema field 'name' to model field 'username'
    if "name" in update_data:
        update_data["username"] = update_data.pop("name")
    
    # Hash password if provided
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int, tenant_id: int):
    """Get user with tenant isolation for security."""
    return db.query(User).filter(User.user_id == user_id, User.tenant_id == tenant_id).first()