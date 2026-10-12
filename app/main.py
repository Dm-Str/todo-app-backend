from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.config import settings
from app.models.base import Base
from app.db.session import engine, get_db
from app.api.routers.task import router as task_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    from app.models.task import TaskORM
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(task_router)


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]

# def category_to_model(category: CategoryORM) -> CategorySchema:
#     """Конвертация объекта ORM в Pydantic"""
#     return CategorySchema(id=category.id, name=category.name)
#
#
# @app.get("/categories", response_model=list[CategorySchema])
# async def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
#     """Получить список категорий"""
#     categories = db.scalars(select(CategoryORM)).all()
#
#     return [category_to_model(category) for category in categories]
#
#
# @app.post("/categories", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
# async def create_category(category_create: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
#     """Создать категорию"""
#     category = CategoryORM(name=category_create.name)
#
#     db.add(category)
#     db.commit()
#
#     return category_to_model(category)
#
#
# @app.patch("/categories/{category_id}", response_model=CategorySchema)
# async def update_category(
#         category_id: str, payload: CategoryUpdateSchema,
#         db: Session = Depends(get_db)
# ) -> CategorySchema:
#     """Обновить категорию"""
#     category = db.get(CategoryORM, category_id)
#
#     if category is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
#
#     category.name = payload.name
#
#     db.commit()
#
#     return category_to_model(category)
#
#
# @app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
#     """Удалить категорию"""
#     category = db.get(CategoryORM, category_id)
#
#     if category is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
#
#     db.delete(category)
#     db.commit()
