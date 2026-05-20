from fastapi import HTTPException, Header, Depends
from typing import Optional
from app.schemas import User
from app.storage import storage

async def get_current_user(
    x_user_id: Optional[str] = Header(None),
    x_user_role: Optional[str] = Header(None, alias="X-User-Role")
) -> User:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="X-User-Id header required")
    
    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid X-User-Id")
    
    role = x_user_role if x_user_role else "user"
    
    return User(id=user_id, role=role)

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def get_storage():
    # Возвращаем глобальное хранилище
    from app.storage import storage
    return storage