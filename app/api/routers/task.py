from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_task_service
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskNotFoundError, TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskSchema])
async def get_tasks(
    service: TaskService = Depends(get_task_service),
) -> list[TaskSchema]:
    """Получить спсиок задач"""
    return service.list_tasks()


@router.post("", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreateSchema, service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    """Создать задачу"""
    return service.create_task(task_create)


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    service: TaskService = Depends(get_task_service),
) -> TaskSchema:
    """Обновить задачу"""
    try:
        return service.update_task(task_id, payload)

    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str, service: TaskService = Depends(get_task_service)
) -> None:
    """Удалить задачу"""
    try:
        service.delete_task(task_id)

    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
