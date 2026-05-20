from fastapi import APIRouter, HTTPException, Header, status, Query
from typing import Optional
from app.schemas import TaskCreate, TaskResponse, TaskUpdateStatus
from app.storage import storage

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> int:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="X-User-Id header required")
    try:
        return int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid X-User-Id")

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, x_user_id: Optional[str] = Header(None)):
    user_id = get_current_user_id(x_user_id)
    task_data = task_in.model_dump()
    task_data["owner_id"] = user_id
    task = storage.create(task_data)
    return TaskResponse(**task)

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    x_user_id: Optional[str] = Header(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    min_priority: Optional[int] = Query(None)
):
    user_id = get_current_user_id(x_user_id)
    tasks = storage.get_by_owner(user_id, status_filter, min_priority)
    return [TaskResponse(**t) for t in tasks]

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, x_user_id: Optional[str] = Header(None)):
    user_id = get_current_user_id(x_user_id)
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**task)

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, update: TaskUpdateStatus, x_user_id: Optional[str] = Header(None)):
    user_id = get_current_user_id(x_user_id)
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = storage.update_status(task_id, update.status.value)
    return TaskResponse(**updated)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, x_user_id: Optional[str] = Header(None)):
    user_id = get_current_user_id(x_user_id)
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    storage.delete(task_id)