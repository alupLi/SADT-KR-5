from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import require_admin, get_storage
from app.storage import TaskStorage
from collections import Counter

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
def get_admin_stats(
    admin: dict = Depends(require_admin),
    storage: TaskStorage = Depends(get_storage)
):
    all_tasks = list(storage.tasks.values())
    total_tasks = len(all_tasks)
    
    status_counts = Counter(task["status"] for task in all_tasks)
    by_status = {
        "todo": status_counts.get("todo", 0),
        "in_progress": status_counts.get("in_progress", 0),
        "done": status_counts.get("done", 0)
    }
    
    return {
        "total_tasks": total_tasks,
        "by_status": by_status
    }

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_task(
    task_id: int,
    admin: dict = Depends(require_admin),
    storage: TaskStorage = Depends(get_storage)
):
    task = storage.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    storage.delete(task_id)