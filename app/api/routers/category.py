from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_category_service
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryService
from app.services.task import TaskNotFoundError

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategorySchema])
async def get_categories(
    service: CategoryService = Depends(get_category_service),
) -> list[CategorySchema]:
    """Получить спсиок категорий"""
    return service.list_categories()


@router.post("", response_model=CategorySchema)
async def create_category(
    category_create: CategoryCreateSchema,
    service: CategoryService = Depends(get_category_service),
) -> CategorySchema:
    """Создать категорю"""
    return service.create_category(category_create)


@router.patch("/{category_id}", response_model=CategoryUpdateSchema)
async def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    service: CategoryService = Depends(get_category_service),
) -> CategorySchema:
    """Обновить категорю"""
    try:
        return service.update_category(category_id, payload)

    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str, service: CategoryService = Depends(get_category_service)
) -> None:
    """Удалить категорю"""
    try:
        service.delete(category_id)

    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
