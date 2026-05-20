from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user, get_storage
from app.schemas import User
from app.storage import TaskStorage

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=User)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=dict)
def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    # Просто демонстрация - возвращаем количество задач пользователя
    tasks = storage.get_by_owner(user_id)
    return {"user_id": user_id, "task_count": len(tasks)}