from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


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


tasks: list[TaskSchema] = []


@app.get("/tasks", response_model=list[TaskSchema])
async def get_tasks() -> list[TaskSchema]:
    """Получить спсиок задач"""
    return tasks


@app.post("/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_create: TaskCreateSchema) -> TaskSchema:
    """Создать задачу"""
    task = TaskSchema(
        id=str(uuid4()),
        **task_create.model_dump(),
        completed=False
    )

    tasks.append(task)

    return task


@app.patch("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: str, payload: TaskUpdateSchema) -> TaskSchema:
    """Обновить задачу"""
    for task in tasks:
        if task.id == task_id:
            update_data = payload.model_dump(exclude_unset=True)

            for k, v in update_data.items():
                setattr(task, k, v)

            return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str) -> None:
    """Удалить задачу"""
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)


class Book(BaseModel):
    book: str


book = ""


@app.get("/book")
async def get_book() -> str:
    """Получить любимую книгу"""
    return f"Любимая книга: {book}"


@app.post("/book", status_code=status.HTTP_201_CREATED)
async def set_book(book_data: Book) -> str:
    """Добавить любимую книгу"""
    global book
    book = book_data.book

    return f"Любимая книга добавленна: {book}"
