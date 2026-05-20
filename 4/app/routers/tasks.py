from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from app.schemas import TaskCreate, TaskResponse, TaskUpdateStatus, User
from app.dependencies import get_current_user, get_storage
from app.storage import TaskStorage

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    task_data = task_in.model_dump()
    task_data["owner_id"] = current_user.id
    task = storage.create(task_data)
    return TaskResponse(**task)

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    status_filter: Optional[str] = Query(None, alias="status"),
    min_priority: Optional[int] = Query(None),
    storage: TaskStorage = Depends(get_storage)
):
    tasks = storage.get_by_owner(current_user.id, status_filter, min_priority)
    return [TaskResponse(**t) for t in tasks]

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**task)

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    update: TaskUpdateStatus,
    current_user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = storage.update_status(task_id, update.status.value)
    return TaskResponse(**updated)

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    storage.delete(task_id)