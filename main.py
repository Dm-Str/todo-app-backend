from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from pydantic import BaseModel


DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryORM(Base):
    __tablename__ = "category"

    name: Mapped[str]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


def task_to_model(task: TaskORM) -> TaskSchema:
    """Конвертация объекта ORM в Pydantic"""
    return TaskSchema(id=task.id, title=task.title, completed=task.completed)


@app.get("/tasks", response_model=list[TaskSchema])
async def get_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    """Получить спсиок задач"""
    tasks = db.scalars(select(TaskORM)).all()

    return [task_to_model(task) for task in tasks]


@app.post("/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    """Создать задачу"""
    task = TaskORM(title=task_create.title, completed=False)

    db.add(task)
    db.commit()

    return task_to_model(task)


@app.patch("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    """Обновить задачу"""
    task = db.get(TaskORM, task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    task.title = payload.title if payload.title is not None else task.title
    task.completed = payload.completed if payload.completed is not None else task.completed

    db.commit()

    return task_to_model(task)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    """Удалить задачу"""
    task = db.get(TaskORM, task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None


def category_to_model(category: CategoryORM) -> CategorySchema:
    """Конвертация объекта ORM в Pydantic"""
    return CategorySchema(id=category.id, name=category.name)


@app.get("/categories", response_model=list[CategorySchema])
async def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    """Получить список категорий"""
    categories = db.scalars(select(CategoryORM)).all()

    return [category_to_model(category) for category in categories]


@app.post("/categories", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category_create: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    """Создать категорию"""
    category = CategoryORM(name=category_create.name)

    db.add(category)
    db.commit()

    return category_to_model(category)


@app.patch("/categories/{category_id}", response_model=CategorySchema)
async def update_category(
        category_id: str, payload: CategoryUpdateSchema,
        db: Session = Depends(get_db)
) -> CategorySchema:
    """Обновить категорию"""
    category = db.get(CategoryORM, category_id)

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    category.name = payload.name

    db.commit()

    return category_to_model(category)


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    """Удалить категорию"""
    category = db.get(CategoryORM, category_id)

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(category)
    db.commit()
